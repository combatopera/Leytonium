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

'Vim wrapper. If there is at least one arg and every arg is a Python file in the configured workspaces, set noexpandtab.'
from aridity.config import ConfigCtrl
from foyndation import dotpy
from lagoon.binary import vim
from pathlib import Path
import sys

def _tabsmode(workspaces, args):
    base = False
    for a in args:
        if not (a.endswith(dotpy) and any(map(Path(a).resolve().is_relative_to, workspaces))):
            return False
        base = True
    return base

def main():
    config = ConfigCtrl().loadappconfig(main, 'tabsmode.arid')
    args = sys.argv[1:]
    vim[exec](*['-c', 'set noexpandtab'] if _tabsmode(list(config.workspace), args) else [], *args)

if '__main__' == __name__:
    main()
