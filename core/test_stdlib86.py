import unittest
from kodowit import Core, Blad
class Extended(unittest.TestCase):
 def check(self,s,w):
  out=[]; Core(out.append).run(s); self.assertEqual(out,w)
 def test_math(self): self.check('wypisz(nwd(12,18)); wypisz(nww(4,6)); wypisz(podloga(2.9)); wypisz(sufit(2.1))',[6,12,2,3])
 def test_stats(self): self.check('wypisz(wariancja([1,3])); wypisz(odchylenie([1,3]))',[1,1])
 def test_text(self): self.check('wypisz(zaczyna_sie("żółć","ż")); wypisz(znajdz("abc","b"))',[True,1])
 def test_lists(self): self.check('wypisz(unikalne([2,1,2])); wypisz(sortuj_malejaco([1,3,2]))',[[2,1],[3,2,1]])
 def test_dates(self): self.check('wypisz(dzien_tygodnia("2024-01-01")); wypisz(rok("2024-01-01"))',[1,2024])
 def test_random(self): self.check('wypisz(wybierz_losowo([7])); wypisz(probka([8],1))',[7,[8]])
 def test_json(self): self.check('zmienna o = obiekt([["a",7]]); wypisz(json_wczytaj(json_zapisz(o))["a"]); wypisz(klucze(o))',[7,['a']])
 def test_errors(self):
  for s in ['json_wczytaj("NaN")','json_wczytaj(3)','probka([1],2)','obiekt([[1,2]])']:
   with self.assertRaises(Blad): Core().run(s)
