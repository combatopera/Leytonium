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

from lagoon import sudo
from pathlib import Path

def main_upgrade():
    'Upgrade the system and silence the nag.'
    apt_get = sudo.apt_get[print]
    apt_get.update()
    apt_get.__with_new_pkgs.upgrade()
    apt_get.autoremove()
    touchpath = Path.home() / 'var' / 'last-upgrade'
    touchpath.parent.mkdir(parents = True, exist_ok = True)
    touchpath.write_text('')
