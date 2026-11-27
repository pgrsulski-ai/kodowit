import unittest, subprocess, sys
from pathlib import Path
from kodowit import repl
P=Path(__file__).with_name('kodowit.py')
class CLI(unittest.TestCase):
 def call(self,*args): return subprocess.run([sys.executable,str(P),*args],capture_output=True,text=True)
 def test_version(self): self.assertIn('1.0.0',self.call('--wersja').stdout)
 def test_code(self): self.assertEqual(self.call('-c','wypisz(42)').stdout.strip(),'42')
 def test_file(self): self.assertEqual(self.call(str(P.with_name('demo.kodowit'))).returncode,0)
 def test_error(self): self.assertEqual(self.call('-c','wypisz(brak)').returncode,1)
 def test_repl(self):
  lines=iter(['zmienna x=2','funkcja f(n) {','zwróć n*x','}','wypisz(f(3))','wypisz(brak)','wypisz(x)',':wyjdz']); out=[]; err=[]
  repl(lambda _:next(lines),out.append,err.append)
  self.assertEqual(out[1:],[6,2]); self.assertEqual(len(err),1)
 def test_reset(self):
  lines=iter(['zmienna x=2',':reset','wypisz(x)',':wyjdz']); err=[]; repl(lambda _:next(lines),lambda _:None,err.append); self.assertEqual(len(err),1)
if __name__=='__main__': unittest.main()
