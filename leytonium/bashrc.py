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

'To eval in your .bashrc file.'
from argparse import ArgumentParser
from pathlib import Path
import shlex, sys

def _insertshlvl(ps1, shlvl):
    try:
        colon = ps1.rindex(':')
    except ValueError:
        return ps1
    tally = '"' * (shlvl // 2) + ("'" if shlvl % 2 else '')
    return f"{ps1[:colon]}{tally}{ps1[colon + 1:]}"

def main():
    parser = ArgumentParser()
    parser.add_argument('ps1')
    parser.add_argument('shlvl', type = int)
    args = parser.parse_args()
    sys.stdout.write(f""". {shlex.quote(str(Path(__file__).parent / 'git_completion.bash'))}
PS1={shlex.quote(_insertshlvl(args.ps1, args.shlvl))}
""")

if '__main__' == __name__:
    main()
