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

from pathlib import Path
import shlex, sys

def main_git_completion_path():
    'Get path to git completion file, used by scripts.'
    print(_git_completion_path())

def _git_completion_path():
    return Path(__file__).parent / 'git_completion.bash'

def main_git_functions_path():
    'Get path to git functions file, used by scripts.'
    print(Path(__file__).parent / 'git_functions.bash')

def main_insertshlvl():
    'Insert SHLVL indicator into given prompt.'
    print(_insertshlvl(*sys.argv[1:]))

def _insertshlvl(ps1, shlvl):
    try:
        colon = ps1.rindex(':')
    except ValueError:
        return ps1
    n = int(shlvl)
    tally = '"' * (n // 2) + ("'" if n % 2 else '')
    return f"{ps1[:colon]}{tally}{ps1[colon + 1:]}"

def main_bashrc():
    'To eval in your .bashrc file.'
    sys.stdout.write(f""". {shlex.quote(str(_git_completion_path()))}
PS1={shlex.quote(_insertshlvl(*sys.argv[1:]))}
""")
