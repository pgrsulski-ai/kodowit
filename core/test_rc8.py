import unittest,tempfile
from pathlib import Path
from database import Database
from stdlib import join,replace
import sqlite3
class RC8(unittest.TestCase):
 def test_read_no_create(self):
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(sqlite3.Error): Database(d).query('missing.db','SELECT 1',read=True)
   self.assertFalse(Path(d,'missing.db').exists())
 def test_read_no_write(self):
  with tempfile.TemporaryDirectory() as d:
   db=Database(d); db.query('a.db','CREATE TABLE t(x)')
   with self.assertRaises(sqlite3.Error): db.query('a.db','CREATE VIEW v AS SELECT 1',read=True)
   self.assertEqual(db.query('a.db','SELECT * FROM t',read=True),[])
 def test_join_limit(self):
  with self.assertRaises(ValueError): join('', ['x'*1000]*1001)
 def test_replace_limit(self):
  with self.assertRaises(ValueError): replace('a'*1000,'a','x'*1001)
