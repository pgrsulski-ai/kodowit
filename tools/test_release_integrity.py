"""Testy kontroli wydania na kopii tymczasowej, bez modyfikowania źródeł."""
import shutil, subprocess, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
class Integrity(unittest.TestCase):
 def test_audit_and_tampering(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp)/'project'
   shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__','dist','node_modules'))
   def run(script):
    return subprocess.run([sys.executable,str(root/'tools'/script)],capture_output=True,text=True)
   self.assertEqual(run('audit_release.py').returncode,0)
   for name in ('compiler.js','compiler/lexer.js'):
    p=root/name; old=p.read_bytes(); p.write_bytes(old+b'\n// test\n')
    result=run('audit_release.py'); self.assertNotEqual(result.returncode,0); self.assertIn('Nieaktualny compiler.js',result.stderr)
    p.write_bytes(old)
   self.assertEqual(run('audit_release.py').returncode,0)
if __name__=='__main__': unittest.main()
