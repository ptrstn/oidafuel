import requests

POSTAL_CODE_DATASET_URL = "https://data.rtr.at/api/v1/tables/plz.json"


def load_postal_code_dataset() -> list[dict]:
    response = requests.get(POSTAL_CODE_DATASET_URL)
    json_response = response.json()
    data = json_response.get("data")
    return data


def extract_postal_codes(dataset: list[dict]) -> list[str]:
    return [entry["plz"] for entry in dataset]


def load_postal_codes():
    dataset = load_postal_code_dataset()
    postal_codes = extract_postal_codes(dataset)
    return sorted(set(postal_codes))
