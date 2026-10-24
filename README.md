# Elections Scraper

Tretí projekt do Engeto Online Python Akadémie.

## Popis projektu

Program sťahuje výsledky volieb do Poslaneckej snemovne z roku 2017
zo stránky [volby.cz](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).
Pre zvolený územný celok stiahne výsledky všetkých obcí a uloží ich
do súboru `.csv`.

## Inštalácia knižníc

Knižnice, ktoré program používa, sú v súbore `requirements.txt`.
Odporúčam vytvoriť si nové virtuálne prostredie a nainštalovať ich takto:

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

(na Linuxe / macOS sa prostredie aktivuje príkazom `source venv/bin/activate`)

## Spustenie projektu

Program sa spúšťa s 2 argumentmi:

1. odkaz na územný celok (v úvodzovkách)
2. názov výstupného súboru s príponou `.csv`

```
python main.py "<odkaz na územný celok>" <nazov_suboru.csv>
```

Ak niektorý argument chýba alebo je nesprávny, program vypíše chybu a skončí.

## Ukážka

Výsledky pre okres Prostějov:

1. argument: `https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103`
2. argument: `vysledky_prostejov.csv`

Spustenie:

```
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" vysledky_prostejov.csv
```

Priebeh:

```
Sťahujem zoznam obcí z: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Sťahujem: Alojzov
Sťahujem: Bedihošť
...
Sťahujem: Želeč
Hotovo, výsledky sú uložené v súbore vysledky_prostejov.csv
```

Časť výstupu:

```
code,location,registered,envelopes,valid,Občanská demokratická strana,...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
...
```

Celý výstup je v súbore `vysledky_prostejov.csv`.
