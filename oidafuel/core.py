from dataclasses import dataclass

from oidafuel.address import search_address
from oidafuel.datatypes import FuelType, GasStation
from oidafuel.econtrol import (
    search_gas_stations_by_coordinates,
    search_gas_stations_by_region,
)
from oidafuel.utils import epsg_3857_to_epsg_4326


@dataclass(frozen=True, order=True)
class GasPrice:
    station_id: int
    fuel_type: FuelType
    label: str
    timestamp: str
    price: float

    @classmethod
    def from_gas_station(cls, gas_station: GasStation):
        kwargs = {
            "station_id": gas_station.identifier,
            "fuel_type": gas_station.prices[0].fuel_type,
            "label": gas_station.prices[0].label,
            "timestamp": gas_station.prices[0].timestamp,
            "price": gas_station.prices[0].amount,
        }
        return cls(**kwargs)


@dataclass
class GasStationInfo:
    station_id: int
    name: str
    address: str
    postal_code: str
    city: str
    latitude: float
    longitude: float

    @classmethod
    def from_gas_station(cls, gas_station: GasStation):
        kwargs = {
            "station_id": gas_station.identifier,
            "name": gas_station.name,
            "address": gas_station.location.address,
            "postal_code": gas_station.location.postal_code,
            "city": gas_station.location.city,
            "latitude": gas_station.location.latitude,
            "longitude": gas_station.location.longitude,
        }
        return cls(**kwargs)


def get_gas_stations_by_coordinates(
    latitude: float, longitude: float, fuel_type: FuelType
) -> list[GasStation]:
    gas_stations = search_gas_stations_by_coordinates(latitude, longitude, fuel_type)
    return gas_stations


def get_gas_stations_by_address(
    address_text: str, fuel_type: FuelType
) -> list[GasStation]:
    addresses = search_address(text=address_text)
    address = addresses[0]
    latitude, longitude = epsg_3857_to_epsg_4326(address.x, address.y)
    gas_stations = get_gas_stations_by_coordinates(latitude, longitude, fuel_type)
    return gas_stations


def get_gas_stations_by_region(
    region_code: int, fuel_type: FuelType
) -> list[GasStation]:
    region_type = "BL" if region_code < 10 else "PB"
    gas_stations = search_gas_stations_by_region(region_code, region_type, fuel_type)
    return gas_stations


def gas_stations_to_gas_prices(gas_stations: list[GasStation]) -> list[GasPrice]:
    """
    Returns a list of gas prices by checking each gas station if it contains a price
    """
    gas_prices = [
        GasPrice.from_gas_station(gas_station)
        for gas_station in gas_stations
        if gas_station.prices
    ]
    return gas_prices
