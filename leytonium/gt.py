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

'Stage all outgoing changes and show them.'
from . import st
from .common import findproject
from lagoon.text import git
from pathlib import Path

def main():
    projectdir = Path(findproject()).resolve()
    git.add[print](*(projectdir / line[line.index("'") + 1:-1] for line in git.add._n(projectdir).splitlines()))
    st.main()

if '__main__' == __name__:
    main()
