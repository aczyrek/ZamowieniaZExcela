"""
Dodaje do konfiguracji robota obsługę jednostki zamówienia (szt / karton).

Użycie:
    python3 narzedzia/konfiguruj_jednostki.py [KATALOG_CONFIG]

Domyślny katalog: /Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela/Config

Zmiany (idempotentne — ponowne uruchomienie niczego nie dubluje):
  - Konfiguracja_klientow.xlsx / Pliki:   kolumna JednostkaZamowienia (istniejący klienci: szt)
                                          + klient Napojex (karton)
  - Konfiguracja_klientow.xlsx / Kolumny: mapowanie kolumn klienta Napojex
  - Mapowanie_indeksow.xlsx / Mapowanie:  kolumna Przelicznik (istniejące indeksy: 1)
                                          + indeksy Napojex (24, 12, pusty = domyślnie 1)
"""

import os
import sys
import openpyxl


KATALOG_DOMYSLNY = "/Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela/Config"

NOWY_KLIENT_PLIKI = ("Napojex", "Napojex", "Zamówienie", "A1", "karton")
NOWY_KLIENT_KOLUMNY = [
    ("Napojex", "Nr zamówienia", "NrZamowienia"),
    ("Napojex", "Indeks", "IndeksKlienta"),
    ("Napojex", "Ilość kartonów", "Ilosc"),
    ("Napojex", "Termin dostawy", "DataDostawy"),
]
# Klient, IndeksKlienta, IndeksWewnetrzny, NazwaProduktu, Przelicznik
NOWE_INDEKSY = [
    ("Napojex", "NP-330", "400101", "Napój gazowany puszka 0,33 l (karton 24 szt.)", 24),
    ("Napojex", "NP-500", "400102", "Woda butelka 0,5 l (karton 12 szt.)", 12),
    ("Napojex", "NP-ZESTAW", "400103", "Zestaw prezentowy (sprzedawany na sztuki)", None),
]


def _naglowki(ws) -> list:
    return [c.value for c in ws[1]]


def _dodaj_kolumne(ws, nazwa: str, wartosc_domyslna) -> int:
    """Dodaje kolumnę (jeśli jej brak) i wypełnia istniejące wiersze. Zwraca numer kolumny (1-based)."""
    naglowki = _naglowki(ws)
    if nazwa in naglowki:
        return naglowki.index(nazwa) + 1
    kol = len(naglowki) + 1
    ws.cell(row=1, column=kol, value=nazwa)
    for r in range(2, ws.max_row + 1):
        if any(ws.cell(row=r, column=c).value not in (None, "") for c in range(1, kol)):
            ws.cell(row=r, column=kol, value=wartosc_domyslna)
    print(f"  {ws.title}: dodano kolumnę {nazwa}")
    return kol


def _istnieje(ws, klucz: tuple) -> bool:
    n = len(klucz)
    return any(tuple(row[:n]) == klucz for row in ws.iter_rows(min_row=2, values_only=True))


def _dopisz(ws, wiersz: tuple, klucz_dl: int) -> None:
    if not _istnieje(ws, tuple(wiersz[:klucz_dl])):
        ws.append(list(wiersz))
        print(f"  {ws.title}: dopisano {wiersz}")


def main() -> None:
    katalog = sys.argv[1] if len(sys.argv) > 1 else KATALOG_DOMYSLNY

    sciezka = os.path.join(katalog, "Konfiguracja_klientow.xlsx")
    wb = openpyxl.load_workbook(sciezka)
    pliki = wb["Pliki"]
    _dodaj_kolumne(pliki, "JednostkaZamowienia", "szt")
    _dopisz(pliki, NOWY_KLIENT_PLIKI, 1)
    kolumny = wb["Kolumny"]
    for w in NOWY_KLIENT_KOLUMNY:
        _dopisz(kolumny, w, 2)
    wb.save(sciezka)

    sciezka = os.path.join(katalog, "Mapowanie_indeksow.xlsx")
    wb = openpyxl.load_workbook(sciezka)
    mapowanie = wb["Mapowanie"]
    _dodaj_kolumne(mapowanie, "Przelicznik", 1)
    for w in NOWE_INDEKSY:
        _dopisz(mapowanie, w, 2)
    wb.save(sciezka)
    print("Gotowe.")


if __name__ == "__main__":
    main()
