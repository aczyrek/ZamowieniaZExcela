# ZamowieniaZExcela

Robot UiPath do przetwarzania zamówień klientów z plików Excel. Odczytuje pliki zamówień z folderu `Input/`, waliduje i normalizuje dane, mapuje indeksy klienckie na wewnętrzne indeksy SAP, deduplikuje zamówienia względem historii i generuje plik gotowy do importu do SAP oraz raport błędów.

---

## Jak działa robot

### Przepływ ogólny

```
Config/*.xlsx  ──┐
                 ├──► Main.xaml ──► PrzetworzPlik.xaml (x N plików)
Input/*.xlsx  ───┘
                              │
              ┌───────────────┼───────────────┐
              ▼               ▼               ▼
       Processed/          Error/         Output/
     (pliki ok)        (pliki z błędem)  Gotowe_do_SAP_<ts>.xlsx
                                         Raport_bledow_<ts>.xlsx
```

### Krok po kroku

#### 1. Wyznaczenie folderu roboczego

`Main.xaml` pobiera zasób Orchestratora `FolderRoboczy` (typ String). Jeśli zasób nie istnieje lub jest pusty, robot loguje ostrzeżenie i używa ścieżki domyślnej:

```
/Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela
```

#### 2. Wczytanie konfiguracji do pamięci

Robot odczytuje cztery arkusze z folderu `Config/`:

| Plik | Arkusz | Kolumny | Przeznaczenie |
|------|--------|---------|---------------|
| `Konfiguracja_klientow.xlsx` | `Pliki` | PrefiksPliku, Klient, Arkusz, KomorkaStart | Mapowanie prefiksu nazwy pliku na klienta i lokalizację danych w pliku |
| `Konfiguracja_klientow.xlsx` | `Kolumny` | Klient, KolumnaKlienta, PoleWspolne | Tłumaczenie nazw kolumn klienta na nazwy kanoniczne |
| `Mapowanie_indeksow.xlsx` | `Mapowanie` | Klient, IndeksKlienta, IndeksWewnetrzny | Mapowanie indeksu klienta na wewnętrzny indeks SAP |
| `Konfiguracja_klientow.xlsx` | `Ustawienia` (opcjonalny) | Klucz, Wartosc | Ustawienia ogólne. `ZnacznikKorekty` — dopisek w nazwie pliku oznaczający korektę zamówienia (domyślnie `_korekta`, gdy arkusza brak — robot loguje ostrzeżenie) |
| `Przetworzone_zamowienia.xlsx` | `Przetworzone` | NrZamowienia, Klient, DataPrzetworzenia | Historia przetworzonych zamówień (ochrona przed duplikatami między uruchomieniami) |

#### 3. Budowanie słowników

- `dictIndeksy` — klucz złożony `"Klient|IndeksKlienta"` → `IndeksWewnetrzny`
- `dictPrzetworzone` — `NrZamowienia` → `True`; zasilany historią z poprzednich uruchomień

#### 4. Przetwarzanie plików z folderu Input

Dla każdego pliku `*.xlsx` (pomijane pliki tymczasowe `~$`):

1. Wywoływany jest `PrzetworzPlik.xaml` z przekazanymi tabelami i słownikami.
2. W przypadku sukcesu: plik przenoszony do `Processed/`, wiersze SAP i błędów scalane z tabelami zbiorczymi.
3. W przypadku wyjątku (np. nieznany klient, brak wymaganych kolumn): do tabeli błędów trafia wpis `CAŁY PLIK: <komunikat>`, plik przenoszony do `Error/`.

#### Korekta zamówienia

Plik, którego nazwa (bez rozszerzenia) zawiera znacznik korekty (`ZnacznikKorekty`, domyślnie `_korekta`,
np. `Budmat_zamowienia_2026-11-05_korekta.xlsx`), jest traktowany jako korekta zamówień o tych samych numerach:

