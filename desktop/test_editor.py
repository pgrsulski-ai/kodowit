import unittest
import tkinter as tk
from editor import spans,indentation
from studio import Studio,execute
class Tests(unittest.TestCase):
 def test_tokens(self):
  s='zmienna x = 2 // wypisz\nwypisz("jeżeli")'
  self.assertEqual([k for a,b,k in spans(s)],['keyword','number','comment','builtin','string'])
 def test_indent(self):
  self.assertEqual(indentation('    dla i w zakres(3) {'),'        ')
  self.assertEqual(indentation('    wypisz("{")'),'    ')
 def test_gui(self):
  root=tk.Tk()
  try:
   app=Studio(root); app.replace('zmienna x = 2\nwypisz(x)'); root.update(); app.editor_tools.refresh(); root.update()
   self.assertTrue(app.editor.tag_ranges('keyword')); self.assertTrue(app.editor_tools.gutter.find_all())
   app.editor.mark_set('insert','end-1c'); app.editor_tools.enter(); self.assertTrue(app.code().endswith('\n'))
  finally:root.destroy()
 def test_run(self):
  self.assertEqual(execute('wypisz(42)').stdout.strip(),'42')
if __name__=='__main__':unittest.main()
