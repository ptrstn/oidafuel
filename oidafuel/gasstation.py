import json
from dataclasses import dataclass
from enum import Enum

import requests


@dataclass
class GasStation:
    identifier: str
    name: str
    address: str
    postal_code: str
    city: str
    latitude: float
    longitude: float


class FuelType(str, Enum):
    """
    https://stackoverflow.com/a/58608362/9907540
    """

    DIESEL = "DIE"
    SUPER_95 = "SUP"
    CNG_ERDGAS = "GAS"


def find_gas_stations(
    longitude: float, latitude: float, fuel_type: FuelType, include_closed: bool = False
):
    url = (
        "https://api.e-control.at"
        "/sprit/1.0/search/gas-stations/by-address"
        f"?latitude={longitude}"
        f"&longitude={latitude}"
        f"&fuelType={fuel_type}"
        f"&includeClosed={json.dumps(include_closed)}"
    )

    response = requests.get(url)
    return response.json()
