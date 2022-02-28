import math

from pyproj import Transformer


def epsg_3857_to_epsg_4326(x, y):
    """
    https://epsg.io/transform#s_srs=3857&t_srs=4326

    :param x: X-Coordinate in EPSG:3857
    :param y: Y-Coordinate in EPSG:3857
    :return: latitude, longitude in EPSG:4326
    """
    transformer = Transformer.from_crs(3857, 4326)
    latitude, longitude = transformer.transform(x, y)
    return latitude, longitude


def epsg_4326_to_epsg_3857(longitude, latitude):
    transformer = Transformer.from_crs(4326, 3857)
    x, y = transformer.transform(latitude, longitude)
    return x, y


def _epsg_4326_to_epsg_3857(lon, lat):
    """
    https://gis.stackexchange.com/a/370496/201532
    https://epsg.io/transform#s_srs=4326&t_srs=3857

    :param lon:
    :param lat:
    :return:
    """
    x = (lon * 20037508.34) / 180
    y = math.log(math.tan(((90 + lat) * math.pi) / 360)) / (math.pi / 180)
    y = (y * 20037508.34) / 180
    return [x, y]
