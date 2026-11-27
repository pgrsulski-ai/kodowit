# KODOWIT 1.0 – pakiet premierowy

Status: pakiet 1.0.0 przygotowany lokalnie. Publikacja po sprawdzeniu wdrożenia; moduły eksperymentalne pozostają testowe.

## Wdrożenie po pracy
- [ ] Kopia repozytorium i gałąź testowa; rozpakować 1.0.0 w katalogu głównym, zachować .git, .github, .gitignore i _headers.
- [ ] Sprawdzić różnice i podgląd Netlify; publikacja z katalogu głównego, bez polecenia budowania. DNS zmieniać dopiero po weryfikacji nazwy i podglądu.
- [ ] Sprawdzić index.html, studio.html, edu.html, dokumentacja.html, przyklady.html, pobierz.html na komputerze i telefonie.
- [ ] Sprawdzić eksport, ponowne otwarcie offline i aktualizację PWA.
- [ ] Po udostępnieniu workflow w gałęzi domyślnej: Actions → KODOWIT Windows installer → Run workflow; pobrać KODOWIT-Windows-x64.
- [ ] Porównać SHA256.txt z Get-FileHash instalatora; sprawdzić instalację, Studio, debugger, odinstalowanie.
- [ ] Sprawdzić macOS, Android, iOS i przeglądarki; udokumentować wyniki oraz błędy.
- [ ] Po weryfikacji połączyć zmiany z main i sprawdzić domenę produkcyjną.
- [ ] Udostępnić źródła po sprawdzeniu, że nie zawierają sekretów; zapewnić publiczny kanał pobierania.
- [ ] Ocenić bezpieczeństwo i pozostałe blokady opisane w docs/RC137.md przed publikacją.

## Tekst ogłoszenia – wydanie 1.0
KODOWIT – Polski kod. Nieograniczone pomysły.

Przedstawiamy KODOWIT 1.0 – polski język programowania i otwartoźródłowy projekt dla osób uczących się kodowania oraz twórców aplikacji. Studio Web, platforma Edu, 100 lekcji i 50 przykładów dla Core pomagają rozpocząć naukę. Projekt jest udostępniany na licencji MIT, bez obowiązkowych subskrypcji. Zapraszamy do testowania i zgłaszania błędów.

https://kodowit.szybkienarzedzia.pl

Publikować dopiero po wdrożeniu i sprawdzeniu dostępności wymienionych funkcji. Nie obiecywać gotowego instalatora przed jego zbudowaniem i testem. Core nie jest sandboxem; kompilator natywny jest eksperymentalny.
