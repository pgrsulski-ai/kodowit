## Wydanie 1.0.0

Pakiet premierowy; zakres i ograniczenia: [docs/RELEASE-1.0.0.md](docs/RELEASE-1.0.0.md).

# KODOWIT 9.0 Desktop & Universal RC

Dystrybucja: Core i Desktop 9.0 RC, Web 5.0.1 RC oraz Edu 8.0 RC. Zobacz [wdrożenie](docs/changelog/WDROZENIE-9.0.md). Są to osobne silniki. Zobacz [instrukcję instalacji](docs/changelog/INSTALACJA-7.0.md).

Polski język programowania i Studio. Wydanie kandydujące, nie certyfikowane wydanie stabilne.

## Uruchomienie
- Lokalnie: `python -m http.server 8000`, otwórz http://localhost:8000.
- Android: rozpakuj ZIP i otwórz OTWORZ-NA-ANDROIDZIE.html. Academy w pełnej wersji internetowej.
- Netlify: zachowaj kopię obecnego repozytorium, wgraj zawartość ZIP do katalogu publikacji istniejącego projektu, bez zmiany DNS. Nie usuwaj istniejących ustawień Netlify. Najpierw użyj deploy preview lub osobnego projektu testowego.

## Funkcje
Studio, projekty lokalne, 26 szablonów, kreator wizualny, biblioteka standardowa, JSON, HTTPS GET (CORS), Academy (10 lekcji), sceny Canvas 3D, eksport HTML/ZIP. Bez konta i płatnych API.

## Ograniczenia
Nie uruchamiaj niezaufanego kodu. Dane lokalne wymagają kopii zapasowych. PWA wymaga HTTPS lub localhost. Kreator nie importuje dowolnego kodu. API nie obsługuje POST ani uwierzytelniania. Renderer nie jest WebGL. Pełne testy przeglądarkowe, audyt bezpieczeństwa i sprawdzenie nazwy pozostają przed premierą.

## Licencja
Kod i dokumentacja tego wydania KODOWIT są udostępniane na licencji MIT (zobacz LICENSE). Odrębne przyszłe produkty mogą mieć inne licencje.

## Modern 4.3
Zobacz [reaktywność](docs/changelog/MODERN-4.3.md).

## 4.6
Cztery nowe szablony Modern; nawigacja WWW używa osobnych stron.

## 4.9 Modern Alpha
Aktualizacja cache i kontrola regresji. Szczegóły oraz ograniczenia: MODERN-4.9.md.

## 5.0 RC
Wydanie testowe obejmuje wszystkie zmiany Modern 4.0–4.9. Przed publikacją wykonaj checklistę WDROZENIE-5.0.md.

## 5.0.1 FIX
Ujednolicono oznaczenia, licznik 26 szablonów, odbudowano uszkodzone pliki Android i zmieniono cache PWA.

## Universal 6.1 Alpha
Terminal lokalny: `kodowit.cmd` (Windows) lub `./kodowit` (Linux/macOS). Szczegóły: core/README.md. Web pozostaje 5.0.1 RC.

## KODOWIT Core 6.3 Alpha
Obsługa plików i katalogów po jawnej zgodzie CLI. Szczegóły: core/README.md. Web 5.0.1 bez zmian.

Biblioteka standardowa Core 6.3: matematyka, statystyka, tekst, listy, daty i losowanie. Zobacz core/README.md.

## Core 6.4 Alpha
Lokalne bazy SQLite, zobacz core/README.md.

## Core 6.5 Alpha
Lokalne HTTP GET/POST i JSON, zobacz core/README.md.

## Core 6.7 Alpha
Integracja z wybranymi funkcjami Python, zobacz core/README.md.

## KODOWIT Core 6.9 Alpha
Diagnostyka i kontrola wykonania: zobacz core/README.md. Web pozostaje 5.0.1 RC.

## Edu 7.1 Alpha
Otwórz `edu.html`. Dziewięć lekcji, lokalny postęp, bez konta. Zobacz EDU-7.1.md.

## Edu 7.3 Alpha
Programowanie bloczkowe w edu.html. Zobacz EDU-7.3.md.

## Edu 7.4 Alpha
Grafika żółwia: zobacz EDU-7.4.md.

## Edu 7.5 Alpha
Interaktywne ćwiczenia: zobacz EDU-7.5.md.

## Edu 7.6 Alpha
Automatyczna ocena zadań: EDU-7.6.md.

## Edu 7.8
Kreator gier 2D: zobacz EDU-7.7.md.

## Edu 7.9
100 lekcji, materiały szkolne, raporty postępów do 100 quizów.

## Studio Desktop 8.1 Alpha
Lokalny edytor: `studio-desktop.cmd` lub `python3 desktop/studio.py`. Szczegóły: `desktop/README.md`.

## Studio Desktop 8.2 Alpha
Kolorowanie składni, numeracja wierszy, wcięcia i podpowiedzi Ctrl+Spacja. Instrukcja: desktop/README.md.

## 8.4 Desktop Alpha
Eksport konsolowych EXE: zobacz desktop/README.md.

## 8.5
Instrukcja budowania instalatora Windows: installer/README.md.

## 8.6
Rozszerzona biblioteka standardowa Core: matematyka, tekst, statystyka, daty, losowanie i JSON.

## 8.7 – katalog pakietów
`python core/registry.py --repo registry lista`

`python core/registry.py --repo registry --pakiety pakiety instaluj matematyka 1.0.0`

