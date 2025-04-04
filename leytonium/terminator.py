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

'Unset SHLVL before launching Terminator in case Cinnamon was wrapped by shell.'
from . import initlogging
from lagoon.text import lsof
from pathlib import Path
import logging, os, re, sys

log = logging.getLogger(__name__)

class Venv:

    @classmethod
    def detachall(cls):
        sepregex = re.escape(os.sep)
        pattern = re.compile(f"n(.+){sepregex}readlocks{sepregex}.+")
        v = lsof._F.fn('-p', os.getpid()).splitlines()
        for f, n in zip(v[1::2], v[2::2]):
            m = pattern.fullmatch(n)
            if m is not None:
                cls(m.group(1), int(f[1:])).detach()

    def __init__(self, path, fd):
        self.bindir = Path(path, 'bin')
        self.fd = fd

    def _bindirs(self):
        for p in os.environ['PATH'].split(os.pathsep):
            if Path(p) == self.bindir:
                log.debug("Filter out: %s", p)
            else:
                yield p

    def detach(self):
        os.environ['PATH'] = os.pathsep.join(self._bindirs())
        log.debug("Close: %s", self.fd)
        os.close(self.fd)

def main():
    initlogging()
    Venv.detachall()
    os.environ.pop('SHLVL')
    os.execv('/usr/bin/terminator', sys.argv)

if '__main__' == __name__:
    main()
