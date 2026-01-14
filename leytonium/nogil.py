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

'Build free-threaded Python Docker image.'
from aridity.config import ConfigCtrl
from foyndation import solo
from lagoon.text import docker
from lagoon.url import URL
from pathlib import Path
from tempfile import TemporaryDirectory
import re

def main():
    config = ConfigCtrl().loadappconfig(main, 'nogil.arid')
    dockerfile = URL.text(config.url)()
    j = solo(re.finditer('--with-ensurepip', dockerfile)).end()
    dockerfile = f"{dockerfile[:j]} --disable-gil{dockerfile[j:]}"
    with TemporaryDirectory() as context:
        Path(context, 'Dockerfile').write_text(dockerfile)
        docker.build[print]('-t', config.tag, context)

if '__main__' == __name__:
    main()