- pliki korekt są przetwarzane **po** wszystkich pozostałych plikach z `Input/`,
- jeśli oryginał zamówienia (ten sam klient i numer) trafił do SAP **w tym samym uruchomieniu**, pozycje oryginału są usuwane z pliku
  do SAP i zastępowane pozycjami z korekty; w raporcie błędów pojawia się wiersz informacyjny
  `Korekta zamówienia: zastąpiono pozycje z pliku <plik oryginału>`; historia dostaje numer tylko raz,
- jeśli numer został wysłany do SAP **we wcześniejszym uruchomieniu** (jest w historii) albo w tym uruchomieniu
  przez innego klienta, wiersz jest odrzucany z powodem `Korekta zamówienia, które zostało już wysłane do SAP (wcześniejsze uruchomienie lub inny klient) — popraw ręcznie w SAP`,
- jeśli oryginału nie ma ani w uruchomieniu, ani w historii, wiersz korekty jest przetwarzany jak zwykłe zamówienie.

Obsługa korekt dotyczy `Main.xaml`; `Dispatcher.xaml` nie przekazuje znacznika, więc tam korekta jest nadal
duplikatem.

#### 5. Zapis wyników

- `Output/Gotowe_do_SAP_<ts>.xlsx` — wszystkie prawidłowe wiersze ze wszystkich plików
- `Output/Raport_bledow_<ts>.xlsx` — wiersze odrzucone i całe pliki z błędem

#### 6. Aktualizacja historii

Nowe zamówienia są dopisywane do `Przetworzone_zamowienia.xlsx` — zapobiega ponownemu przetworzeniu tych samych numerów zamówień w kolejnych uruchomieniach.

---

### PrzetworzPlik.xaml — przetwarzanie jednego pliku

#### Identyfikacja klienta

Robot bierze pierwszy segment nazwy pliku przed `_` (prefiks) i szuka go w konfiguracji `Pliki`. Brak dopasowania = wyjątek → cały plik trafia do `Error/`.

#### Normalizacja kolumn

Kolumny z pliku klienta są przemianowywane na nazwy kanoniczne:

| Nazwa kanoniczna | Opis |
|-----------------|------|
| `NrZamowienia` | Numer zamówienia |
| `IndeksKlienta` | Indeks produktu po stronie klienta |
| `Ilosc` | Ilość (dziesiętna, InvariantCulture) |
| `DataDostawy` | Data dostawy (opcjonalna) |

#### Walidacja wierszy (6 reguł, zatrzymanie na pierwszym błędzie)

1. `NrZamowienia` nie może być puste
2. `IndeksKlienta` nie może być puste
3. `Ilosc` musi dać się sparsować jako liczba dziesiętna
4. `Ilosc` musi być większa od 0
5. Klucz `Klient|IndeksKlienta` musi istnieć w słowniku indeksów
6. `NrZamowienia` nie może być duplikatem (historia + bieżące uruchomienie + bieżący plik) — wyjątek: plik korekty (patrz *Korekta zamówienia*)

Wiersz prawidłowy → tabela SAP. Wiersz błędny → tabela błędów z polem `Powod`.

---

### Schemat pliku wyjściowego SAP

**Arkusz: SAP** (`Gotowe_do_SAP_<ts>.xlsx`)

| Kolumna | Źródło |
|---------|--------|
| NrZamowienia | Numer zamówienia z pliku klienta |
| Klient | Nazwa klienta z konfiguracji |
| IndeksKlienta | Indeks klienta |
| IndeksWewnetrzny | Zmapowany indeks wewnętrzny SAP |
| Ilosc | Ilość (string, InvariantCulture) |
| DataDostawy | Data dostawy yyyy-MM-dd lub puste |
| PlikZrodlowy | Nazwa pliku źródłowego |

**Arkusz: Bledy** (`Raport_bledow_<ts>.xlsx`)

