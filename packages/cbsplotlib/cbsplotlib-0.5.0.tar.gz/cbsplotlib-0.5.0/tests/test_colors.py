from cbsplotlib.colors import CBS_COLORS_HEX

__author__ = "Eelco van Vliet"
__copyright__ = "Eelco van Vliet"
__license__ = "MIT"


def test_hex():
    """API Tests"""

    assert CBS_COLORS_HEX["corporateblauw"] == "#271D6C"
    assert CBS_COLORS_HEX["corporateblauw"] == "#271D6C"
    assert CBS_COLORS_HEX["corporatelichtblauw"] == "#00A1CD"
    assert CBS_COLORS_HEX["donkerblauw"] == "#0058B8"
    assert CBS_COLORS_HEX["donkerblauwvergrijsd"] == "#163A72"
    assert CBS_COLORS_HEX["lichtblauw"] == "#00A1CD"
    assert CBS_COLORS_HEX["lichtblauwvergrijsd"] == "#0581A2"
    assert CBS_COLORS_HEX["geel"] == "#FFCC00"
    assert CBS_COLORS_HEX["geelvergrijsd"] == "#FFB600"
    assert CBS_COLORS_HEX["oranje"] == "#F39200"
    assert CBS_COLORS_HEX["oranjevergrijsd"] == "#CE7C00"
    assert CBS_COLORS_HEX["rood"] == "#E94C0A"
    assert CBS_COLORS_HEX["roodvergrijsd"] == "#B23D02"
    assert CBS_COLORS_HEX["roze"] == "#AF0E80"
    assert CBS_COLORS_HEX["rozevergrijsd"] == "#82045E"
    assert CBS_COLORS_HEX["grasgroen"] == "#53A31D"
    assert CBS_COLORS_HEX["grasgroenvergrijsd"] == "#488225"
    assert CBS_COLORS_HEX["appelgroen"] == "#AFCB05"
    assert CBS_COLORS_HEX["appelgroenvergrijsd"] == "#899D0C"
    assert CBS_COLORS_HEX["violet"] == "#AC218E"
    assert CBS_COLORS_HEX["lichtgrijs"] == "#E0E0E0"
    assert CBS_COLORS_HEX["grijs"] == "#666666"
    assert CBS_COLORS_HEX["logogrijs"] == "#929292"
    assert CBS_COLORS_HEX["codekleur"] == "#585858"
