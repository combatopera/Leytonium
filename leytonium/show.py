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

'Show a commit that was listed by st.'
from .common import showmenu, AllBranches, savedcommits
from argparse import ArgumentParser
from lagoon.text import git

def main():
    parser = ArgumentParser()
    parser.add_argument('-x', action = 'store_true', help = 'name/status only')
    parser.add_argument('number', type = int, help = 'commit number')
    args = parser.parse_args()
    n = args.number
    if n > 0:
        commit = showmenu(AllBranches().branchcommits(), False)[n]
    else:
        saved = savedcommits()
        commit = saved[len(saved) - 1 + n]
    git.show[exec](*['--name-status'] if args.x else [], commit)

if '__main__' == __name__:
    main()
