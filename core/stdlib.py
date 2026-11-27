"""Standard library for KODOWIT Core 6.3."""
import math
import random
import statistics
from datetime import datetime, date, timedelta

def join(separator, values):
    if not isinstance(separator,str) or not isinstance(values,(list,tuple)) or not all(isinstance(v,str) for v in values): raise ValueError('Oczekiwano separatora i listy tekstów')
    if sum(map(len,values))+max(0,len(values)-1)*len(separator)>1000000: raise ValueError('Za duży wynik')
    return separator.join(values)

def replace(value, old, new, count=-1):
    if not all(isinstance(v,str) for v in (value,old,new)): raise ValueError('Oczekiwano tekstu')
    n=value.count(old)
    if count>=0: n=min(n,count)
    if len(value)+n*(len(new)-len(old))>1000000: raise ValueError('Za duży wynik')
    return value.replace(old,new,count)

def date_add(value, days):
    return (date.fromisoformat(value) + timedelta(days=days)).isoformat()

def bindings():
    return {
        'pi': math.pi, 'euler': math.e,
        'pierwiastek': math.sqrt, 'sinus': math.sin, 'cosinus': math.cos,
        'logarytm': math.log, 'potega': math.pow, 'zaokraglij': round,
        'bezwzgledna': abs, 'minimum': min, 'maksimum': max,
        'srednia': statistics.mean, 'mediana': statistics.median,
        'sortuj': sorted, 'odwroc': lambda x: x[::-1],
        'male_litery': str.lower, 'wielkie_litery': str.upper,
        'przytnij': str.strip, 'podziel': str.split, 'polacz': join,
        'zamien': replace, 'zawiera': lambda x,y: y in x,
        'losuj': random.randint, 'losowa': random.random,
        'dzisiaj': lambda: date.today().isoformat(),
        'teraz': lambda: datetime.now().astimezone().isoformat(timespec='seconds'),
        'dodaj_dni': date_add,
        'roznica_dni': lambda a,b: (date.fromisoformat(a)-date.fromisoformat(b)).days,
    }

# 8.6: additional functions, using only the Python standard library.
import json

def json_read(value):
    if not isinstance(value,str): raise ValueError("Oczekiwano tekstu JSON")
    if len(value)>1000000: raise ValueError('JSON jest za duży')
    return json.loads(value, parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nieprawidłowa liczba JSON')))

def json_write(value):
    result=json.dumps(value, ensure_ascii=False, allow_nan=False)
    if len(result)>1000000: raise ValueError('JSON jest za duży')
    return result

def object_from_pairs(pairs):
    if not all(isinstance(p,list) and len(p)==2 and isinstance(p[0],str) for p in pairs):
        raise ValueError('Oczekiwano listy par [klucz, wartość]')
    return dict(pairs)

def sample(values, count):
    if not 0<=count<=min(len(values),100000): raise ValueError('Nieprawidłowa liczba elementów')
    return random.sample(values,count)

_original_bindings=bindings
def bindings():
    result=_original_bindings()
    result.update({
        'podloga':math.floor, 'sufit':math.ceil, 'tangens':math.tan,
        'nwd':math.gcd, 'nww':math.lcm, 'odchylenie':statistics.pstdev,
        'wariancja':statistics.pvariance, 'licz_wystapienia':lambda x,y:x.count(y),
        'zaczyna_sie':str.startswith, 'konczy_sie':str.endswith,
        'znajdz':str.find, 'sortuj_malejaco':lambda x:sorted(x,reverse=True),
        'unikalne':lambda x:list(dict.fromkeys(x)), 'wybierz_losowo':random.choice,
        'probka':sample, 'rok':lambda x:date.fromisoformat(x).year,
        'miesiac':lambda x:date.fromisoformat(x).month,
        'dzien':lambda x:date.fromisoformat(x).day,
        'dzien_tygodnia':lambda x:date.fromisoformat(x).isoweekday(),
        'json_wczytaj':json_read, 'json_zapisz':json_write,
        'obiekt':object_from_pairs, 'klucze':lambda x:list(x.keys()) if isinstance(x,dict) else [],
    })
    return result
