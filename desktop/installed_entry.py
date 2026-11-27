"""Entry point for the frozen Studio and its child processes."""
import sys
import runpy
from pathlib import Path

def main():
    if len(sys.argv)>1 and sys.argv[1] in ('--core-worker','--debug-worker'):
        mode=sys.argv.pop(1)
        if mode=='--core-worker':
            from kodowit import main as core_main
            return core_main()
        runpy.run_module('debugger',run_name='__main__')
        return 0
    import tkinter as tk
    from studio import Studio
    root=tk.Tk(); Studio(root); root.mainloop()
    return 0

if __name__=='__main__': sys.exit(main())
