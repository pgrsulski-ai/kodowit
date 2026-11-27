# Studio Desktop 8.3 Alpha
Windows: uruchom studio-desktop.cmd. Linux/macOS: python3 desktop/studio.py.
Wymaga Python 3.10+ z Tkinter. F5 uruchamia, Ctrl+S zapisuje.
Kod wykonuje Core 7.0 w osobnym procesie z limitem 10 sekund; bez dodatkowych uprawnień CLI. Nie jest to izolacja bezpieczeństwa. Uruchamiaj zaufany kod. Konsola nie obsługuje interaktywnego wejścia. Brak instalatora EXE.

Nowości: kolorowanie składni, numery wierszy, wcięcia po Enter, Tab = 4 spacje, Ctrl+Spacja = menu podpowiedzi słów kluczowych i wybranych funkcji.

Debugger: ustaw punkt na bieżącym wierszu, Debuguj, Krok, Kontynuuj, Stop. Podgląd zmiennych przed instrukcją. Punkty są numerami wierszy; po edycji ustaw je ponownie. Brak limitu czasu sesji debugowania, obowiązuje limit kroków Core.

## 8.4 – eksport EXE (Windows)
Na komputerze twórcy: `python -m pip install -r installer/requirements-build.txt`. Następnie przycisk Eksport EXE albo `python desktop/export_exe.py core/demo.kodowit demo.exe`. Odbiorca nie potrzebuje Pythona. Eksport obejmuje podstawowy Core bez dodatkowych uprawnień GUI, sieci, plików i pakietów. Nazwa ASCII. Nie nadpisuje istniejących plików. Kod jest pakowany, nie kompilowany natywnie ani szyfrowany. Windows i faktyczne pakowanie wymagają testu; PyInstaller nie jest dostarczany w ZIP.

## 8.5
Instalator: ../installer/README.md.
