"""Local filesystem functions, enabled explicitly by CLI flag."""
from pathlib import Path
import platform

class SystemIO:
    def __init__(self, root):
        self.root = Path(root).resolve(strict=True)
        if not self.root.is_dir(): raise ValueError('Katalog roboczy nie jest katalogiem')
    def path(self, name):
        if not isinstance(name, str): raise ValueError('Ścieżka musi być tekstem')
        p = Path(name)
        if p.is_absolute() or '..' in p.parts: raise ValueError('Dozwolone są ścieżki względne bez ..')
        target = (self.root / p).resolve()
        if not target.is_relative_to(self.root): raise ValueError('Ścieżka poza katalogiem roboczym')
        return target
    def read(self, name):
        with self.path(name).open('rb') as f: data = f.read(1000001)
        if len(data)>1000000: raise ValueError('Plik przekracza 1 MB')
        return data.decode('utf-8-sig')
    def write(self, name, value, append=False):
        if not isinstance(value,str): raise ValueError('Zawartość musi być tekstem')
        data=value.encode('utf-8'); p=self.path(name)
        if len(data)+(p.stat().st_size if append and p.exists() else 0)>1000000: raise ValueError('Limit pliku: 1 MB')
        with p.open('ab' if append else 'wb') as f: f.write(data)
        return len(data)
    def bindings(self):
        return {'czytaj_plik':self.read,'zapisz_plik':self.write,'dopisz_plik':lambda n,v:self.write(n,v,True), 'istnieje':lambda n:self.path(n).exists(),'utworz_katalog':lambda n:self.path(n).mkdir(parents=True,exist_ok=True),'lista_katalogu':lambda n:sorted(p.name for p in self.path(n).iterdir()),'system':platform.system,'katalog_roboczy':lambda:str(self.root)}
