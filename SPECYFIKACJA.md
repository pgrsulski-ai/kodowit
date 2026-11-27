# KODOWIT — wspólny podzbiór (projekt specyfikacji)
Kod UTF-8. Komentarze # oraz //. Identyfikatory literowe z cyframi i podkreśleniem. Instrukcje: zmienna nazwa = wyrażenie, przypisanie, wypisz(wartość), jeśli warunek { ... } inaczej { ... }, dopóki warunek { ... }, dla nazwa w lista { ... }, funkcja nazwa(parametry) { ... }, zwróć wyrażenie. Literały: liczby, tekst w podwójnych cudzysłowach, listy, prawda i fałsz. Operatory arytmetyczne i porównania; oraz, lub, nie. Zakres zgodności gwarantowany wyłącznie przez aktualne testy wspólne; formatowanie wartości logicznych, indeksowanie, modulo i typy nadal wymagają pełnej normalizacji Web/Core/Edu. Web posiada osobną składnię interfejsów, Core rozszerzenia systemowe, Edu grafikę żółwia. Nie jest to kompletna specyfikacja normatywna.

## Profil wspólny RC100
Normatywny cel: arytmetyka liczb skończonych, tekst, listy, warunki, pętle i funkcje. Modulo ma znak dzielnika; operatory logiczne zwracają wartość logiczną i działają krótkospięciowo; listy porównuje się strukturalnie. Docelowy zapis wartości logicznych: prawda/fałsz. Te reguły nie są jeszcze w pełni zaimplementowane.

| Funkcja | Web | Core/CLI | Edu |
|---|---|---|---|
| 12 programów wspólnych RC100 | tak | tak | tak |
| Strony, komponenty, DOM | tak | nie | nie |
| Pliki systemowe, SQLite, HTTP lokalny | nie | opcjonalne uprawnienia | nie |
| Grafika żółwia | nie w tym profilu | nie w tym profilu | tak |
| Klasy i dziedziczenie | poza profilem | tak | poza profilem |

### Znane rozbieżności (Web / Edu / Core)
- `-5 % 3`: -2 / 1 / 1.
- `2 oraz 3`: 3 / prawda / True.
- Równość dwóch list o tej samej zawartości: fałsz / prawda / prawda.
- `wypisz(prawda)`: true / prawda / True.

Test `node tests/test-conformance-rc100.cjs` wykonuje 12 przypadków z oczekiwanym wynikiem i cztery sondy diagnostyczne. Web testuje wygenerowany JS w Node, nie pełny runtime DOM. Sondy nie stanowią zaliczonej zgodności. Nie uruchamiać niezaufanego kodu w Node VM.

### RC102 — wspólne zachowanie
Modulo ma znak dzielnika; operatory logiczne zwracają wartości logiczne i zachowują krótkie spięcie. Listy porównujemy rekurencyjnie. Wypisywanie pojedynczych wartości logicznych w CLI i Web używa słów prawda/fałsz. Nie oznacza to pełnej zgodności typów ani formatowania złożonych wartości.
