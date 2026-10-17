# -*- coding: utf-8 -*-
"""
Laboratorul 6, Lucrarea B - forensics pe fisiere si steganografie LSB.
"""

import re
import zipfile
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

SEMNATURI = [
    (b"%PDF", "pdf"),
    (b"\x89PNG", "png"),
    (b"\xff\xd8", "jpeg"),
    (b"PK\x03\x04", "zip/docx"),
]


def tip_real(cale):
    cap = open(cale, "rb").read(8)
    for semnatura, nume in SEMNATURI:
        if cap.startswith(semnatura):
            return nume
    return cap.hex()


def strings(cale, lungime_minima=4):
    date = open(cale, "rb").read()
    rezultate = []
    for m in re.findall((rb"[ -~]{%d,}" % lungime_minima), date):
        rezultate.append(m.decode())
    return rezultate


def _grade_zecimale(valoare_dms, emisfera):
    grade, minute, secunde = valoare_dms
    zecimal = float(grade) + float(minute) / 60 + float(secunde) / 3600
    if emisfera in ("S", "W"):
        zecimal = -zecimal
    return zecimal


def citeste_exif_si_gps(cale):
    exif = Image.open(cale)._getexif() or {}
    citibile = {}
    gps = {}
    for id_, val in exif.items():
        nume = TAGS.get(id_, id_)
        citibile[nume] = val
        if nume == "GPSInfo":
            for gps_id, gps_val in val.items():
                gps[GPSTAGS.get(gps_id, gps_id)] = gps_val

    lat = lon = None
    if gps:
        if "GPSLatitude" in gps and "GPSLatitudeRef" in gps:
            lat = _grade_zecimale(gps["GPSLatitude"], gps["GPSLatitudeRef"])
        if "GPSLongitude" in gps and "GPSLongitudeRef" in gps:
            lon = _grade_zecimale(gps["GPSLongitude"], gps["GPSLongitudeRef"])
    return citibile, gps, lat, lon


def extrage_ascuns(cale, semnatura=b"PK\x03\x04", iesire="gasit.zip"):
    date = open(cale, "rb").read()
    i = date.find(semnatura)
    if i != -1:
        with open(iesire, "wb") as f:
            f.write(date[i:])
        return i, iesire
    return -1, None


def ascunde_lsb(cale_poza, mesaj_bytes, cale_iesire="stego.png"):
    img = Image.open(cale_poza).convert("RGB")
    px = list(img.getdata())

    mesaj_cu_terminator = mesaj_bytes + b"\x00"
    biti = "".join(f"{x:08b}" for x in mesaj_cu_terminator)

    if len(biti) > len(px) * 3:
        raise ValueError("Mesajul e prea lung pentru aceasta poza.")

    px_nou = []
    idx_bit = 0
    for (r, g, b) in px:
        canale = [r, g, b]
        for c in range(3):
            if idx_bit < len(biti):
                bit = int(biti[idx_bit])
                canale[c] = (canale[c] & ~1) | bit
                idx_bit += 1
        px_nou.append(tuple(canale))

    img.putdata(px_nou)
    img.save(cale_iesire)
    return cale_iesire


def dezvaluie_lsb(cale_stego):
    px = list(Image.open(cale_stego).convert("RGB").getdata())
    biti = ""
    for (r, g, b) in px:
        biti += str(r & 1)
        biti += str(g & 1)
        biti += str(b & 1)

    octeti = bytearray()
    for i in range(0, len(biti) - 7, 8):
        octet = int(biti[i:i + 8], 2)
        if octet == 0:
            break
        octeti.append(octet)
    return bytes(octeti)


print("=== B1. Magic bytes ===")
for cale in ["probe/foto.jpg", "probe/ascuns.png", "probe/xor.bin"]:
    print(" ", cale, "->", tip_real(cale))

print()
print("=== B2. strings pe probe/ascuns.png ===")
for s in strings("probe/ascuns.png"):
    print(" ", s)

print()
print("=== B3. EXIF + GPS din probe/foto.jpg ===")
citibile, gps, lat, lon = citeste_exif_si_gps("probe/foto.jpg")
for nume, val in citibile.items():
    if nume != "GPSInfo":
        print(f"  {nume} = {val}")
if lat is not None and lon is not None:
    print(f"  Coordonate zecimale: {lat:.6f}, {lon:.6f}")

print()
print("=== B4. file carving pe probe/ascuns.png ===")
offset, cale_zip = extrage_ascuns("probe/ascuns.png")
if offset != -1:
    print(f"  arhiva gasita la octetul {offset}, extrasa in {cale_zip}")
    with zipfile.ZipFile(cale_zip) as z:
        print("  continut arhiva:", z.namelist())
        for nume in z.namelist():
            continut = z.read(nume).decode(errors="replace")
            print(f"    {nume}: {continut.strip()}")
else:
    print("  nicio arhiva gasita")

print()
print("=== B5. Ascunde mesaj LSB ===")
mesaj = b"FLAG{ascuns_in_pixeli}"
cale_stego = ascunde_lsb("probe/foto.jpg", mesaj, "stego.png")
print(f"  mesaj ascuns in {cale_stego}")

print()
print("=== B6. Dezvaluie mesajul LSB ===")
mesaj_gasit = dezvaluie_lsb("stego.png")
print("  mesaj dezvaluit:", mesaj_gasit.decode())
assert mesaj_gasit == mesaj
print("  verificare OK: mesajul dezvaluit == mesajul ascuns")
