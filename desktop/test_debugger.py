import unittest
from debugger import debug
class DebugTests(unittest.TestCase):
 def test_step(self):
  events=[]; cmds=iter(['step','continue']); debug('zmienna x = 2\nwypisz(x)',set(),events.append,lambda:next(cmds)); self.assertEqual(events[1]['variables']['x'],'2'); self.assertEqual(events[2]['text'],'2')
 def test_break(self):
  events=[]; debug('zmienna x = 2\nwypisz(x)',{2},events.append,lambda:'continue'); self.assertEqual([e['line'] for e in events if e['type']=='pause'],[1,2])
 def test_stop(self):
  events=[]; debug('wypisz(1)',set(),events.append,lambda:'stop'); self.assertEqual(events[-1]['text'],'Przerwano')
