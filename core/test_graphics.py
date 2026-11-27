import unittest,os
from kodowit import Core,Blad
@unittest.skipUnless(os.environ.get('DISPLAY'),'Wymaga ekranu')
class GraphicsTests(unittest.TestCase):
 def test_canvas(self):
  c=Core(gui=True); c.run('okno("Test"); plotno("p"); zmienna a = prostokat("p",10,10,20,20,"red"); zmienna b = elipsa("p",15,15,20,20,"blue"); zmienna hit = kolizja("p",a,b); przesun_figure("p",b,100,0); zmienna miss = kolizja("p",a,b)')
  g=c.env.get('gui_start').__self__
  try: self.assertTrue(c.env.get('hit')); self.assertFalse(c.env.get('miss'))
  finally: g.root.destroy()
 def test_timer(self):
  c=Core(gui=True); c.run('zmienna wynik = 0; funkcja f() { wynik = 42; gui_zamknij() }; okno("Test"); po_czasie(10,f); gui_start()'); self.assertEqual(c.env.get('wynik'),42)
 def test_widgets(self):
  c=Core(gui=True); c.run('okno("Test"); pole_wyboru("a","Tak"); pasek_postepu("b"); postep_ustaw("b",75); zmienna v = wybrane("a")'); g=c.env.get('gui_start').__self__
  try: self.assertFalse(c.env.get('v')); self.assertEqual(float(g.widgets['b'][1]['value']),75)
  finally: g.root.destroy()
