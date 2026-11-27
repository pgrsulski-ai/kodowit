"""Buduje czystą paczkę źródłową i osobną dystrybucję webową."""
from pathlib import Path
import argparse, zipfile, re, json, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
def build(out,web=False):
 version=(ROOT/'VERSION').read_text().strip()
 if not re.fullmatch(r'\d+\.\d+\.\d+(?:-rc\d+)?',version): raise ValueError('Niepoprawna wersja')
 for script,args in [('version_release.py',['--check']),('audit_release.py',[]),('check_deployment.py',[]),('build_web.py',['--check'])]: subprocess.run([sys.executable,str(ROOT/'tools'/script),*args],check=True)
 out.mkdir(parents=True,exist_ok=True)
 target=out/('KODOWIT-'+version.upper()+('-WEB' if web else '')+'.zip')
 excluded={'.git','__pycache__','node_modules','dist','build','.pytest_cache'}
 assets=set(json.loads(re.search(r'const F=(\[.*?\]);',(ROOT/'sw.js').read_text()).group(1)))
 with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(ROOT.rglob('*')):
   rel=p.relative_to(ROOT); name=rel.as_posix()
   if not p.is_file() or p.is_symlink() or excluded.intersection(rel.parts) or p.suffix in ('.pyc','.pyo','.zip') or p.name.startswith('.env'): continue
   if web and not (name in assets or len(rel.parts)==1 and p.suffix in ('.html','.js','.css','.svg','.xml','.txt','.md','.webmanifest') or name in ('_headers','LICENSE','VERSION') or rel.parts[0] in ('szablony','przyklady','docs','registry')): continue
   z.write(p,name)
 with zipfile.ZipFile(target) as z:
  if z.testzip(): raise ValueError('Uszkodzone archiwum')
 print(target)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,default=ROOT/'dist');p.add_argument('--web',action='store_true');a=p.parse_args();build(a.out,a.web)
