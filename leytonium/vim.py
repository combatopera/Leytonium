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

'Vim wrapper. If there is at least one arg with a configured suffix in a configured workspace, and no args that fail the check, set noexpandtab.'
from aridity.config import ConfigCtrl
from pathlib import Path
import os, sys

def _command(suffixes, workspaces, args):
    tabs = spaces = 0
    for a in args:
        if a.startswith('+'):
            continue
        if a.endswith(suffixes) and any(map(Path(a).resolve().is_relative_to, workspaces)):
            tabs += 1
        else:
            spaces += 1
    if tabs:
        if spaces:
            return 'redraw | echohl Error | echo "MIX" | echohl None'
        return 'set noexpandtab'
    return ':'

def main():
    config = ConfigCtrl().loadappconfig(main, 'vim.arid')
    arg0, *appargs = sys.argv
    os.execv('/usr/bin/vim', [arg0, '+' + _command(tuple(config.tabsmode.suffix), list(config.tabsmode.workspace), appargs), *appargs])

if '__main__' == __name__:
    main()
