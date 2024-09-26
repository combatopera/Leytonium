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

'Show tree with hidden descendants but not their descendants.'
from lagoon import tree
from lagoon.program import partial
from lagoon.util import stripansi
from pathlib import Path
import re, sys

intro = '── '
denymatch = re.compile(f"{re.escape(intro)}[.]").search
indent = 4

def main():
    allow = True
    allowmatch = None
    parts = []
    with tree._aC[partial](*sys.argv[1:]) as f:
        for line in f:
            bwline = stripansi(line)
            if not allow and allowmatch(bwline) is not None:
                allow = True
            if allow:
                try:
                    depth, r = divmod(bwline.index(intro) + len(intro), indent)
                    assert not r
                except ValueError:
                    depth = 0
                name, = bwline[depth * indent:].splitlines()
                del parts[depth:]
                parts.append(name)
                path = Path(*parts)
                m = denymatch(bwline)
                if m is None:
                    sys.stdout.write(line)
                else:
                    sanseol, = line.splitlines()
                    sys.stdout.write(sanseol)
                    try:
                        n = sum(1 for _ in path.iterdir())
                    except (FileNotFoundError, NotADirectoryError):
                        n = 0
                    sys.stdout.write('/' * n)
                    sys.stdout.write(line[len(sanseol):])
                    allow = False
                    allowmatch = re.compile(f".{{,{m.start()}}}── ").match

if '__main__' == __name__:
    main()
