import unittest
from kodowit import Env, Parser, Blad
class TestRC12(unittest.TestCase):
 def test_deep_scope(self):
  root=Env();root.d['x']=42;env=root
  for _ in range(1500):env=Env(env)
  self.assertEqual(env.get('x'),42)
  with self.assertRaises(Blad):env.get('missing')
 def test_shadow(self):
  root=Env();root.d['x']=1;child=Env(root);child.d['x']=2
  self.assertIs(child.owner('x'),child)
 def test_line(self):
  self.assertEqual(Parser('wypisz(1)\n\n').t[-1][2],3)
