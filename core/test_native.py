import unittest, tempfile, pathlib, subprocess, shutil
from native import translate
from kodowit import Blad
class NativeTests(unittest.TestCase):
 def test_reject(self):
  with self.assertRaises(Blad): translate('wypisz("tekst")')
 def test_unknown(self):
  with self.assertRaises(Blad): translate('wypisz(x)')
 @unittest.skipUnless(shutil.which('gcc'),'brak gcc')
 def test_binary(self):
  with tempfile.TemporaryDirectory() as d:
   c=pathlib.Path(d)/'a.c'; e=pathlib.Path(d)/'a'; c.write_text(translate('zmienna a = 20\na = a + 1\nwypisz(a * 2)'))
   subprocess.run(['gcc',str(c),'-o',str(e)],check=True)
   self.assertEqual(subprocess.check_output([str(e)],text=True).strip(),'42')
