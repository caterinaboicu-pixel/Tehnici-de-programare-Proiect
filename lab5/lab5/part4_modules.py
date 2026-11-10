# Laborator: funcții, metode și importuri pe web
# Student: Boicu Ecaterina
#
# Rulare:  python part4_modules.py        -> rulează toate exercițiile 35-43
#          python part4_modules.py 39     -> rulează doar exercițiul 39

import hashlib
import json
import re
import socket
import ssl
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

_cache = {}


def run(n, title=""):
    """Returnează True dacă exercițiul n trebuie rulat și afișează un antet."""
    if len(sys.argv) > 1 and str(n) not in sys.argv[1:]:
        return False
    print(f"\n=== Exercițiul {n}: {title} ===")
    return True


def page_html(url: str) -> str:
    """Descarcă o singură dată codul HTML al paginii (următoarele apeluri folosesc memoria)."""
    if url not in _cache:
        _cache[url] = requests.get(url, timeout=TIMEOUT).text
    return _cache[url]


# ------------------------------------------------------------------ Ex. 35
def describe_url(url: str) -> None:
    """Descompune url cu urlparse și afișează fiecare componentă."""
    parts = urllib.parse.urlparse(url)
    print("scheme:  ", parts.scheme)
    print("netloc:  ", parts.netloc)
    print("path:    ", parts.path)
    print("query:   ", parts.query)
    print("fragment:", parts.fragment)


# ------------------------------------------------------------------ Ex. 36
def make_absolute(base: str, links: list) -> list:
    """Transformă legăturile relative în URL-uri complete, pornind de la base."""
    return [urllib.parse.urljoin(base, link) for link in links]


# ------------------------------------------------------------------ Ex. 37
def extract_links(html: str) -> list:
    """Returnează legăturile (href) din html, fără duplicate, în ordinea apariției."""
    links = re.findall(r'href="([^"]+)"', html)
    return list(dict.fromkeys(links))


# ------------------------------------------------------------------ Ex. 38
def split_links(links: list, domain: str):
    """Împarte legăturile în (interne, externe) față de domain (ex. 'cybercor.org').

    Legăturile relative se transformă mai întâi cu urljoin; apoi se compară
    urlparse().netloc cu domeniul. Schemele non-web (mailto:, javascript:) se ignoră.
    """
    domain = domain.lower().replace("www.", "", 1)
    internal, external = [], []
    for link in links:
        absolute = urljoin("https://" + domain, link)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        host = parsed.netloc.lower().replace("www.", "", 1)
        if host == domain:
            internal.append(absolute)
        else:
            external.append(absolute)
    return internal, external


# ------------------------------------------------------------------ Ex. 39
class ImageFinder(HTMLParser):
    """Parser HTML care colectează atributul src al fiecărui tag <img>."""

    def __init__(self):
        """Pregătește lista goală în care se vor colecta adresele imaginilor."""
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Apelată automat de parser la fiecare tag de deschidere (și la <img ... />)."""
        if tag == "img":  # HTMLParser dă numele tag-urilor deja cu litere mici
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


# ------------------------------------------------------------------ Ex. 40
def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA-256 (hexazecimal) a conținutului paginii url."""
    response = requests.get(url, timeout=TIMEOUT)
    return hashlib.sha256(response.content).hexdigest()


# ------------------------------------------------------------------ Ex. 41
def save_headers(url: str, filename: str = "headers.json") -> dict:
    """Salvează antetele paginii url în filename (JSON) și returnează ce s-a salvat."""
    response = requests.get(url, timeout=TIMEOUT)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(dict(response.headers), file, indent=2)
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


# ------------------------------------------------------------------ Ex. 42
def resolve(hostname: str) -> str:
    """Returnează adresa IP a domeniului hostname (interogare DNS)."""
    return socket.gethostbyname(hostname)


# ------------------------------------------------------------------ Ex. 43
def cert_days_left(hostname: str) -> int:
    """Returnează câte zile mai sunt până la expirarea certificatului lui hostname."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()
    expires = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notAfter"]), tz=timezone.utc)
    return (expires - datetime.now(timezone.utc)).days


# =============================================================== APELURI
if run(35, "Descompunerea unui URL"):
    describe_url("https://cybercor.org/path?x=1#top")

if run(36, "Compunerea URL-urilor"):
    for link, full in zip(["/about", "contact.html", "../index.html"],
                          make_absolute(BASE_URL, ["/about", "contact.html", "../index.html"])):
        print(f"{link:15} -> {full}")

if run(37, "Extragerea legăturilor"):
    links = extract_links(page_html(BASE_URL))
    print(len(links), "legături unice:")
    for link in links:
        print(" ", link)

if run(38, "Interne sau externe?"):
    internal, external = split_links(extract_links(page_html(BASE_URL)), "cybercor.org")
    print("Interne:", len(internal))
    for link in internal:
        print("  ", link)
    print("Externe:", len(external))
    for link in external:
        print("  ", link)

if run(39, "Propriile metode (HTMLParser)"):
    test_html = """
    <html><body>
    <img src="/logo.png" alt="Logo">
    <IMG SRC="poza.jpg">
    <img alt="imagine fără src">
    <img src="https://cdn.example.com/banner.webp" />
    <a href="/despre">Aceasta nu este o imagine</a>
    </body></html>
    """
    finder = ImageFinder()
    finder.feed(test_html)
    print(finder.images)
    assert finder.images == [
        "/logo.png",  # imagine obișnuită
        "poza.jpg",  # tag scris cu majuscule
        "https://cdn.example.com/banner.webp",  # tag care se închide singur
    ], "Parserul nu a găsit exact imaginile așteptate"
    print("Testul a trecut!")

    html = page_html(BASE_URL)
    finder = ImageFinder()
    finder.feed(html)
    print(len(finder.images), "imagini găsite")
    for src in finder.images:
        print(src)
    print('Verificare: html.lower().count("<img") =', html.lower().count("<img"))

if run(40, "Amprenta paginii"):
    first = page_fingerprint(BASE_URL)
    time.sleep(1)
    second = page_fingerprint(BASE_URL)
    print("Prima:  ", first)
    print("A doua: ", second)
    print("Identice:", first == second)
    # Amprentele ar fi diferite dacă pagina s-a modificat între cereri: conținut
    # dinamic (dată/oră, contor de vizite, token CSRF, reclame, recomandări) sau
    # dacă administratorul a actualizat pagina. Chiar și un singur octet diferit
    # schimbă complet hash-ul SHA-256.

if run(41, "Salvarea în JSON"):
    data = save_headers(BASE_URL)
    print("Salvate", len(data), "antete în headers.json")
    ctype = next((v for k, v in data.items() if k.lower() == "content-type"), "lipsește")
    print("Content-Type din fișier:", ctype)

if run(42, "Interogare DNS"):
    print("Adresa IP pentru cybercor.org:", resolve("cybercor.org"))

if run(43, "Expirarea certificatului"):
    print("Zile rămase până la expirarea certificatului:", cert_days_left("cybercor.org"))

# ----------------------------------------------------- Întrebare de verificare
# handle_starttag() este apelată de PARSER, nu de noi: când apelăm feed(html),
# HTMLParser parcurge textul și, la fiecare tag de deschidere întâlnit, apelează
# automat metoda handle_starttag(tag, attrs). Noi doar o suprascriem (override)
# ca să spunem ce să se întâmple - este principiul "callback" / "nu ne sunați,
# vă sunăm noi" (inversiunea controlului).
