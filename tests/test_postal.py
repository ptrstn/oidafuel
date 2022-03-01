from oidafuel.postal import load_postal_code_dataset, load_postal_codes


def test_load_postal_code_dataset():
    dataset = load_postal_code_dataset()
    assert dataset[0]["plz"] == 1010
    assert dataset[1]["plz"] == 1020
    assert dataset[2]["plz"] == 1030
    assert dataset[3]["plz"] == 1040
    assert dataset[4]["plz"] == 1050
    assert dataset[5]["plz"] == 1060
    assert dataset[6]["plz"] == 1070
    assert dataset[7]["plz"] == 1080
    assert dataset[8]["plz"] == 1090
    assert dataset[9]["plz"] == 1100
    assert dataset[10]["plz"] == 1110
    assert dataset[11]["plz"] == 1120
    assert dataset[12]["plz"] == 1130


def test_load_postal_codes():
    postal_codes = load_postal_codes()
    assert postal_codes[0] == 1010
    assert postal_codes[12] == 1130
    assert 3000 > len(postal_codes) > 2220
