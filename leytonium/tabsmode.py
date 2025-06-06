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

'''Vim wrapper that applies `set noexpandtab` if at least one arg matches the configured regex and no args don't match.'''
from aridity.config import ConfigCtrl
from pathlib import Path
import os, re, sys

def _commandornone(pattern, mixmessage, args):
    tabs = spaces = 0
    for a in args:
        if a.startswith('+'):
            continue
        if pattern.search(str(Path(a).resolve())) is None:
            spaces += 1
        else:
            tabs += 1
    if tabs:
        if spaces:
            return f"""redr|echoh Error|ec'{mixmessage.replace("'", "''")}'|echoh None""" # TODO: Unduplicate vimstr.
        return 'se noet'

def main():
    config = ConfigCtrl().loadappconfig(main, 'tabsmode.arid')
    arg0, *appargs = sys.argv
    command = _commandornone(re.compile(config.regex), config.mixmessage, appargs)
    os.execv(config.realvim, [arg0, *([] if command is None else [f"+{command}"]), *appargs])

if '__main__' == __name__:
    main()
