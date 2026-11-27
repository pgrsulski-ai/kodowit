"""Lightweight Tk editor helpers, without external dependencies."""
import re
import tkinter as tk
KEYWORDS=set('klasa ja dziedziczy dziedzicz konstruktor sprobuj spróbuj przechwyc zglos zgłoś zmienna stan funkcja jezeli jeżeli jeśli jesli inaczej dopoki dopóki dla w zwroc zwróć prawda falsz fałsz nie i lub'.split())
BUILTINS=set('wypisz zakres dlugosc długość liczba tekst calkowita suma importuj_pakiet python_wywolaj api_trasa api_start'.split())
TOKEN=re.compile(r'(?P<comment>//[^\n]*|\#[^\n]*)|(?P<string>"(?:\\.|[^"\\])*"?)|(?P<number>\d+(?:\.\d+)?)|(?P<word>[^\W\d]\w*)',re.UNICODE)
def spans(source):
    for m in TOKEN.finditer(source):
        kind=m.lastgroup
        if kind=='word':
            kind='keyword' if m.group() in KEYWORDS else 'builtin' if m.group() in BUILTINS else None
        if kind: yield m.start(),m.end(),kind

def indentation(line):
    prefix=re.match(r'[ \t]*',line).group()
    clean=TOKEN.sub(lambda m:'' if m.lastgroup in ('comment','string') else m.group(),line).rstrip()
    return prefix+('    ' if clean.endswith('{') else '')

class Editor:
    def __init__(self,text,gutter,scroll):
        self.text=text; self.gutter=gutter; self.pending=None
        for tag,color in {'keyword':'#c084fc','builtin':'#67e8f9','string':'#86efac','number':'#fbbf24','comment':'#94a3b8'}.items():text.tag_configure(tag,foreground=color)
        text.configure(yscrollcommand=lambda a,b:(scroll.set(a,b),self.draw()))
        text.bind('<<Modified>>',self.changed,add='+'); text.bind('<Configure>',lambda e:self.draw(),add='+')
        text.bind('<Return>',self.enter); text.bind('<Tab>',self.tab); text.bind('<Control-space>',self.complete)
        text.edit_modified(False)
    def changed(self,event=None):
        if not self.text.edit_modified():return
        self.text.edit_modified(False)
        if self.pending is not None:self.text.after_cancel(self.pending)
        self.pending=self.text.after(100,self.refresh)
    def refresh(self):
        self.pending=None; t=self.text; source=t.get('1.0','end-1c')
        for tag in ('keyword','builtin','string','number','comment'):t.tag_remove(tag,'1.0','end')
        for a,b,tag in spans(source):t.tag_add(tag,f'1.0+{a}c',f'1.0+{b}c')
        self.draw()
    def draw(self):
        t=self.text; g=self.gutter; g.delete('all'); index=t.index('@0,0')
        while True:
            info=t.dlineinfo(index)
            if info is None:break
            g.create_text(42,info[1],anchor='ne',text=index.split('.')[0],fill='#94a3b8',font=('Consolas',12))
            index=t.index(f'{index}+1line')
            if t.compare(index,'>=','end'):break
    def enter(self,event=None):
        t=self.text; line=t.get('insert linestart','insert'); t.insert('insert','\n'+indentation(line)); return 'break'
    def tab(self,event=None):
        self.text.insert('insert','    '); return 'break'
    def complete(self,event=None):
        t=self.text; before=t.get('insert linestart','insert'); m=re.search(r'\w+$',before); prefix=m.group() if m else ''
        options=sorted(w for w in KEYWORDS|BUILTINS if w.startswith(prefix) and w!=prefix)
        if not options:return 'break'
        menu=tk.Menu(t,tearoff=False)
        for word in options:menu.add_command(label=word,command=lambda w=word:t.insert('insert',w[len(prefix):]))
        pos=t.bbox('insert')
        if pos:menu.post(t.winfo_rootx()+pos[0],t.winfo_rooty()+pos[1]+pos[3])
        return 'break'
