import unittest, subprocess, sys
from pathlib import Path
from kodowit import Core, Blad
class Debug(unittest.TestCase):
 def test_line(self):
  with self.assertRaisesRegex(Blad,'Wiersz 3'): Core().run('zmienna x=1\n\n wypisz(brak)')
 def test_trace(self):
  events=[]; Core(out=lambda x:None,trace=lambda l,k:events.append((l,k))).run('zmienna x=1\nwypisz(x)'); self.assertEqual(events,[(1,'let'),(2,'expr')])
 def test_limit(self):
  with self.assertRaisesRegex(Blad,'limit'): Core(limit=20).run('dopoki prawda {}')
 def test_check(self):
  p=subprocess.run([sys.executable,str(Path(__file__).with_name('kodowit.py')),'--sprawdz','-c','wypisz(brak)'],capture_output=True,text=True); self.assertEqual(p.returncode,0); self.assertIn('Składnia poprawna',p.stdout)
 def test_size(self):
  with self.assertRaises(Blad): Core().run(' '*1000001)
