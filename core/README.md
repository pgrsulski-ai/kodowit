# KODOWIT Core 7.0 Universal RC
Eksperymentalny interpreter drzewa składniowego napisany w Pythonie 3.10+. Nie używa eval ani exec. Nie wymaga dodatkowych bibliotek. Dotychczasowy KODOWIT Web 5.0.1 RC pozostaje bez zmian; jego stabilizacja nadal wymaga testów przeglądarkowych.

Uruchom z katalogu głównego: `python core/kodowit.py core/demo.kodowit` (Windows: `py core/kodowit.py core/demo.kodowit`). Testy: `python core/test_core.py`.

Składnia: zmienna/stan, przypisanie, funkcja, zwróć, jeżeli/inaczej, dopóki, dla ... w ..., prawda/fałsz/nic, oraz/lub/nie. Liczby, teksty w podwójnych cudzysłowach, listy i indeksy od zera. Średniki opcjonalne. Komentarze # lub //. Funkcje: wypisz, zakres, długość, suma, liczba, tekst, calkowita. Wybrane słowa mają aliasy bez polskich znaków. Funkcje mają zakres leksykalny; przypisanie aktualizuje istniejącą zmienną. Pętla nie tworzy osobnego zakresu. Limit kroków nie stanowi kompletnej izolacji zasobów; nie uruchamiać niezaufanego kodu. Brak integracji Studio, klas i instalatora. Interpreter wymaga Pythona, ale nie tłumaczy kodu KODOWIT na kod źródłowy Pythona.

## Terminal 6.1
Windows: w katalogu paczki uruchom `kodowit.cmd` lub `kodowit.cmd core\demo.kodowit` (w PowerShell użyj ` .\kodowit.cmd`). Linux/macOS: `./kodowit` lub `./kodowit core/demo.kodowit`. Wymagany Python 3.10+ (Windows: launcher py). Bez instalacji globalnej. `--wersja`, `--help`, `-c "wypisz(42)"`. Konsola zachowuje zmienne, obsługuje bloki wielowierszowe i polecenia :pomoc, :reset, :anuluj, :wyjdz. Limit kroków odnawia się dla każdego polecenia. Testy: `python -m unittest discover -s core`. Nie jest to piaskownica dla niezaufanego kodu.

## 6.2 – pliki lokalne
Uruchom `python core/kodowit.py --pliki . core/pliki.kodowit` w katalogu paczki.
Flaga `--pliki KATALOG` jawnie włącza funkcje plikowe. Domyślnie są niedostępne.
Funkcje: `czytaj_plik`, `zapisz_plik` (nadpisuje), `dopisz_plik`, `istnieje`, `utworz_katalog`, `lista_katalogu`, `system`, `katalog_roboczy`. Tekst UTF-8, limit 1 MB na odczyt/zapis. Ścieżki względne; kontrola dowiązań przy rozwiązywaniu ścieżki nie stanowi pełnej izolacji przed równoczesnymi zmianami systemu plików. Uruchamiaj wyłącznie zaufany kod. Brak wykonywania poleceń powłoki.

## 6.3 – biblioteka standardowa
Funkcje dostępne bez importu: pierwiastek, sinus, cosinus (radiany), logarytm, potega, zaokraglij, bezwzgledna, minimum, maksimum, srednia, mediana, sortuj, odwroc, male_litery, wielkie_litery, przytnij, podziel, polacz(separator, lista), zamien, zawiera, losuj(a,b) (obie granice włącznie), losowa(), dzisiaj(), teraz(), dodaj_dni(data, dni), roznica_dni(a,b). Stałe pi i euler. Daty ISO YYYY-MM-DD, czas lokalny z przesunięciem UTC. Losowanie nie jest kryptograficzne. Przykład: `python core/kodowit.py core/biblioteka.kodowit`. Funkcje korzystają z biblioteki standardowej Pythona; nie stanowią izolacji zasobów.

## 6.4 – SQLite
`python core/kodowit.py --pliki . core/baza.kodowit` tworzy lokalną bazę. `baza_wykonaj(plik, sql, parametry)` wykonuje pojedyncze polecenie i zatwierdza transakcję; `baza_pobierz(plik, sql, parametry)` zwraca listę wierszy. Parametry są opcjonalną listą, używaj znaczników ?. Dostęp wymaga --pliki. ATTACH, DETACH i PRAGMA są blokowane. Limit wyników 10000 i budżet instrukcji SQLite; nie jest to pełna izolacja ani limit rozmiaru bazy. Zapytanie może utworzyć plik bazy. Tylko zaufany kod. Brak transakcji wielopoleceniowych.

