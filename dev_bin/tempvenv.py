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
        python3._m.venv.print(venvdir)
        Program.text(venvdir / 'bin' / 'pip').install.print(*sys.argv[1:])
        Program.text(shellpath)._c.print('. "$1" && "$2"', '-c', venvdir / 'bin' / 'activate', shellpath)
