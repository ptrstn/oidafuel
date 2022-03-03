import json
from dataclasses import asdict

from oidafuel.datatypes import FuelType, RegionType
from oidafuel.econtrol import (
    ping,
    get_regions,
    get_administrative_units,
    search_gas_stations_by_coordinates,
    search_gas_stations_by_region,
)


def test_ping():
    response = ping()
    assert response.startswith("Welcome to Spritpreisrechner")


def test_get_regions():
    regions = get_regions()

    assert len(regions) == 9
    assert regions[0].region_code == 1
    assert regions[0].name == "Burgenland"
    assert regions[8].region_code == 9
    assert regions[8].name == "Wien"
    assert not regions[0].cities
    assert not regions[8].sub_regions[19].cities

    regions = get_regions(include_cities=True)

    assert len(regions) == 9, "Should be 9 Austrian states"
    assert regions[0].region_code == 1
    assert regions[0].region_type == "BL"
    assert regions[0].name == "Burgenland"

    assert regions[8].region_code == 9
    assert regions[8].region_type == "BL"
    assert regions[8].name == "Wien"
    assert regions[8].postal_codes[0] == "1010"
    assert regions[8].postal_codes[-1] == "1230"

    assert regions[8].sub_regions[19].region_code == 919
    assert regions[8].sub_regions[19].region_type == "PB"
    assert regions[8].sub_regions[19].name == "Wien 19.,Döbling"
    assert regions[8].sub_regions[19].postal_codes[0] == "1190"
    assert regions[8].sub_regions[19].cities[0] == "Wien"


def test_get_administrative_units():
    units = get_administrative_units()

    assert len(units) == 9
    assert units[0].region_code == 1
    assert units[0].name == "Burgenland"

    assert units[8].region_code == 9
    assert units[8].name == "Wien"

    assert units[8].districts[19].region_code == 919
    assert units[8].districts[19].name == "Wien 19.,Döbling"
    assert (
        units[8].districts[19].municipalities[0].postal_code == "1190"
    ), "Postal code should be 1190"
    assert units[8].districts[19].municipalities[0].name == "Wien"
    assert (
        units[8].districts[19].municipalities[0].longitude == 16.34565761
    ), "Longitude should be 16.34565761"
    assert (
        units[8].districts[19].municipalities[0].latitude == 48.24574918
    ), "Latitude/Breitengrad should be 48.24574918"


def test_search_gas_stations_by_coordinates():
    latitude = 48.21901214325078
    longitude = 16.40138450873383
    fuel_type = FuelType.DIESEL
    include_closed = False
    stations = search_gas_stations_by_coordinates(
        latitude=latitude,
        longitude=longitude,
        fuel_type=fuel_type,
        include_closed=include_closed,
    )
    assert len(stations) == 10

    prices = [price for station in stations for price in station.prices]
    assert len(prices) >= 5, "At least five cheapest prices"
    assert stations[0].prices[0].timestamp.startswith("20")
    assert not stations[-1].prices


def test_search_gas_stations_by_region():
    region_code = 920
    region_type = RegionType.PB
    fuel_type = FuelType.SUPER_95
    include_closed = True

    stations = search_gas_stations_by_region(
        region_code=region_code,
        region_type=region_type,
        fuel_type=fuel_type,
        include_closed=include_closed,
    )

    assert len(stations) >= 5
    prices = [price for station in stations for price in station.prices]
    assert len(prices) >= 5, "At least five cheapest prices"
    price_dicts = [asdict(station) for station in stations]
    print(json.dumps(price_dicts, indent=2, ensure_ascii=False))
