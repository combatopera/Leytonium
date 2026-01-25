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

'Shell for cron.'
from datetime import datetime
from lagoon.text import bash, lsof
from pathlib import Path
from subprocess import DEVNULL
import shlex, sys

def main():
    assert '-c' == sys.argv[1]
    script = sys.argv[2]
    name = Path(shlex.split(script)[0]).name
    logpath = Path('var', 'log', f"{name}.log")
    inuse = 'aw' in lsof._F.a[::DEVNULL](logpath, check = False).stdout.splitlines()
    with logpath.open('a') as f:
        def log(text):
            print(datetime.now(), text, file = f)
        if inuse:
            log('Previous instance still running.')
        else:
            bash._lc[:f:f](sys.stdin.read() + script) # XXX: Is login shell needed in .xsessionrc case?
            log('Normal end.')

if '__main__' == __name__:
    main()
