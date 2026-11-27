## Wydanie 1.0.0

Pakiet premierowy; zakres i ograniczenia: [docs/RELEASE-1.0.0.md](docs/RELEASE-1.0.0.md).

## RC137 — końcowa kontrola lokalna bezpieczeństwa

Bez nowych funkcji; ograniczenia w docs/RC137.md.

## RC136 — regresja automatyczna i oznaczenia Beta

## RC135 — procedura pilotażu i bramki premiery

## RC134 — ochrona przed spóźnioną odpowiedzią logowania Cloud

## RC133 — lokalne kopie projektów Cloud

Eksport JSON wczytanego projektu i prywatnych migawek.

## RC132 — historia publikacji Cloud

Dwie poprzednie migawki, przywracanie pod tym samym adresem.

## RC131 — preflight wdrożenia i instrukcja pilotażu

## RC130 — prywatne migawki źródeł Cloud

Zapisy, odczyt i usuwanie wersji projektów z RLS.

## RC129 — zarządzanie Cloud

Panel publikacji i RPC właściciela.

## RC128
- Pełna regresja lokalna; poprawka rejestracji PWA strony cloud-app.html.

## RC127
- Walidacja publicznych kluczy Cloud, limit czasu API i globalny limit publikacji.

## RC126
- Wykrywanie modeli Ollama i anulowanie oczekiwania na odpowiedź.

## RC125
- Pilotaż publikacji Cloud z opcjonalnym backendem Supabase; reset importu Marketplace.

## RC124
- Walidacja Builder i Enterprise oraz obsługa blokady IndexedDB Business.

## RC123
- Walidacja postępu Academy, komunikaty błędów zapisu, walidacja geometrii Edu i odczyt Academic.

## RC122
- Poprawki walidacji edycji i importu projektów Studio Free/PRO.

## RC121
- Końcowa regresja: 114 testów Core, 11 Desktop i 56 zestawów JS.
- Ocena blokad premiery w docs/RC121.md.

## RC120
- Uściślenie ograniczeń 13 produktów w katalogu i raport audytu funkcjonalnego.

## RC119
- Ograniczony odczyt stdout/stderr procesu Core; kontrola czasu i nowe testy.
- CSP worker-src self.

## RC118
- Inwentaryzacja zależności i wspólna deklaracja PyInstaller dla CI i instrukcji.
- Dodano procedurę audytu CVE; wynik online pozostaje niezweryfikowany.

## RC117
- Audyt wydania sprawdza zgodność bajtową i raportuje SHA256 kompilatora.

## RC116
- Końcowy audyt statyczny; dodano zadanie CI dla Core i Desktop.
- Udokumentowano blokady wydania Stable.

## RC115
- Regresja: 56 zestawów JS, 111 testów Core, 11 Desktop.

## RC114
- Synchronizacja wersji instalatora Windows; testy Core i Desktop w Xvfb.

## RC113
- Wspólna rejestracja PWA na stronach produktów; test statyczny i symulacja rejestracji.

## RC112
- Testy funkcjonalne Cloud i Academic z symulowanym DOM oraz kompilacji projektu.

## RC111
- Strona startowa: trzy ścieżki produktowe, zachowane dotychczasowe odnośniki.

## 1.0.0 RC110

- Reorganizacja 35 zasobów Edu, School i Business; zachowane adresy stron HTML.
- 54/54 zestawów JavaScript zaliczone.

# Historia wydań KODOWIT

## 1.0.0-rc94
- Wydzielono biblioteki współdzielone, silnik bazodanowy i silnik aplikacji.
- Zachowano adresy stron HTML i klucze danych lokalnych.

## 1.0.0-rc93
- Dodano VERSION i skrypt synchronizacji oznaczeń wydania.
- Historia wcześniejszych wydań: [docs/changelog](docs/changelog/).

## 1.0.0-rc92
- Uporządkowano dokumentację i testy, usunięto kopie Android i artefakty Pythona.

## 1.0.0 RC96
- System budowania ZIP i dalsze wydzielenie bibliotek.

## 1.0.0 RC98
- Moduły źródłowe kompilatora i automatyczny bundle.
- CSP podglądu Studio i Buildera, bez zmiany eksportu HTML.

## 1.0.0 RC100
Profil wspólny, 12 testów zgodności i 4 udokumentowane rozbieżności.

## RC102
- Zgodność czterech operacji i automatyzacja testów.

## 1.0.0-rc104
- Wydzielono moduły AI; mikrobenchmark kompilatora i ograniczenie alokacji w lexerze.

## 1.0.0-rc105
- Wstępny audyt statyczny, korekta nieaktualnego testu i planu premiery. Zobacz docs/RC105.md.

## RC106
- Regresja 80 zestawów; wyniki i ograniczenia: docs/RC106.md.

## RC107
- Blokowanie przekierowań rejestru HTTPS do niezabezpieczonych protokołów; test regresji i ograniczenie źródła manifestu CSP. Zobacz docs/RC107.md.

## 1.0.0 RC108
- Walidacja czasu i ograniczenie środowiska procesu limitowanego; polskie wartości logiczne.
- CORP dla Service Worker; dwa dodatkowe testy regresji.

## 1.0.0 RC109
- Pomiary czasu i pamięci, oznaczenie generowanego kompilatora.
