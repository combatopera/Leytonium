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

'Open a shell in a throwaway container of the given image.'
from foyndation import initlogging
from lagoon.program import NOEOL
from lagoon.text import docker
from pathlib import Path
from tempfile import TemporaryDirectory
import logging, sys

log = logging.getLogger(__name__)
dockerfile = """FROM python
WORKDIR /image
COPY --from={} / ."""

def _examine(runimage, shell):
    docker.run.__network.host._ti.__rm[print]('--entrypoint', shell, '-u', 0, runimage)

def main():
    initlogging()
    image, = sys.argv[1:]
    shells = docker.run.__rm.__entrypoint.ls(image, '/bin/bash', '/bin/sh', check = False).stdout.splitlines()
    if shells:
        _examine(image, shells[0])
    else:
        with TemporaryDirectory() as context:
            Path(context, 'Dockerfile').write_text(dockerfile.format(image))
            log.info("Build: %s", context)
            delimage = docker.build._q[NOEOL]('--platform', 'linux/amd64', context)
            try:
                _examine(delimage, 'bash')
            finally:
                docker.image.rm[print](delimage)

if '__main__' == __name__:
    main()
