import unittest,tempfile
from pathlib import Path
from kodowit import Core,Blad
class Files(unittest.TestCase):
 def test_roundtrip(self):
  with tempfile.TemporaryDirectory() as d:
   out=[]; Core(out.append,root=d).run('utworz_katalog("dane"); zapisz_plik("dane/a.txt","żółć"); dopisz_plik("dane/a.txt","!"); wypisz(czytaj_plik("dane/a.txt")); wypisz(lista_katalogu("dane")); wypisz(istnieje("dane/a.txt"))'); self.assertEqual(out,['żółć!',['a.txt'],True])
 def test_disabled(self):
  with self.assertRaises(Blad): Core().run('czytaj_plik("a")')
 def test_escape(self):
  with tempfile.TemporaryDirectory() as d:
   for path in ('../a','/tmp/a'):
    with self.assertRaises(Blad): Core(root=d).run('czytaj_plik("'+path+'")')
 def test_symlink(self):
  with tempfile.TemporaryDirectory() as d, tempfile.TemporaryDirectory() as other:
   (Path(d)/'link').symlink_to(other,target_is_directory=True)
   with self.assertRaises(Blad): Core(root=d).run('zapisz_plik("link/a","x")')
 def test_missing(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(Blad): Core(root=d).run('czytaj_plik("brak")')
