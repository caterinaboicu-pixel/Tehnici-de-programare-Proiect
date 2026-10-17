# Laboratorul 6 — Informații invizibile: forensics și steganografie

## Lucrarea A — Decoderul universal

- Mesajul din `mesaj.txt` se desface prin: base64 → base64 → hex → **FLAG{straturi_de_encoding}**
- Cheia XOR găsită prin forță brută pe `xor.bin`: **128 (0x80)** → text clar: „Un singur octet tine tot secretul... gaseste-l! FLAG{xor_un_octet}"
- Parola spartă prin dicționar din primul hash MD5: **password**

## Lucrarea B — Forensics și steganografie

- **B1**: `foto.jpg` și `ascuns.png` sunt confirmate ca fiind cu adevărat JPEG/PNG (magic bytes corecte); `xor.bin` nu are nicio semnătură cunoscută.
- **B2**: `strings` pe `ascuns.png` dezvăluie textul `secret.txt` și semnătura `PK` lipite la coadă.
- **B3**: EXIF din `foto.jpg` arată Apple iPhone 13, dată 2026:09:14, coordonate GPS **47.016667, 28.857500** (Chișinău).
- **B4**: arhiva ZIP ascunsă în `ascuns.png` a fost extrasă (găsită la octetul 782) → `secret.txt` conține **FLAG{ascuns_prin_carving}**
- **B5/B6**: mesajul `FLAG{ascuns_in_pixeli}` a fost ascuns prin steganografie LSB în `stego.png` și recuperat cu succes, identic cu originalul.