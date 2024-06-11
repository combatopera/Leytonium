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

'Edit gpg-encrypted file.'
from argparse import ArgumentParser
from lagoon import gpg, gpgconf
from lagoon.program import Program
from lagoon.util import atomic, mapcm
from pathlib import Path
from tempfile import TemporaryDirectory
import os

def main():
    parser = ArgumentParser()
    parser.add_argument('-f', action = 'store_true')
    parser.add_argument('path', type = Path)
    args = parser.parse_args()
    if args.f:
        gpgconf.__reload.gpg_agent[print]()
    path = args.path
    with mapcm(Path, TemporaryDirectory()) as tempdir:
        x = tempdir / path.name
        if path.exists():
            gpg.__decrypt[print]('--output', x, path)
        Program.text(os.environ['EDITOR'])[print](x)
        with atomic(path) as y:
            gpg.__symmetric[print]('--output', y, x)

if '__main__' == __name__:
    main()
