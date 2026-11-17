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

'Drop this branch.'
from .abandon import abandon
from .co import co
from .common import AllBranches, thisbranch
from .dx import dxprogram
from argparse import ArgumentParser
from lagoon.text import git
from pathlib import Path
import os, sys

def main():
    parser = ArgumentParser()
    parser.add_argument('-f', action = 'store_true')
    args = parser.parse_args()
    if not args.f and dxprogram(True, None)():
        sys.exit('Unmerged changes!')
    git.rebase.__abort[print](check = False)
    if git.status.__porcelain():
        abandon()
    todrop = thisbranch()
    v = AllBranches().names
    for b, next in zip(v, [*v[1:], v[0]]):
        if b == todrop:
            break
    co(next) # FIXME: Wraparound is surprising, select nearest with preference for next.
    git.branch[print]('-D', todrop)
    while not Path('.git').is_dir():
        os.chdir('..')
    try:
        Path('.pb', todrop).unlink()
    except FileNotFoundError:
        pass

if '__main__' == __name__:
    main()
