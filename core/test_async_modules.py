import unittest,tempfile
from pathlib import Path
from kodowit import Core,Blad
class AsyncModules(unittest.TestCase):
 def test_jobs(self):
  out=[]; Core(out.append).run('zmienna a = zadanie("wypisz(21 * 2)") zmienna b = zadanie("wypisz(7)") wypisz(oczekuj(a)) wypisz(oczekuj(b))'); self.assertEqual(out,['42','7'])
 def test_error(self):
  with self.assertRaises(Blad): Core().run('oczekuj(zadanie("wypisz(1 / 0)"))')
 def test_modules(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'m.kodowit').write_text('zmienna x = 7 funkcja razy(n) { zwroc n * x }',encoding='utf8'); out=[]; Core(out.append,root=d).run('zmienna m = importuj_modul("m.kodowit") wypisz(m.razy(6))'); self.assertEqual(out,[42])
 def test_cycle(self):
  with tempfile.TemporaryDirectory() as d:
   Path(d,'m.kodowit').write_text('importuj_modul("m.kodowit")',encoding='utf8')
   with self.assertRaises(Blad): Core(root=d).run('importuj_modul("m.kodowit")')
 def test_escape(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(Blad): Core(root=d).run('importuj_modul("../m.kodowit")')
