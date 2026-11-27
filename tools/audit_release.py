"""Kontrola lokalnych zasobów wydania, bez dostępu do sieci."""
import json,re,sys
from build_compiler import build as check_compiler
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).resolve().parents[1]
check_compiler(check=True)
errors=[]
class Links(HTMLParser):
 def handle_starttag(self,tag,attrs):
  for key,value in attrs:
   if key not in ('href','src') or not value: continue
   u=urlsplit(value)
   if not u.scheme and not u.netloc and u.path:
    target=(ROOT if u.path.startswith('/') else self.path.parent)/unquote(u.path.lstrip('/'))
    if not target.exists(): errors.append(f'{self.path.name}: {value}')
for path in ROOT.glob('*.html'):
 parser=Links();parser.path=path;parser.feed(path.read_text(encoding='utf-8'))
assets=json.loads(re.search(r'const F=(\[.*?\]);',(ROOT/'sw.js').read_text()).group(1))
for asset in assets:
 if not (ROOT/asset).exists(): errors.append('PWA: '+asset)
print(f'PWA: {len(assets)} zasobów; szablony: {len(list((ROOT/"szablony").glob("*.kodowit")))}')
if errors: print('\n'.join(errors));sys.exit(1)
print('OK: lokalne odnośniki HTML i zasoby PWA')
