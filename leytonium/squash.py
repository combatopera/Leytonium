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

'Semi-interactively squash a most-recent chunk of commits.'
from .common import menu, pb
from lagoon.text import git

def _commitmessage(id):
    return git.log('-n', 1, '--pretty=format:%B', id)

def main():
    base = pb()
    ids = [row.split()[1] for row in reversed(git.cherry(base).splitlines())]
    index = menu([(id, _commitmessage(id).splitlines()[0]) for id in ids], 'Which commit should absorb all newer commits')[0] - 1
    id = ids[index]
    git.reset.__hard[print](id)
    git.cherry_pick[print](*(ids[i] for i in range(index)[::-1]))
    git.reset.__soft[print](f"{id}~1")
    message = ''.join(f"{index - i + 1}. {_commitmessage(ids[i])}" for i in range(index + 1)[::-1])
    git.commit._e[print]('-m', message)

if '__main__' == __name__:
    main()
