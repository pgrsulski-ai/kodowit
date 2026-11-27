"""Buduje zgodny z przeglądarką i Node pakiet kompilatora."""
from pathlib import Path
import argparse
import hashlib
ROOT=Path(__file__).resolve().parents[1]
FILES=('lexer.js','parser-generator.js','runtime.js','project.js','index.js')
def render():
 return "// PLIK GENEROWANY: python tools/build_compiler.py; nie edytuj ręcznie.\n(function(root){\n'use strict';\n"+''.join((ROOT/'compiler'/f).read_text(encoding='utf-8') for f in FILES)+'})(globalThis);\n'

def build(check=False):
 expected=render().encode('utf-8')
 p=ROOT/'compiler.js'
 if check:
  actual=p.read_bytes()
  if actual!=expected: raise SystemExit('Nieaktualny compiler.js: SHA256 rzeczywisty '+hashlib.sha256(actual).hexdigest()+'; oczekiwany '+hashlib.sha256(expected).hexdigest())
  print('OK: compiler.js SHA256 '+hashlib.sha256(actual).hexdigest())
 else:p.write_bytes(expected)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');build(p.parse_args().check)
