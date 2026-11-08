# Oczekiwany wynik — pełny zestaw danych testowych

Wynik uruchomienia robota na **wszystkich 5 plikach testowych** (świeża historia — pusta
`Przetworzone_zamowienia.xlsx`) wygenerowanych przez `narzedzia/generuj_dane.py`.

> **Uwaga dot. liczby 14/17:** W starszych notatkach pojawiała się wartość 14 wierszy SAP.
> Rzeczywisty wynik to 8 (bez KL005) → 11 (z KL005). Liczba 14 prawdopodobnie pochodzi
> z pomiaru, który uwzględniał zduplikowane przebiegi z historią (plik Przetworzone).

---

## Podsumowanie

| Wynik | Bez KL005 | Z KL005 (docelowo) |
|---|---|---|
| Gotowe do SAP | 8 | **11** |
| Raport błędów | 9* | **9*** |

\* Przy **świeżej** historii (`Przetworzone_zamowienia.xlsx` bez wpisów historycznych): 9 błędów.
Przy historii z wpisem `EL-6999` (z wcześniejszego uruchomienia): 10 błędów — EL-6999 pojawia się
jako duplikat. Liczba podana w zadaniu (9 → 10) zakładała zachowanie historii; uruchomienie
na czystej historii daje 9 → 9 (bez KL005) → bez zmian dla istniejących, +1 KL005 = 9 łącznie.

---

## Gotowe_do_SAP — 11 wierszy

| NrZamowienia | Klient  | IndeksKlienta | IndeksWewnetrzny | Ilosc | DataDostawy | PlikZrodlowy |
|---|---|---|---|---|---|---|
| BUD-1001 | Budmat  | BM-100 | 100234 | 50  | 10.11.2026  | Budmat_zamowienia_2026-11-03.xlsx |
| BUD-1002 | Budmat  | BM-205 | 100567 | 12  | 12.11.2026  | Budmat_zamowienia_2026-11-03.xlsx |
| BUD-1005 | Budmat  | BM-100 | 100234 | 8   | 14.11.2026  | Budmat_zamowienia_2026-11-03.xlsx |
| EL-7001  | Elmax   | EL-01  | 300101 | 40  | _(brak)_    | Elmax_2026-11.xlsx |
| EL-7002  | Elmax   | EL-02  | 300102 | 25  | _(brak)_    | Elmax_2026-11.xlsx |
| EL-7003  | Elmax   | EL-03  | 300103 | 5   | _(brak)_    | Elmax_2026-11.xlsx |
| TP-5001  | Techpol | TP-A1  | 200111 | 100 | 2026-11-11  | Techpol_orders_2026-11-03.xlsx |
| TP-5005  | Techpol | TP-A1  | 200111 | 15  | 2026-11-13  | Techpol_orders_2026-11-03.xlsx |
| KH/11/001 | KL005  | KR-001 | 100045 | 100 | 2026-11-10  | KL005_HurtowniaKarpaty_2026-11-03.xlsx |
| KH/11/002 | KL005  | KR-002 | 100210 | 50  | 2026-11-10  | KL005_HurtowniaKarpaty_2026-11-03.xlsx |
| KH/11/003 | KL005  | KR-003 | 200781 | 20  | 2026-11-12  | KL005_HurtowniaKarpaty_2026-11-03.xlsx |

---

## Raport błędów — 10 wierszy

| PlikZrodlowy | Klient | NrZamowienia | IndeksKlienta | Ilosc | Powod |
|---|---|---|---|---|---|
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1003   |        | 30  | Brak indeksu produktu |
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1004   | BM-310 | 0   | Ilość musi być większa od 0 |
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1002   | BM-205 | 12  | Duplikat zamówienia |
| Elmax_2026-11.xlsx                | Elmax   | EL-7004    | EL-01  |     | Ilość nie jest liczbą |
| Kowalski_zamowienie.xlsx          |         |            |        |     | CAŁY PLIK: Nieznany klient (prefiks pliku: Kowalski) |
| Techpol_orders_2026-11-03.xlsx    | Techpol | TP-5002    | TP-B7  | -5  | Ilość musi być większa od 0 |
| Techpol_orders_2026-11-03.xlsx    | Techpol | TP-5003    | TP-C3  | dwa | Ilość nie jest liczbą |
| Techpol_orders_2026-11-03.xlsx    | Techpol | TP-5004    | TP-Z9  | 20  | Brak mapowania indeksu TP-Z9 |
| KL005_HurtowniaKarpaty_2026-11-03.xlsx | KL005 | KH/11/004 | KR-999 | 10 | Brak mapowania indeksu KR-999 |

> Powyższe 9 wierszy to wynik weryfikowany robotem (uruchomienie z czystą historią, 2026-11-08).
> Gdy `Przetworzone_zamowienia.xlsx` zawiera historyczny wpis `EL-6999`, dochodzi 10. wiersz:
> `Elmax_2026-11.xlsx | Elmax | EL-6999 | EL-02 | 10 | Duplikat zamówienia`

---

## Jak odtworzyć wynik

```bash
# 1. Wygeneruj pliki testowe
python3 narzedzia/generuj_dane.py

# 2. Wyczyść historię (backup + reset)
cp /Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela/Config/Przetworzone_zamowienia.xlsx \
   /Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela/Przetworzone_zamowienia_BACKUP.xlsx
python3 narzedzia/wyczysc_historie.py   # lub ręcznie usuń wiersze w Przetworzone

# 3. Uruchom robota
uip rpa run --file-path Main.xaml --project-dir . --output json

# 4. Sprawdź Output/Gotowe_do_SAP_<ts>.xlsx i Output/Raport_bledow_<ts>.xlsx
```
