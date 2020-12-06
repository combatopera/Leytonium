from argparse import ArgumentParser
from lagoon import python3
from lagoon.program import Program
from pathlib import Path
from tempfile import TemporaryDirectory
import logging, os

log = logging.getLogger(__name__)
shellpath = os.environ['SHELL']

def main_tempvenv():
    'Activate a temporary venv.'
    logging.basicConfig(level = logging.DEBUG, format = "[%(levelname)s] %(message)s")
    parser = ArgumentParser()
    parser.add_argument('-w', action = 'store_true', help = 'enable bdist_wheel command')
    parser.add_argument('reqs', nargs = '*')
    args = parser.parse_args()
    with TemporaryDirectory() as venvdir:
        venvdir = Path(venvdir)
        log.info("Create venv: %s", venvdir)
        python3._m.venv.print(venvdir) # Must use host executable to get pip apparently.
        pipinstall = Program.text(venvdir / 'bin' / 'pip').install
        if args.w:
            pipinstall.wheel.print()
        if args.reqs:
            pipinstall.print(*args.reqs)
        Program.text(shellpath)._c.print('. "$1" && exec "$2"', '-c', venvdir / 'bin' / 'activate', shellpath)
