import unittest,subprocess,sys,shutil
from eksport import eksport
from kodowit import Core,Blad
class ExportTest(unittest.TestCase):
 def test_outputs(self):
  for code in ['wypisz((2+3)*4)','zmienna x = 0\ndopóki x < 5 { x = x+1 }\nwypisz(x)','zmienna żółć = 7\nwypisz(żółć*2)', 'funkcja podwoj(x) { zwróć x*2 } wypisz(podwoj(6))', 'jeżeli 2 < 3 { wypisz(7) } inaczej { wypisz(8) }', 'zmienna lista = [2,4,6] wypisz(lista[-1])', 'wypisz("Witaj")']:
   out=[];Core(out=out.append).run(code);expected='\n'.join(map(str,out))
   for target,cmd in [('python',[sys.executable,'-c']),('javascript',['node','-e'])]:
    if not shutil.which(cmd[0]): self.skipTest('Brak środowiska docelowego')
    self.assertEqual(subprocess.check_output(cmd+[eksport(code,target)],text=True,timeout=3).strip(),expected)
 def test_reject(self):
  for code in ['wypisz(2/3)','klasa A {}','dopóki 1 { zmienna x = 1 }']:
   with self.assertRaises(Blad): eksport(code,'python')
