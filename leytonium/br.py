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

from .common import addparents, args, AllBranches, menu
from lagoon import git

def main_br():
    'Create given branch with completion and dashes, show menu for parent.'
    _, base = menu([[n, ''] for n in AllBranches().names], 'From')
    name = '-'.join(args())
    git.checkout._b[print](name, base)
    addparents(name, base)

if '__main__' == __name__:
    main_br()
