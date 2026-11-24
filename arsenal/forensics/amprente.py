# arsenal/forensics/amprente.py
# Unealta de forensics: tip dupa magic bytes + amprenta SHA-256, cu with.
import argparse
import hashlib
import os

MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}


def tip(head):
    """Intoarce tipul fisierului dupa primii octeti (magic bytes)."""
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"          # DUPA bucla, nu inauntru


def amprenta_fisier(cale):
    """Citeste fisierul in mod binar (cu with) si intoarce o fisa."""
    with open(cale, "rb") as f:   # "rb" = binar; with il inchide singur
        date = f.read()
    return {
        "nume": os.path.basename(cale),
        "tip": tip(date[:8]),
        "sha256": hashlib.sha256(date).hexdigest()[:16],
    }


def scaneaza(folder):
    """Amprenteaza toate fisierele dintr-un folder (in ordine alfabetica)."""
    rez = []
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            rez.append(amprenta_fisier(cale))
    return rez


def main():
    parser = argparse.ArgumentParser(
        description="Amprente SHA-256 si tip (magic bytes) pentru fisierele unui folder"
    )
    parser.add_argument("folder", help="folderul cu fisierele de examinat")
    args = parser.parse_args()

    for fisa in scaneaza(args.folder):
        print(f"{fisa['nume']:14} {fisa['tip']:11} {fisa['sha256']}")


if __name__ == "__main__":
    main()
