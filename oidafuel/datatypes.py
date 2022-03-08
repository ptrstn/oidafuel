from dataclasses import dataclass, field
from enum import Enum


class FuelType(str, Enum):
    DIESEL = "DIE"
    SUPER_95 = "SUP"
    CNG_ERDGAS = "GAS"


class RegionType(str, Enum):
    BUNDESLAND = "BL"
    PB = "PB"


def instantiate_dataclass_field(klass, dictionary, field):
    dictionary[field] = klass.from_response_dict(dictionary[field])


def instantiate_dataclass_tuple_field(klass, dictionary, field):
    dictionary[field] = tuple(
        klass.from_response_dict(element) for element in dictionary[field]
    )


@dataclass(frozen=True, order=True)
class Region:
    region_code: int
    region_type: RegionType
    name: str
    sub_regions: tuple["Region"]
    postal_codes: tuple[str] = field(default_factory=tuple)
    cities: tuple[str] = field(default_factory=tuple)

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

        for key, value in kwargs.items():
            if isinstance(value, list):
                kwargs[key] = tuple(value)

        instantiate_dataclass_tuple_field(cls, kwargs, "sub_regions")
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
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


@dataclass(frozen=True, order=True)
class District:
    """
    Bezirk (b)

    A district (German: Bezirk) is a second-level division
    of the executive arm of the country's government in Austria.

    - region_code (int): Postal code of the municipality [c]
    - municipalities (tuple[Municipality]): List of the municipalities (Gemeinden) [g]
    - name (str): Name of the district [n]
    """

    region_code: int  # Code c
    municipalities: tuple[Municipality]  # Gemeinden g
    name: str  # Name n

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "District":
        mapping = {
            "c": "region_code",
            "g": "municipalities",
            "n": "name",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        instantiate_dataclass_tuple_field(Municipality, kwargs, "municipalities")
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class State:
    """
    Bundesland (b)

    Austria is a made up of nine states (German: Bundesländer)

    - districts (tuple[District]): b List of the districts (Bezirke) in the state [b]
    - region_code (int): Postal code of the state [c]
    - name (str): Name of the district [n]
    """

    districts: tuple[District]  # Bezirke b
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
        instantiate_dataclass_tuple_field(District, kwargs, "districts")
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class Price:
    fuel_type: FuelType
    label: str
    timestamp: str
    amount: int

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "Price":
        mapping = {
            "amount": "amount",
            "fuelType": "fuel_type",
            "label": "label",
            "timestamp": "timestamp",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class Location:
    postal_code: str
    city: str
    latitude: float
    longitude: float
    address: str = None

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "Location":
        mapping = {
            "address": "address",
            "postalCode": "postal_code",
            "city": "city",
            "latitude": "latitude",
            "longitude": "longitude",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class Contact:
    fax: str = field(default=None)
    mail: str = field(default=None)
    telephone: str = field(default=None)
    website: str = field(default=None)

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "Contact":
        return cls(**response_dict)


@dataclass(frozen=True, order=True)
class OpeningHour:
    day: str
    label: str
    order: int
    from_time: str
    to_time: str

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "OpeningHour":
        mapping = {
            "day": "day",
            "label": "label",
            "order": "order",
            "from": "from_time",
            "to": "to_time",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class OfferInformation:
    service: bool = field(default=None)
    self_service: bool = field(default=None)
    unattended: bool = field(default=None)

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "OfferInformation":
        mapping = {
            "service": "service",
            "selfService": "self_service",
            "unattended": "unattended",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class PaymentMethods:
    cash: bool = field(default=None)
    debit_card: bool = field(default=None)
    credit_card: bool = field(default=None)
    others: str = field(default=None)

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "PaymentMethods":
        mapping = {
            "cash": "cash",
            "debitCard": "debit_card",
            "creditCard": "credit_card",
            "others": "others",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class PaymentArrangements:
    access_mod: str = field(default=None)
    club_card: bool = field(default=None)
    club_card_text: str = field(default=None)
    cooperative: bool = field(default=None)

    @classmethod
    def from_response_dict(cls, response_dict: dict) -> "PaymentArrangements":
        mapping = {
            "accessMod": "access_mod",
            "clubCard": "club_card",
            "clubCardText": "club_card_text",
            "cooperative": "cooperative",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}
        return cls(**kwargs)


@dataclass(frozen=True, order=True)
class GasStation:
    identifier: int
    location: Location
    name: str = field(default=None)
    prices: tuple[Price] = field(default_factory=tuple)
    open: bool = field(default=None, compare=False, hash=False, repr=False)
    position: int = field(default=None, compare=False, hash=False, repr=False)
    contact: Contact = field(default=None, compare=False, hash=False, repr=False)
    opening_hours: tuple[OpeningHour] = field(
        default_factory=tuple, compare=False, hash=False, repr=False
    )
    offer_information: OfferInformation = field(
        default=None, compare=False, hash=False, repr=False
    )
    payment_methods: PaymentMethods = field(
        default=None, compare=False, hash=False, repr=False
    )
    payment_arrangements: PaymentArrangements = field(
        default=None, compare=False, hash=False, repr=False
    )
    distance: float = field(default=None, compare=False, hash=False, repr=False)
    other_service_offers: str = field(
        default=None, compare=False, hash=False, repr=False
    )

    @classmethod
    def from_response_dict(cls, response_dict: dict, timestamp: str) -> "GasStation":
        mapping = {
            "id": "identifier",
            "name": "name",
            "location": "location",
            "contact": "contact",
            "openingHours": "opening_hours",
            "offerInformation": "offer_information",
            "paymentMethods": "payment_methods",
            "paymentArrangements": "payment_arrangements",
            "position": "position",
            "open": "open",
            "distance": "distance",
            "prices": "prices",
            "otherServiceOffers": "other_service_offers",
        }
        kwargs = {mapping[key]: value for key, value in response_dict.items()}

        for price in kwargs["prices"]:
            price["timestamp"] = timestamp

        instantiate_dataclass_field(Location, kwargs, "location")
        instantiate_dataclass_field(Contact, kwargs, "contact")
        instantiate_dataclass_tuple_field(OpeningHour, kwargs, "opening_hours")
        instantiate_dataclass_field(OfferInformation, kwargs, "offer_information")
        instantiate_dataclass_field(PaymentMethods, kwargs, "payment_methods")
        instantiate_dataclass_field(PaymentArrangements, kwargs, "payment_arrangements")
        instantiate_dataclass_tuple_field(Price, kwargs, "prices")

        return cls(**kwargs)
