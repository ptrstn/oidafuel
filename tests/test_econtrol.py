import json

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
    assert regions[0]["code"] == 1
    assert regions[0]["name"] == "Burgenland"
    assert regions[8]["code"] == 9
    assert regions[8]["name"] == "Wien"
    assert "cities" not in regions[0]
    assert "cities" not in regions[8]["subRegions"][19]

    regions = get_regions(include_cities=True)

    assert len(regions) == 9, "Should be 9 Austrian states"
    assert regions[0]["code"] == 1
    assert regions[0]["type"] == "BL"
    assert regions[0]["name"] == "Burgenland"

    assert regions[8]["code"] == 9
    assert regions[8]["type"] == "BL"
    assert regions[8]["name"] == "Wien"
    assert regions[8]["postalCodes"][0] == "1010"
    assert regions[8]["postalCodes"][-1] == "1230"

    assert regions[8]["subRegions"][19]["code"] == 919
    assert regions[8]["subRegions"][19]["type"] == "PB"
    assert regions[8]["subRegions"][19]["name"] == "Wien 19.,Döbling"
    assert regions[8]["subRegions"][19]["postalCodes"][0] == "1190"
    assert regions[8]["subRegions"][19]["cities"][0] == "Wien"


def test_get_administrative_units():
    units = get_administrative_units()

    assert len(units) == 9
    assert units[0]["c"] == 1
    assert units[0]["n"] == "Burgenland"

    assert units[8]["c"] == 9
    assert units[8]["n"] == "Wien"

    assert units[8]["b"][19]["c"] == 919
    assert units[8]["b"][19]["n"] == "Wien 19.,Döbling"
    assert units[8]["b"][19]["g"][0]["p"] == "1190", "Postal code should be 1190"
    assert units[8]["b"][19]["g"][0]["n"] == "Wien"
    assert (
        units[8]["b"][19]["g"][0]["l"] == 16.34565761
    ), "Longitude should be 16.34565761"
    assert (
        units[8]["b"][19]["g"][0]["b"] == 48.24574918
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

    prices = [price for station in stations for price in station["prices"]]
    assert len(prices) >= 5, "At least five cheapest prices"


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
    prices = [price for station in stations for price in station["prices"]]
    assert len(prices) >= 5, "At least five cheapest prices"
    print(json.dumps(stations, indent=2))


def test_compare_search_region_address():
    regions = get_regions()
    units = get_administrative_units()

    region_brigittenau = regions[8]["subRegions"][20]
    unit_brigittenau = units[8]["b"][20]

    longitude = unit_brigittenau["g"][0]["l"]
    latitude = unit_brigittenau["g"][0]["b"]

    assert region_brigittenau["code"] == unit_brigittenau["c"]
    region_code = region_brigittenau["code"]
    region_type = region_brigittenau["type"]

    fuel_type = FuelType.SUPER_95
    include_closed = False

    region_stations = search_gas_stations_by_region(
        region_code=region_code,
        region_type=region_type,
        fuel_type=fuel_type,
        include_closed=include_closed,
    )
    region_prices = [
        price for station in region_stations for price in station["prices"]
    ]

    unit_stations = search_gas_stations_by_coordinates(
        latitude=latitude,
        longitude=longitude,
        fuel_type=fuel_type,
        include_closed=include_closed,
    )
    unit_prices = [price for station in unit_stations for price in station["prices"]]

    assert region_prices
    assert unit_prices
