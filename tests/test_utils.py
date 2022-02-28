from oidafuel.utils import (
    epsg_3857_to_epsg_4326,
    _epsg_4326_to_epsg_3857,
    epsg_4326_to_epsg_3857,
)


def test_epsg_3857_to_epsg_4326():
    x = "1822265.950171771"
    y = "6147727.640812264"

    a = 1822265.950171771
    b = 6147727.640812264

    expected_latitude = 48.24509762761856
    expected_longitude = 16.36969354769884

    assert epsg_3857_to_epsg_4326(x, y) == (expected_latitude, expected_longitude)
    assert epsg_3857_to_epsg_4326(a, b) == (expected_latitude, expected_longitude)


def test_epsg_4326_to_epsg_3857():
    latitude = 48.24509762761856
    longitude = 16.36969354769884

    expected_x = 1822265.950171771
    expected_y = 6147727.640812264

    x, y = epsg_4326_to_epsg_3857(longitude, latitude)

    assert x == expected_x
    assert y == expected_y


def test__epsg_4326_to_epsg_3857():
    expected_x = 1822265.950171771
    expected_y = 6147727.640812264

    latitude = 48.24509762761856
    longitude = 16.36969354769884

    x, y = _epsg_4326_to_epsg_3857(longitude, latitude)

    assert abs(x - expected_x) < 0.001
    assert abs(y - expected_y) < 0.001
