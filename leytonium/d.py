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

'Show local changes.'
from . import st
from .common import findproject, infodirname, savedcommits
from lagoon import clear, git

def main():
    clear[print]()
    git.diff[print]()

def main_dup():
    'Apply the last slammed commit.'
    git.cherry_pick.__no_commit[print](savedcommits()[-1])
    git.reset[print]()
    st.main_st()

def main_scrub():
    'Remove all untracked items, including the git-ignored.'
    git.clean._xdi[print]('-e', infodirname, cwd = findproject())

if '__main__' == __name__:
    main()
