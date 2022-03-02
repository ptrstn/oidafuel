from oidafuel.core import get_gas_prices_by_address, get_gas_prices_by_region
from oidafuel.datatypes import FuelType


def test_get_gas_prices_by_address():
    address_text = "Molkereistrasse 1, Wien"
    fuel_type = FuelType.SUPER_95
    prices = get_gas_prices_by_address(address_text, fuel_type)
    assert prices


def test_get_gas_prices_by_region():
    region_code = 920
    fuel_type = FuelType.DIESEL
    prices = get_gas_prices_by_region(region_code, fuel_type)
    assert prices
