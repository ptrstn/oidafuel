from dataclasses import dataclass
from enum import Enum


class FuelType(str, Enum):
    DIESEL = "DIE"
    SUPER_95 = "SUP"
    CNG_ERDGAS = "GAS"


class RegionType(str, Enum):
    BUNDESLAND = "BL"
    PB = "PB"


@dataclass
class Region:
    region_code: int
    region_type: RegionType
    name: str
    sub_regions: list["Region"]
    postal_codes: list[str] = None
    cities: list[str] = None

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "Region":
        mapping = {
            "code": "region_code",
            "type": "region_type",
            "name": "name",
            "subRegions": "sub_regions",
            "postalCodes": "postal_codes",
            "cities": "cities",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}

        if kwargs["sub_regions"]:
            kwargs["sub_regions"] = [
                cls.from_response_dict(sub_region)
                for sub_region in kwargs["sub_regions"]
            ]

        return cls(**kwargs)


@dataclass
class Municipality:
    """
    Gemeinde (g)

    A Municipality (German: Gemeinde) is the administrative division
    encompassing a single village, town, or city in Austria.

    - postal_code (str): Postal code of the municipality (german: Postleitzahl) [p]
    - name (str): Name of the municipality [n]
    - longitude (float): Longitude coordinate (german: Längengrad) [l]
    - latitude (float): Latitude coordinate (german: Breitengrad) [b]
    """

    postal_code: str  # Postleitzahl p
    name: str  # Name n
    longitude: float  # Längengrad l
    latitude: float  # Breitengrad b

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "Municipality":
        mapping = {
            "p": "postal_code",
            "n": "name",
            "l": "longitude",
            "b": "latitude",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        return cls(**kwargs)


@dataclass
class District:
    """
    Bezirk (b)

    A district (German: Bezirk) is a second-level division
    of the executive arm of the country's government in Austria.

    - region_code (int): Postal code of the municipality [c]
    - municipalities (list[Municipality]): List of the municipalities (Gemeinden) [g]
    - name (str): Name of the district [n]
    """

    region_code: int  # Code c
    municipalities: list[Municipality]  # Gemeinden g
    name: str  # Name n

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "District":
        mapping = {
            "c": "region_code",
            "g": "municipalities",
            "n": "name",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        if kwargs["municipalities"]:
            kwargs["municipalities"] = [
                Municipality.from_response_dict(municipality)
                for municipality in kwargs["municipalities"]
            ]
        return cls(**kwargs)


@dataclass
class State:
    """
    Bundesland (b)

    Austria is a made up of nine states (German: Bundesländer)

    - districts (list[District]): b List of the districts (Bezirke) in the state [b]
    - region_code (int): Postal code of the state [c]
    - name (str): Name of the district [n]
    """

    districts: list[District]  # Bezirke b
    region_code: int  # Code c
    name: str  # Name n

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "State":
        mapping = {
            "b": "districts",
            "c": "region_code",
            "n": "name",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        if kwargs["districts"]:
            kwargs["districts"] = [
                District.from_response_dict(district)
                for district in kwargs["districts"]
            ]
        return cls(**kwargs)
