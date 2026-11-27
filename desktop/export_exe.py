"""Build a Windows console executable with a bundled KODOWIT runtime."""
import argparse
import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path
CORE = Path(__file__).resolve().parents[1] / 'core'
sys.path.insert(0, str(CORE))
from kodowit import Parser, Blad

def launcher(source):
    Parser(source).seq()
    return ('import sys\nfrom kodowit import Core, Blad\n'
            'try:\n    Core().run(' + repr(source) + ')\n'
            'except Blad as e:\n    print("KODOWIT: " + str(e), file=sys.stderr)\n    sys.exit(1)\n')

def build(source, target):
    target = Path(target).resolve()
    if target.suffix.lower() != '.exe' or not re.fullmatch(r'[A-Za-z0-9_-]+', target.stem):
        raise ValueError('Nazwa EXE: litery ASCII, cyfry, myślnik lub podkreślenie')
    code = launcher(source)
    if sys.platform != 'win32':
        raise RuntimeError('Budowanie EXE wymaga Windows; PyInstaller nie jest kompilatorem krzyżowym.')
    if importlib.util.find_spec('PyInstaller') is None:
        raise RuntimeError('Zainstaluj PyInstaller: python -m pip install pyinstaller')
    if target.exists():
        raise ValueError('Plik już istnieje. Wybierz inną nazwę.')
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp); script = p/'start.py'; script.write_text(code, encoding='utf-8')
        r = subprocess.run([sys.executable,'-m','PyInstaller','--onefile','--console','--noupx','--name',target.stem,'--paths',str(CORE),'--distpath',str(p/'dist'),'--workpath',str(p/'work'),'--specpath',str(p),str(script)],cwd=tmp,capture_output=True,text=True,errors='replace',timeout=600)
        if r.returncode: raise RuntimeError('Błąd pakowania:\n'+r.stdout[-3000:]+r.stderr[-3000:])
        data=(p/'dist'/target.name).read_bytes()
        if not data.startswith(b'MZ'): raise RuntimeError('Nieprawidłowy plik EXE')
        with target.open('xb') as f: f.write(data)
    return target

def main():
    p=argparse.ArgumentParser(description='KODOWIT – eksport programu do EXE'); p.add_argument('plik'); p.add_argument('exe'); a=p.parse_args()
    try: print(build(Path(a.plik).read_text(encoding='utf-8-sig'),a.exe)); return 0
    except (Blad,ValueError,OSError,RuntimeError,subprocess.TimeoutExpired,RecursionError) as e: print('KODOWIT: '+str(e),file=sys.stderr); return 1
if __name__=='__main__': sys.exit(main())
