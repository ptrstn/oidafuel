# Python client to the Spritpreisrechner-API:
# https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api
from datetime import datetime
from zoneinfo import ZoneInfo

import requests

from oidafuel.datatypes import FuelType, Region, State, GasStation

BASE_URL = "https://api.e-control.at"

APPLICATION = "sprit"
VERSION = "1.0"

PING_PATH = "/ping"
REGIONS_PATH = "/regions"
UNITS_PATH = "/regions/units"
GAS_STATIONS_PATH = "/search/gas-stations"
GAS_STATIONS_BY_ADDRESS_PATH = f"{GAS_STATIONS_PATH}/by-address"
GAS_STATIONS_BY_REGION_PATH = f"{GAS_STATIONS_PATH}/by-region"

BASE_ENDPOINT = f"{BASE_URL}/{APPLICATION}/{VERSION}"
PING_ENDPOINT = f"{BASE_ENDPOINT}{PING_PATH}"
REGIONS_ENDPOINT = f"{BASE_ENDPOINT}{REGIONS_PATH}"
UNITS_ENDPOINT = f"{BASE_ENDPOINT}{UNITS_PATH}"
GAS_STATIONS_BY_ADDRESS_ENDPOINT = f"{BASE_ENDPOINT}{GAS_STATIONS_BY_ADDRESS_PATH}"
GAS_STATIONS_BY_REGION_ENDPOINT = f"{BASE_ENDPOINT}{GAS_STATIONS_BY_REGION_PATH}"

TIME_ZONE = ZoneInfo("Europe/Vienna")
TIME_FORMAT = "%Y-%m-%d %H:%M"


def ping() -> str:
    """
    Returns a welcome message and current time of the application

    https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/ping/pingUsingGET_3

    :return: Welcome message and current time
    """
    url = PING_ENDPOINT
    response = requests.get(url)
    return response.text


def get_regions(include_cities: bool = False) -> list[Region]:
    """
    Delivers all possible regions that can be used for the region search

    https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/regions/getRegionsUsingGET

    :param include_cities: Include cities to regions
    :return:
    """
    parameters = {"includeCities": include_cities}
    url = f"{REGIONS_ENDPOINT}"
    response = requests.get(url, params=parameters)
    json_response = response.json()
    regions = [
        Region.from_response_dict(response_dict) for response_dict in json_response
    ]
    return regions


def get_administrative_units() -> list[State]:
    """
    Delivers all possible administrative units with coordinates

    https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/regions/getAdministrativeUnitsUsingGET

    :return:
    """
    url = UNITS_ENDPOINT
    response = requests.get(url)
    json_response = response.json()
    units = [State.from_response_dict(response_dict) for response_dict in json_response]
    return units


def _search_gas_stations(url: str, parameters: dict) -> list[GasStation]:
    response = requests.get(url=url, params=parameters)
    json_response = response.json()
    timestamp = datetime.now(tz=TIME_ZONE).strftime(TIME_FORMAT)

    gas_stations = [
        GasStation.from_response_dict(response_dict, timestamp)
        for response_dict in json_response
    ]
    return gas_stations


def search_gas_stations_by_coordinates(
    latitude: float,
    longitude: float,
    fuel_type: FuelType,
    include_closed: bool = False,
) -> list[GasStation]:
    """
    Searches for gas stations at the given location

    https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/search/searchGasStationsByAddressUsingGET

    :param latitude: Latitude
    :param longitude: Longitude
    :param fuel_type: Fuel type, allowed values: DIE, SUP, GAS
    :param include_closed: Include closed gas stations
    :return:
    """
    url = GAS_STATIONS_BY_ADDRESS_ENDPOINT

    parameters = {
        "latitude": latitude,
        "longitude": longitude,
        "fuelType": fuel_type,
        "includeClosed": include_closed,
    }

    gas_stations = _search_gas_stations(url, parameters)
    return gas_stations


def search_gas_stations_by_region(
    region_code: int,
    region_type: str,
    fuel_type: FuelType,
    include_closed: bool = False,
) -> list[GasStation]:
    """
    Searches for gas stations at the given region

    https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/search/searchGasStationsByRegionUsingGET_1

    :param region_code: Region code
    :param region_type: Region type, allowed values: BL, PB
    :param fuel_type: Fuel type, allowed values: DIE, SUP, GAS
    :param include_closed: Include closed gas stations
    :return:
    """
    url = GAS_STATIONS_BY_REGION_ENDPOINT

    parameters = {
        "code": region_code,
        "type": region_type,
        "fuelType": fuel_type,
        "includeClosed": include_closed,
    }

    gas_stations = _search_gas_stations(url, parameters)
    return gas_stations
