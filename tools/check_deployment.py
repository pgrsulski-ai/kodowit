"""Offline preflight; does not contact Supabase or certify production."""
import argparse, re, sys, json, base64
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def check(config, production=False):
    m=re.fullmatch(r"\s*globalThis\.KODOWIT_CLOUD_CONFIG\s*=\s*\{\s*url:\s*'([^']*)'\s*,\s*key:\s*'([^']*)'\s*\};\s*", '\n'.join(x for x in config.splitlines() if not x.strip().startswith('//')))
    if not m: raise ValueError('Nieobsługiwany format konfiguracji')
    url,key=m.groups()
    if not url and not key:
        if production: raise ValueError('Cloud nie skonfigurowany')
        return 'Cloud wyłączony – tryb offline'
    if not re.fullmatch(r'https://[a-z0-9-]+\.supabase\.co/?',url): raise ValueError('Niepoprawny URL Supabase')
    if re.fullmatch(r'sb_publishable_[A-Za-z0-9_-]+',key): return 'Format publicznego klucza poprawny; backend niezweryfikowany'
    try:
        parts=key.split('.')
        if len(parts)!=3: raise ValueError()
        payload=json.loads(base64.urlsafe_b64decode(parts[1]+'='*(-len(parts[1])%4)))
        if payload.get('role')!='anon': raise ValueError()
    except Exception: raise ValueError('Wymagany publiczny klucz anon lub publishable') from None
    return 'Format publicznego klucza poprawny; backend niezweryfikowany'
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--production',action='store_true');a=p.parse_args()
    try: print(check((ROOT/'cloud-config.js').read_text(),a.production))
    except ValueError as e: sys.exit(str(e))
