
import sys
import time

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def run(n, title=""):
    """Returnează True dacă exercițiul n trebuie rulat și afișează un antet."""
    if len(sys.argv) > 1 and str(n) not in sys.argv[1:]:
        return False
    print(f"\n=== Exercițiul {n}: {title} ===")
    return True



def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Descarcă url cu GET și returnează obiectul răspuns (timeout implicit 10 s)."""
    return requests.get(url, timeout=timeout)



def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.status_code



def get_title(html: str) -> str:
    """Returnează titlul paginii (textul dintre <title> și </title>).

    Funcția primește codul HTML ca șir de caractere și nu face operații de
    rețea. Dacă pagina nu are titlu, returnează un șir gol.
    """
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()



def page_exists(url: str) -> bool:
    """Returnează True dacă pagina răspunde cu un cod sub 400, altfel False.

    Erorile de rețea (domeniu inexistent, timeout etc.) dau False, nu excepție.
    """
    try:
        response = requests.get(url, timeout=TIMEOUT)
        return response.status_code < 400
    except requests.RequestException:
        return False



def check_paths(base: str, paths: list) -> dict:
    """Returnează un dicționar {cale: cod_de_stare} pentru fiecare cale din paths.

    Dacă o cerere eșuează, în dicționar se pune None. Între cereri se așteaptă 1 s.
    """
    results = {}
    for index, path in enumerate(paths):
        if index > 0:
            time.sleep(1)
        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None
    return results



def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea antetului name pentru url, sau default dacă lipsește."""
    response = requests.get(url, timeout=TIMEOUT)
    return response.headers.get(name, default)



def security_headers(url: str) -> dict:
    """Returnează {antet: True/False} pentru cele 5 antete de securitate."""
    response = requests.get(url, timeout=TIMEOUT)
    return {name: name in response.headers for name in SECURITY_HEADERS}



    """Primește dicționarul din security_headers și returnează un scor, ex. '3/5'."""
    return f"{sum(results.values())}/{len(results)}"



def fetch_robots(base: str):
    """Returnează textul fișierului /robots.txt sau None dacă lipsește."""
    try:
        response = requests.get(base.rstrip("/") + "/robots.txt", timeout=TIMEOUT)
    except requests.RequestException:
        return None
    if response.status_code != 200:
        return None
    return response.text


def disallowed_paths(robots_text) -> list:
    """Returnează lista valorilor Disallow: din robots_text (listă goală pentru None)."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()  # ignoră comentariile
        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                paths.append(value)
    return paths



def response_times(*urls: str) -> dict:
    """Returnează {url: secunde} pentru oricâte adrese primește."""
    times = {}
    for index, url in enumerate(urls):
        if index > 0:
            time.sleep(1)
        start = time.perf_counter()
        requests.get(url, timeout=TIMEOUT)
        times[url] = round(time.perf_counter() - start, 3)
    return times



def log(message: str, **details) -> None:
    """Afișează mesajul urmat de fiecare detaliu, în forma: mesaj | cheie=valoare."""
    parts = [message] + [f"{key}={value}" for key, value in details.items()]
    print(" | ".join(parts))



if run(21, "Prima funcție"):
    response = fetch(BASE_URL)
    print("Cod de stare:", response.status_code)

if run(22, "Returnarea unei singure valori"):
    for path in ("/", "/robots.txt", "/sitemap.xml"):
        print(path, "->", get_status(BASE_URL + path))
        time.sleep(1)

if run(23, "Parametri impliciți"):
    print("timeout implicit (10 s):", fetch(BASE_URL).status_code)
    time.sleep(1)
    print("timeout=3:", fetch(BASE_URL, timeout=3).status_code)

if run(24, "O singură sarcină pe funcție"):
    html = fetch(BASE_URL).text  
    print("Titlu:", get_title(html))  
    print("Test fără rețea:", get_title("<html><title> Test </title></html>"))

if run(25, "Docstring-uri"):
    help(get_title)

if run(26, "Adnotări de tip"):
    try:
        print(get_status(123))
    except Exception as error:
        print("Eroare:", type(error).__name__, "-", error)


if run(27, "Fără opriri neașteptate"):
    print(BASE_URL, "->", page_exists(BASE_URL))
    print("https://this-domain-does-not-exist.invalid ->",
          page_exists("https://this-domain-does-not-exist.invalid"))

if run(28, "Returnarea unui dicționar"):
    print(check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

if run(29, "Argumente cu nume"):
    print("Server:", get_header(BASE_URL, name="Server"))
    time.sleep(1)
    print("X-Inexistent:", get_header(BASE_URL, name="X-Inexistent"))

if run(30, "Antete de securitate"):
    for name, present in security_headers(BASE_URL).items():
        print(f"{name}: {present}")

if run(31, "Funcții care apelează funcții"):
    print("Scor:", score_headers(security_headers(BASE_URL)))

if run(32, "Două funcții, o sarcină"):
    robots = fetch_robots(BASE_URL)
    print("Căi interzise:", disallowed_paths(robots))
    print("Cu None:", disallowed_paths(None))

if run(33, "Oricâte argumente"):
    print(response_times(BASE_URL, ECHO_URL + "/get"))

if run(34, "Argumente cu nume colectate"):
    log("verificat", url=BASE_URL, status=200)

