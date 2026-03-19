from __future__ import annotations

import importlib
from functools import lru_cache
from pathlib import Path


GEONAMES_ADMIN1_FILE = Path(__file__).resolve().parent.parent / "data" / "admin1CodesASCII.txt"


def _pretty_label(value: str) -> str:
    return value.replace("_", " ").replace("-", " ").strip()


def _optional_import(module_name: str):
    try:
        return importlib.import_module(module_name)
    except ModuleNotFoundError:
        return None


def _load_runtime_dependencies():
    pycountry_module = _optional_import("pycountry")
    geonamescache_module = _optional_import("geonamescache")
    timezonefinder_module = _optional_import("timezonefinder")
    geonamescache_class = getattr(geonamescache_module, "GeonamesCache", None) if geonamescache_module else None
    timezonefinder_class = getattr(timezonefinder_module, "TimezoneFinder", None) if timezonefinder_module else None
    return pycountry_module, geonamescache_class, timezonefinder_class


def _normalize_country_name(name: str) -> str:
    return name.replace("Korea, Republic of", "South Korea").replace("Korea, Democratic People's Republic of", "North Korea")


def _normalize_subdivision_name(name: str) -> str:
    return (
        name.replace(" Sheng", "")
        .replace(" Shi", "")
        .replace(" Zizhiqu", "")
        .replace(" Shengfen", "")
        .strip()
    )


