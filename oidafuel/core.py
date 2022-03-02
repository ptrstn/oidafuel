from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo

from oidafuel.address import search_address
from oidafuel.datatypes import FuelType, GasStation
from oidafuel.econtrol import (
    search_gas_stations_by_coordinates,
    search_gas_stations_by_region,
)
from oidafuel.utils import epsg_3857_to_epsg_4326

TIME_ZONE = ZoneInfo("Europe/Vienna")
TIME_FORMAT = "%Y-%m-%d %H:%M"


@dataclass
class GasPrice:
    identifier: int
    name: str
    address: str
    city: str
    postal_code: str
    latitude: float
    longitude: float
    fuel_type: FuelType
    label: str
    price: float
    timestamp: str

    @classmethod
    def from_gas_station(cls, gas_station: GasStation, timestamp: str):
        kwargs = {
            "identifier": gas_station.identifier,
            "name": gas_station.name,
            "address": gas_station.location.address,
            "city": gas_station.location.city,
            "postal_code": gas_station.location.postal_code,
            "latitude": gas_station.location.latitude,
            "longitude": gas_station.location.longitude,
            "fuel_type": gas_station.prices[0].fuel_type,
            "label": gas_station.prices[0].label,
            "price": gas_station.prices[0].amount,
            "timestamp": timestamp,
        }
        return cls(**kwargs)


def gas_stations_to_gas_prices(gas_stations: list[GasStation]) -> list[GasPrice]:
    gas_stations_with_price = [
        gas_station for gas_station in gas_stations if gas_station.prices
    ]
    timestamp = datetime.now(tz=TIME_ZONE).strftime(TIME_FORMAT)
    gas_prices = [
        GasPrice.from_gas_station(gas_station, timestamp)
        for gas_station in gas_stations_with_price
    ]
    return gas_prices


def get_gas_prices_by_coordinates(
    latitude: float, longitude: float, fuel_type: FuelType
) -> list[GasPrice]:
    gas_stations = search_gas_stations_by_coordinates(latitude, longitude, fuel_type)
    gas_prices = gas_stations_to_gas_prices(gas_stations)
    return gas_prices


def get_gas_prices_by_address(address_text: str, fuel_type: FuelType) -> list[GasPrice]:
    addresses = search_address(text=address_text)
    address = addresses[0]
    latitude, longitude = epsg_3857_to_epsg_4326(address.x, address.y)
    return get_gas_prices_by_coordinates(latitude, longitude, fuel_type)


def get_gas_prices_by_region(region_code: int, fuel_type: FuelType) -> list[GasPrice]:
    region_type = "BL" if region_code < 10 else "PB"
    gas_stations = search_gas_stations_by_region(region_code, region_type, fuel_type)
    gas_prices = gas_stations_to_gas_prices(gas_stations)
    return gas_prices
