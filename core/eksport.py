"""Eksperymentalny eksport przenośnego podzbioru liczbowego KODOWIT."""
import argparse,json
from pathlib import Path
from kodowit import Parser, Blad

def eksport(source, target):
 if target not in ('python','javascript'): raise Blad('Nieznany język docelowy')
 js=target=='javascript'
 ast=Parser(source).seq()
 functions={a[1]:len(a[2]) for a in ast if a[0]=='fn'}
 def name(n): return 'k_'+n
 def expr(a):
  k,*v=a
  if k=='lit' and type(v[0]) is int and abs(v[0])<=1000000: return str(v[0])
  if k=='lit' and isinstance(v[0],str): return json.dumps(v[0],ensure_ascii=False)
  if k=='list': return '['+', '.join(map(expr,v[0]))+']'
  if k=='idx': return '__kw_index('+expr(v[0])+', '+expr(v[1])+')' if js else '('+expr(v[0])+')['+expr(v[1])+']'
  if k=='call' and v[0][0]=='var' and functions.get(v[0][1])==len(v[1]): return name(v[0][1])+'('+', '.join(map(expr,v[1]))+')'
  if k=='var': return name(v[0])
  if k=='un' and v[0] in ('nie','!'): return '(!__kw_truth('+expr(v[1])+'))' if js else '(not '+expr(v[1])+')'
  if k=='bin' and v[0] in ('oraz','lub'):
   op=('&&' if v[0]=='oraz' else '||') if js else ('and' if v[0]=='oraz' else 'or'); f='__kw_truth' if js else 'bool'; return '('+f+'('+expr(v[1])+') '+op+' '+f+'('+expr(v[2])+'))'
  if k=='bin' and js and v[0] in ('==','!='): return '('+('!' if v[0]=='!=' else '')+'__kw_equal('+expr(v[1])+', '+expr(v[2])+'))'
  if k=='un' and v[0]=='-': return '(-'+expr(v[1])+')'
  if k=='bin' and v[0] in ('+','-','*','<','>','<=','>=','==','!='):
   op={'==':'===','!=':'!=='}.get(v[0],v[0]) if js else v[0]
   return '('+expr(v[1])+' '+op+' '+expr(v[2])+')'
  raise Blad('Eksport nie obsługuje wyrażenia: '+k)
 def block(nodes, depth=0, local=None, nested=False):
  lines=[]; p='    '*depth
  for k,*v in nodes:
   if k=='let' and (nested or local is not None and v[0] in local): raise Blad('Deklaracja w bloku lub ponowna deklaracja')
   if k=='let' and local is not None: local.add(v[0])
   if k=='set' and local is not None and v[0] not in local: raise Blad('Zmiana zmiennej zewnętrznej')
   if k in ('let','set'): lines.append(p+('let ' if js and k=='let' else '')+name(v[0])+' = '+expr(v[1])+(';' if js else ''))
   elif k=='expr' and v[0][0]=='call' and v[0][1]==('var','wypisz') and len(v[0][2])==1:
    lines.append(p+('console.log' if js else 'print')+'('+expr(v[0][2][0])+')'+(';' if js else ''))
   elif k=='return' and local is not None: lines.append(p+'return '+expr(v[0])+(';' if js else ''))
   elif k=='fn' and local is None and not nested:
    lines.append(p+('function ' if js else 'def ')+name(v[0])+'('+', '.join(map(name,v[1]))+(') {' if js else '):')); lines+=block(v[2],depth+1,set(v[1]))
    if js: lines.append(p+'}')
   elif k in ('while','if'):
    lines.append(p+(k+' (__kw_truth('+expr(v[0])+')) {' if js else k+' '+expr(v[0])+':')); lines+=block(v[1],depth+1,local,True)
    if js: lines.append(p+'}')
    if k=='if' and v[2]:
     lines.append(p+('else {' if js else 'else:')); lines+=block(v[2],depth+1,local,True)
     if js: lines.append(p+'}')
   else: raise Blad('Eksport nie obsługuje instrukcji: '+k)
  return lines or ([p+'pass'] if not js else [])
 return ("function __kw_truth(v){return Array.isArray(v)?v.length>0:Boolean(v);}\nfunction __kw_equal(a,b){return Array.isArray(a)||Array.isArray(b)?Array.isArray(a)&&Array.isArray(b)&&a.length===b.length&&a.every((v,i)=>__kw_equal(v,b[i])):a===b;}\nfunction __kw_index(a,i){if(typeof a==='string')a=Array.from(a);if(!Array.isArray(a)||!Number.isInteger(i)||i>=a.length||i< -a.length)throw Error('Niepoprawny indeks');return a.at(i);}\n" if js else '')+'\n'.join(block(ast))+'\n'

if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('plik');p.add_argument('--cel',choices=['python','javascript'],required=True);p.add_argument('-o',required=True);a=p.parse_args()
 try:
  result=eksport(Path(a.plik).read_text(encoding='utf-8-sig'),a.cel)
  with Path(a.o).open('x',encoding='utf-8') as f: f.write(result)
 except (Blad,OSError) as e: p.exit(1,str(e)+'\n')
