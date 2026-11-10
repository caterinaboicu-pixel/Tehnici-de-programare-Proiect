# Laborator: funcții, metode și importuri pe web
# Student: Boicu Ecaterina
"""webtools - modulul propriu cu funcțiile reutilizabile pentru analiza unui site."""

import csv
import json
import socket
import ssl
import time
from datetime import datetime, timezone
from urllib.parse import urljoin, urlparse
import re

import requests

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  # secunde

# Ex. 47: constantă de modul, folosită în fetch()
DEFAULT_HEADERS = {"User-Agent": "WebLab-Boicu_Ecaterina"}

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


# ------------------------------------------------------- Ex. 44: funcțiile mutate
def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descarcă url cu GET (cu User-Agent personalizat) și returnează răspunsul."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru adresa url."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Returnează titlul paginii (textul dintre <title> și </title>), sau '' dacă lipsește."""
    start = html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = html.find("</title>", start)
    return html[start:end].strip()


def security_headers(url: str) -> dict:
    """Returnează {antet: True/False} pentru cele 5 antete de securitate."""
    response = fetch(url)
    return {name: name in response.headers for name in SECURITY_HEADERS}


# ----------------------------------------------- funcții folosite de site_report
def score_headers(results: dict) -> str:
    """Primește rezultatul lui security_headers și returnează scorul, ex. '3/5'."""
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list) -> dict:
    """Returnează {cale: cod_de_stare} pentru fiecare cale (None dacă cererea eșuează)."""
    results = {}
    for index, path in enumerate(paths):
        if index > 0:
            time.sleep(1)
        try:
            results[path] = get_status(base.rstrip("/") + path)
        except requests.RequestException:
            results[path] = None
    return results


def fetch_robots(base: str):
    """Returnează textul fișierului /robots.txt sau None dacă lipsește."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
    except requests.RequestException:
        return None
    return response.text if response.status_code == 200 else None


def disallowed_paths(robots_text) -> list:
    """Returnează lista valorilor Disallow: din robots_text (listă goală pentru None)."""
    if robots_text is None:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.split("#", 1)[0].strip()
        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                paths.append(value)
    return paths


def extract_links(html: str) -> list:
    """Returnează legăturile (href) din html, fără duplicate, în ordinea apariției."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links: list, domain: str):
    """Împarte legăturile în (interne, externe) față de domain; ignoră mailto:, javascript: etc."""
    domain = domain.lower().replace("www.", "", 1)
    internal, external = [], []
    for link in links:
        absolute = urljoin("https://" + domain, link)
        parsed = urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        if parsed.netloc.lower().replace("www.", "", 1) == domain:
            internal.append(absolute)
        else:
            external.append(absolute)
    return internal, external


def resolve(hostname: str) -> str:
    """Returnează adresa IP a domeniului hostname."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returnează câte zile mai sunt până la expirarea certificatului lui hostname."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()
    expires = datetime.fromtimestamp(ssl.cert_time_to_seconds(cert["notAfter"]), tz=timezone.utc)
    return (expires - datetime.now(timezone.utc)).days


def redirect_chain(hostname: str) -> list:
    """Pornește de la http://hostname și returnează lanțul de redirecționări (listă de șiruri)."""
    response = fetch("http://" + hostname)
    urls = [hop.url for hop in response.history] + [response.url]
    return [f"{hop.status_code} -> {nxt}" for hop, nxt in zip(response.history, urls[1:])]


# --------------------------------------------------------- Ex. 49: raport CSV
def save_csv(results: dict, filename: str = "report.csv") -> None:
    """Salvează rezultatul lui check_paths în CSV, cu coloanele path, status, checked_at."""
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in results.items():
            writer.writerow([path, status, datetime.now().isoformat()])


# ------------------------------------------------- Ex. 50: proiectul final
def site_report(url: str, filename: str = "report.json") -> dict:
    """Colectează, afișează și salvează în report.json raportul complet despre site."""
    hostname = urlparse(url).hostname

    response = fetch(url)  # 1. cod de stare și URL final
    time.sleep(1)
    title = get_title(response.text)  # 2. titlul
    ip = resolve(hostname)  # 3. adresa IP
    redirects = redirect_chain(hostname)  # 4. redirecționări pornind de la http://
    time.sleep(1)
    score = score_headers(security_headers(url))  # 5. scorul antetelor de securitate
    try:
        days = cert_days_left(hostname)  # 6. expirarea certificatului
    except (ssl.SSLError, OSError):
        days = None
    internal, external = split_links(extract_links(response.text), hostname)  # 7. legături
    time.sleep(1)
    disallowed = disallowed_paths(fetch_robots(url))  # 8. căi interzise

    report = {
        "url": url,
        "status_code": response.status_code,
        "final_url": response.url,
        "title": title,
        "ip": ip,
        "redirects": redirects,
        "security_score": score,
        "cert_days_left": days,
        "internal_links": len(internal),
        "external_links": len(external),
        "disallowed_paths": disallowed,
        "generated_at": datetime.now().isoformat(),
    }

    print(f"=== Raport site: {url} ===")
    print("Cod de stare:", report["status_code"], "| URL final:", report["final_url"])
    print("Titlu:", title)
    print("Adresă IP:", ip)
    print("Redirecționări:", ", ".join(redirects) if redirects else "nicio redirecționare")
    print("Scor securitate:", score)
    print("Certificat:", f"{days} de zile rămase" if days is not None else "nedeterminat")
    print("Legături:", len(internal), "interne,", len(external), "externe")
    print("Căi interzise:", ", ".join(disallowed) if disallowed else "niciuna")

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)
    print(f"Salvat în {filename}")
    return report


# ------------------------------------------------------------ Ex. 46: blocul main
if __name__ == "__main__":
    # Se execută DOAR când rulăm "python webtools.py" (atunci __name__ == "__main__").
    # La "import webtools" din main.py, __name__ este "webtools", deci blocul se sare.
    print("Autotest:", get_status("https://cybercor.org"))
