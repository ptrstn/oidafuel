from oidafuel.econtrol import FuelType
from oidafuel.gasstation import find_gas_stations


def test_find_gas_stations():
    latitude = 48.21901214325078
    longitude = 16.40138450873383
    fuel_type = FuelType.DIESEL
    include_closed = False

    stations = find_gas_stations(latitude, longitude, fuel_type, include_closed)
    assert len(stations) == 10
