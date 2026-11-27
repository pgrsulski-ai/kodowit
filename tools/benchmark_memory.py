"""Pomiar czasu i szczytu alokacji Python (nie RSS)."""
import sys, time, statistics, tracemalloc
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'core'))
from kodowit import Core
for name,source in [('petla','zmienna x = 0\ndopóki x < 1000 { x = x + 1 }\nwypisz(x)'),('funkcja','funkcja dwa(x) { zwróć x * 2 }\nzmienna x = 0\ndopóki x < 1000 { dwa(x) x = x + 1 }\nwypisz(x)')]:
 times=[]; peaks=[]
 for i in range(7):
  out=[]; c=Core(out=out.append); t=time.perf_counter(); c.run(source); times.append((time.perf_counter()-t)*1000); assert out==[1000],out
  out=[]; c=Core(out=out.append); tracemalloc.start()
  try: c.run(source); peaks.append(tracemalloc.get_traced_memory()[1]); assert out==[1000],out
  finally: tracemalloc.stop()
 print(f'{name}: {statistics.median(times):.3f} ms; szczyt alokacji {statistics.median(peaks)/1024:.2f} KiB (mediana 7 prób)')
