from oidafuel.gasstation import find_gas_stations, FuelType


def test_find_gas_stations():
    longtiude = 48.21901214325078
    latitude = 16.40138450873383
    fuel_type = FuelType.DIESEL
    include_closed = False

    stations = find_gas_stations(longtiude, latitude, fuel_type, include_closed)
    assert len(stations) == 10
