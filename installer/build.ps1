$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') { throw 'Budowanie wymaga Windows' }
Set-Location (Split-Path $PSScriptRoot -Parent)
python tools/version_release.py --check
if ($LASTEXITCODE -ne 0) { throw 'Niespójna wersja wydania' }
python -m PyInstaller --noconfirm --clean --onedir --console --noupx --name KODOWIT-Studio --paths core --paths desktop --hidden-import debugger --hidden-import kodowit --hidden-import editor desktop/installed_entry.py
if ($LASTEXITCODE -ne 0) { throw 'Błąd budowania Studio' }
& '.\dist\KODOWIT-Studio\KODOWIT-Studio.exe' --core-worker --wersja
if ($LASTEXITCODE -ne 0) { throw 'Błąd testu Core' }
$iscc = Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe'
if (!(Test-Path $iscc)) { throw 'Zainstaluj Inno Setup 6' }
& $iscc installer/kodowit.iss
if ($LASTEXITCODE -ne 0) { throw 'Błąd instalatora' }
