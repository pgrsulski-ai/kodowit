"""KODOWIT Core 1.0.1: parser and bounded tree-walking interpreter."""
import sqlite3
import re, json, sys, operator
OPS={'+':operator.add,'-':operator.sub,'*':operator.mul,'/':operator.truediv,'%':operator.mod,'==':operator.eq,'!=':operator.ne,'<':operator.lt,'>':operator.gt,'<=':operator.le,'>=':operator.ge}
class Blad(Exception): pass
class LimitBlad(Blad): pass
RUNTIME_ERRORS=(TypeError,ValueError,ZeroDivisionError,IndexError,KeyError,OverflowError,OSError,UnicodeError,sqlite3.Error)
ALIASES={'bezwzględna':'bezwzgledna','podłoga':'podloga','średnia':'srednia','jeżeli':'jezeli','jeśli':'jezeli','jesli':'jezeli','inaczej':'inaczej','zwróć':'zwroc','fałsz':'falsz','długość':'dlugosc','dopóki':'dopoki','dziedzicz':'dziedziczy','spróbuj':'sprobuj','zgłoś':'zglos'}
PAT=re.compile(r'(?P<space>\s+|//[^\n]*|\#[^\n]*)|(?P<string>"(?:\\.|[^"\\])*" )|(?P<num>\d+(?:\.\d+)?)|(?P<id>[^\W\d]\w*)|(?P<op>==|!=|<=|>=|[{}()\[\],.;=+*/%<>!-])'.replace('*" )','*" )').replace('" )','")'))
class Statement(tuple):
 def __new__(cls, value, line):
  obj=super().__new__(cls,value); obj.line=line; return obj
class Parser:
 def __init__(self,s):
  if len(s)>1000000: raise Blad("Kod przekracza 1 MB znaków")
  self.t=[]; self.i=0; p=0; line=1
  while p<len(s):
   m=PAT.match(s,p)
   if not m: raise Blad(f'Nieznany znak w wierszu {s.count(chr(10),0,p)+1}: {s[p]}')
   k=m.lastgroup; v=m.group(); p=m.end(); token_line=line; line+=v.count('\n')
   if k!='space': self.t.append((k,ALIASES.get(v,v) if k=='id' else v,token_line))
  self.t.append(('end','<koniec>',line))
 def peek(self): return self.t[self.i][1]
 def take(self,v=None):
  t=self.t[self.i]
  if t[0]=='end' or (v is not None and t[1]!=v): raise Blad(f'Wiersz {t[2]}: oczekiwano {v or "wyrażenia"}, jest {t[1]}')
  self.i+=1; return t
 def accept(self,v):
  if self.peek()==v: self.take(); return True
  return False
 def name(self):
  k,v,l=self.take()
  if k!='id': raise Blad(f'Wiersz {l}: oczekiwano nazwy')
  return v
 def seq(self,end='<koniec>'):
  a=[]
  while self.peek()!=end:
   if self.accept(';'): continue
   line=self.t[self.i][2]; a.append(Statement(self.stmt(),line))
  return a
 def block(self):
  self.take('{'); a=self.seq('}'); self.take('}'); return a
 def args(self,end,fn):
  a=[]
  if self.peek()!=end:
   a.append(fn())
   while self.accept(','): a.append(fn())
  self.take(end); return a
 def stmt(self):
  v=self.peek()
  if v=='klasa':
   self.take(); n=self.name(); base=self.name() if self.accept('dziedziczy') else None; body=self.block()
   if any(x[0] not in ('let','fn') for x in body): raise Blad('Klasa zawiera tylko pola i metody')
   names=[x[1] for x in body]
   if len(set(names))!=len(names) or 'ja' in names: raise Blad('Powtórzona lub zastrzeżona nazwa w klasie')
   return ('class',n,body,base)
  if v=='sprobuj':
   self.take(); body=self.block(); self.take('przechwyc'); self.take('('); name=self.name(); self.take(')'); return ('try',body,name,self.block())
  if v=='zglos': self.take(); return ('raise',self.expr())
  if v=='funkcja':
   self.take(); n=self.name(); self.take('('); a=self.args(')',self.name); return ('fn',n,a,self.block())
  if v=='jezeli':
   self.take(); e=self.expr(); a=self.block(); b=self.block() if self.accept('inaczej') else []; return ('if',e,a,b)
  if v=='dopoki': self.take(); return ('while',self.expr(),self.block())
  if v=='dla':
   self.take(); n=self.name(); self.take('w'); return ('for',n,self.expr(),self.block())
  if v=='zwroc': self.take(); return ('return',self.expr())
  if v in ('zmienna','stan'):
   self.take(); n=self.name(); self.take('='); return ('let',n,self.expr())
  if self.t[self.i][0]=='id' and self.t[self.i+1][1]=='=':
   n=self.name(); self.take('='); return ('set',n,self.expr())
  a=self.expr()
  if self.accept('='):
   if a[0]!='member': raise Blad('Nieprawidłowy cel przypisania')
   return ('member_set',a[1],a[2],self.expr())
  return ('expr',a)
 def expr(self,minp=0):
  k,v,l=self.take()
  if v in ('-','nie','!'): a=('un',v,self.expr(7))
  elif v=='(': a=self.expr(); self.take(')')
  elif v=='[': a=('list',self.args(']',self.expr))
  elif k=='num': a=('lit',float(v) if '.' in v else int(v))
  elif k=='string': a=('lit',json.loads(v))
  elif v in ('prawda','falsz','nic'): a=('lit',{'prawda':True,'falsz':False,'nic':None}[v])
  elif k=='id': a=('var',v)
  else: raise Blad(f'Wiersz {l}: niepoprawne wyrażenie {v}')
  prec={'lub':1,'oraz':2,'==':3,'!=':3,'<':4,'>':4,'<=':4,'>=':4,'+':5,'-':5,'*':6,'/':6,'%':6}
  while True:
   v=self.peek()
   if v=='(':
    self.take(); a=('call',a,self.args(')',self.expr)); continue
   if v=='.':
    self.take(); a=('member',a,self.name()); continue
   if v=='[':
    self.take(); b=self.expr(); self.take(']'); a=('idx',a,b); continue
   p=prec.get(v,0)
   if p<=minp: break
   self.take(); a=('bin',v,a,self.expr(p))
  return a
