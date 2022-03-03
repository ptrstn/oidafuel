from oidafuel.core import (
    get_gas_stations_by_address,
    get_gas_stations_by_region,
    gas_stations_to_gas_prices,
)
from oidafuel.datatypes import FuelType


def test_get_gas_stations_by_address():
    address_text = "Molkereistrasse 1, Wien"
    fuel_type = FuelType.SUPER_95
    stations = get_gas_stations_by_address(address_text, fuel_type)
    assert stations
    prices = gas_stations_to_gas_prices(stations)
    assert prices
    assert len(stations) > len(prices)


def test_get_gas_stations_by_region():
    region_code = 920
    fuel_type = FuelType.DIESEL
    stations = get_gas_stations_by_region(region_code, fuel_type)
    assert stations
    prices = gas_stations_to_gas_prices(stations)
    assert prices
    assert len(stations) >= len(prices)
