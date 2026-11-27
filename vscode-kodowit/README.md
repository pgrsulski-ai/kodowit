# KODOWIT dla VS Code (8.8 Alpha)
Rozszerzenie lokalne, MIT. Obsługuje składnię Core, nie pełną składnię Web.
Otwórz katalog `vscode-kodowit` w VS Code i uruchom F5 (Extension Development Host; konfiguracja w .vscode). W nowym oknie otwórz zaufany katalog z plikami .kodowit. Python 3.10+ musi być dostępny. Ustaw `kodowit.python` i w razie potrzeby `kodowit.corePath` w ustawieniach użytkownika. Paleta Ctrl+Shift+P: KODOWIT: Uruchom program / Sprawdź składnię. Ctrl+Spacja: podpowiedzi. Kod wykonuje się lokalnie, bez dodatkowych uprawnień Core; uruchamiaj tylko zaufane programy.
Opcjonalne pakowanie: `npx @vscode/vsce package` w tym katalogu (wymaga pobrania narzędzia); potem instalacja VSIX z menu rozszerzeń. Po instalacji VSIX ustaw ścieżkę Core ręcznie. Nie opublikowano w Marketplace.
