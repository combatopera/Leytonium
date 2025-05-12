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
from aridity.config import ConfigCtrl
from pathlib import Path
import shlex, sys

setaf = "\x1b[38;5;{}m"
sgr0 = '\x1b[0m'

def _insertshlvl(ps1, shlvl, color):
    try:
        colon = ps1.rindex(':')
        digraph = ps1.rindex(r'\$')
    except ValueError:
        return ps1
    tally = '"' * (shlvl // 2) + ("'" if shlvl % 2 else '')
    return fr"{ps1[:colon]}{tally}{ps1[colon + 1:digraph]}\[{setaf.format(color)}\]{ps1[digraph:digraph + 2]}\[{sgr0}\]{ps1[digraph + 2:]}"

def main():
    config = ConfigCtrl().loadappconfig(main, 'bashrc.arid')
    parser = ArgumentParser()
    parser.add_argument('ps1')
    parser.add_argument('shlvl', type = int)
    parser.parse_args(namespace = config.cli)
    sys.stdout.write(f""". {shlex.quote(str(Path(__file__).parent / 'git_completion.bash'))}
PS1={shlex.quote(_insertshlvl(config.ps1, config.shlvl, config.color))}
""")

if '__main__' == __name__:
    main()
