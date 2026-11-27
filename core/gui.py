"""Local desktop GUI, explicitly enabled by the caller."""
class GUI:
 def __init__(self, invoke):
  self.invoke=invoke; self.root=None; self.widgets={}; self.error=None
 def window(self,title,width=480,height=320):
  import tkinter as tk
  if self.root is not None: raise ValueError('Okno już istnieje')
  if not (100<=width<=2000 and 100<=height<=2000): raise ValueError('Nieprawidłowy rozmiar okna')
  self.root=tk.Tk(); self.root.title(str(title)); self.root.geometry(f'{width}x{height}')
 def add(self,name,kind,text='',fn=None):
  from tkinter import ttk
  if self.root is None: raise ValueError('Najpierw utwórz okno')
  if name in self.widgets: raise ValueError('Powtórzona nazwa elementu')
  if kind=='label': w=ttk.Label(self.root,text=str(text))
  elif kind=='entry': w=ttk.Entry(self.root); w.insert(0,str(text))
  else:
   if not isinstance(fn,tuple) or fn[0]!='function' or fn[1]: raise ValueError('Przycisk wymaga funkcji bez parametrów')
   def click():
    try: self.invoke(fn)
    except Exception as e: self.error=e; self.root.quit()
   w=ttk.Button(self.root,text=str(text),command=click)
  w.pack(fill='x',padx=16,pady=8); self.widgets[name]=(kind,w)
 def get(self,name):
  kind,w=self.widgets[name]; return w.get() if kind=='entry' else w.cget('text')
 def set(self,name,text):
  kind,w=self.widgets[name]
  if kind=='entry': w.delete(0,'end'); w.insert(0,str(text))
  else: w.configure(text=str(text))
 def close(self):
  if self.root is not None: self.root.quit()
 def run(self):
  if self.root is None: raise ValueError('Najpierw utwórz okno')
  try: self.root.mainloop()
  finally:
   try: self.root.destroy()
   except Exception: pass
   self.root=None; self.widgets.clear()
  if self.error: e=self.error; self.error=None; raise e
 def bindings(self):
  return {'okno':self.window,'etykieta':lambda n,t:self.add(n,'label',t),'pole':lambda n,t='':self.add(n,'entry',t),'przycisk':lambda n,t,f:self.add(n,'button',t,f),'gui_odczytaj':self.get,'gui_ustaw':self.set,'gui_start':self.run,'gui_zamknij':self.close}

# Extended GUI and 2D canvas API. All callbacks execute on Tk's event thread.
def _extend():
 def widget(self,name,kind,text=''):
  from tkinter import ttk
  import tkinter as tk
  if self.root is None or name in self.widgets: raise ValueError('Brak okna lub powtórzona nazwa')
  if len(self.widgets)>=200: raise ValueError('Za dużo elementów')
  if kind=='check':
   v=tk.BooleanVar(master=self.root); w=ttk.Checkbutton(self.root,text=str(text),variable=v); w.kodowit_var=v
  elif kind=='progress': w=ttk.Progressbar(self.root,maximum=100)
  else: w=tk.Canvas(self.root,width=480,height=280,bg=str(text),highlightthickness=0)
  w.pack(fill='both' if kind=='canvas' else 'x',expand=kind=='canvas',padx=16,pady=4); self.widgets[name]=(kind,w)
 def canvas(self,name):
  kind,w=self.widgets[name]
  if kind!='canvas': raise ValueError('Element nie jest płótnem')
  return w
 def draw(self,name,kind,x,y,a,b,color):
  w=canvas(self,name)
  if len(w.find_all())>=5000: raise ValueError('Limit figur')
  if kind=='line': return w.create_line(x,y,a,b,fill=color,width=2)
  f=w.create_rectangle if kind=='rect' else w.create_oval
  return f(x,y,x+a,y+b,fill=color,outline='')
 def callback(self,fn):
  if not isinstance(fn,tuple) or fn[0]!='function' or fn[1]: raise ValueError('Wymagana funkcja bez parametrów')
  def call(*args):
   try: self.invoke(fn)
   except Exception as e: self.error=e; self.close()
  return call
 def timer(self,ms,fn):
  if self.root is None or not isinstance(ms,int) or not 10<=ms<=3600000: raise ValueError('Nieprawidłowy czas')
  if len(self.root.tk.call('after','info'))>=100: raise ValueError('Limit timerów')
  self.root.after(ms,callback(self,fn))
 def key(self,k,fn):
  if k not in ('Left','Right','Up','Down','space','Return',*'abcdefghijklmnopqrstuvwxyz'): raise ValueError('Nieobsługiwany klawisz')
  self.root.bind('<KeyPress-'+k+'>',callback(self,fn))
 def collision(self,n,a,b):
  w=canvas(self,n); r=w.bbox(a); s=w.bbox(b)
  return bool(r and s and r[0]<s[2] and s[0]<r[2] and r[1]<s[3] and s[1]<r[3])
 old=GUI.bindings
 def bindings(self):
  return {**old(self),'pole_wyboru':lambda n,t:widget(self,n,'check',t),'wybrane':lambda n:bool(self.widgets[n][1].kodowit_var.get()),'pasek_postepu':lambda n:widget(self,n,'progress'),'postep_ustaw':lambda n,v:self.widgets[n][1].configure(value=max(0,min(100,v))),'plotno':lambda n,t='#ffffff':widget(self,n,'canvas',t),'prostokat':lambda n,x,y,a,b,c:draw(self,n,'rect',x,y,a,b,c),'elipsa':lambda n,x,y,a,b,c:draw(self,n,'oval',x,y,a,b,c),'linia':lambda n,x,y,a,b,c:draw(self,n,'line',x,y,a,b,c),'przesun_figure':lambda n,i,x,y:canvas(self,n).move(i,x,y),'usun_figure':lambda n,i:canvas(self,n).delete(i),'wyczysc_plotno':lambda n:canvas(self,n).delete('all'),'kolizja':lambda n,a,b:collision(self,n,a,b),'po_czasie':lambda ms,f:timer(self,ms,f),'po_klawiszu':lambda k,f:key(self,k,f)}
 GUI.bindings=bindings
_extend()
