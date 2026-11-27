import unittest
from kodowit import Core, Blad
class Features(unittest.TestCase):
 def check(self,code,expected):
  out=[]; Core(out.append).run(code); self.assertEqual(out,expected)
 def test_inheritance(self):
  self.check('klasa A { zmienna x = 1 funkcja konstruktor(n) { ja.x = n } funkcja wartosc() { zwroc ja.x } } klasa B dziedziczy A { funkcja wartosc() { zwroc ja.x + 1 } } zmienna b = B(4) wypisz(b.wartosc())',[5])
 def test_constructor(self):
  self.check('klasa A { zmienna x = 0 funkcja konstruktor(n) { ja.x = n } } zmienna a = A(7) wypisz(a.x)',[7])
 def test_catch(self):
  self.check('sprobuj { zglos "test" } przechwyc(e) { wypisz(e) } wypisz(42)',['test',42])
 def test_runtime(self):
  self.check('sprobuj { wypisz(1 / 0) } przechwyc(e) { wypisz(7) }',[7])
 def test_limit(self):
  with self.assertRaises(Blad): Core(limit=30).run('sprobuj { dopoki prawda {} } przechwyc(e) {}')
 def test_return(self):
  self.check('funkcja f() { sprobuj { zwroc 3 } przechwyc(e) { zwroc 4 } } wypisz(f())',[3])
