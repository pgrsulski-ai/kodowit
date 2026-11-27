"""Uruchamia niezależne zestawy JS, raportuje wszystkie błędy i limity."""
import subprocess, sys, time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
failed=[]; tests=sorted((ROOT/'tests').glob('test*.cjs'))
for p in tests:
    start=time.monotonic()
    try:
        r=subprocess.run(['node',str(p)],cwd=ROOT,capture_output=True,text=True,timeout=60)
        if r.returncode: failed.append(p.name); print(r.stdout,r.stderr)
        print(('FAIL' if r.returncode else 'OK'),p.name,round(time.monotonic()-start,2),flush=True)
    except subprocess.TimeoutExpired: failed.append(p.name); print('TIMEOUT',p.name,flush=True)
print(f'{len(tests)-len(failed)}/{len(tests)}; błędy: {failed}')
sys.exit(bool(failed) or not tests)