def _coerce_float(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _build_subdivision_name_lookup(pycountry_module) -> dict[tuple[str, str], str]:
    if pycountry_module is None:
        return {}

    lookup: dict[tuple[str, str], str] = {}
    for subdivision in pycountry_module.subdivisions:
        country_code = getattr(subdivision, "country_code", "")
        code = getattr(subdivision, "code", "")
        name = getattr(subdivision, "name", "")
        if not country_code or not code or not name:
            continue

        normalized_name = _normalize_subdivision_name(name)
        short_code = code.split("-", 1)[-1]
        lookup[(country_code, code)] = normalized_name
        lookup[(country_code, short_code)] = normalized_name
    return lookup


def _load_geonames_admin1_lookup() -> dict[tuple[str, str], str]:
    if not GEONAMES_ADMIN1_FILE.exists():
        return {}

    lookup: dict[tuple[str, str], str] = {}
    for line in GEONAMES_ADMIN1_FILE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        composite_code, admin_name, *_rest = line.split("\t")
        country_code, admin_code = composite_code.split(".", 1)
        lookup[(country_code, admin_code)] = admin_name.strip()
    return lookup


def _location_backend_signature() -> str:
    pycountry_module, geonamescache_class, timezonefinder_class = _load_runtime_dependencies()
    backend = "libraries" if pycountry_module and geonamescache_class and timezonefinder_class else "fallback"
    admin1_stamp = str(GEONAMES_ADMIN1_FILE.stat().st_mtime_ns) if GEONAMES_ADMIN1_FILE.exists() else "missing"
    return f"{backend}:{admin1_stamp}"


def _upsert_city(country_bucket: dict, subdivision_name: str, city_name: str, timezone_name: str, population: int) -> None:
    subdivision_bucket = country_bucket["subdivisions"].setdefault(subdivision_name, {})
    current_city = subdivision_bucket.get(city_name)
    if current_city is None or population > current_city["population"]:
        subdivision_bucket[city_name] = {
            "name": city_name,
            "timezone": timezone_name,
            "population": population,
        }


def _finalize_catalog(countries: dict[str, dict]) -> list[dict]:
    catalog = []
    for country_code, country_data in countries.items():
        subdivision_entries = []
        has_named_subdivisions = any(name != country_data["name"] for name in country_data["subdivisions"])
        for subdivision_name, city_map in country_data["subdivisions"].items():
            display_name = "Other regions" if has_named_subdivisions and subdivision_name == country_data["name"] else subdivision_name
            if not city_map:
                continue
            representative_city = max(city_map.values(), key=lambda item: item["population"])
            subdivision_entries.append(
                {
                    "name": display_name,
                    "timezone": representative_city["timezone"],
                    "city_name": representative_city["name"],
                }
            )
        if subdivision_entries:
            subdivision_entries.sort(key=lambda item: item["name"])
            catalog.append(
                {
                    "code": country_code,
                    "name": country_data["name"],
                    "subdivisions": subdivision_entries,
                }
            )
    catalog.sort(key=lambda item: item["name"])
    return catalog


def _build_catalog_from_libraries() -> list[dict] | None:
    pycountry_module, geonamescache_class, timezonefinder_class = _load_runtime_dependencies()
    if pycountry_module is None or geonamescache_class is None or timezonefinder_class is None:
        return None

    gc = geonamescache_class(min_city_population=5000)
    timezone_finder = timezonefinder_class()
    subdivision_lookup = _build_subdivision_name_lookup(pycountry_module)
    geonames_admin1_lookup = _load_geonames_admin1_lookup()
    raw_countries = gc.get_countries()
    raw_cities = gc.get_cities()
    countries: dict[str, dict] = {}

    for country_code, country_data in raw_countries.items():
        pycountry_match = pycountry_module.countries.get(alpha_2=country_code)
        country_name = pycountry_match.name if pycountry_match else country_data.get("name", country_code)
        countries[country_code] = {
            "code": country_code,
            "name": _normalize_country_name(country_name),
            "subdivisions": {},
        }

    for city_data in raw_cities.values():
        country_code = city_data.get("countrycode")
        if not country_code or country_code not in countries:
            continue

        timezone_name = city_data.get("timezone")
        if not timezone_name:
            latitude = _coerce_float(city_data.get("latitude"))
            longitude = _coerce_float(city_data.get("longitude"))
            if latitude is None or longitude is None:
                continue
            timezone_name = timezone_finder.timezone_at(lat=latitude, lng=longitude)
            if not timezone_name:
                timezone_name = timezone_finder.closest_timezone_at(lat=latitude, lng=longitude)
        if not timezone_name:
            continue

        city_name = city_data.get("name")
        if not city_name:
            continue

        subdivision_code = city_data.get("admin1code") or city_data.get("subcountrycode") or city_data.get("regioncode")
        subdivision_name = geonames_admin1_lookup.get((country_code, str(subdivision_code)), "") if subdivision_code else ""
        if not subdivision_name and subdivision_code:
            subdivision_name = subdivision_lookup.get((country_code, str(subdivision_code)), "")
        if not subdivision_name and subdivision_code:
            subdivision_name = _normalize_subdivision_name(str(subdivision_code))
        if not subdivision_name:
            subdivision_name = countries[country_code]["name"]
        population = int(city_data.get("population") or 0)
        _upsert_city(countries[country_code], subdivision_name, city_name, timezone_name, population)

    for country_code, country_data in raw_countries.items():
        country_bucket = countries.get(country_code)
        if not country_bucket or country_bucket["subdivisions"]:
            continue

        capital_name = country_data.get("capital")
        if not capital_name:
            continue

        capital_matches = gc.get_cities_by_name(capital_name)
        matching_cities = [
            next(iter(item.values()))
            for item in capital_matches
            if next(iter(item.values())).get("countrycode") == country_code
        ]
        if not matching_cities:
            continue

        capital_city = max(matching_cities, key=lambda item: int(item.get("population") or 0))
        latitude = _coerce_float(capital_city.get("latitude"))
        longitude = _coerce_float(capital_city.get("longitude"))
        timezone_name = None
        if latitude is not None and longitude is not None:
            timezone_name = timezone_finder.timezone_at(lat=latitude, lng=longitude)
            if not timezone_name:
                timezone_name = timezone_finder.closest_timezone_at(lat=latitude, lng=longitude)
        timezone_name = timezone_name or capital_city.get("timezone")
        if not timezone_name:
            continue

        subdivision_code = capital_city.get("admin1code")
        subdivision_name = geonames_admin1_lookup.get((country_code, str(subdivision_code)), "") if subdivision_code else ""
        if not subdivision_name and subdivision_code:
            subdivision_name = subdivision_lookup.get((country_code, str(subdivision_code)), "")
        if not subdivision_name and subdivision_code:
            subdivision_name = _normalize_subdivision_name(str(subdivision_code))
        if not subdivision_name:
            subdivision_name = country_bucket["name"]
        _upsert_city(country_bucket, subdivision_name, capital_city["name"], timezone_name, int(capital_city.get("population") or 0))

    return _finalize_catalog(countries)


@lru_cache(maxsize=4)
def _get_location_catalog_cached(signature: str) -> list[dict]:
    library_catalog = _build_catalog_from_libraries()
    if library_catalog:
        return library_catalog
    raise RuntimeError("Location dependencies are unavailable. Install pycountry, geonamescache, timezonefinder, and admin1CodesASCII.txt.")


def get_location_catalog() -> list[dict]:
    return _get_location_catalog_cached(_location_backend_signature())


@lru_cache(maxsize=4)
def _get_location_index_cached(signature: str) -> dict[str, dict]:
    return {country["code"]: country for country in _get_location_catalog_cached(signature)}


def get_location_index() -> dict[str, dict]:
    return _get_location_index_cached(_location_backend_signature())


def get_country_options() -> list[dict]:
    return get_location_catalog()


def get_subdivision_options(country_code: str) -> list[dict]:
    country = get_location_index().get(country_code)
    return country["subdivisions"] if country else []


def get_city_options(country_code: str, subdivision_name: str) -> list[dict]:
    for subdivision in get_subdivision_options(country_code):
        if subdivision["name"] == subdivision_name:
            return [{"name": subdivision["city_name"], "timezone": subdivision["timezone"]}]
    return []


def resolve_location(country_code: str, subdivision_name: str, city_name: str | None = None) -> dict | None:
    country = get_location_index().get(country_code)
    if not country:
        return None
    for subdivision in country["subdivisions"]:
        if subdivision["name"] != subdivision_name:
            continue
        return {
            "country_code": country["code"],
            "country_name": country["name"],
            "subdivision_name": subdivision["name"],
            "city_name": subdivision["city_name"],
            "timezone": subdivision["timezone"],
        }
    return None


@lru_cache(maxsize=128)
def _infer_location_from_timezone_libraries(timezone_name: str) -> dict | None:
    pycountry_module, geonamescache_class, timezonefinder_class = _load_runtime_dependencies()
    if pycountry_module is None or geonamescache_class is None or timezonefinder_class is None:
        return None

    gc = geonamescache_class(min_city_population=5000)
    timezone_finder = timezonefinder_class()
    subdivision_lookup = _build_subdivision_name_lookup(pycountry_module)
    geonames_admin1_lookup = _load_geonames_admin1_lookup()
    raw_countries = gc.get_countries()

    best_city = None
    for city_data in gc.get_cities().values():
        resolved_timezone = city_data.get("timezone")
        if not resolved_timezone:
            latitude = _coerce_float(city_data.get("latitude"))
            longitude = _coerce_float(city_data.get("longitude"))
            if latitude is not None and longitude is not None:
                resolved_timezone = timezone_finder.timezone_at(lat=latitude, lng=longitude)
                if not resolved_timezone:
                    resolved_timezone = timezone_finder.closest_timezone_at(lat=latitude, lng=longitude)
        if resolved_timezone != timezone_name:
            continue

        if best_city is None or int(city_data.get("population") or 0) > int(best_city.get("population") or 0):
            best_city = city_data

    if best_city is None:
        return None

    country_code = best_city.get("countrycode", "")
    country_data = raw_countries.get(country_code, {})
    pycountry_match = pycountry_module.countries.get(alpha_2=country_code) if country_code else None
    country_name = _normalize_country_name(pycountry_match.name if pycountry_match else country_data.get("name", country_code))

    subdivision_code = best_city.get("admin1code") or best_city.get("subcountrycode") or best_city.get("regioncode")
    subdivision_name = geonames_admin1_lookup.get((country_code, str(subdivision_code)), "") if subdivision_code else ""
    if not subdivision_name and subdivision_code:
        subdivision_name = subdivision_lookup.get((country_code, str(subdivision_code)), "")
    if not subdivision_name and subdivision_code:
        subdivision_name = _normalize_subdivision_name(str(subdivision_code))
    if not subdivision_name:
        subdivision_name = country_name

    return {
        "country_code": country_code,
        "country_name": country_name,
        "subdivision_name": subdivision_name,
        "city_name": best_city.get("name", ""),
        "timezone": timezone_name,
    }


def infer_location_from_timezone(timezone_name: str) -> dict:
    inferred = _infer_location_from_timezone_libraries(timezone_name)
    if inferred:
        return inferred

    for country in get_location_catalog():
        for subdivision in country["subdivisions"]:
            for city in subdivision["cities"]:
                if city["timezone"] == timezone_name:
                    return {
                        "country_code": country["code"],
                        "country_name": country["name"],
                        "subdivision_name": subdivision["name"],
                        "city_name": city["name"],
                        "timezone": timezone_name,
                    }

    city_guess = _pretty_label(timezone_name.split("/")[-1]) if "/" in timezone_name else timezone_name
    return {
        "country_code": "",
        "country_name": "",
        "subdivision_name": "",
        "city_name": city_guess,
        "timezone": timezone_name,
    }
