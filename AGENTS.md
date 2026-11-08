# AGENTS.md — ZamowieniaZExcela

Ten plik opisuje dostępne agenty (skille Cezara) i kiedy każdy z nich powinien być wywołany
dla tego projektu.

---

## Agenty UiPath

### `uipath:uipath-rpa`
**Kiedy**: tworzenie, edycja, walidacja, pakowanie plików `.xaml` i `.cs`.
Obejmuje: dodawanie aktywności, zmiany argumentów, budowanie `.nupkg`, uruchamianie lokalnie.

**Przykładowe zadania dla tego projektu**:
- Dodanie nowej reguły walidacji w `PrzetworzPlik.xaml`
- Wydzielenie logiki walidacji do osobnego `WalidujWiersz.xaml`
- Zmiana schematu tabeli SAP (nowe kolumny)
- Pakowanie do NuGet przed deploymentem

---

### `uipath:uipath-review`
**Kiedy**: review logiki workflow — poprawność algorytmu, struktura przepływu, użycie aktywności.

**Przykładowe zadania dla tego projektu**:
- Przegląd PR dodającego nowego klienta
- Weryfikacja czy `dictPrzetworzone` jest poprawnie aktualizowany między plikami
- Ocena czy obsługa błędów jest kompletna

---

### `uipath:uipath-troubleshoot`
**Kiedy**: debugowanie — wyjątki runtime, niepoprawne wyniki, robot się zawiesza, logi wskazują błąd.

**Przykładowe zadania dla tego projektu**:
- Robot zgłasza `KeyNotFoundException` przy słowniku indeksów
- Plik nie zostaje przeniesiony do `Processed/`
- Asset `FolderRoboczy` nie jest pobierany poprawnie
- Duplikaty trafiają do SAP mimo słownika historii

---

### `uipath:uipath-test`
**Kiedy**: pisanie i uruchamianie testów automatycznych dla workflow.

**Przykładowe zadania dla tego projektu**:
- Test jednostkowy dla `PrzetworzPlik.xaml` z mock danymi
- Test walidacji: wiersz z brakującym numerem zamówienia trafia do tabeli błędów
- Test duplikatu: to samo zamówienie nie zostaje wysłane dwa razy

---

### `uipath:uipath-project-discovery-agent`
**Kiedy**: odświeżenie kontekstu projektu po dużych zmianach strukturalnych.
Nadpisuje `.claude/rules/project-context.md` i ten plik.

---

### `uipath:uipath-platform`
**Kiedy**: operacje na Orchestratorze — foldery, assets, kolejki, pakiety, harmonogramy.

**Przykładowe zadania dla tego projektu**:
- Aktualizacja wartości assetu `FolderRoboczy` w Orchestratorze
- Monitorowanie statusu ostatnich uruchomień
- Upload nowej wersji pakietu

---

## Agenty generyczne (Cezar)

### `code-review` (skill)
**Kiedy**: review kodu przed PR — czystość kodu, duplikacje, wydajność.
Użyj `--comment` żeby opublikować jako inline comments na PR, `--fix` żeby automatycznie poprawić.

```
/code-review high          # pełne review
/code-review high --fix    # review + automatyczna naprawa
```

---

### `verify` (skill)
**Kiedy**: weryfikacja że zmiana działa w praktyce — uruchom i obserwuj.

---

### `uipath:uipath-troubleshoot` (jako fallback)
Każdy niewyjaśniony błąd zaczyna się od tego agenta, niezależnie od warstwy (XAML, Orchestrator,
Agent, połączenie).

---

## Routing decyzji: który agent?

```
Nowa funkcja w .xaml          → uipath-rpa
Edycja istniejącej .xaml      → uipath-rpa
Coś się psuje w runtime       → uipath-troubleshoot
Review przed merge            → uipath-review LUB code-review
Pisanie testów                → uipath-test
Operacje Orchestrator         → uipath-platform
Kontekst projektu nieaktualny → uipath-project-discovery-agent
Weryfikacja że działa         → verify
```
