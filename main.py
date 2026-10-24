"""
main.py: tretí projekt do Engeto Online Python Akadémie

author: Roman Nagy
email: romankonagy@gmail.com
"""
import csv
import sys

import requests
from bs4 import BeautifulSoup

ZACIATOK_ODKAZU = "https://www.volby.cz/pls/ps2017nss/ps32"
ZAKLAD_WEBU = "https://www.volby.cz/pls/ps2017nss/"


def skontroluj_argumenty(argumenty: list[str]) -> tuple[str, str]:
    """Skontroluje argumenty z prikazoveho riadku a vrati odkaz a subor.

    Ak nieco nesedi, vypise chybu a ukonci program.
    """
    if len(argumenty) != 3:
        print("Zadaj 2 argumenty: odkaz na územný celok a názov súboru .csv")
        print('Príklad: python main.py "<odkaz>" vysledky.csv')
        sys.exit()

    odkaz = argumenty[1]
    subor = argumenty[2]

    # odkaz moze byt aj bez www
    odkaz = odkaz.replace("https://volby.cz", "https://www.volby.cz")

    if not odkaz.startswith(ZACIATOK_ODKAZU):
        print("Prvý argument musí byť odkaz na územný celok z volby.cz")
        print("(napr. " + ZACIATOK_ODKAZU + "?xjazyk=CZ&xkraj=12"
              + "&xnumnuts=7103)")
        sys.exit()

    if not subor.endswith(".csv"):
        print("Druhý argument musí byť názov súboru s príponou .csv")
        sys.exit()

    return odkaz, subor


def stiahni_stranku(odkaz: str) -> BeautifulSoup:
    """Stiahne stranku a vrati ju ako BeautifulSoup objekt."""
    odpoved = requests.get(odkaz)
    odpoved.encoding = "utf-8"
    return BeautifulSoup(odpoved.text, "html.parser")


def najdi_obce(stranka: BeautifulSoup) -> list[dict]:
    """Najde vsetky obce v tabulke a vrati ich kod, nazov a odkaz."""
    obce = []
    for bunka in stranka.find_all("td", class_="cislo"):
        odkaz = bunka.find("a")
        if odkaz is None:
            continue
        # nazov obce je v dalsej bunke vedla kodu
        nazov = bunka.find_next_sibling("td").text
        obce.append({
            "kod": odkaz.text,
            "nazov": nazov,
            "odkaz": ZAKLAD_WEBU + odkaz["href"]
        })
    return obce


def uprav_cislo(text: str) -> str:
    """Odstrani medzery z cisla (napr. '1 224' -> '1224')."""
    # na webe je medzi tisickami specialna medzera \xa0
    return text.replace("\xa0", "").replace(" ", "")


def vysledky_obce(stranka: BeautifulSoup) -> tuple[list[str], dict]:
    """Z obce vytiahne volicov, obalky, platne hlasy a hlasy pre strany."""
    volici = stranka.find("td", headers="sa2").text
    obalky = stranka.find("td", headers="sa3").text
    platne = stranka.find("td", headers="sa6").text
    zakladne = [uprav_cislo(volici), uprav_cislo(obalky), uprav_cislo(platne)]

    strany = {}
    for nazov in stranka.find_all("td", class_="overflow_name"):
        hlasy = nazov.find_next_sibling("td").text
        strany[nazov.text] = uprav_cislo(hlasy)

    return zakladne, strany


def zozbieraj_data(obce: list[dict]) -> tuple[list[str], list[list[str]]]:
    """Prejde vsetky obce a vrati nazvy stran a riadky do csv."""
    nazvy_stran = []
    riadky = []

    for obec in obce:
        print("Sťahujem:", obec["nazov"])
        stranka = stiahni_stranku(obec["odkaz"])
        zakladne, strany = vysledky_obce(stranka)

        # nazvy stran si zoberiem z prvej obce
        if len(nazvy_stran) == 0:
            nazvy_stran = list(strany.keys())

        riadok = [obec["kod"], obec["nazov"]] + zakladne
        for strana in nazvy_stran:
            riadok.append(strany.get(strana, "0"))
        riadky.append(riadok)

    return nazvy_stran, riadky


def uloz_csv(subor: str, hlavicka: list[str], riadky: list[list[str]]) -> None:
    """Ulozi data do csv suboru."""
    # utf-8-sig aby Excel spravne zobrazil diakritiku
    with open(subor, "w", newline="", encoding="utf-8-sig") as f:
        zapisovac = csv.writer(f)
        zapisovac.writerow(hlavicka)
        zapisovac.writerows(riadky)


def main() -> None:
    """Hlavna funkcia programu."""
    odkaz, subor = skontroluj_argumenty(sys.argv)

    print("Sťahujem zoznam obcí z:", odkaz)
    stranka = stiahni_stranku(odkaz)
    obce = najdi_obce(stranka)

    if len(obce) == 0:
        print("Na stránke som nenašiel žiadne obce, skontroluj odkaz.")
        sys.exit()

    nazvy_stran, riadky = zozbieraj_data(obce)

    hlavicka = ["code", "location", "registered", "envelopes", "valid"]
    hlavicka = hlavicka + nazvy_stran
    uloz_csv(subor, hlavicka, riadky)

    print("Hotovo, výsledky sú uložené v súbore", subor)


if __name__ == "__main__":
    main()
