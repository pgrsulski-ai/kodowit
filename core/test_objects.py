import unittest
from kodowit import Core, Blad
class Objects(unittest.TestCase):
 def test_instances(self):
  out=[]; Core(out.append).run('klasa Licznik { zmienna n = 0 funkcja dodaj(x) { ja.n = ja.n + x zwroc ja.n } } zmienna a = Licznik() zmienna b = Licznik() wypisz(a.dodaj(5)) wypisz(b.n) a.n = 8 wypisz(a.n)'); self.assertEqual(out,[5,0,8])
 def test_fields(self):
  out=[]; Core(out.append).run('klasa A { zmienna x = 2 zmienna y = ja.x + 3 } zmienna a = A() wypisz(a.y)'); self.assertEqual(out,[5])
 def test_errors(self):
  for code in ['klasa A { zmienna x = 1 zmienna x = 2 }','klasa A {} zmienna a = A() a.x = 2','klasa A {} A(1)','zmienna a = 1 wypisz(a.x)']:
   with self.subTest(code=code), self.assertRaises(Blad): Core().run(code)
