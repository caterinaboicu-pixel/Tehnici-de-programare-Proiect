# Laborator: funcții, metode și importuri pe web
# Student: Boicu Ecaterina
# Bonus: get_title() și extract_links() rescrise cu BeautifulSoup
# Instalare:  pip install beautifulsoup4

import requests
from bs4 import BeautifulSoup

import webtools

BASE_URL = "https://cybercor.org"


def get_title_bs4(html: str) -> str:
    """Returnează titlul paginii folosind BeautifulSoup (șir gol dacă lipsește)."""
    soup = BeautifulSoup(html, "html.parser")
    return soup.title.get_text(strip=True) if soup.title else ""


def extract_links_bs4(html: str) -> list:
    """Returnează legăturile (href) fără duplicate, folosind BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")
    return list(dict.fromkeys(a["href"] for a in soup.find_all("a", href=True)))


if __name__ == "__main__":
    html = requests.get(BASE_URL, timeout=10).text
    print("Titlu (manual):", webtools.get_title(html))
    print("Titlu (bs4):   ", get_title_bs4(html))
    print("Legături (re): ", len(webtools.extract_links(html)))
    print("Legături (bs4):", len(extract_links_bs4(html)))
    # Comparație: cu bs4 funcțiile au 2-3 linii, fără find()/slicing sau regex.
    # Sunt și mai sigure: bs4 înțelege HTML-ul real (<title lang="ro">, <TITLE>,
    # href cu apostrof sau fără ghilimele, majuscule), pe când find("<title>") și
    # regex-ul r'href="..."' ratează aceste cazuri.
