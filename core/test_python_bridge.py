import unittest
from kodowit import Core, Blad
class BridgeTests(unittest.TestCase):
 def test_math(self):
  out=[]; Core(out.append,python_modules=['math']).run('wypisz(python_wywolaj("math","sqrt",144))'); self.assertEqual(out,[12.0])
 def test_statistics(self):
  out=[]; Core(out.append,python_modules=['statistics']).run('wypisz(python_wywolaj("statistics","mean",[2,4,6]))'); self.assertEqual(out,[4])
 def test_disabled(self):
  with self.assertRaises(Blad): Core().run('python_wywolaj("math","sqrt",4)')
 def test_denied(self):
  with self.assertRaises(Blad): Core(python_modules=['math']).run('python_wywolaj("math","__dict__")')
 def test_module(self):
  with self.assertRaises(Blad): Core(python_modules=['os'])
 def test_error(self):
  with self.assertRaises(Blad): Core(python_modules=['math']).run('python_wywolaj("math","sqrt",-1)')
