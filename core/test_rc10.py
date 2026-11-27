import unittest,sys
from limited_run import run,collect,MAX_OUTPUT_BYTES,MAX_ERROR_BYTES
import tempfile,os
@unittest.skipUnless(sys.platform.startswith('linux'),'Linux only')
class Limited(unittest.TestCase):
 def test_output(self): self.assertEqual(run('wypisz(42)').strip(),'42')
 def test_steps(self):
  with self.assertRaises(ValueError): run('dopóki prawda {}')
 def test_no_files(self):
  with self.assertRaises(ValueError): run('czytaj_plik("program.kodowit")')
 def test_source(self):
  with self.assertRaises(ValueError): run(' '*20001)

 def test_timeout_validation(self):
  for value in (0,-1,float('nan'),float('inf'),True,31,'3'):
   with self.subTest(value=value), self.assertRaises(ValueError): run('wypisz(42)',value)
 def test_polish_boolean(self): self.assertEqual(run('wypisz(prawda, fałsz)').strip(),'prawda fałsz')

 def test_process_output_caps(self):
  with tempfile.TemporaryDirectory() as d:
   for stream,cap in (('stdout',MAX_OUTPUT_BYTES),('stderr',MAX_ERROR_BYTES)):
    with self.subTest(stream=stream),self.assertRaisesRegex(ValueError,'limit danych'):
     collect([sys.executable,'-c',f'import sys; sys.{stream}.buffer.write(b"x"*{cap+1})'],d,os.environ.copy(),3)
 def test_process_timeout(self):
  with tempfile.TemporaryDirectory() as d,self.assertRaisesRegex(ValueError,'czas wykonania'):
   collect([sys.executable,'-c','import time; time.sleep(5)'],d,os.environ.copy(),0.1)
 def test_process_unicode(self):
  with tempfile.TemporaryDirectory() as d:
   self.assertEqual(collect([sys.executable,'-c','print("żółć")'],d,os.environ.copy(),3),(0,'żółć\n',''))