## 6.5 – lokalne HTTP API
`python core/kodowit.py --siec core/api.kodowit` uruchamia serwer na 127.0.0.1:8080. GET /witaj oraz POST /echo (JSON). `api_trasa(metoda, ścieżka, funkcja)` rejestruje funkcję z jednym parametrem (ciało JSON lub nic); zwracana wartość jest serializowana do JSON. `api_start(port)` blokuje do Ctrl+C. Serwer jednowątkowy, tylko loopback, bez TLS, uwierzytelniania i obsługi produkcyjnej. Limit ciała 64 KiB, timeout gniazda 5 s; nie jest to piaskownica. Nie uruchamiać niezaufanego kodu. Opcjonalne --pliki włącza SQLite i pliki.

## 6.6 – aplikacje desktopowe
`python core/kodowit.py --gui core/gui.kodowit` uruchamia okno Tkinter. Wymaga Pythona z Tkinter oraz środowiska graficznego (na Linuxie może być potrzebny python3-tk). Funkcje: okno(tytul,szerokosc,wysokosc), etykieta(nazwa,tekst), pole(nazwa,tekst), przycisk(nazwa,tekst,funkcja_bez_parametrow), gui_odczytaj(nazwa), gui_ustaw(nazwa,tekst), gui_start(), gui_zamknij(). Jedno okno, pionowy układ, brak eksportu EXE. Tylko zaufany kod. Testy GUI na wirtualnym ekranie Linux: xvfb-run -a python -m unittest discover -s core.

## 6.7 – integracja Python
`python core/kodowit.py --python math --python statistics core/python.kodowit`.
`python_wywolaj(modul, funkcja, ...argumenty)` działa wyłącznie po jawnym zezwoleniu CLI. Lista funkcji w python_bridge.py. Obsługiwane moduły math, statistics, json i opcjonalnie numpy (instalowany osobno). Dane proste i listy, bez słowników i obiektów Python. Nie jest to dowolny import, piaskownica ani limit zasobów. Używaj zaufanego kodu i zaufanych bibliotek.

## 6.8 – pakiety lokalne
`python core/kodowit.py --pakiety biblioteki --pakiet instaluj matematyka core/pakiet-demo.kodowit` instaluje plik źródłowy. `--pakiet lista` i `--pakiet usun matematyka` zarządzają pakietami. Uruchom program z `--pakiety biblioteki` i użyj `importuj_pakiet("matematyka")`. Pakiety wykonują kod we wspólnej przestrzeni nazw, raz na interpreter; brak rejestru online, wersjonowania i zależności. Instaluj wyłącznie zaufany kod.

## 6.9 – diagnostyka

- `python core/kodowit.py --sprawdz core/demo.kodowit` – kontrola składni bez wykonania.
- `python core/kodowit.py --sledz core/demo.kodowit` – ślad instrukcji na stderr.
- `python core/kodowit.py --limit 50000 core/demo.kodowit` – budżet kroków.
- Błędy wykonania zawierają numer ostatniej wykonywanej instrukcji, jeśli dostępny.
- Limit źródła: milion znaków. Budżet kroków nie ogranicza czasu funkcji natywnych ani całkowitej pamięci. To nie jest izolacja systemowa ani pełny debugger z punktami przerwania.
- Testy: 54 unittest (Linux, Xvfb) oraz pięć zestawów Web.

## Biblioteka 8.6
Nowe funkcje: `podloga`, `sufit`, `tangens`, `nwd`, `nww`, `odchylenie`, `wariancja` (populacyjne), `licz_wystapienia`, `zaczyna_sie`, `konczy_sie`, `znajdz` (indeks od zera, -1 gdy brak), `sortuj_malejaco`, `unikalne` (elementy haszowalne), `wybierz_losowo`, `probka` (bez zwracania), `rok`, `miesiac`, `dzien`, `dzien_tygodnia` (poniedziałek=1), `json_wczytaj`, `json_zapisz`, `obiekt`, `klucze`.
Daty ISO YYYY-MM-DD. JSON obsługuje obiekty poprzez indeksowanie kluczem; brak literałów słownikowych. Funkcje dostępne w Core, nie w Edu/Web.

## 9.8 – GUI i grafika 2D
Uruchom `python core/kodowit.py --gui core/gra2d.kodowit` z katalogu głównego. Wymaga Tkinter i ekranu. `plotno(nazwa,tlo)` tworzy płótno; `prostokat` i `elipsa` przyjmują nazwę, x, y, szerokość, wysokość, kolor i zwracają ID. `linia` przyjmuje współrzędne obu końców. `przesun_figure(nazwa,id,dx,dy)`, `usun_figure(nazwa,id)`, `wyczysc_plotno(nazwa)` i `kolizja(nazwa,id1,id2)` operują na figurach; kolizja używa prostokątów ograniczających. `po_czasie(ms,f)` to jednorazowy timer, `po_klawiszu(klawisz,f)` wiąże zdarzenie; funkcje bez argumentów. `pole_wyboru(nazwa,tekst)`, `wybrane(nazwa)`, `pasek_postepu(nazwa)`, `postep_ustaw(nazwa,wartosc)` rozszerzają GUI. Nie jest to pełny silnik gier. Studio nie włącza automatycznie uprawnienia GUI.
