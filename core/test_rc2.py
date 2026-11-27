import unittest, subprocess, sys, tempfile
from pathlib import Path
from kodowit import Core, Blad, LimitBlad, repl
class RC2(unittest.TestCase):
 def test_output_separators(self):
  c=Core(lambda *a:None); c.output_left=3
  with self.assertRaises(LimitBlad): c.output("a","b")
 def test_bool_limit(self):
  with self.assertRaises(Blad): Core(limit=True)
 def test_repl_large_number(self):
  lines=iter(["9"*5000, "wypisz(42)", ":wyjdz"]); out=[]; err=[]
  repl(lambda _:next(lines),out.append,err.append)
  self.assertEqual(out[-1],42); self.assertEqual(len(err),1)
 def test_native_bad_utf8(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"bad.kodowit"; p.write_bytes(b"\xff")
   r=subprocess.run([sys.executable,str(Path(__file__).with_name("native.py")),str(p),"-o",str(Path(d)/"out"),"--c"],capture_output=True)
   self.assertEqual(r.returncode,1); self.assertNotIn(b"Traceback",r.stderr)
