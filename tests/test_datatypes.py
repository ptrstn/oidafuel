from oidafuel.datatypes import (
    Region,
    RegionType,
    Municipality,
    District,
    State,
    GasStation,
)


class TestRegion:
    def test_from_response_dict(self):
        region_dict = {
            "code": 9,
            "type": "BL",
            "name": "Wien",
            "subRegions": [
                {
                    "code": 900,
                    "type": "PB",
                    "name": "Wien(Stadt)",
                    "subRegions": [],
                },
                {
                    "code": 901,
                    "type": "PB",
                    "name": "Wien  1.,Innere Stadt",
                    "subRegions": [],
                    "postalCodes": ["1010"],
                    "cities": ["Wien"],
                },
                {
                    "code": 902,
                    "type": "PB",
                    "name": "Wien  2.,Leopoldstadt",
                    "subRegions": [],
                    "postalCodes": ["1020"],
                    "cities": ["Wien"],
                },
            ],
            "postalCodes": [
                "1010",
                "1020",
            ],
            "cities": ["Wien"],
        }
        region = Region.from_response_dict(region_dict)
        assert region.region_code == 9
        assert region.region_type == RegionType.BUNDESLAND
        assert len(region.sub_regions) == 3
        assert region.sub_regions[0].region_code == 900
        assert region.sub_regions[0].region_type == RegionType.PB
        assert region.sub_regions[0].name == "Wien(Stadt)"
        assert not region.sub_regions[0].sub_regions
        assert region.sub_regions[1].region_code == 901
        assert region.sub_regions[1].region_type == RegionType.PB
        assert region.sub_regions[1].name == "Wien  1.,Innere Stadt"
        assert not region.sub_regions[1].sub_regions
        assert not region.sub_regions[2].sub_regions


def test_municipality_from_response_dict():
    response_dict = {"p": "1190", "n": "Wien", "l": 16.34565761, "b": 48.24574918}
    municipality = Municipality.from_response_dict(response_dict)
    assert municipality.postal_code == "1190"
    assert municipality.name == "Wien"
    assert municipality.longitude == 16.34565761
    assert municipality.latitude == 48.24574918


def test_district_from_response_dict():
    response_dict = {
        "c": 909,
        "n": "Wien  9.,Alsergrund",
        "g": [{"p": "1090", "n": "Wien", "l": 16.35787343, "b": 48.22326154}],
    }
    district = District.from_response_dict(response_dict)
    assert district.region_code == 909
    assert district.name == "Wien  9.,Alsergrund"
    assert len(district.municipalities) == 1
    assert district.municipalities[0].postal_code == "1090"
    assert district.municipalities[0].name == "Wien"
    assert district.municipalities[0].longitude == 16.35787343
    assert district.municipalities[0].latitude == 48.22326154

    response_dict = {"c": 909, "n": "Wien  9.,Alsergrund", "g": []}
    district = District.from_response_dict(response_dict)
    assert district.region_code == 909
    assert district.name == "Wien  9.,Alsergrund"
    assert len(district.municipalities) == 0


def test_state_from_response_dict():
    response_dict = {
        "c": 5,
        "n": "Salzburg",
        "b": [
            {
                "c": 501,
                "n": "Salzburg(Stadt)",
                "g": [
                    {
                        "p": "5020",
                        "n": "Salzburg",
                        "l": 13.03999414,
                        "b": 47.80459405,
                    },
                    {
                        "p": "5023",
                        "n": "Salzburg-Gnigl",
                        "l": 13.0736893,
                        "b": 47.81883887,
                    },
                ],
            },
        ],
    }
    state = State.from_response_dict(response_dict)
    assert state.region_code == 5
    assert state.name == "Salzburg"
    assert state.districts[0].name == "Salzburg(Stadt)"
    assert state.districts[0].region_code == 501
    assert state.districts[0].municipalities[1].name == "Salzburg-Gnigl"

    response_dict = {
        "c": 99,
        "n": "Problems",
        "b": [],
    }
    state = State.from_response_dict(response_dict)
    assert state.region_code == 99
    assert state.name == "Problems"
    assert not state.districts


def test_gas_station_from_response_dict():
    response_dict = {
        "id": 1354895,
        "name": "avanti - Wien Nordbahnstraße 1",
        "location": {
            "address": "Nordbahnstrasse 1",
            "postalCode": "1020",
            "city": "Wien",
            "latitude": 48.22912,
            "longitude": 16.38852,
        },
        "contact": {"telephone": "800202055", "fax": "800", "website": "www.omv.com"},
        "openingHours": [
            {
                "day": "MO",
                "label": "Montag",
                "order": 1,
                "from": "00:00",
                "to": "24:00",
            },
            {
                "day": "FE",
                "label": "Feiertag",
                "order": 8,
                "from": "00:00",
                "to": "24:00",
            },
        ],
        "offerInformation": {"service": False, "selfService": True, "unattended": True},
        "paymentMethods": {
            "cash": False,
            "debitCard": True,
            "creditCard": True,
            "others": "OMV STATIONSKARTE, DKV, MASTERCARD, DINERS, VISA",
        },
        "paymentArrangements": {"cooperative": False, "clubCard": False},
        "position": 1,
        "open": True,
        "distance": 1.4750915593739207,
        "prices": [{"fuelType": "DIE", "amount": 1.519, "label": "Diesel"}],
    }

    timestamp = "2022-03-03 03:54"

    gas_station = GasStation.from_response_dict(response_dict, timestamp)
    assert gas_station
    assert gas_station.prices[0].timestamp == timestamp
