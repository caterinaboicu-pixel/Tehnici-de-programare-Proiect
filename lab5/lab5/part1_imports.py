# Laborator: funcții, metode și importuri pe web
# Student: Boicu Ecaterina
#
# Rulare:  python part1_imports.py        -> rulează toate exercițiile 1-8
#          python part1_imports.py 3      -> rulează doar exercițiul 3 (util pentru capturi de ecran)

import inspect
import sys
import time
import urllib.request  # Ex. 1: modul din biblioteca standard

import requests  # Ex. 1: modul extern (instalat cu pip)

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde


def run(n, title=""):
    """Returnează True dacă exercițiul n trebuie rulat și afișează un antet."""
    if len(sys.argv) > 1 and str(n) not in sys.argv[1:]:
        return False
    print(f"\n=== Exercițiul {n}: {title} ===")
    return True


# ---------------------------------------------------------------- Ex. 1
if run(1, "Primul import"):
    print("Versiunea requests:", requests.__version__)
    print("Modul standard importat:", urllib.request.__name__)
    # Explicație: requests este o bibliotecă EXTERNĂ (scrisă de terți), care nu
    # vine odată cu Python, deci trebuie descărcată cu pip install requests.
    # urllib face parte din biblioteca STANDARD: este inclus în instalarea
    # Python, așa că poate fi importat direct, fără instalare.

# ---------------------------------------------------------------- Ex. 2
if run(2, "Două stiluri de import"):
    # Stilul 1: import requests
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Stilul 1 (requests.get) -> cod de stare:", response.status_code)
    time.sleep(1)

    # Stilul 2: from requests import get
    from requests import get

    response = get(BASE_URL, timeout=TIMEOUT)
    print("Stilul 2 (get)          -> cod de stare:", response.status_code)
    # Avantaj "import requests": se vede mereu de unde vine funcția
    #   (requests.get) și nu există risc de conflict cu alte nume "get".
    # Avantaj "from requests import get": cod mai scurt, fără prefix repetat.
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 3
if run(3, "Alias-uri"):
    import requests as rq

    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print("Cod de stare (rq.get):", response.status_code)
    # Un alias face codul mai ușor de citit când numele este lung sau când
    # alias-ul este unul consacrat (import numpy as np, import pandas as pd).
    # Îl face mai greu de citit când alias-ul este criptic sau inventat
    # (rq, r, x): cine citește codul trebuie să ghicească ce înseamnă.
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 4
if run(4, "Doar biblioteca standard"):
    with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as resp:
        print("Status:", resp.status)
        body = resp.read().decode("utf-8")  # .read() dă octeți (bytes)
    print("Primele 200 de caractere:")
    print(body[:200])
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 5
if run(5, "Priviți în interiorul unui modul"):
    print(dir(requests))
    for name in ("get", "Session", "exceptions"):
        obj = getattr(requests, name)
        if inspect.ismodule(obj):
            kind = "modul"
        elif inspect.isclass(obj):
            kind = "clasă"
        else:
            kind = "funcție"
        print(f"requests.{name} este: {kind}")
    # requests.get        -> funcție
    # requests.Session    -> clasă
    # requests.exceptions -> modul

# ---------------------------------------------------------------- Ex. 6
if run(6, "Citiți documentația"):
    # Dacă apare un pager (":" jos), apăsați q pentru a ieși.
    help(requests.get)
    # În help(requests.get) se vede că **kwargs sunt argumentele lui
    # requests.request(...); acolo este documentat parametrul "timeout"
    # = timpul maxim de așteptare, în secunde.
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Cerere cu timeout=", TIMEOUT, "-> cod de stare:", response.status_code)
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 7
if run(7, "Cronometrarea unei cereri"):
    start = time.perf_counter()
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    end = time.perf_counter()
    print(f"time.perf_counter(): {end - start:.3f} s")
    print(f"response.elapsed:    {response.elapsed.total_seconds():.3f} s")
    # perf_counter măsoară tot timpul din programul nostru (inclusiv citirea
    # corpului răspunsului și munca internă a bibliotecii), deci iese de obicei
    # puțin mai mare. response.elapsed măsoară doar intervalul dintre trimiterea
    # cererii și primirea antetelor răspunsului.
    time.sleep(1)

# ---------------------------------------------------------------- Ex. 8
if run(8, "Când un import eșuează"):
    try:
        import bs4

        print("bs4 este instalat, versiunea:", bs4.__version__)
    except ImportError:
        print("Instalați modulul cu: pip install beautifulsoup4")

# ----------------------------------------------------- Întrebare de verificare
# Modul    = un singur fișier .py care conține cod (funcții, clase, constante).
# Pachet   = un director de module (cu __init__.py) ce poate conține și subpachete,
#            de ex. urllib (urllib.request, urllib.parse).
# Bibliotecă = termen general: o colecție de module/pachete cu un scop comun,
#            de ex. requests sau biblioteca standard Python.
