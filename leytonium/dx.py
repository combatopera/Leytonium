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

'Diff from target branch or passed-in commit number.'
from .common import AllBranches, pb, savedcommits, showmenu
from argparse import ArgumentParser
from foyndation import initlogging
from lagoon.text import git
import logging

log = logging.getLogger(__name__)

def main():
    initlogging()
    parser = ArgumentParser()
    parser.add_argument('-x', action = 'store_true', help = 'name/status only')
    parser.add_argument('number', type = int, help = 'commit number', nargs = '?')
    args = parser.parse_args()
    n = args.number
    if n is None:
        commit = pb()
        log.info("Target branch: %s", commit)
    elif n > 0:
        v = showmenu(AllBranches().branchcommits(), False)
        commit = v[n] if n in v else f"{v[n - 1]}^"
    else:
        saved = savedcommits()
        commit = saved[len(saved) - 1 + n]
    git.diff._M25[exec](*['--name-status'] if args.x else [], commit)

if '__main__' == __name__:
    main()
