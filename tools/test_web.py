"""Uruchamia testy JS z katalogu projektu."""
import subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if __name__ == "__main__":
    tests=sorted((ROOT/"tests").glob("test*.cjs"))
    if not tests: sys.exit("Brak testów")
    for test in tests:
        subprocess.run(["node",str(test)],cwd=ROOT,check=True,timeout=60)
    print(f"OK: {len(tests)} zestawów")