class Return(Exception):
 def __init__(self,v): self.v=v
class Env:
 def __init__(self,parent=None): self.d={}; self.parent=parent
 def owner(self,n):
  env=self
  while env is not None:
   if n in env.d: return env
   env=env.parent
  raise Blad('Nieznana nazwa: '+n)
 def get(self,n): return self.owner(n).d[n]
class KodowitClass:
 def __init__(self,name,body,env,base=None): self.name=name; self.body=body; self.env=env; self.base=base
 def __repr__(self): return '<klasa '+self.name+'>'
class KodowitObject:
 def __init__(self,cls): self.cls=cls; self.fields={}; self.methods={}
 def __repr__(self): return '<obiekt '+self.cls.name+'>'
class Core:
 def __init__(self,out=print,limit=100000, root=None, network=False, gui=False, python_modules=(), packages=None, trace=None, debug=None):
  if type(limit) is not int or not 1<=limit<=10000000: raise Blad('Nieprawidłowy limit kroków')
  self.trace=trace; self.debug=debug; self.line=None
  self.out=out; self.output_left=1000000; self.limit=limit; self.left=limit; self.env=Env(); self.env.d.update({'wypisz':self.output,'zakres':self.range,'zakres_otwarty':self.range,'dlugosc':len,'liczba':float,'tekst':str,'calkowita':int,'suma':sum})
  from stdlib import bindings
  self.env.d.update(bindings())
  from concurrent.futures import ThreadPoolExecutor
  self.jobs={}; self.job_count=0; self.pool=None
  def start(source):
   if not isinstance(source,str) or len(source)>100000: raise Blad('Nieprawidłowy kod zadania')
   if self.job_count>=16: raise Blad('Limit zadań')
   if self.pool is None: self.pool=ThreadPoolExecutor(max_workers=4)
   self.job_count+=1
   def work():
    lines=[]
    child=Core(lambda *a: lines.append(' '.join(map(str,a))),limit=min(self.limit,100000))
    # Zadania nie mogą uruchamiać kolejnych zadań.
    for key in ('zadanie','oczekuj','gotowe'): child.env.d.pop(key,None)
    child.run(source)
    return '\n'.join(lines)
   self.jobs[self.job_count]=self.pool.submit(work)
   return self.job_count
  def job(n):
   if type(n)!=int or n not in self.jobs: raise Blad('Nieznane zadanie')
   return self.jobs[n]
  self.env.d.update({'zadanie':start,'oczekuj':lambda n:job(n).result(),'gotowe':lambda n:job(n).done()})
  if root is not None:
   from pathlib import Path
   base=Path(root).resolve(); modules={}; active_modules=set(); builtins=self.env
   def module(name):
    if not isinstance(name,str) or not re.fullmatch(r'[\w-]+(?:/[\w-]+)*\.kodowit',name): raise Blad('Nieprawidłowa ścieżka modułu')
    path=(base/name).resolve()
    if not path.is_relative_to(base): raise Blad('Moduł poza katalogiem')
    if path in active_modules: raise Blad('Cykliczny import modułu')
    if path in modules: return modules[path]
    if len(modules)+len(active_modules)>=64: raise Blad('Limit modułów')
    active_modules.add(path)
    try:
     with path.open('rb') as f: data=f.read(400001)
     if len(data)>400000: raise Blad('Moduł za duży')
     local=Env(builtins); self.block(Parser(data.decode('utf-8-sig')).seq(),local)
     obj=KodowitObject(KodowitClass(name,[],local)); obj.fields={k:v for k,v in local.d.items() if not k.startswith('_')}
     modules[path]=obj; return obj
    finally: active_modules.remove(path)
   self.env.d['importuj_modul']=module
  if packages is not None:
   from packages import Packages
   store=Packages(packages); loaded=set(); active=set()
   def load(name):
    if name in active: raise Blad('Cykliczny import pakietu')
    if name in loaded: return
    source=store.read(name); active.add(name)
    try:
     self.block(Parser(source).seq(),self.env)
     loaded.add(name)
    finally: active.remove(name)
   self.env.d['importuj_pakiet']=load
  if root is not None:
   from system_io import SystemIO
   self.env.d.update(SystemIO(root).bindings())
   from database import Database
   self.env.d.update(Database(root).bindings())
  if network:
   from http_api import API
   api=API()
   def route(method,path,fn):
    if not isinstance(fn,tuple) or fn[0]!='function' or len(fn[1])!=1: raise Blad('Trasa wymaga funkcji z jednym parametrem')
    def handler(payload):
     self.left=self.limit
     local=Env(fn[3]); local.d[fn[1][0]]=payload
     try: self.block(fn[2],local)
     except Return as r: return r.v
    api.route(method,path,None); api.routes[method,path]=handler
   self.env.d.update({'api_trasa':route,'api_start':api.serve})
  if python_modules:
   from python_bridge import PythonBridge
   self.env.d["python_wywolaj"]=PythonBridge(python_modules).call
  if gui:
   from gui import GUI
   def invoke(fn):
    self.left=self.limit
    try: self.block(fn[2],Env(fn[3]))
    except Return: pass
   self.env.d.update(GUI(invoke).bindings())
 def output(self,*args):
  size=sum(len(str(x)) for x in args)+max(0,len(args)-1)+1
  if size>self.output_left: raise LimitBlad('Przekroczono limit wyjścia')
  self.output_left-=size
  return self.out(*args)
 def range(self,*a):
  r=range(*a)
  if len(r)>100000: raise Blad('Za duży zakres')
  return r
 def tick(self):
  self.left-=1
  if self.left<0: raise LimitBlad('Przekroczono limit kroków')
 def run(self,s):
  self.left=self.limit; self.output_left=1000000; self.line=None
  try: self.block(Parser(s).seq(),self.env)
  except Blad as e:
   if self.line is not None: raise Blad(f"Wiersz {self.line}: {e}") from None
   raise
  except Return: raise Blad('zwróć poza funkcją') from None
  except (TypeError,ValueError,ZeroDivisionError,IndexError,KeyError,OverflowError,RecursionError,OSError,UnicodeError,sqlite3.Error) as e: raise Blad((f'Wiersz {self.line}: ' if self.line else '')+'Błąd wykonania: '+str(e)) from None
  finally:
   if self.pool is not None: self.pool.shutdown(wait=True); self.pool=None
   self.jobs.clear(); self.job_count=0
 def block(self,ss,e):
  for s in ss:
   self.line=getattr(s,"line",None); self.tick(); k,*a=s
   if self.trace: self.trace(self.line,k)
   if self.debug: self.debug(self.line,k,e)
   if k=='let': e.d[a[0]]=self.val(a[1],e)
   elif k=='set': e.owner(a[0]).d[a[0]]=self.val(a[1],e)
   elif k=='expr': self.val(a[0],e)
   elif k=='return': raise Return(self.val(a[0],e))
   elif k=='if': self.block(a[1] if self.val(a[0],e) else a[2],e)
   elif k=='while':
    while self.val(a[0],e): self.tick(); self.block(a[1],e)
   elif k=='for':
    for x in self.val(a[1],e): self.tick(); e.d[a[0]]=x; self.block(a[2],e)
   elif k=='class':
    base=e.get(a[2]) if a[2] else None
    if a[2] and not isinstance(base,KodowitClass): raise Blad('Oczekiwano klasy bazowej')
    e.d[a[0]]=KodowitClass(a[0],a[1],e,base)
   elif k=='raise': raise Blad(str(self.val(a[0],e)))
   elif k=='try':
    try: self.block(a[0],e)
    except LimitBlad: raise
    except (Blad,*RUNTIME_ERRORS) as err:
     local=Env(e); local.d[a[1]]=str(err); self.block(a[2],local)
   elif k=='member_set':
    obj=self.val(a[0],e)
    if not isinstance(obj,KodowitObject) or a[1] not in obj.fields: raise Blad('Nieznane pole: '+a[1])
    obj.fields[a[1]]=self.val(a[2],e)
   elif k=='fn': e.d[a[0]]=('function',a[1],a[2],e)
 def val(self,s,e):
  self.tick(); k,*a=s
  if k=='lit': return a[0]
  if k=='var': return e.get(a[0])
  if k=='list': return [self.val(x,e) for x in a[0]]
  if k=='member':
   obj=self.val(a[0],e); n=a[1]
   if not isinstance(obj,KodowitObject): raise Blad('Oczekiwano obiektu KODOWIT')
   if n in obj.fields: return obj.fields[n]
   if n in obj.methods: return obj.methods[n]
   raise Blad('Nieznany element: '+n)
  if k=='idx': return self.val(a[0],e)[self.val(a[1],e)]
  if k=='un':
   x=self.val(a[1],e); return -x if a[0]=='-' else not x
  if k=='bin':
   op,x,y=a; x=self.val(x,e)
   if op=='oraz': return bool(x) and bool(self.val(y,e))
   if op=='lub': return bool(x) or bool(self.val(y,e))
   y=self.val(y,e)
   if op=='*' and ((isinstance(x,(str,list)) and isinstance(y,int) and len(x)*y>1000000) or (isinstance(y,(str,list)) and isinstance(x,int) and len(y)*x>1000000)): raise Blad('Za duży wynik')
   if op=='+' and isinstance(x,(str,list)) and isinstance(y,type(x)) and len(x)+len(y)>1000000: raise Blad('Za duży wynik')
   if op=='*' and type(x)==type(y)==int and x.bit_length()+y.bit_length()>14000: raise Blad('Za duża liczba')
   result=OPS[op](x,y)
   if isinstance(result,int) and result.bit_length()>14000: raise Blad('Za duża liczba')
   return result
  if k=='call':
   f=self.val(a[0],e); args=[self.val(x,e) for x in a[1]]
   if isinstance(f,KodowitClass):
    obj=KodowitObject(f); chain=[]; cls=f
    while cls is not None:
     self.tick(); chain.append(cls); cls=cls.base
    scopes=[]
    for cls in reversed(chain):
     local=Env(cls.env); local.d['ja']=obj; scopes.append((cls,local))
     for item in cls.body:
      self.tick()
      if item[0]=='fn': obj.methods[item[1]]=('function',item[2],item[3],local)
    for cls,local in scopes:
     for item in cls.body:
      self.tick()
      if item[0]=='let': obj.fields[item[1]]=self.val(item[2],local)
    if 'konstruktor' in obj.methods:
     self.invoke_function(obj.methods['konstruktor'],args)
    elif args: raise Blad('Klasa nie przyjmuje argumentów')
    return obj
   if callable(f): return f(*args)
   if isinstance(f,tuple) and len(f)==4 and f[0]=='function':
    return self.invoke_function(f,args)
   raise Blad('To nie jest funkcja')
 def invoke_function(self,f,args):
  _,names,body,parent=f
  if len(names)!=len(args): raise Blad('Nieprawidłowa liczba argumentów')
  local=Env(parent); local.d.update(zip(names,args))
  try: self.block(body,local)
  except Return as r: return r.v
  return None
