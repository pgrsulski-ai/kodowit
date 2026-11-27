import unittest
from kodowit import Core, Blad
class Test(unittest.TestCase):
 def check(self,s,w):
  out=[]; Core(out.append).run(s); self.assertEqual(out,w)
 def test_math(self): self.check('wypisz(2+3*4)',[14])
 def test_text(self): self.check('wypisz("Witaj " + "KODOWIT")',['Witaj KODOWIT'])
 def test_list(self): self.check('zmienna a = [2,3,4]; wypisz(a[1]); wypisz(suma(a))',[3,9])
 def test_loop(self): self.check('zmienna x=0; dla i w zakres(5) { x=x+i } wypisz(x)',[10])
 def test_while(self): self.check('zmienna x=3; dopóki x>0 { wypisz(x); x=x-1 }',[3,2,1])
 def test_recursion(self): self.check('funkcja f(n) { jeżeli n<=1 { zwróć 1 } zwróć n*f(n-1) } wypisz(f(5))',[120])
 def test_if(self): self.check('jeżeli fałsz { wypisz(0) } inaczej { wypisz(1) }',[1])
 def test_logic(self): self.check('wypisz(fałsz oraz brak); wypisz(prawda lub brak)',[False,True])
 def test_errors(self):
  for s in ['wypisz(brak)','wypisz(1/0)','jeżeli prawda {','zwróć 1','dopóki prawda {}']:
   with self.subTest(s=s),self.assertRaises(Blad): Core(limit=100).run(s)
if __name__=='__main__': unittest.main()
