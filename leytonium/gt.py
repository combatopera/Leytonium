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

from . import st
from .brown import main_brown, brown
from .common import findproject
from aridity.config import ConfigCtrl
from lagoon import git
from pathlib import Path

def main_gt():
    'Stage all outgoing changes and show them.'
    config = (-ConfigCtrl().loadappconfig(main_brown, 'common.arid')).reapplysettings(main_gt)
    projectdir = Path(findproject()).resolve()
    paths = [projectdir / line[line.index("'") + 1:-1] for line in git.add._n(projectdir).splitlines()]
    if projectdir.name in config.formattedprojects:
        toformat = [path for path in paths if path.exists() and path.name.endswith('.py')]
        if toformat:
            brown(config.cols, toformat)
    git.add[print](*paths)
    st.main_st()

if '__main__' == __name__:
    main_gt()