| Kolumna | Opis |
|---------|------|
| PlikZrodlowy | Nazwa pliku |
| Klient | Nazwa klienta |
| NrZamowienia | Numer zamówienia (może być puste) |
| IndeksKlienta | Indeks klienta (może być puste) |
| Ilosc | Surowa wartość ilości |
| Powod | Przyczyna odrzucenia lub `CAŁY PLIK: <komunikat>` |

---

## Struktura folderów

```
<FolderRoboczy>/
├── Config/
│   ├── Konfiguracja_klientow.xlsx     # Arkusze: Pliki, Kolumny
│   ├── Mapowanie_indeksow.xlsx        # Arkusz: Mapowanie
│   └── Przetworzone_zamowienia.xlsx   # Arkusz: Przetworzone (historia)
├── Input/                             # Tutaj wrzucamy pliki zamówień *.xlsx
├── Processed/                         # Pliki przetworzone pomyślnie
├── Error/                             # Pliki z błędem na poziomie całego pliku
└── Output/
    ├── Gotowe_do_SAP_<ts>.xlsx
    └── Raport_bledow_<ts>.xlsx
```

---

## Wymagania

- UiPath Studio 2025+ lub UiPath Robot z obsługą projektu Portable (net10.0)
- Pakiety NuGet:
  - `UiPath.System.Activities` 26.10.0
  - `UiPath.Excel.Activities` 3.6.1
- Pliki konfiguracyjne przygotowane przed pierwszym uruchomieniem (patrz sekcja wyżej)
- Pliki zamówień w folderze `Input/` z nazwą według schematu `<PrefixKlienta>_*.xlsx`

---

## Jak uruchomić

### Z UiPath Studio

1. Otwórz projekt w UiPath Studio.
2. Upewnij się, że folder roboczy istnieje i zawiera wypełnione pliki konfiguracyjne.
3. Wrzuć pliki zamówień do `Input/`.
4. Naciśnij **Run** (F5).

Domyślna ścieżka folderu roboczego: `/Users/adrianczyrek/Documents/RPA_Zamowienia_z_Excela`

### Z wiersza poleceń (UiPath CLI)

```bash
uip rpa run \
  --file-path "Main.xaml" \
  --project-dir "<ścieżka do projektu>" \
  --output json
```

### Z UiPath Orchestrator

1. Opublikuj projekt do Orchestratora (`uip rpa pack` → wgraj paczkę `.nupkg`).
2. Utwórz zasób (Asset) typu String o nazwie `FolderRoboczy` z wartością pełnej ścieżki do folderu roboczego.
3. Uruchom proces z poziomu Orchestratora.

Jeśli zasób `FolderRoboczy` nie istnieje, robot użyje domyślnej ścieżki lokalnej.

### Walidacja projektu (bez uruchamiania)

```bash
uip rpa validate \
  --file-path "Main.xaml" \
  --project-dir "<ścieżka do projektu>" \
  --output json
```

---

## Obsługa błędów

| Sytuacja | Zachowanie robota |
|----------|-------------------|
| Nieznany prefiks pliku | Cały plik → `Error/`; wpis w raporcie błędów |
| Brak wymaganej kolumny | Cały plik → `Error/`; wpis w raporcie błędów |
| Nieprawidłowy wiersz (walidacja) | Wiersz → tabela błędów; pozostałe wiersze przetwarzane dalej |
| Duplikat zamówienia | Wiersz odrzucony; powód: duplikat |
| Brak zasobu `FolderRoboczy` | Ostrzeżenie w logu; użyta ścieżka domyślna |

---

## Pliki projektu

| Plik | Rola |
|------|------|
| `Main.xaml` | Główny workflow — orkiestracja, pętla po plikach, zapis wyników |
| `PrzetworzPlik.xaml` | Worker — przetwarzanie jednego pliku zamówień |
| `project.json` | Metadane projektu i zależności NuGet |
