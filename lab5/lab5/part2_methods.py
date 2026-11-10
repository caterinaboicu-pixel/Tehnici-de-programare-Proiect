# Laborator: funcții, metode și importuri pe web
# Student: Boicu Ecaterina
#
# Rulare:  python part2_methods.py        -> rulează toate exercițiile 9-20
#          python part2_methods.py 12     -> rulează doar exercițiul 12

import sys
import time

import requests

STUDENT = "Boicu_Ecaterina"
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def run(n, title=""):
    """Returnează True dacă exercițiul n trebuie rulat și afișează un antet."""
    if len(sys.argv) > 1 and str(n) not in sys.argv[1:]:
        return False
    print(f"\n=== Exercițiul {n}: {title} ===")
    return True


# O singură cerere către pagina principală, folosită în exercițiile 9-16 și 19
# (ca să nu trimitem inutil multe cereri către site).
response = requests.get(BASE_URL, timeout=TIMEOUT)

# ---------------------------------------------------------------- Ex. 9
if run(9, "Elementele de bază ale răspunsului"):
    print("status_code:", response.status_code)  # atribut
    print("ok:", response.ok)  # atribut (property, fără paranteze)
    print("url:", response.url)  # atribut
    print("encoding:", response.encoding)  # atribut

# ---------------------------------------------------------------- Ex. 10
if run(10, "Tratarea erorilor cu o metodă"):
    response.raise_for_status()  # metodă: nu face nimic dacă totul e în regulă
    print("Pagina principală: fără erori.")
    missing = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    try:
        missing.raise_for_status()
    except requests.HTTPError as error:
        print("Pagina căutată nu există, dar programul continuă normal.")
        print("Detalii:", error)
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 11
if run(11, "Toate antetele"):
    for name, value in response.headers.items():
        print(f"{name}: {value}")

# ---------------------------------------------------------------- Ex. 12
if run(12, "Metode de dicționar"):
    print("Server:", response.headers.get("Server", "lipsește"))
    print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
    print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))
    # Observație: se obține aceeași valoare. response.headers este un dicționar
    # care NU ține cont de majuscule/minuscule (CaseInsensitiveDict), conform
    # standardului HTTP, în care numele antetelor sunt insensibile la majuscule.

# ---------------------------------------------------------------- Ex. 13
if run(13, "Înlănțuirea metodelor de șir"):
    count = response.text.lower().count("cyber")
    print('Cuvântul "cyber" apare de', count, "ori")
    # Se pot înlănțui deoarece .lower() returnează un șir nou (str), iar pe un
    # șir se poate apela direct metoda .count(). Fiecare metodă lucrează pe
    # rezultatul celei dinaintea ei.

# ---------------------------------------------------------------- Ex. 14
if run(14, "Găsirea titlului"):
    html = response.text
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    title = html[start:end].strip()
    print("Titlul paginii:", title)

# ---------------------------------------------------------------- Ex. 15
if run(15, "Numărarea liniilor"):
    lines = response.text.splitlines()
    print("Număr de linii:", len(lines))
    print("Lungimea celei mai lungi linii:", len(max(lines, key=len)))

# ---------------------------------------------------------------- Ex. 16
if run(16, "Verificarea HTTPS"):
    if response.url.startswith("https://"):
        print("Conexiune securizată")
    else:
        print("Conexiune nesecurizată")

# ---------------------------------------------------------------- Ex. 17
if run(17, "Urmărirea redirecționărilor"):
    r = requests.get("http://cybercor.org", timeout=TIMEOUT)
    if not r.history:
        print("Nicio redirecționare.")
    for hop in r.history:
        print(hop.status_code, hop.url)
    print("URL final:", r.url)
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 18
if run(18, "HEAD versus GET"):
    head = requests.head(BASE_URL, timeout=TIMEOUT)
    time.sleep(1)
    get = requests.get(BASE_URL, timeout=TIMEOUT)
    print("len(content) la HEAD:", len(head.content))
    print("len(content) la GET: ", len(get.content))
    # HEAD cere serverului doar antetele, fără corpul paginii, deci content este
    # gol (0 octeți). GET returnează și corpul (codul HTML), deci este mai mare.
    # HEAD e util pentru a verifica rapid o pagină fără a descărca tot conținutul.
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 19
if run(19, "Cookie-uri"):
    found = False
    for cookie in response.cookies:
        found = True
        print("Cookie:", cookie.name, "| secure:", cookie.secure)
    if not found:
        print("Niciun cookie setat")

# ---------------------------------------------------------------- Ex. 20
if run(20, "Sesiuni"):
    session = requests.Session()
    session.headers.update({"User-Agent": f"WebLab-{STUDENT}"})
    echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
    sent = echo.json()["headers"].get("User-Agent")
    print("User-Agent primit de server:", sent)
    if sent == f"WebLab-{STUDENT}":
        print("Confirmat: antetul personalizat a fost trimis.")
    else:
        print("Atenție: antetul nu coincide.")

# ----------------------------------------------------- Întrebare de verificare
# response.text este un ATRIBUT (property): îl citim, nu îl "executăm"; valoarea
# (corpul ca șir de caractere) este deja disponibilă, deci nu are paranteze.
# response.json() este o METODĂ: execută o acțiune (analizează corpul ca JSON
# și construiește un dicționar/o listă), poate primi argumente și poate eșua
# (ValueError dacă textul nu este JSON valid) - de aceea se apelează cu paranteze.
