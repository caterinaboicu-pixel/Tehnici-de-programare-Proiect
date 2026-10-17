import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


# Partea 1: apeluri pentru build_url si is_https

def build_url(host, path):
    """Returneaza o adresă completă, de exemplu https://example.com/login."""
    host = host.strip().rstrip("/")
    path = path.strip().lstrip("/")
    return f"https://{host}/{path}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.strip().lower().startswith("https://")


# Partea 2: apeluri pentru show_response

def show_response(url):
    """Trimite un GET la url si afișează statusul și Content-Type."""
    try:
        response = requests.get(url, timeout=5)
        print("Status:", response.status_code)
        print("Content-Type:", response.headers.get("Content-Type", "unknown"))
    except requests.RequestException as error:
        print("Cererea a esuat:", error)


# Partea 3: apeluri pentru check_site

def check_site(url):
    """Returnează un dicționar cu status, content_type, length și server."""
    try:
        response = requests.get(url, timeout=5)

        # Pastreaza tipul principal, de exemplu text/html.
        content_type = response.headers.get("Content-Type", "unknown")
        content_type = content_type.split(";", 1)[0].strip()

        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": response.headers.get("Server", "unknown"),
        }
    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error) or "Cererea a eșuat",
        }


# Partea 4: apelul scan_sites()

def scan_sites():
    """Verifică toate site-urile, afișează rezultatele cu status 200 și un rezumat."""
    results = []

    for url in SITES:
        result = check_site(url)
        results.append((url, result))

    working_sites = [
        (url, result)
        for url, result in results
        if result.get("status") == 200
    ]

    # Sorteaza descrescator dupa lungimea raspunsului.
    working_sites.sort(
        key=lambda item: item[1].get("length", 0),
        reverse=True,
    )

    for url, result in working_sites:
        print(f"{url} -> {result['status']}, {result['length']} octeți")

    failed_count = len(results) - len(working_sites)
    print(f"Reușite: {len(working_sites)} | Eșuate: {failed_count}")


# Partea 5: apeluri pentru check_headers

def check_headers(url):
    """Returnează listele antetelor prezente și lipsă, plus scorul."""
    try:
        response = requests.get(url, timeout=5)

        # Facem comparatia cu litere mici ca sa nu conteze majusculele.
        response_headers = {name.lower() for name in response.headers}

        present = [
            name for name in SECURITY_HEADERS
            if name.lower() in response_headers
        ]
        missing = [
            name for name in SECURITY_HEADERS
            if name.lower() not in response_headers
        ]

        if SECURITY_HEADERS:
            score = int(len(present) * 100 / len(SECURITY_HEADERS))
        else:
            score = 100

        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except requests.RequestException as error:
        return {
            "status": None,
            "error": str(error) or "Cererea a eșuat",
        }


# Partea 6: apeluri pentru retry_check

def retry_check(url, attempts=3):
    """Reîncearcă cererea la erori de conexiune sau status 500+."""
    if attempts <= 0:
        return {"status": None, "attempts": 0}

    last_status = None
    last_error = None

    for attempt_number in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code

            # La status sub 500, inclusiv 404, ne oprim imediat.
            if last_status < 500:
                return {
                    "status": last_status,
                    "attempts": attempt_number,
                }

            # Daca aceasta era ultima incercare, intoarcem ultimul status.
            if attempt_number == attempts:
                return {
                    "status": last_status,
                    "attempts": attempt_number,
                }

        except requests.RequestException as error:
            last_error = str(error) or "Cererea a eșuat"

            if attempt_number == attempts:
                result = {
                    "status": last_status,
                    "attempts": attempt_number,
                }

                # Daca n-am primit niciun status, toate incercarile au esuat
                # din cauza conexiunii.
                if last_status is None:
                    result["error"] = last_error

                return result
