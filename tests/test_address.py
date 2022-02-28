from oidafuel.address import search_address


def test_search_address():
    addresses = search_address("Molkereistraße 1, Wien")
    assert len(addresses) == 2
    assert addresses[0].title == "Molkereistraße 1/ 1 1020 Wien"
    assert addresses[0].x == "1825793.7718169354"
    assert addresses[0].y == "6143368.301029718"

    addresses = search_address("Brigittenauer Lände")
    assert len(addresses) == 5

    addresses = search_address("Brigittenauer Lände 224")
    assert len(addresses) == 1
    assert addresses[0].title == "Brigittenauer Lände 224- 228 1200 Wien"
    assert addresses[0].x == "1822265.950171771"
    assert addresses[0].y == "6147727.640812264"
