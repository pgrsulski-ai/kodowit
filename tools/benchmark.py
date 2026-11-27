"""Powtarzalny mikrobenchmark Core; bez deklaracji przewagi nad innymi językami."""
import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'core'))
from kodowit import Core
cases={'pętla 1000':'zmienna x = 0\ndopóki x < 1000 { x = x + 1 }\nwypisz(x)', 'funkcja 1000':'funkcja dwa(x) { zwróć x * 2 }\nzmienna x = 0\ndopóki x < 1000 { dwa(x) x = x + 1 }\nwypisz(x)'}
for name,code in cases.items():
 times=[]
 for _ in range(7):
  out=[];c=Core(out=out.append);t=time.perf_counter();c.run(code);times.append((time.perf_counter()-t)*1000)
  assert str(out[-1])=='1000',out
 print(f'{name}: mediana {statistics.median(times):.2f} ms (7 prób)')
