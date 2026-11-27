"""Oddzielny proces z limitami zasobów na Linux; nie jest piaskownicą OS."""
import subprocess,sys,tempfile,math,os,selectors,time
from pathlib import Path

MAX_OUTPUT_BYTES=4*1024**2
MAX_ERROR_BYTES=64*1024

def collect(command,cwd,env,seconds):
 deadline=time.monotonic()+seconds
 with subprocess.Popen(command,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True) as proc:
  try:
   with selectors.DefaultSelector() as sel:
    buffers={proc.stdout:bytearray(),proc.stderr:bytearray()}
    for stream in buffers: sel.register(stream,selectors.EVENT_READ)
    while sel.get_map():
     remaining=deadline-time.monotonic()
     if remaining<=0: raise ValueError('Przekroczono czas wykonania')
     for key,_ in sel.select(remaining):
      stream=key.fileobj; chunk=os.read(stream.fileno(),65536)
      if not chunk: sel.unregister(stream); continue
      buf=buffers[stream]; cap=MAX_OUTPUT_BYTES if stream is proc.stdout else MAX_ERROR_BYTES
      if len(buf)+len(chunk)>cap: raise ValueError('Przekroczono limit danych procesu')
      buf.extend(chunk)
    try: code=proc.wait(timeout=max(0,deadline-time.monotonic()))
    except subprocess.TimeoutExpired: raise ValueError('Przekroczono czas wykonania') from None
    return code,*(buffers[x].decode('utf-8',errors='replace') for x in (proc.stdout,proc.stderr))
  finally:
   if proc.poll() is None: proc.kill(); proc.wait()

def run(source,seconds=3):
 if not sys.platform.startswith('linux'): raise ValueError('Tryb limitowany wymaga Linux')
 if type(seconds) not in (int,float) or not math.isfinite(seconds) or not 0<seconds<=30: raise ValueError('Limit czasu: 0–30 sekund')
 if not isinstance(source,str) or len(source)>20000: raise ValueError('Limit kodu: 20000 znaków')
 with tempfile.TemporaryDirectory() as d:
  path=Path(d)/'program.kodowit';path.write_text(source,encoding='utf-8')
  worker=Path(__file__).resolve()
  code,out,err=collect([sys.executable,'-I',str(worker),'--worker',str(path)],d,{'PATH':os.defpath,'LANG':'C.UTF-8','HOME':d},seconds)
  if code: raise ValueError(err[:2000] or 'Przekroczono limit zasobów lub błąd procesu')
  return out

def worker(path):
 import resource
 resource.setrlimit(resource.RLIMIT_AS,(768*1024**2,768*1024**2))
 resource.setrlimit(resource.RLIMIT_CPU,(2,2))
 resource.setrlimit(resource.RLIMIT_FSIZE,(0,0))
 resource.setrlimit(resource.RLIMIT_CORE,(0,0))
 sys.path.insert(0,str(Path(__file__).resolve().parent))
 from kodowit import Core
 try:
  def output(*args): print(*('prawda' if x is True else 'fałsz' if x is False else x for x in args))
  Core(out=output,limit=20000).run(Path(path).read_text(encoding='utf-8'))
 except Exception as e: print(str(e),file=sys.stderr);return 1
 return 0
if __name__=='__main__' and len(sys.argv)==3 and sys.argv[1]=='--worker': sys.exit(worker(sys.argv[2]))
