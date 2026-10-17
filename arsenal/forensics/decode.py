# -*- coding: utf-8 -*-
"""
Laboratorul 6, Lucrarea A - decoderul universal.
"""

import re
import base64
import hashlib
from urllib.parse import unquote


def ghici_strat(s):
    # URL-encoded: contine secvente %xx (doua cifre hex dupa %)
    if re.search(r"%[0-9A-Fa-f]{2}", s):
        return "url"
    # Hex: doar 0-9 a-f A-F, lungime para, si nevid
    if len(s) > 0 and len(s) % 2 == 0 and re.fullmatch(r"[0-9A-Fa-f]+", s):
        return "hex"
    # Base64: alfabetul standard, lungime multiplu de 4 (cu padding optional)
    if len(s) > 0 and len(s) % 4 == 0 and re.fullmatch(r"[A-Za-z0-9+/]+={0,2}", s):
        return "base64"
    return "necunoscut"


def desfa(s):
    strat = ghici_strat(s)
    if strat == "base64":
        rezultat = base64.b64decode(s)
    elif strat == "hex":
        rezultat = bytes.fromhex(s)
    elif strat == "url":
        rezultat = unquote(s).encode()
    else:
        rezultat = s.encode()
    return strat, rezultat


def citibil(b):
    """True daca toti octetii sunt in intervalul tiparibil ASCII 32..126."""
    return len(b) > 0 and all(32 <= c < 127 for c in b)


def despica(val, max_incercari=8, afiseaza=False):
    """
    Decodeaza repetat 'val' cat timp forma lui mai este recunoscuta ca un
    strat de codare (ghici_strat != "necunoscut"), pana nu mai e nimic de
    desfacut (text clar) sau se epuizeaza incercarile.
    """
    straturi = []
    cur = val
    b = cur.encode() if isinstance(cur, str) else cur
    for _ in range(max_incercari):
        strat, b = desfa(cur)
        if strat == "necunoscut":
            break
        straturi.append(strat)
        try:
            cur = b.decode()
        except UnicodeDecodeError:
            break
    if afiseaza:
        print("straturi:", " -> ".join(straturi) if straturi else "(niciunul)")
        try:
            print("rezultat:", b.decode())
        except UnicodeDecodeError:
            print("rezultat (hex):", b.hex())
    return straturi, b


def sparge_xor(date):
    """Incearca toate cele 256 de chei pe un singur octet; intoarce
    lista de (cheie, text_clar) pentru rezultatele citibile."""
    gasite = []
    for k in range(256):
        clar = bytes(b ^ k for b in date)
        if citibil(clar):
            gasite.append((k, clar.decode()))
    return gasite


ALGORITM_DUPA_LUNGIME = {32: "md5", 40: "sha1", 64: "sha256"}


def sparge_hash(tinta, cale_wordlist):
    tinta = tinta.strip().lower()
    algoritm = ALGORITM_DUPA_LUNGIME.get(len(tinta))
    if algoritm is None:
        return None, None
    for cuv in open(cale_wordlist, encoding="latin1"):
        cuv = cuv.strip()
        if not cuv:
            continue
        h = hashlib.new(algoritm, cuv.encode())
        if h.hexdigest() == tinta:
            return algoritm, cuv
    return algoritm, None

import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    p = argparse.ArgumentParser(
        description="Decoder universal: recunoaste si desface straturi de "
                     "codare; sparge XOR pe un octet sau hash prin dictionar."
    )
    p.add_argument("intrare", help="sirul de decodat, sau calea unui fisier (cu --fisier)")
    p.add_argument("--fisier", action="store_true", help="trateaza 'intrarea' ca o cale catre un fisier binar")
    p.add_argument("--wordlist", default=os.path.join(HERE, "..", "..", "probe", "wordlist.txt"),
                    help="wordlist pentru sparge_hash (implicit probe/wordlist.txt)")
    p.add_argument("--xor", action="store_true", help="trateaza intrarea (fisier) ca text XOR-at pe un octet si sparge-l")
    p.add_argument("--hash", action="store_true", help="trateaza intrarea ca un hash de parola si sparge-l prin dictionar")
    a = p.parse_args()

    fisa = {}

    if a.fisier:
        with open(a.intrare, "rb") as f:
            date = f.read()
    else:
        date = None

    if a.xor:
        continut = date if date is not None else a.intrare.encode()
        gasite = sparge_xor(continut)
        fisa = {"mod": "xor", "rezultate": [{"cheie": k, "text": t} for k, t in gasite]}
        for k, t in gasite:
            print("cheie:", k, "->", t)

    elif a.hash:
        algoritm, parola = sparge_hash(a.intrare, a.wordlist)
        fisa = {"mod": "hash", "algoritm": algoritm, "tinta": a.intrare, "parola": parola}
        if parola:
            print("algoritm:", algoritm, "| gasit:", parola)
        else:
            print("algoritm:", algoritm, "| nu s-a gasit in wordlist")

    else:
        if date is not None:
            try:
                sursa = date.decode()
            except UnicodeDecodeError:
                sursa = date.hex()
        else:
            sursa = a.intrare

        straturi, rezultat = despica(sursa)
        try:
            rezultat_text = rezultat.decode()
        except UnicodeDecodeError:
            rezultat_text = rezultat.hex()

        fisa = {"straturi": straturi, "rezultat": rezultat_text}
        print("straturi:", " -> ".join(straturi) if straturi else "(niciunul)")
        print("rezultat:", rezultat_text)

    cale_fisa = os.path.join(HERE, "fisa.json")
    with open(cale_fisa, "w", encoding="utf-8") as f:
        json.dump(fisa, f, ensure_ascii=False, indent=2)
        print("fisa salvata in:", cale_fisa)


if __name__ == "__main__":
    main()