def repl(read=input, out=print, err=None, root=None, network=False, gui=False, python_modules=(), packages=None):
 if err is None: err=lambda s: print(s,file=sys.stderr)
 core=Core(out,root=root,network=network,gui=gui,python_modules=python_modules,packages=packages); lines=[]
 out('KODOWIT Core 1.0.1 — :pomoc, :wyjdz')
 while True:
  try: line=read('... ' if lines else 'kodowit> ')
  except EOFError: break
  except KeyboardInterrupt: lines=[]; out('Przerwano'); continue
  if line.strip() in (':wyjdz',':wyjdź'): break
  if line.strip()==':anuluj': lines=[]; continue
  if line.strip()==':pomoc': out(':wyjdz — koniec; :anuluj — porzuć blok; :reset — wyczyść zmienne'); continue
  if line.strip()==':reset': core=Core(out,root=root,network=network,gui=gui,python_modules=python_modules,packages=packages); lines=[]; continue
  lines.append(line); source='\n'.join(lines)
  try:
   parser=Parser(source)
   stack=[]
   for kind,value,_ in parser.t:
    if kind!='op': continue
    if value in ('{','(','['): stack.append(value)
    elif value in ('}',')',']'):
     if not stack or stack.pop()!={'}':'{',')':'(',']':'['}[value]: raise Blad('Niezgodne nawiasy')
   if stack: continue
   core.run(source)
  except (Blad,ValueError,RecursionError) as e: err('KODOWIT: '+str(e))
  except KeyboardInterrupt: out('Przerwano')
  lines=[]
 return 0

