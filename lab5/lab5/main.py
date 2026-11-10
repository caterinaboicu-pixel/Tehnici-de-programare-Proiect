# Laborator: funcții, metode și importuri pe web
# Student: Boicu Ecaterina
#
# Rulare:  python main.py https://cybercor.org

import argparse
import sys
import time

import requests

import webtools  # Ex. 44: importăm modulul întreg
from webtools import get_title, security_headers  # Ex. 45: importăm doar anumite nume
from webtools import DEFAULT_HEADERS  # Ex. 47: importăm constanta

# Ex. 45 - Dacă main.py ar avea și o funcție proprie get_title, ar exista două
# nume get_title în același spațiu de nume: ultima definiție/atribuire o
# "suprascrie" pe cealaltă (fără nicio eroare). Dacă def get_title ar veni
# după import, ar fi folosită funcția din main.py; dacă importul ar veni după,
# ar câștiga cea din webtools. Pentru a evita conflictul se folosește
# "import webtools" (webtools.get_title) sau un alias: "import ... as ...".


def main() -> None:
    """Citește URL-ul din linia de comandă și rulează exercițiile 44-50."""
    # Ex. 48: argumentul URL vine din linia de comandă (nu din BASE_URL)
    parser = argparse.ArgumentParser(description="Raport despre un site web.")
    parser.add_argument("url", help="adresa site-ului, de ex. https://cybercor.org")
    args = parser.parse_args()
    url = args.url if args.url.startswith(("http://", "https://")) else "https://" + args.url

    try:
        print("\n=== Ex. 44: modulul webtools ===")
        response = webtools.fetch(url)
        print("Titlu:", webtools.get_title(response.text))
        time.sleep(1)

        print("\n=== Ex. 45: from webtools import get_title, security_headers ===")
        print("Titlu:", get_title(response.text))
        print("Antete de securitate:", security_headers(url))
        time.sleep(1)

        print("\n=== Ex. 47: constanta DEFAULT_HEADERS ===")
        print(DEFAULT_HEADERS)

        print("\n=== Ex. 49: raport CSV ===")
        results = webtools.check_paths(url, ["/", "/robots.txt", "/sitemap.xml"])
        webtools.save_csv(results, "report.csv")
        print(results)
        print("Salvat în report.csv")
        time.sleep(1)

        print("\n=== Ex. 50: raportul site-ului ===")
        webtools.site_report(url)
    except requests.RequestException as error:
        print("Eroare de rețea:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
