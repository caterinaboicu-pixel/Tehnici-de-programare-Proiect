import re
import sys
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")


def esec(linie):
    """Intoarce (user, ip) daca linia e un esec de autentificare, altfel None."""
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))


def citeste_esecuri(cale):
    """Intoarce lista de dictionare {"user": ..., "ip": ...} din jurnal."""
    esecuri = []
    try:
        f = open(cale, encoding="utf-8")
    except FileNotFoundError:
        print("nu gasesc", cale)
        return esecuri
    with f:
        for linie in f:
            r = esec(linie)
            if r is not None:
                esecuri.append({"user": r[0], "ip": r[1]})
    return esecuri


def pe_ip(esecuri):
    """Intoarce un Counter al adreselor IP din lista de esecuri."""
    return Counter(e["ip"] for e in esecuri)


def main():
    if len(sys.argv) < 2:
        print("utilizare: python -m arsenal.aparare.parse_auth <jurnal>")
        return
    esecuri = citeste_esecuri(sys.argv[1])
    counts = pe_ip(esecuri)
    print("Esecuri de autentificare:", len(esecuri))
    for ip, n in counts.most_common():
        print(f"  {ip}: {n}")


if __name__ == "__main__":
    main()