def main(argv=None):
 import argparse
 from pathlib import Path
 parser=argparse.ArgumentParser(description='KODOWIT Core — uruchamianie programów i konsola')
 parser.add_argument('plik',nargs='?',help='plik .kodowit')
 parser.add_argument('-c','--kod',help='wykonaj kod z argumentu')
 parser.add_argument('--wersja','--version',action='version',version='KODOWIT Core 1.0.1')
 parser.add_argument('--pliki', metavar='KATALOG', help='włącz dostęp do plików w podanym katalogu')
 parser.add_argument('--siec',action='store_true',help='włącz lokalny serwer HTTP')
 parser.add_argument('--gui',action='store_true',help='włącz lokalne okna')
 parser.add_argument("--python",action="append",default=[],metavar="MODUL",help="zezwól na wybrane funkcje modułu Python")
 parser.add_argument('--pakiety',metavar='KATALOG',help='włącz lokalne pakiety')
 parser.add_argument('--limitowany',action='store_true',help='oddzielny proces z limitami Linux, bez dodatkowych uprawnień')
 parser.add_argument('--sprawdz',action='store_true',help='sprawdź składnię bez wykonywania')
 parser.add_argument('--sledz',action='store_true',help='wypisz wykonywane instrukcje na stderr')
 parser.add_argument('--limit',type=int,default=100000,help='limit kroków wykonania')
 parser.add_argument('--pakiet',nargs='+',help='instaluj NAZWA PLIK | lista | usun NAZWA')
 args=parser.parse_args(argv)
 if args.limitowany and (not (args.plik or args.kod is not None) or args.pliki or args.siec or args.gui or args.python or args.pakiety or args.pakiet or args.sprawdz or args.sledz or args.limit!=100000): parser.error('Tryb limitowany wymaga kodu lub pliku i nie obsługuje dodatkowych uprawnień ani opcji wykonania')
 if args.limit<1 or args.limit>10000000: parser.error("Limit musi wynosić 1–10000000")
 if (args.sprawdz or args.sledz or args.limit!=100000) and not (args.plik or args.kod is not None): parser.error("Wskaż kod lub plik")
 if args.plik and args.kod is not None: parser.error('Wybierz plik albo --kod')
 try:
  if args.pakiet:
   from packages import Packages
   if not args.pakiety: raise Blad('Wskaż --pakiety KATALOG')
   store=Packages(args.pakiety); cmd=args.pakiet
   if len(cmd)==3 and cmd[0]=='instaluj': store.install(cmd[1],cmd[2])
   elif cmd==['lista']: print('\n'.join(store.list()))
   elif len(cmd)==2 and cmd[0]=='usun': store.remove(cmd[1])
   else: raise Blad('Nieprawidłowe polecenie pakietu')
   return 0
  if not args.plik and args.kod is None: return repl(root=args.pliki,network=args.siec,gui=args.gui,python_modules=args.python,packages=args.pakiety)
  if args.kod is not None: source=args.kod
  else:
   with Path(args.plik).open('rb') as f: data=f.read(4000004)
   if len(data)>4000003: raise Blad('Plik źródłowy za duży')
   source=data.decode('utf-8-sig')
  if args.limitowany:
   from limited_run import run
   print(run(source),end=""); return 0
  if args.sprawdz:
   Parser(source).seq(); print('Składnia poprawna'); return 0
  trace=(lambda line,kind: print(f'Ślad: wiersz {line}, {kind}',file=sys.stderr)) if args.sledz else None
  Core(out=lambda *a: print(*('prawda' if x is True else 'fałsz' if x is False else x for x in a)),root=args.pliki,network=args.siec,gui=args.gui,python_modules=args.python,packages=args.pakiety,limit=args.limit,trace=trace).run(source)
  return 0
 except (Blad,OSError,UnicodeError,ValueError,RecursionError) as e: print('KODOWIT: '+str(e),file=sys.stderr); return 1
 except KeyboardInterrupt: return 130

if __name__=='__main__': sys.exit(main())
