"""KODOWIT Studio Desktop 8.4 — local editor for trusted programs."""
import tkinter as tk
from editor import Editor
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import subprocess, sys, tempfile, threading, queue, os, json
CORE = Path(__file__).resolve().parents[1] / 'core' / 'kodowit.py'

def worker_command(mode):
    if getattr(sys, "frozen", False):
        return [sys.executable, mode]
    return [sys.executable, "-X", "utf8", str(CORE if mode=="--core-worker" else Path(__file__).with_name("debugger.py"))]

def execute(source, check=False):
    with tempfile.TemporaryDirectory() as folder:
        path = Path(folder)/'program.kodowit'
        path.write_text(source, encoding='utf-8')
        return subprocess.run([*worker_command('--core-worker'), *(['--sprawdz'] if check else []), str(path)], cwd=folder, stdin=subprocess.DEVNULL, capture_output=True, encoding='utf-8', errors='replace', timeout=10)

class Studio:
    def __init__(self, root):
        self.root=root; self.path=None; self.saved=''; self.busy=False; self.results=queue.Queue(); self.debug_events=queue.Queue(); self.proc=None; self.paused=False; self.breakpoints=set()
        root.title('KODOWIT Studio Desktop 1.0.1'); root.geometry('950x700'); root.minsize(600,420)
        root.configure(bg='#111827'); style=ttk.Style(root); style.theme_use('clam'); style.configure('TFrame',background='#111827'); style.configure('TLabel',background='#111827',foreground='#e2e8f0'); style.configure('TLabelframe',background='#111827',bordercolor='#334155'); style.configure('TLabelframe.Label',background='#111827',foreground='#93c5fd'); style.configure('TButton',background='#243449',foreground='#f1f5f9',padding=6); style.map('TButton',background=[('active','#36557a')]); style.configure('TPanedwindow',background='#111827')
        bar=ttk.Frame(root,padding=8); bar.pack(fill='x')
        for label, fn in [('Nowy',self.new),('Otwórz',self.open),('Zapisz',self.save),('Zapisz jako',lambda:self.save(True)),('Uruchom',lambda:self.run(False)),('Sprawdź składnię',lambda:self.run(True)),('Eksport EXE',self.export_exe)]:
            ttk.Button(bar,text=label,command=fn).grid(row=0 if label in ('Nowy','Otwórz','Zapisz','Zapisz jako') else 1,column={'Nowy':0,'Otwórz':1,'Zapisz':2,'Zapisz jako':3,'Uruchom':0,'Sprawdź składnię':1,'Eksport EXE':2}[label],sticky='ew',padx=3,pady=2)
        debugbar=ttk.Frame(root,padding=4); debugbar.pack(fill='x')
        for label,fn in [('Punkt przerwania',self.toggle_break),('Debuguj',self.start_debug),('Krok',lambda:self.debug_command('step')),('Kontynuuj',lambda:self.debug_command('continue')),('Stop',self.stop_debug)]:
            ttk.Button(debugbar,text=label,command=fn).pack(side='left',padx=2)
        self.variables=tk.StringVar(value='Zmienne: —'); ttk.Label(root,textvariable=self.variables,wraplength=850).pack(fill='x')
        pane=ttk.Panedwindow(root,orient='vertical'); pane.pack(fill='both',expand=True,padx=10,pady=5)
        for label in ['Kod KODOWIT','Konsola']:
            frame=ttk.Labelframe(pane,text=label,padding=5); pane.add(frame,weight=3 if label=='Kod KODOWIT' else 1)
            text=tk.Text(frame,undo=label=='Kod KODOWIT',wrap='none',font=('Consolas',12),bg='#172033',fg='#e2e8f0',insertbackground='white')
            scroll=ttk.Scrollbar(frame,command=text.yview); scroll.pack(side='right',fill='y'); text.configure(yscrollcommand=scroll.set); text.pack(fill='both',expand=True)
            if label=='Kod KODOWIT':
                gutter=tk.Canvas(frame,width=50,bg='#111827',highlightthickness=0); gutter.pack(side='left',fill='y',before=text); self.editor=text; text.tag_configure("breakpoint",background="#713333"); text.tag_configure("debugline",background="#315b36"); self.editor_tools=Editor(text,gutter,scroll)
            else: self.console=text; text.configure(state='disabled')
        self.status=tk.StringVar(value='Gotowy • Core 1.0.1'); ttk.Label(root,textvariable=self.status,padding=8).pack(fill='x')
        root.protocol('WM_DELETE_WINDOW',self.close); root.bind('<Control-s>',lambda e:self.save()); root.bind('<F5>',lambda e:self.run(False)); root.after(100,self.poll)
        self.replace('wypisz("Witaj w KODOWIT!")\n')
    def code(self): return self.editor.get('1.0','end-1c')
    def replace(self,source):
        self.breakpoints.clear(); self.editor.delete('1.0','end'); self.editor.insert('1.0',source); self.editor.edit_reset(); self.saved=source
    def confirm(self):
        if self.code()==self.saved:return True
        answer=messagebox.askyesnocancel('Niezapisane zmiany','Zapisać zmiany?')
        return False if answer is None else self.save() if answer else True
    def new(self):
        if not self.busy and self.confirm(): self.path=None; self.replace(''); self.status.set('Nowy program')
    def open(self):
        if self.busy or not self.confirm():return
        name=filedialog.askopenfilename(filetypes=[('KODOWIT','*.kodowit'),('Wszystkie','*')]);
        if not name:return
        try: source=Path(name).read_text(encoding='utf-8-sig'); self.path=Path(name); self.replace(source); self.status.set(name)
        except (OSError,UnicodeError) as e:messagebox.showerror('Błąd odczytu',str(e))
    def save(self,as_new=False):
        path=self.path
        if path is None or as_new:
            name=filedialog.asksaveasfilename(defaultextension='.kodowit',filetypes=[('KODOWIT','*.kodowit')]);
            if not name:return False
            path=Path(name)
        try: path.write_text(self.code(),encoding='utf-8'); self.path=path; self.saved=self.code(); self.status.set(str(path)); return True
        except OSError as e:messagebox.showerror('Błąd zapisu',str(e)); return False
    def output(self,text):
        self.console.configure(state='normal'); self.console.delete('1.0','end'); self.console.insert('1.0',text); self.console.configure(state='disabled')
    def run(self,check):
        if self.busy:return
        self.busy=True; self.status.set('Wykonywanie…'); self.output(''); source=self.code()
        def worker():
            try:
                r=execute(source,check); self.results.put((r.stdout+r.stderr, f'Kod zakończenia: {r.returncode}'))
            except subprocess.TimeoutExpired:self.results.put(('Przekroczono 10 sekund.','Przerwano'))
            except Exception as e:self.results.put((str(e),'Błąd'))
        threading.Thread(target=worker,daemon=True).start()
    def export_exe(self):
        if self.busy:return
        if getattr(sys, "frozen", False):
            messagebox.showinfo("Eksport EXE", "Eksport wymaga wersji źródłowej Studio oraz Pythona i PyInstaller."); return
        name=filedialog.asksaveasfilename(defaultextension='.exe',filetypes=[('Windows EXE','*.exe')])
        if not name:return
        source=self.code(); self.busy=True; self.status.set('Budowanie EXE…')
        def worker():
            try:
                from export_exe import build
                path=build(source,name); self.results.put((str(path),'Eksport zakończony'))
            except Exception as e:self.results.put((str(e),'Błąd eksportu'))
        threading.Thread(target=worker,daemon=True).start()
    def toggle_break(self):
        if self.busy:return
        line=int(self.editor.index('insert').split('.')[0])
        if line in self.breakpoints:self.breakpoints.remove(line); self.editor.tag_remove('breakpoint',f'{line}.0',f'{line+1}.0')
        else:self.breakpoints.add(line); self.editor.tag_add('breakpoint',f'{line}.0',f'{line+1}.0')
    def start_debug(self):
        if self.busy:return
        self.busy=True; self.output(''); self.variables.set('Zmienne: —'); self.editor.configure(state='disabled')
        try:
            self.proc=subprocess.Popen(worker_command('--debug-worker'),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
            self.proc.stdin.write(json.dumps({'source':self.code(),'breaks':sorted(self.breakpoints)})+'\n'); self.proc.stdin.flush()
        except Exception as e:
            self.stop_debug(); self.status.set(str(e)); return
        proc=self.proc
        def reader():
            for line in proc.stdout:
                try:self.debug_events.put((proc,json.loads(line)))
                except ValueError:self.debug_events.put((proc,{'type':'output','text':line.strip()}))
            proc.wait(); self.debug_events.put((proc,{'type':'exit'}))
        threading.Thread(target=reader,daemon=True).start()
        self.status.set('Debugowanie…')
    def debug_command(self,cmd):
        if self.proc and self.paused:
            self.paused=False
            try:self.proc.stdin.write(cmd+'\n'); self.proc.stdin.flush()
            except OSError:self.stop_debug()
    def stop_debug(self):
        if self.proc:
            if self.proc.poll() is None:self.proc.kill()
            self.proc=None
        self.paused=False; self.busy=False; self.editor.configure(state='normal'); self.editor.tag_remove('debugline','1.0','end'); self.status.set('Debugowanie zakończone')
    def poll(self):
        for _ in range(100):
            try:proc,event=self.debug_events.get_nowait()
            except queue.Empty:break
            if proc is not self.proc:continue
            kind=event['type']
            if kind=='pause':
                self.paused=True; line=event['line']; self.editor.tag_remove('debugline','1.0','end')
                if line:self.editor.tag_add('debugline',f'{line}.0',f'{line+1}.0'); self.editor.see(f'{line}.0')
                self.variables.set('Zmienne: '+str(event['variables'])); self.status.set(f'Pauza: wiersz {line}')
            elif kind in ('output','done'):self.output(self.console.get('1.0','end-1c')+event['text']+'\n')
            elif kind=='exit':self.stop_debug()

        try:
            text,status=self.results.get_nowait(); self.output(text); self.status.set(status); self.busy=False
        except queue.Empty:pass
        self.root.after(100,self.poll)
    def close(self):
        if self.busy:messagebox.showinfo('KODOWIT','Poczekaj na zakończenie programu.');return
        if self.confirm():self.root.destroy()

if __name__=='__main__':
    root=tk.Tk(); Studio(root); root.mainloop()
