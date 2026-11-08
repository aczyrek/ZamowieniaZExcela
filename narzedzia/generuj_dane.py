"""
Generuje wszystkie pliki testowe dla projektu ZamowieniaZExcela.

Użycie:
    python3 narzedzia/generuj_dane.py [KATALOG_WYJSCIOWY]

Domyślny katalog wyjściowy: /Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela/Input

Każde wywołanie NADPISUJE istniejące pliki w katalogu docelowym.
"""

import sys
import os
from datetime import date
import openpyxl
from openpyxl.styles import Font


KATALOG_DOMYSLNY = "/Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela/Input"


def _zapisz(wb: openpyxl.Workbook, katalog: str, nazwa: str) -> None:
    sciezka = os.path.join(katalog, nazwa)
    wb.save(sciezka)
    print(f"  zapisano: {sciezka}")


# ---------------------------------------------------------------------------
# Budmat — Zamówienia (A1), kolumny PL, z datą; błędy: brak indeksu, ilość 0,
#          duplikat w pliku
# ---------------------------------------------------------------------------
def generuj_budmat(katalog: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zamówienia"
    ws.append(["Nr zamówienia", "Indeks", "Ilość", "Termin dostawy"])
    ws.append(["BUD-1001", "BM-100", 50,   "10.11.2026"])  # poprawny
    ws.append(["BUD-1002", "BM-205", 12,   "12.11.2026"])  # poprawny
    ws.append(["BUD-1003", None,     30,   "12.11.2026"])  # błąd: brak indeksu
    ws.append(["BUD-1004", "BM-310", 0,    "14.11.2026"])  # błąd: ilość <= 0
    ws.append(["BUD-1005", "BM-100", 8,    "14.11.2026"])  # poprawny
    ws.append(["BUD-1002", "BM-205", 12,   "12.11.2026"])  # błąd: duplikat
    _zapisz(wb, katalog, "Budmat_zamowienia_2026-11-03.xlsx")


# ---------------------------------------------------------------------------
# Techpol — Orders (A1), kolumny EN, data jako datetime; błędy: ilość ujemna,
#           ilość tekstowa, brak mapowania indeksu
# ---------------------------------------------------------------------------
def generuj_techpol(katalog: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Orders"
    ws.append(["Delivery date",          "Qty",   "Order No", "Product Code", "Comment"])
    ws.append([date(2026, 11, 11), 100,  "TP-5001", "TP-A1", None])    # poprawny
    ws.append([date(2026, 11, 11), -5,   "TP-5002", "TP-B7", "korekta"])  # błąd: ilość <= 0
    ws.append([date(2026, 11, 12), "dwa","TP-5003", "TP-C3", None])    # błąd: ilość nie jest liczbą
    ws.append([date(2026, 11, 12), 20,   "TP-5004", "TP-Z9", "nowy produkt"])  # błąd: brak mapowania
    ws.append([date(2026, 11, 13), 15,   "TP-5005", "TP-A1", None])    # poprawny
    _zapisz(wb, katalog, "Techpol_orders_2026-11-03.xlsx")


# ---------------------------------------------------------------------------
# Elmax — Arkusz1 (A3), 2 wiersze nagłówkowe; bez kolumny DataDostawy;
#         błędy: pusta ilość
# ---------------------------------------------------------------------------
def generuj_elmax(katalog: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Arkusz1"
    ws.append(["ZAMÓWIENIE ELMAX Sp. z o.o.", None, None, None, None])
    ws.append(["Data: 03.11.2026",             None, None, None, None])
    ws.append(["Lp.", "Numer zam.", "Kod produktu", "Ilość szt.", "Uwagi"])
    ws.append([1, "EL-7001", "EL-01",    40,   None])      # poprawny
    ws.append([2, "EL-7002", "EL-02",    25,   "pilne"])   # poprawny
    ws.append([3, "EL-7003", "  EL-03 ", 5,    None])      # poprawny (spacje wokół indeksu)
    ws.append([4, "EL-7004", "EL-01",    None, None])      # błąd: pusta ilość
    _zapisz(wb, katalog, "Elmax_2026-11.xlsx")


# ---------------------------------------------------------------------------
# Kowalski — nieznany klient (brak w Konfiguracja_klientow.xlsx)
# ---------------------------------------------------------------------------
def generuj_kowalski(katalog: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sheet1"
    ws.append(["Zam", "Towar", "Szt"])
    ws.append(["K-1", "X-1", 3])
    _zapisz(wb, katalog, "Kowalski_zamowienie.xlsx")


# ---------------------------------------------------------------------------
# KL005 — Hurtownia Karpaty — Zamówienie (A4), 3 wiersze nagłówkowe,
#         4 kolumny (Numer zlecenia, Kod towaru, Ilość szt., Termin dostawy);
#         błąd: brak mapowania indeksu KR-999
# ---------------------------------------------------------------------------
def generuj_kl005(katalog: str) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Zamówienie"
    ws["A1"] = "Hurtownia Karpaty Sp. z o.o."
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "ul. Zakopiańska 15, 34-500 Zakopane"
    ws["A3"] = None                                         # pusty wiersz
    ws.append(["Numer zlecenia", "Kod towaru", "Ilość szt.", "Termin dostawy"])
    ws.append(["KH/11/001", "KR-001", 100, date(2026, 11, 10)])  # poprawny
    ws.append(["KH/11/002", "KR-002", 50,  date(2026, 11, 10)])  # poprawny
    ws.append(["KH/11/003", "KR-003", 20,  date(2026, 11, 12)])  # poprawny
    ws.append(["KH/11/004", "KR-999", 10,  date(2026, 11, 12)])  # błąd: brak mapowania KR-999
    _zapisz(wb, katalog, "KL005_HurtowniaKarpaty_2026-11-03.xlsx")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    katalog = sys.argv[1] if len(sys.argv) > 1 else KATALOG_DOMYSLNY
    os.makedirs(katalog, exist_ok=True)
    print(f"Generowanie plików testowych → {katalog}")
    generuj_budmat(katalog)
    generuj_techpol(katalog)
    generuj_elmax(katalog)
    generuj_kowalski(katalog)
    generuj_kl005(katalog)
    print("Gotowe.")


if __name__ == "__main__":
    main()
