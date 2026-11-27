# KODOWIT 1.0.0 RC4 – podręcznik

## Pierwsze kroki
Python 3.10+ z Tkinter jest potrzebny do Core i Desktop. Z katalogu głównego uruchom `python core/kodowit.py przyklady/01-powitanie.kodowit`. Windows: można użyć `py` zamiast `python`. Studio Web i Edu działają w przeglądarce; nie wymagają Pythona.

## Składnia Core
Pliki UTF-8, bloki w klamrach, komentarze # lub //. Zmienna: `zmienna x = 5`; przypisanie: `x = x + 1`. Listy indeksowane od zera. Warunki: `jezeli x > 0 { wypisz(x) } inaczej { wypisz(0) }`. Pętle: `dla i w [1,2,3] { wypisz(i) }`, `dopoki x > 0 { x = x - 1 }`. Funkcje: `funkcja f(x) { zwroc x*2 }`. Operatory logiczne: oraz, lub, nie. Wybrane aliasy mają polskie znaki.

## Zgodność silników
Core: wszystkie przykłady w katalogu przyklady. Web: deklaracje stron, komponenty, style i wspólny podzbiór instrukcji; zobacz dokumentacja.html. Edu: podstawy programowania, żółw, bloczki i ćwiczenia. Klasy, wyjątki, zadania, SQLite, lokalne pliki i Tkinter są funkcjami Core; nie zakładaj ich dostępności w Web/Edu. Kompilator natywny jest eksperymentalny i obsługuje ograniczony podzbiór liczb całkowitych.

## Uprawnienia i uruchamianie
`--sprawdz` sprawdza składnię, `--sledz` pokazuje ślad, `--limit 50000` ustala budżet kroków. `--pliki KATALOG` włącza pliki, moduły i SQLite; `--gui` włącza Tkinter; `--siec` lokalny serwer HTTP. Uruchamiaj wyłącznie zaufany kod. Limity nie stanowią piaskownicy. Przykłady plikowe uruchamiaj w osobnym pustym katalogu, z wyjątkiem modułu, który wymaga pomocniczy.kodowit. Przykład SQLite wymaga nowej bazy przy każdym uruchomieniu.

## Biblioteka i zaawansowane funkcje
Przykłady 01–38 obejmują obliczenia, teksty, daty, listy, pętle i funkcje. 39–44: JSON, klasy, konstruktor, dziedziczenie pojedyncze, wyjątki i zadania. 45–47: moduły, pliki, SQLite. 48–50: okna, formularz i gra. Zadania zwracają tekst wyjścia, nie współdzielą zmiennych. GUI wymaga ekranu; zamknij okno ręcznie. Szczegóły funkcji, API, pakietów i ograniczeń: core/README.md (historyczne opisy etapów).

## Katalog przykładów
- [01-powitanie.kodowit](przyklady/01-powitanie.kodowit)
- [02-zakupy.kodowit](przyklady/02-zakupy.kodowit)
- [03-rabat.kodowit](przyklady/03-rabat.kodowit)
- [04-vat.kodowit](przyklady/04-vat.kodowit)
- [05-pole-prostokata.kodowit](przyklady/05-pole-prostokata.kodowit)
- [06-objetosc.kodowit](przyklady/06-objetosc.kodowit)
- [07-temperatura.kodowit](przyklady/07-temperatura.kodowit)
- [08-kilometry.kodowit](przyklady/08-kilometry.kodowit)
- [09-paliwo.kodowit](przyklady/09-paliwo.kodowit)
- [10-energia.kodowit](przyklady/10-energia.kodowit)
- [11-srednia-ocen.kodowit](przyklady/11-srednia-ocen.kodowit)
- [12-mediana.kodowit](przyklady/12-mediana.kodowit)
- [13-najwieksza.kodowit](przyklady/13-najwieksza.kodowit)
- [14-najmniejsza.kodowit](przyklady/14-najmniejsza.kodowit)
- [15-sortowanie.kodowit](przyklady/15-sortowanie.kodowit)
- [16-unikalne.kodowit](przyklady/16-unikalne.kodowit)
- [17-nwd.kodowit](przyklady/17-nwd.kodowit)
- [18-nww.kodowit](przyklady/18-nww.kodowit)
- [19-pierwiastek.kodowit](przyklady/19-pierwiastek.kodowit)
- [20-potega.kodowit](przyklady/20-potega.kodowit)
- [21-zaokraglenie.kodowit](przyklady/21-zaokraglenie.kodowit)
- [22-wariancja.kodowit](przyklady/22-wariancja.kodowit)
- [23-wielkie-litery.kodowit](przyklady/23-wielkie-litery.kodowit)
- [24-przycinanie.kodowit](przyklady/24-przycinanie.kodowit)
- [25-zamiana.kodowit](przyklady/25-zamiana.kodowit)
- [26-laczenie.kodowit](przyklady/26-laczenie.kodowit)
- [27-wyszukiwanie.kodowit](przyklady/27-wyszukiwanie.kodowit)
- [28-data.kodowit](przyklady/28-data.kodowit)
- [29-roznica-dat.kodowit](przyklady/29-roznica-dat.kodowit)
- [30-dzien-tygodnia.kodowit](przyklady/30-dzien-tygodnia.kodowit)
- [31-losowanie.kodowit](przyklady/31-losowanie.kodowit)
- [32-probka.kodowit](przyklady/32-probka.kodowit)
- [33-budzet.kodowit](przyklady/33-budzet.kodowit)
- [34-prog.kodowit](przyklady/34-prog.kodowit)
- [35-odliczanie.kodowit](przyklady/35-odliczanie.kodowit)
- [36-silnia.kodowit](przyklady/36-silnia.kodowit)
- [37-fibonacci.kodowit](przyklady/37-fibonacci.kodowit)
- [38-tabliczka.kodowit](przyklady/38-tabliczka.kodowit)
- [39-json.kodowit](przyklady/39-json.kodowit)
- [40-licznik.kodowit](przyklady/40-licznik.kodowit)
- [41-produkt.kodowit](przyklady/41-produkt.kodowit)
- [42-dziedziczenie.kodowit](przyklady/42-dziedziczenie.kodowit)
- [43-wyjatek.kodowit](przyklady/43-wyjatek.kodowit)
- [44-zadania.kodowit](przyklady/44-zadania.kodowit)
- [45-modul.kodowit](przyklady/45-modul.kodowit)
- [46-plik.kodowit](przyklady/46-plik.kodowit)
- [47-sqlite.kodowit](przyklady/47-sqlite.kodowit)
- [48-okno.kodowit](przyklady/48-okno.kodowit)
- [49-formularz.kodowit](przyklady/49-formularz.kodowit)
- [50-gra-2d.kodowit](przyklady/50-gra-2d.kodowit)
