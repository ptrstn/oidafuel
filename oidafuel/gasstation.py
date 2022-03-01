import json
from dataclasses import dataclass

import requests

from oidafuel.datatypes import FuelType


@dataclass
class GasStation:
    identifier: str
    name: str
    address: str
    postal_code: str
    city: str
    latitude: float
    longitude: float


def find_gas_stations(
    latitude: float, longitude: float, fuel_type: FuelType, include_closed: bool = False
):
    """
    https://api.e-control.at/sprit/1.0/doc/index.html?url=https://api.e-control.at/sprit/1.0/api-docs%3Fgroup%3Dpublic-api#/search/searchGasStationsByRegionUsingGET_1

    :param latitude:
    :param longitude:
    :param fuel_type:
    :param include_closed:
    :return:
    """
    url = (
        "https://api.e-control.at"
        "/sprit/1.0/search/gas-stations/by-address"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        f"&fuelType={fuel_type}"
        f"&includeClosed={json.dumps(include_closed)}"
    )

    response = requests.get(url)
    return response.json()
