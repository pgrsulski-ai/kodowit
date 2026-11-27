import unittest, subprocess, sys, os
from unittest.mock import patch
from export_exe import launcher, build, CORE, Blad
class ExportTests(unittest.TestCase):
 def test_launcher(self):
  r=subprocess.run([sys.executable,'-c',launcher('wypisz("Zażółć")')],env={**os.environ,'PYTHONPATH':str(CORE)},capture_output=True,text=True)
  self.assertEqual(r.returncode,0); self.assertEqual(r.stdout.strip(),'Zażółć')
 def test_invalid(self):
  with self.assertRaises(Blad):launcher('wypisz(')
 def test_platform(self):
  with patch('export_exe.sys.platform','linux'):
   with self.assertRaisesRegex(RuntimeError,'Windows'):build('wypisz(1)','test.exe')
 def test_name(self):
  with self.assertRaises(ValueError):build('wypisz(1)','test.txt')
