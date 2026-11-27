import unittest,tempfile
from pathlib import Path
from packages import Packages
from kodowit import Core,Blad
class TestPackages(unittest.TestCase):
 def test_lifecycle(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'source.kodowit'; p.write_text('funkcja podwoj(x) { zwróć x*2 }',encoding='utf8'); store=Packages(Path(d)/'store'); store.install('mat',p); self.assertEqual(store.list(),['mat']); out=[]; Core(out.append,packages=store.root).run('importuj_pakiet("mat") wypisz(podwoj(4))'); self.assertEqual(out,[8]); store.remove('mat'); self.assertEqual(store.list(),[])
 def test_traversal(self):
  with self.assertRaises(ValueError): Packages('.').path('../x')
 def test_disabled(self):
  with self.assertRaises(Blad): Core().run('importuj_pakiet("mat")')
 def test_cycle(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'a.kodowit').write_text('importuj_pakiet("a")');
   with self.assertRaises(Blad): Core(packages=d).run('importuj_pakiet("a")')
