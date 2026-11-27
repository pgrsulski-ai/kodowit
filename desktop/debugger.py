"""Debugger protocol: one JSON event per line, commands on stdin."""
import json, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'core'))
from kodowit import Core
class Stop(Exception): pass

def debug(source, breaks, emit, command):
    stepping=True
    def snapshot(env):
        values={}
        while env:
            for k,v in env.d.items():
                if k not in values and not callable(v) and not (isinstance(v,tuple) and v and v[0]=='function'):
                    values[k]=repr(v)[:500]
            env=env.parent
        return values
    def hook(line,kind,env):
        nonlocal stepping
        if stepping or line in breaks:
            emit({'type':'pause','line':line,'variables':snapshot(env)})
            c=command()
            if c not in ('step','continue'): raise Stop()
            stepping=c=='step'
    try:
        Core(out=lambda *a:emit({'type':'output','text':' '.join(map(str,a))}),debug=hook).run(source)
        emit({'type':'done','text':'Zakończono'})
    except Stop: emit({'type':'done','text':'Przerwano'})
    except Exception as e: emit({'type':'done','text':str(e)})
if __name__=='__main__':
    request=json.loads(sys.stdin.readline())
    debug(request['source'],set(request['breaks']),lambda e:print(json.dumps(e,ensure_ascii=True),flush=True),lambda:sys.stdin.readline().strip())
