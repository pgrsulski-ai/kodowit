"""Eksperymentalny kompilator podzbioru całkowitoliczbowego do C11."""
import argparse, pathlib, subprocess, shutil, tempfile
from kodowit import Parser, Blad

def translate(source):
    names = {}
    def expr(a):
        if a[0]=='lit' and type(a[1]) is int and abs(a[1])<=2147483647: return str(a[1])+'LL'
        if a[0]=='var' and a[1] in names: return names[a[1]]
        if a[0]=='bin' and a[1] in ('+','-','*'): return f'calc({expr(a[2])},{expr(a[3])},\'{a[1]}\')'
        if a[0]=='un' and a[1]=='-': return f"calc(0,{expr(a[2])},'-')"
        raise Blad('Kompilator natywny: nieobsługiwane wyrażenie')
    lines=[]
    for a in Parser(source).seq():
        if a[0] in ('let','set'):
            n=a[1]; v=expr(a[2]); new=n not in names
            if new and a[0]=='set': raise Blad('Nieznana zmienna')
            if not new and a[0]=='let': raise Blad('Powtórzona deklaracja')
            if new: names[n]='v'+str(len(names))
            lines.append(('long long ' if new else '')+names[n]+' = '+v+';')
        elif a[0]=='expr' and a[1][0]=='call' and a[1][1]==('var','wypisz') and len(a[1][2])==1:
            lines.append('printf("%lld\\n", '+expr(a[1][2][0])+');')
        else: raise Blad('Kompilator natywny: nieobsługiwana instrukcja')
    return '''#include <stdio.h>
#include <stdlib.h>
static long long calc(long long a,long long b,char op){
 long long r=op=='+'?a+b:op=='-'?a-b:a*b;
 if(r>2147483647LL || r< -2147483647LL){fputs("Przekroczony zakres liczby\\n",stderr);exit(1);}return r;
}
int main(void){\n'''+ '\n'.join(lines)+'\nreturn 0;\n}\n'

def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('plik'); p.add_argument('-o',required=True); p.add_argument('--c',action='store_true'); a=p.parse_args()
    try:
        src=pathlib.Path(a.plik); out=pathlib.Path(a.o)
        if out.exists(): raise Blad('Plik wyjściowy już istnieje')
        if src.stat().st_size>100000: raise Blad('Za duży plik')
        code=translate(src.read_text(encoding='utf-8'))
        if a.c:
            with out.open('x',encoding='utf-8') as f: f.write(code)
        else:
            cc=shutil.which('gcc') or shutil.which('clang')
            if not cc: raise Blad('Zainstaluj GCC lub Clang')
            with tempfile.TemporaryDirectory() as d:
                c=pathlib.Path(d)/'program.c'; c.write_text(code,encoding='utf-8'); exe=pathlib.Path(d)/'program.exe'
                subprocess.run([cc,'-std=c11','-O2',str(c),'-o',str(exe)],check=True,timeout=30)
                with out.open('xb') as f: f.write(exe.read_bytes())
                out.chmod(0o755)
    except (Blad,OSError,ValueError,RecursionError,subprocess.SubprocessError) as e: p.exit(1,f'Błąd: {e}\n')
if __name__=='__main__': main()
