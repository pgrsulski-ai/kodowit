import unittest,tempfile,shutil
from pathlib import Path
from registry import catalog,install,HTTPSRedirectHandler
from urllib.request import Request
from kodowit import Core
class TestRegistry(unittest.TestCase):
 def test_redirect(self):
  handler=HTTPSRedirectHandler(); req=Request("https://example.org/index.json")
  for target in ("http://example.org/index.json", "ftp://example.org/index.json"):
   with self.assertRaises(ValueError): handler.redirect_request(req,None,302,"",{},target)
  self.assertEqual(handler.redirect_request(req,None,302,"",{},"https://example.net/index.json").full_url,"https://example.net/index.json")
 def test_install(self):
  with tempfile.TemporaryDirectory() as d:
   repo=Path(__file__).resolve().parents[1]/'registry'; self.assertEqual(len(catalog(str(repo))),1)
   install(str(repo),d,'matematyka','1.0.0'); out=[]; Core(out.append,packages=d).run('importuj_pakiet("matematyka") wypisz(podwoj(21))'); self.assertEqual(out,[42])
   with self.assertRaises(FileExistsError): install(str(repo),d,'matematyka','1.0.0')
 def test_hash(self):
  with tempfile.TemporaryDirectory() as d:
   repo=Path(d)/'repo'; shutil.copytree(Path(__file__).resolve().parents[1]/'registry',repo); (repo/'matematyka-1.0.0.kodowit').write_text('wypisz(1)')
   with self.assertRaises(ValueError): install(str(repo),Path(d)/'store','matematyka','1.0.0')
 def test_missing(self):
  with self.assertRaises(ValueError): install(str(Path(__file__).resolve().parents[1]/'registry'),'.','../x','1.0.0')
