import os

from arsenal.privesc.enum import citeste_linii, nume, GTFO

START = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start")


def cai(fisier):
    """Intoarce MULTIMEA cailor din fisier."""
    return set(citeste_linii(fisier))


def main():
    # B1: doua multimi, curat si acum
    baza = cai(os.path.join(START, "baza_suid.txt"))
    acum = cai(os.path.join(START, "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))

    # B2: diferenta, ce a aparut
    noi = acum - baza
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)

    # B3: dictionar de risc si filtrul final
    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in sorted(noi) if nume(c) in GTFO]
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()