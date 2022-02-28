import re
from dataclasses import dataclass
from urllib.parse import quote

import requests


@dataclass
class Address:
    """
    x and y coordinates are using the EPSG:3857 system

    https://epsg.io/transform#s_srs=3857&t_srs=4326
    """

    identifier: str
    address_code: str
    address_subcode: str
    timestamp: str
    title: str
    postal_code: str
    city: str
    street: str
    house_number: str
    house_number_suffix: str
    x: str
    y: str


def _extract_address(address: dict) -> Address:
    identifier: str = address["id"]
    address_code: str = address["Adresscode"][0]
    address_subcode: str = address["AdressSubcode"][0]
    timestamp: str = address["timestamp"]
    title: str = address["title"][0]
    postal_code: str = address["PLZ"][0]
    city: str = address["Ort"][0]
    street: str = address["Strasse"][0]
    house_number: str = address["Hausnummer"][0]
    house_number_suffix: str = address["Hausnummernzusatz"][0]
    geo: str = address["geo"][0]
    x, y = re.findall(r"[\d.]+", geo)

    return Address(
        identifier=identifier,
        address_code=address_code,
        address_subcode=address_subcode,
        timestamp=timestamp,
        title=title,
        postal_code=postal_code,
        city=city,
        street=street,
        house_number=house_number,
        house_number_suffix=house_number_suffix,
        x=x,
        y=y,
    )


def extract_addresses(json_response: dict) -> list[Address]:
    return [_extract_address(address) for address in json_response["response"]["docs"]]


def search_address(text: str) -> list[Address]:
    text_suggest = f'"{text}"~20'
    encoded_text_suggest = quote(text_suggest)
    url = (
        "https://srv.doris.at"
        "/solr/searchservice/search/adressen2/"
        "?wt=json2"
        "&q=("
        f"textsuggest:{encoded_text_suggest}"
        ")"
    )

    response = requests.get(url)
    json_response = response.json()
    addresses: list[Address] = extract_addresses(json_response)

    return addresses
