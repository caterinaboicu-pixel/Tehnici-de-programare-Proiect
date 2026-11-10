

import inspect
import sys
import time
import urllib.request  

import requests  

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  


def run(n, title=""):
    """Returnează True dacă exercițiul n trebuie rulat și afișează un antet."""
    if len(sys.argv) > 1 and str(n) not in sys.argv[1:]:
        return False
    print(f"\n=== Exercițiul {n}: {title} ===")
    return True



if run(1, "Primul import"):
    print("Versiunea requests:", requests.__version__)
    print("Modul standard importat:", urllib.request.__name__)
  


if run(2, "Două stiluri de import"):
    
    response = requests.get(BASE_URL, timeout=TIMEOUT)
    print("Stilul 1 (requests.get) -> cod de stare:", response.status_code)
    time.sleep(1)

    
    from requests import get

    response = get(BASE_URL, timeout=TIMEOUT)
    print("Stilul 2 (get)          -> cod de stare:", response.status_code)
    time.sleep(1)

    import requests as rq

    response = rq.get(BASE_URL, timeout=TIMEOUT)
    print("Cod de stare (rq.get):", response.status_code)
    time.sleep(1)


if run(4, "Doar biblioteca standard"):
    with urllib.request.urlopen(BASE_URL, timeout=TIMEOUT) as resp:
        print("Status:", resp.status)
        body = resp.read().decode("utf-8")  
    print("Primele 200 de caractere:")
    print(body[:200])
    time.sleep(1)

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
   
if run(6, "Citiți documentația"):
   
    help(requests.get)
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
    time.sleep(1)

if run(8, "Când un import eșuează"):
    try:
        import bs4

        print("bs4 este instalat, versiunea:", bs4.__version__)
    except ImportError:
        print("Instalați modulul cu: pip install beautifulsoup4")

#            de ex. urllib (urllib.request, urllib.parse).
# Bibliotecă = termen general: o colecție de module/pachete cu un scop comun,
#            de ex. requests sau biblioteca standard Python.
