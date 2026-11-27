import unittest, os
from kodowit import Core, Blad
from gui import GUI
class GUITests(unittest.TestCase):
 def test_disabled(self):
  with self.assertRaises(Blad): Core().run('okno("test")')
 @unittest.skipUnless(os.environ.get('DISPLAY'), 'Wymaga ekranu')
 def test_widgets(self):
  g=GUI(lambda f: g.set('wynik',g.get('imie')))
  g.window('Test'); g.add('imie','entry','Anna'); g.add('wynik','label',''); g.add('b','button','OK',('function',[],[],None))
  g.widgets['b'][1].invoke(); self.assertEqual(g.get('wynik'),'Anna'); g.root.after(10,g.close); g.run()
 @unittest.skipUnless(os.environ.get('DISPLAY'), 'Wymaga ekranu')
 def test_interpreter(self):
  c=Core(gui=True); c.run('funkcja f() { gui_ustaw("wynik", gui_odczytaj("imie")) }; okno("Test"); pole("imie","Ola"); etykieta("wynik",""); przycisk("b","OK",f)')
  g=c.env.get('gui_start').__self__; g.widgets['b'][1].invoke(); self.assertEqual(g.get('wynik'),'Ola'); g.root.after(10,g.close); g.run()
