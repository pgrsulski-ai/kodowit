import unittest,tempfile,json
from pathlib import Path
from kodowit import Core,Blad,main
from registry import catalog
class Hardening(unittest.TestCase):
 def test_concat(self):
  with self.assertRaises(Blad): Core().run('zmienna x="a"*600000; wypisz(x+x)')
 def test_integer(self):
  with self.assertRaises(Blad): Core().run('zmienna x=2; dla i w zakres(20) { x=x*x }')
 def test_output(self):
  with self.assertRaises(Blad): Core(lambda x:None).run('wypisz("a"*600000); wypisz("a"*600000)')
 def test_limit(self):
  with self.assertRaises(Blad): Core(limit=0)
 def test_catalog(self):
  with tempfile.TemporaryDirectory() as d:
   for data in [[],{'schema':1,'packages':[{}]}]:
    Path(d,'index.json').write_text(json.dumps(data))
    with self.assertRaises(ValueError): catalog(d)
 def test_source(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d,'large.kodowit'); p.write_bytes(b' '*4000004)
   self.assertEqual(main([str(p)]),1)
