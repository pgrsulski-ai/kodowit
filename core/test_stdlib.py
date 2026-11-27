import unittest
from kodowit import Core, Blad
class Standard(unittest.TestCase):
 def check(self,s,w):
  out=[]; Core(out.append).run(s); self.assertEqual(out,w)
 def test_math(self): self.check('wypisz(pierwiastek(144)); wypisz(potega(2,3)); wypisz(sinus(0))',[12,8,0])
 def test_stats(self): self.check('wypisz(srednia([1,2,6])); wypisz(mediana([1,9,3]))',[3,3])
 def test_text(self): self.check('wypisz(wielkie_litery("żółć")); wypisz(polacz("-", podziel("a b")))',['ŻÓŁĆ','a-b'])
 def test_lists(self): self.check('wypisz(sortuj([3,1,2])); wypisz(odwroc([1,2]))',[[1,2,3],[2,1]])
 def test_dates(self): self.check('wypisz(dodaj_dni("2024-02-28",1)); wypisz(roznica_dni("2024-03-01","2024-02-28"))',['2024-02-29',2])
 def test_random(self): self.check('wypisz(losuj(7,7)); wypisz(losowa() < 1)',[7,True])
 def test_errors(self):
  for s in ['pierwiastek(-1)','srednia([])','dodaj_dni("x",1)']:
   with self.assertRaises(Blad): Core().run(s)
