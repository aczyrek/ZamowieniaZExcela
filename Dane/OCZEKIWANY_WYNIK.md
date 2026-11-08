# Oczekiwany wynik — pełny zestaw danych testowych

Wynik uruchomienia robota na **wszystkich 8 plikach testowych** (świeża historia — pusta
`Przetworzone_zamowienia.xlsx`) wygenerowanych przez `narzedzia/generuj_dane.py`.

> **Uwaga dot. liczby 14/17:** W starszych notatkach pojawiała się wartość 14 wierszy SAP.
> Rzeczywisty wynik to 8 (bez KL005) → 11 (z KL005). Liczba 14 prawdopodobnie pochodzi
> z pomiaru, który uwzględniał zduplikowane przebiegi z historią (plik Przetworzone).

---

## Podsumowanie

| Wynik | Bez KL005 | Z KL005 | Z korektą Budmat (zadanie: korekta zamówienia) |
|---|---|---|---|
| Gotowe do SAP | 8 | 11 | **13** |
| Raport błędów | 11* | 11* | **13*** |

Korekta zamówienia (pliki `Budmat_zamowienia_2026-11-05.xlsx` + `Budmat_zamowienia_2026-11-05_korekta.xlsx`):
+2 wiersze SAP (BM/11/001 = 20 szt. z oryginału, BM/11/003 = **80** szt. z korekty — pozycja 60 szt.
z oryginału została zastąpiona), +1 wiersz informacyjny w raporcie błędów.
Plik `Techpol_orders_2026-11-05_korekta.xlsx` (korekta numeru BM/11/001, który należy do Budmat):
+1 wiersz odrzucony — korekta nie może usunąć pozycji innego klienta.

\* Po dodaniu walidacji daty dostawy (zadanie 3): +2 nowe błędy w Budmat (BUD-1006 brak daty,
BUD-1007 data w przeszłości). Raport rośnie z 9 do 11 przy świeżej historii; korekta zamówienia
dodaje 12. wiersz (informacyjny) i 13. (korekta cudzego numeru). Przy historii z wpisem `EL-6999` dochodzi kolejny: `Duplikat zamówienia`.

---

## Gotowe_do_SAP — 13 wierszy

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
| BM/11/001 | Budmat | BM-100 | 100234 | 20  | 20.11.2026  | Budmat_zamowienia_2026-11-05.xlsx |
| BM/11/003 | Budmat | BM-205 | 100567 | 80  | 20.11.2026  | Budmat_zamowienia_2026-11-05_korekta.xlsx |

> BM/11/003 występuje **tylko raz** — z ilością 80 z pliku korekty. Wiersz 60 szt. z oryginału
> nie trafia do SAP. Historia (`Przetworzone`) dostaje BM/11/003 jeden raz.

---

## Raport błędów — 13 wierszy

| PlikZrodlowy | Klient | NrZamowienia | IndeksKlienta | Ilosc | Powod |
|---|---|---|---|---|---|
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1003   |        | 30  | Brak indeksu produktu |
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1004   | BM-310 | 0   | Ilość musi być większa od 0 |
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1002   | BM-205 | 12  | Duplikat zamówienia |
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1006   | BM-100 | 5   | Brak daty dostawy |
| Budmat_zamowienia_2026-11-03.xlsx | Budmat  | BUD-1007   | BM-205 | 10  | Data dostawy w przeszłości (01.11.2026) |
| Elmax_2026-11.xlsx                | Elmax   | EL-7004    | EL-01  |     | Ilość nie jest liczbą |
| Kowalski_zamowienie.xlsx          |         |            |        |     | CAŁY PLIK: Nieznany klient (prefiks pliku: Kowalski) |
| Techpol_orders_2026-11-03.xlsx    | Techpol | TP-5002    | TP-B7  | -5  | Ilość musi być większa od 0 |
| Techpol_orders_2026-11-03.xlsx    | Techpol | TP-5003    | TP-C3  | dwa | Ilość nie jest liczbą |
| Techpol_orders_2026-11-03.xlsx    | Techpol | TP-5004    | TP-Z9  | 20  | Brak mapowania indeksu TP-Z9 |
| KL005_HurtowniaKarpaty_2026-11-03.xlsx | KL005 | KH/11/004 | KR-999 | 10 | Brak mapowania indeksu KR-999 |
| Budmat_zamowienia_2026-11-05_korekta.xlsx | Budmat | BM/11/003 | BM-205 | 80 | Korekta zamówienia: zastąpiono pozycje z pliku Budmat_zamowienia_2026-11-05.xlsx |
| Techpol_orders_2026-11-05_korekta.xlsx | Techpol | BM/11/001 | TP-A1 | 5 | Korekta zamówienia, które zostało już wysłane do SAP (wcześniejsze uruchomienie lub inny klient) — popraw ręcznie w SAP |

> Wiersz korekty Budmat jest **informacyjny** (pozycja nie została odrzucona — trafiła do SAP), żeby
> handlowiec wiedział, że zamówienie zostało skorygowane.

### Wariant: korekta zamówienia wysłanego we wcześniejszym uruchomieniu

Gdy oryginał BM/11/003 jest już w `Przetworzone_zamowienia.xlsx` (wysłany do SAP w poprzednim
uruchomieniu), a w bieżącym uruchomieniu przychodzi tylko plik korekty, robot **nie** może zastąpić
pozycji automatycznie. Wiersz zostaje odrzucony z jasnym powodem (zamiast „Duplikat zamówienia”):

| PlikZrodlowy | Klient | NrZamowienia | IndeksKlienta | Ilosc | Powod |
|---|---|---|---|---|---|
| Budmat_zamowienia_2026-11-05_korekta.xlsx | Budmat | BM/11/003 | BM-205 | 80 | Korekta zamówienia, które zostało już wysłane do SAP (wcześniejsze uruchomienie lub inny klient) — popraw ręcznie w SAP |

> Powyższe 13 wierszy to wynik z czystą historią (walidacja daty dostawy + korekta zamówienia).
> Gdy `Przetworzone_zamowienia.xlsx` zawiera historyczny wpis `EL-6999`, dochodzi 12. wiersz:
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

# 2a. (opcjonalnie) arkusz Config/Konfiguracja_klientow.xlsx → Ustawienia: Klucz=ZnacznikKorekty, Wartosc=_korekta
#     — bez arkusza robot użyje domyślnego "_korekta" (wynik identyczny)

# 3. Uruchom robota
uip rpa run --file-path Main.xaml --project-dir . --output json

# 4. Sprawdź Output/Gotowe_do_SAP_<ts>.xlsx i Output/Raport_bledow_<ts>.xlsx
```
