from lagoon import python3
from lagoon.program import Program
from pathlib import Path
from tempfile import TemporaryDirectory
import os, sys

shellpath = os.environ['SHELL']

def main_tempvenv():
    'Activate a temporary venv.'
    with TemporaryDirectory() as venvdir:
        venvdir = Path(venvdir)
        python3._m.venv.print(venvdir) # Must use host executable to get pip apparently.
        reqs = sys.argv[1:]
        if reqs:
            Program.text(venvdir / 'bin' / 'pip').install.print(*reqs)
        Program.text(shellpath)._c.print('. "$1" && exec "$2"', '-c', venvdir / 'bin' / 'activate', shellpath)
