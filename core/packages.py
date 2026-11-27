"""Local source packages, explicitly enabled by the caller."""
import re
from pathlib import Path

class Packages:
 def __init__(self, root):
  self.root=Path(root).resolve()
 def path(self,name):
  if not isinstance(name,str) or not re.fullmatch(r'[a-zA-Z][a-zA-Z0-9_-]{0,63}',name): raise ValueError('Nieprawidłowa nazwa pakietu')
  p=self.root/(name+'.kodowit')
  if p.is_symlink(): raise ValueError('Dowiązania pakietów niedozwolone')
  return p
 def read(self,name):
  with self.path(name).open('rb') as f: data=f.read(262145)
  if len(data)>262144: raise ValueError('Pakiet za duży')
  return data.decode('utf-8-sig')
 def install(self,name,source):
  from kodowit import Parser
  with Path(source).open('rb') as f: data=f.read(262145)
  if len(data)>262144: raise ValueError('Pakiet za duży')
  Parser(data.decode('utf-8-sig')).seq()
  self.root.mkdir(parents=True,exist_ok=True)
  with self.path(name).open('xb') as f: f.write(data)
 def remove(self,name): self.path(name).unlink()
 def list(self): return sorted(p.stem for p in self.root.glob('*.kodowit') if p.is_file() and not p.is_symlink())
