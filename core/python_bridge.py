"""Explicit, limited Python interoperability for trusted programs."""
import importlib
from kodowit import Blad

EXPORTS = {'math': {'sqrt','factorial','hypot','gcd','log','sin','cos'}, 'statistics': {'mean','median','stdev'}, 'numpy': {'mean','median','std','sum','dot'}, 'json': {'dumps','loads'}}

def convert(value, depth=0):
    if depth > 20: raise Blad('Za głęboka struktura Python')
    if type(value) in (str,int,float,bool,type(None)): return value
    if type(value) in (list,tuple):
        if len(value)>10000: raise Blad('Za duża lista Python')
        return [convert(x,depth+1) for x in value]
    if type(value).__module__.startswith('numpy') and hasattr(value,'tolist'):
        return convert(value.tolist(),depth+1)
    raise Blad('Nieobsługiwany typ danych Python')

class PythonBridge:
    def __init__(self, allowed):
        self.allowed=set(allowed)
        if self.allowed-EXPORTS.keys(): raise Blad('Niedozwolony moduł Python')
    def call(self,module,name,*args):
        if not isinstance(module,str) or not isinstance(name,str) or module not in self.allowed or name not in EXPORTS[module]:
            raise Blad('Brak zezwolenia na funkcję Python')
        try:
            fn=getattr(importlib.import_module(module),name)
            return convert(fn(*(convert(a) for a in args)))
        except Blad: raise
        except Exception as e: raise Blad('Błąd biblioteki Python: '+str(e)) from None
