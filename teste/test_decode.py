# teste/test_decode.py
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "arsenal", "forensics"))
from decoder import desfa, ghici_strat, despica, sparge_xor


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_hex():
    strat, b = desfa("48656c6c6f")
    assert strat == "hex"
    assert b == b"Hello"


def test_url():
    strat, b = desfa("%2Fetc")
    assert strat == "url"
    assert b == b"/etc"


def test_ghici_strat_necunoscut():
    assert ghici_strat("nu e nicio codare!!") == "necunoscut"


def test_despica_straturi_multiple():
    import base64
    clar = b"FLAG{test}"
    strat_hex = clar.hex().encode()
    strat_b64_1 = base64.b64encode(strat_hex)
    strat_b64_2 = base64.b64encode(strat_b64_1)
    straturi, rezultat = despica(strat_b64_2.decode())
    assert straturi == ["base64", "base64", "hex"]
    assert rezultat == clar


def test_sparge_xor():
    secret = b"test secret"
    k = 0x42
    date = bytes(b ^ k for b in secret)
    gasite = sparge_xor(date)
    chei_gasite = {cheie for cheie, _ in gasite}
    assert k in chei_gasite
    text = dict(gasite)[k]
    assert text == "test secret"