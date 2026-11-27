"""Synchronizuje kompilator i samodzielne wydania HTML; bez zależności."""
import json,re,argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
NAMES=['OTWORZ-NA-ANDROIDZIE.html']
def build(check=False):
 compiler=(ROOT/'compiler.js').read_text()
 studio=(ROOT/'studio.html').read_text()
 standalone=re.sub(r'<script src="compiler\.js"></script>',lambda _: '<script>'+compiler+'</script>',studio,count=1)
 if standalone==studio: raise ValueError('Brak odwołania do kompilatora')
 for asset in ('edu/edu-core.js','eksport.js'):
  standalone=standalone.replace('<script src="'+asset+'"></script>','<script>'+(ROOT/asset).read_text()+'</script>')
 standalone=standalone.replace('<script src="shared/pwa.js"></script>','')
 for name in NAMES:
  path=ROOT/name; old=path.read_text(); start=old.index('const pages=')+len('const pages='); pages,n=json.JSONDecoder().raw_decode(old[start:]); pages['studio']=standalone
  new=old[:start]+json.dumps(pages,ensure_ascii=False).replace('<','\\u003c')+old[start+n:]
  if check and new!=old: raise SystemExit('Nieaktualny plik: '+name)
  if not check: path.write_text(new)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');build(p.parse_args().check)
