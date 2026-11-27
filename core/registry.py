"""Explicit installation from a static HTTPS or local package catalogue."""
import argparse, hashlib, json, re, tempfile
from pathlib import Path
from urllib.request import build_opener, HTTPRedirectHandler
from urllib.parse import urlsplit
from packages import Packages


class HTTPSRedirectHandler(HTTPRedirectHandler):
    """Reject insecure redirects before sending the next request."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urlsplit(newurl).scheme != "https":
            raise ValueError("Wymagany HTTPS")
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def fetch(base, name, limit):
    if base.startswith('https://'):
        with build_opener(HTTPSRedirectHandler()).open(base.rstrip('/')+'/'+name, timeout=10) as f:
            if urlsplit(f.geturl()).scheme != 'https':
                raise ValueError('Wymagany HTTPS')
            data=f.read(limit+1)
    else:
        with (Path(base)/name).open('rb') as f: data=f.read(limit+1)
    if len(data)>limit: raise ValueError('Plik za duży')
    return data


def catalog(base):
    data=json.loads(fetch(base,'index.json',262144))
    if not isinstance(data,dict): raise ValueError('Nieprawidłowy katalog')
    if data.get('schema')!=1 or not isinstance(data.get('packages'),list): raise ValueError('Nieprawidłowy katalog')
    seen=set()
    for p in data['packages']:
        if not isinstance(p,dict) or not all(isinstance(p.get(k),str) for k in ('name','version','sha256','license','description')): raise ValueError('Nieprawidłowy wpis')
        name=p['name']; version=p['version']
        if not re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]{0,63}',name) or not re.fullmatch(r'\d+\.\d+\.\d+',version): raise ValueError('Nieprawidłowy pakiet')
        if not re.fullmatch(r'[0-9a-f]{64}',p['sha256']) or (name,version) in seen: raise ValueError('Nieprawidłowy wpis')
        seen.add((name,version))
    return data['packages']


def install(base,store,name,version):
    p=next((p for p in catalog(base) if p['name']==name and p['version']==version),None)
    if p is None: raise ValueError('Nie znaleziono wersji pakietu')
    data=fetch(base,f'{name}-{version}.kodowit',262144)
    if hashlib.sha256(data).hexdigest()!=p['sha256']: raise ValueError('Niezgodna suma SHA-256')
    with tempfile.TemporaryDirectory() as d:
        source=Path(d)/'source.kodowit'; source.write_bytes(data)
        Packages(store).install(name,source)


def main():
    a=argparse.ArgumentParser(description='KODOWIT – katalog pakietów'); a.add_argument('--repo',required=True); a.add_argument('--pakiety',default='pakiety'); a.add_argument('akcja',choices=['lista','instaluj']); a.add_argument('nazwa',nargs='?'); a.add_argument('wersja',nargs='?'); args=a.parse_args()
    try:
        if args.akcja=='lista':
            for p in catalog(args.repo): print(p['name'],p['version'],p['license'],p['description'])
        else:
            if not args.nazwa or not args.wersja: raise ValueError('Podaj nazwę i wersję')
            install(args.repo,args.pakiety,args.nazwa,args.wersja); print('Zainstalowano pakiet')
    except Exception as e: a.exit(1,f'Błąd: {e}\n')

if __name__=='__main__': main()
