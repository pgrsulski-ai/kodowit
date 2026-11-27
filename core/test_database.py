import unittest,tempfile
from kodowit import Core,Blad
class DatabaseTests(unittest.TestCase):
 def test_roundtrip(self):
  with tempfile.TemporaryDirectory() as d:
   out=[]; Core(out.append,root=d).run('baza_wykonaj("a.db","CREATE TABLE t (n TEXT)"); baza_wykonaj("a.db","INSERT INTO t VALUES (?)",["żółć"]); wypisz(baza_pobierz("a.db","SELECT n FROM t"))'); self.assertEqual(out,[[['żółć']]])
 def test_disabled(self):
  with self.assertRaises(Blad): Core().run('baza_pobierz("a.db","SELECT 1")')
 def test_escape(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(Blad): Core(root=d).run('baza_pobierz("../a.db","SELECT 1")')
 def test_attach(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(Blad): Core(root=d).run('baza_wykonaj("a.db","ATTACH DATABASE ? AS other",["other.db"])')
 def test_update_delete(self):
  with tempfile.TemporaryDirectory() as d:
   out=[]; Core(out.append,root=d).run('baza_wykonaj("a.db","CREATE TABLE t (n INTEGER)"); baza_wykonaj("a.db","INSERT INTO t VALUES (1)"); baza_wykonaj("a.db","UPDATE t SET n = ?",[2]); wypisz(baza_pobierz("a.db","SELECT n FROM t")); baza_wykonaj("a.db","DELETE FROM t"); wypisz(baza_pobierz("a.db","SELECT n FROM t"))'); self.assertEqual(out,[[[2]],[]])
 def test_read_write(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(Blad): Core(root=d).run('baza_pobierz("a.db","CREATE TABLE t(n)")')
