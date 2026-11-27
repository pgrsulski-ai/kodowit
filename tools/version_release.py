"""Synchronizuje publiczne oznaczenia wydania z VERSION, nie zmienia kluczy danych."""
import argparse,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sync(check=False):
 v=(ROOT/'VERSION').read_text().strip(); m=re.fullmatch(r'(\d+\.\d+\.\d+)(?:-rc(\d+))?',v)
 if not m: raise ValueError('Niepoprawna wersja')
 label=f'{m[1]} RC{m[2]}' if m[2] else m[1]
 short=f'RC{m[2]}' if m[2] else m[1]
 for p in [*ROOT.glob('*.html'),ROOT/'core/kodowit.py',ROOT/'desktop/studio.py',ROOT/'sw.js',ROOT/'installer/kodowit.iss']:
  if p.name=='OTWORZ-NA-ANDROIDZIE.html':continue
  old=p.read_text(); s=old
  if p.suffix=='.html':
   s=re.sub(r'1\.0\.0 RC\d+',label,s)
   s=re.sub(r'(<title>[^<]*?)\bRC\d+',lambda x:x[1]+short,s)
   if p.name=='ekosystem.html':s=re.sub(r'RC\d+ – katalog',f'{short} – katalog',s)
  elif p.name=='sw.js':s=re.sub(r'const C="kodowit-[^"]+"',f'const C="kodowit-{v.replace(".","-")}"',s)
  else:s=re.sub(r'1\.0\.0 RC\d+',label,s)
  if s!=old:
   if check:raise SystemExit('Nieaktualne oznaczenie: '+str(p))
   p.write_text(s)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');sync(p.parse_args().check)
