import sys,time,statistics
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'core'))
from kodowit import Core
from eksport import eksport
source='zmienna x = 0\ndopóki x < 1000 { x = x+1 }\nwypisz(x)'
compiled=compile(eksport(source,'python'),'<eksport>','exec')
for target in ('Core','Python'):
 times=[]
 for _ in range(7):
  out=[]; c=Core(out=out.append); t=time.perf_counter()
  if target=='Core': c.run(source)
  else: exec(compiled,{'print':out.append})
  times.append((time.perf_counter()-t)*1000); assert out==[1000]
 print(target,round(statistics.median(times),3),'ms')