Katalog statyczny można opublikować przez HTTPS. Wpisy zawierają wersję, licencję, opis i SHA-256. Instalacja nie uruchamia kodu; import uruchamia kod z uprawnieniami interpretera. Używaj tylko zaufanych repozytoriów: suma kontrolna nie potwierdza tożsamości autora. Brak automatycznych zależności, aktualizacji i podpisów. Publikacja polega na ręcznym dodaniu pliku i wpisu do index.json.

## 8.8 – VS Code
Rozszerzenie lokalne: [instrukcja](vscode-kodowit/README.md).

## 8.9 Desktop Alpha
Ograniczenia zasobów Core i walidacja katalogu pakietów: [docs/changelog/BEZPIECZENSTWO-8.9.md](docs/changelog/BEZPIECZENSTWO-8.9.md).

## 9.1 Unified Language Alpha
Wspólny podzbiór i testy: [docs/changelog/UNIFIED-9.1.md](docs/changelog/UNIFIED-9.1.md).

## Etap 9.2 — klasy i obiekty (Core)
`klasa Nazwa { zmienna pole = 0 funkcja metoda(x) { ja.pole = x } }`.
Instancja: `zmienna a = Nazwa()`. Pola i metody: `a.pole`, `a.metoda(5)`.
Każda instancja ma własne pola; `ja` oznacza bieżący obiekt. Pola są publiczne.
Na razie bez konstruktorów z argumentami, dziedziczenia i obsługi klas w Web/Edu.
Przykład: `core/obiekty.kodowit`. Planowane wydanie publiczne: 1.0.0 po weryfikacji.

## 9.4 Object & Exception Alpha
Core/Desktop: `klasa B dziedziczy A`, `funkcja konstruktor(...)`, `sprobuj { ... } przechwyc(e) { ... }`, `zglos "opis"`. Dziedziczenie pojedyncze; konstruktor potomny zastępuje bazowy, a odziedziczony jest używany, gdy brak własnego. Brak super i finally. Limity kroków i wyjścia nie są przechwytywane. Web/Edu bez zmian.

## 9.6 Async & Modules Alpha
`zadanie(kod)` uruchamia niezależny interpreter w puli maksymalnie 4 wątków (16 zadań na uruchomienie). `oczekuj(id)` zwraca tekst konsoli, `gotowe(id)` sprawdza zakończenie. Zadania nie dziedziczą uprawnień ani zmiennych; błędy są zgłaszane przy oczekiwaniu. Koniec programu czeka na zadania. Nie jest to sandbox ani pełne async/await.

`importuj_modul("biblioteka.kodowit")` wymaga `--pliki KATALOG`, zwraca przestrzeń nazw z publicznymi deklaracjami. Import jest buforowany, cykle i ścieżki poza katalogiem są odrzucane. Eksportowane wartości są migawką deklaracji, nie żywymi powiązaniami. Moduły mogą korzystać z uprawnień programu głównego; używaj tylko zaufanego kodu.

## 9.8 GUI & Graphics Alpha
Nowe API GUI i grafiki 2D: zobacz core/README.md oraz core/gra2d.kodowit.

## KODOWIT 1.0.0 RC
Zobacz [informacje o wydaniu](docs/changelog/WYDANIE-1.0.0.md).

## 1.0.0 RC2
Pierwszy przegląd i poprawki regresyjne: [docs/changelog/AUDYT-RC2.md](docs/changelog/AUDYT-RC2.md).

## 1.0.0 RC3
Zmiany zgodności i Studio: [docs/changelog/RC3.md](docs/changelog/RC3.md).

## 1.0.0 RC4
[Podręcznik](PODRECZNIK.md) i [50 programów](przyklady.html). 47 przykładów konsolowych sprawdzono wykonaniem; 3 GUI wymagają interakcji.

## RC5
Centrum pobierania: pobierz.html. Budowanie Windows: .github/workflows/windows.yml; instrukcja installer/README.md.

## RC6 – przygotowanie premiery
[Lista kontrolna i wyniki testów](docs/changelog/PREMIERA-RC6.md). Status RC do weryfikacji na urządzeniach.

## RC8
Zobacz [docs/changelog/RC8.md](docs/changelog/RC8.md) – zakres poprawek i ograniczenia.

## RC10
Zobacz docs/changelog/RC10.md i SPECYFIKACJA.md.

## RC12
Zobacz [docs/changelog/RC12.md](docs/changelog/RC12.md).

## RC13–RC14
Zobacz [docs/changelog/RC14.md](docs/changelog/RC14.md).

## RC15–RC16
Zobacz [docs/changelog/RC16.md](docs/changelog/RC16.md) i [PLAN-PREMIERY.md](PLAN-PREMIERY.md).

Eksperymentalny eksport Python/JavaScript: zobacz [docs/changelog/RC18.md](docs/changelog/RC18.md).

## RC20
Zobacz [docs/changelog/RC20.md](docs/changelog/RC20.md): eksperymentalny eksport Python/JavaScript w Studio i CLI.

## RC24
Prototyp Builder: [builder.html](builder.html), ograniczenia w RC24.md.

## RC28
Zobacz [docs/changelog/RC28.md](docs/changelog/RC28.md) oraz [Business](business.html).

## RC92 – porządki
[Opis zmian](docs/changelog/RC92.md). Testy JS: `python tools/test_web.py`.

## Struktura wydania RC94
Numer wydania: `VERSION`. Aktualizacja oznaczeń: `python tools/version_release.py`, następnie `python tools/build_web.py`. Kontrola: oba polecenia z `--check`, `python tools/audit_release.py`, `python tools/test_web.py`.
Biblioteki: `shared/`, `database-engine/`, `application-engine/`. Strony HTML zachowują dotychczasowe adresy. Historia: `CHANGELOG.md` i `docs/changelog/`. Pozostałe moduły będą przenoszone etapami.
