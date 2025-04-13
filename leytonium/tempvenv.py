# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

'Find a venv (optionally writable) from the pool with the given requires and open a new shell in which it is activated.'
from . import initlogging
from argparse import ArgumentParser
from inspect import getsource
from lagoon.program import Program
from lagoon.text import chmod
from pathlib import Path
from tempfile import TemporaryDirectory
from venvpool import ParsedRequires, Pool
from venvpool.util import detach
import logging, os, sys

log = logging.getLogger(__name__)
shellpath = os.environ['SHELL']

def _temppip():
    from pathlib import Path
    from shutil import which
    import os, sys
    assert sys.argv[1] in {'check', 'debug', 'download', 'freeze', 'hash', 'help', 'list', 'search', 'show', 'wheel'}
    os.execv(Path(which('python')).parent / 'pip', sys.argv)

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('-w', action = 'store_true')
    parser.add_argument('reqs', nargs = '*')
    args = parser.parse_args()
    requires = ParsedRequires(args.reqs)
    env = detach()
    if args.w:
        with Pool().readwrite(requires) as venv:
            Program.text(shellpath)._c[print]('. "$1" && exec "$2"', '-c', Path(venv.venvpath, 'bin', 'activate'), shellpath, absenv = env)
    else:
        with Pool().readonly(requires) as venv, TemporaryDirectory() as tempdir:
            temppip = Path(tempdir, 'pip')
            temppip.write_text(f"#!{sys.executable}\n{getsource(_temppip)}_temppip()\n")
            chmod[print]('+x', temppip)
            Program.text(shellpath)._c[print]('. "$1" && PATH="$2:$PATH" && exec "$3"', '-c', Path(venv.venvpath, 'bin', 'activate'), tempdir, shellpath, absenv = env)

if '__main__' == __name__:
    main()
