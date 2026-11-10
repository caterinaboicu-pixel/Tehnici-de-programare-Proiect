import sys
import time

import requests

STUDENT = "Boicu_Ecaterina"
BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10  


def run(n, title=""):
    """Returnează True dacă exercițiul n trebuie rulat și afișează un antet."""
    if len(sys.argv) > 1 and str(n) not in sys.argv[1:]:
        return False
    print(f"\n=== Exercițiul {n}: {title} ===")
    return True


response = requests.get(BASE_URL, timeout=TIMEOUT)


if run(9, "Elementele de bază ale răspunsului"):
    print("status_code:", response.status_code)  
    print("ok:", response.ok)  
    print("url:", response.url)  
    print("encoding:", response.encoding)  


if run(10, "Tratarea erorilor cu o metodă"):
    response.raise_for_status()  
    print("Pagina principală: fără erori.")
    missing = requests.get(BASE_URL + "/this-page-does-not-exist", timeout=TIMEOUT)
    try:
        missing.raise_for_status()
    except requests.HTTPError as error:
        print("Pagina căutată nu există, dar programul continuă normal.")
        print("Detalii:", error)
    time.sleep(1)

if run(11, "Toate antetele"):
    for name, value in response.headers.items():
        print(f"{name}: {value}")


if run(12, "Metode de dicționar"):
    print("Server:", response.headers.get("Server", "lipsește"))
    print("Content-Type:", response.headers.get("Content-Type", "lipsește"))
    print("content-type (litere mici):", response.headers.get("content-type", "lipsește"))
   
if run(13, "Înlănțuirea metodelor de șir"):
    count = response.text.lower().count("cyber")
    print('Cuvântul "cyber" apare de', count, "ori")
  
if run(14, "Găsirea titlului"):
    html = response.text
    start = html.find("<title>") + len("<title>")
    end = html.find("</title>")
    title = html[start:end].strip()
    print("Titlul paginii:", title)


if run(15, "Numărarea liniilor"):
    lines = response.text.splitlines()
    print("Număr de linii:", len(lines))
    print("Lungimea celei mai lungi linii:", len(max(lines, key=len)))


if run(16, "Verificarea HTTPS"):
    if response.url.startswith("https://"):
        print("Conexiune securizată")
    else:
        print("Conexiune nesecurizată")


if run(17, "Urmărirea redirecționărilor"):
    r = requests.get("http://cybercor.org", timeout=TIMEOUT)
    if not r.history:
        print("Nicio redirecționare.")
    for hop in r.history:
        print(hop.status_code, hop.url)
    print("URL final:", r.url)
    time.sleep(1)


if run(18, "HEAD versus GET"):
    head = requests.head(BASE_URL, timeout=TIMEOUT)
    time.sleep(1)
    get = requests.get(BASE_URL, timeout=TIMEOUT)
    print("len(content) la HEAD:", len(head.content))
    print("len(content) la GET: ", len(get.content))
   
    time.sleep(1)


if run(19, "Cookie-uri"):
    found = False
    for cookie in response.cookies:
        found = True
        print("Cookie:", cookie.name, "| secure:", cookie.secure)
    if not found:
        print("Niciun cookie setat")


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

