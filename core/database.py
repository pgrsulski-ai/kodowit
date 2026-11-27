"""SQLite, enabled only with an explicit workspace."""
import sqlite3
from contextlib import closing
from system_io import SystemIO

class Database:
    def __init__(self, root):
        self.io = SystemIO(root)
    def query(self, name, sql, params=None, read=False):
        if not isinstance(sql,str) or len(sql)>100000: raise ValueError('Nieprawidłowe SQL')
        if params is None: params=[]
        if not isinstance(params,list): raise ValueError('Parametry muszą być listą')
        path=self.io.path(name)
        with closing(sqlite3.connect(path.as_uri()+"?mode=ro",uri=True,timeout=2) if read else sqlite3.connect(path,timeout=2)) as conn:
            conn.enable_load_extension(False)
            if read: conn.execute("PRAGMA query_only=ON")
            if hasattr(conn,"setlimit"): conn.setlimit(sqlite3.SQLITE_LIMIT_LENGTH,1000000)
            denied={sqlite3.SQLITE_ATTACH,sqlite3.SQLITE_DETACH,sqlite3.SQLITE_PRAGMA}
            writes={sqlite3.SQLITE_INSERT,sqlite3.SQLITE_UPDATE,sqlite3.SQLITE_DELETE,sqlite3.SQLITE_CREATE_TABLE,sqlite3.SQLITE_DROP_TABLE,sqlite3.SQLITE_ALTER_TABLE,sqlite3.SQLITE_CREATE_INDEX,sqlite3.SQLITE_DROP_INDEX}
            def authorize(action,a,b,c,d):
                if action in denied or (read and action in writes) or (action==sqlite3.SQLITE_FUNCTION and (b or '').lower()=='load_extension'): return sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK
            conn.set_authorizer(authorize)
            steps=[0]
            def progress():
                steps[0]+=1
                return int(steps[0]>1000)
            conn.set_progress_handler(progress,1000)
            with conn:
                cur=conn.execute(sql,params)
                if read:
                    if cur.description is None: raise ValueError('Oczekiwano zapytania zwracającego dane')
                    rows=cur.fetchmany(10001)
                    if len(rows)>10000: raise ValueError('Za dużo wyników')
                    return [list(row) for row in rows]
                if cur.description is not None: raise ValueError('Użyj baza_pobierz dla wyników')
                return cur.rowcount
    def bindings(self):
        return {'baza_wykonaj':self.query,'baza_pobierz':lambda n,s,p=None:self.query(n,s,p,True)}
