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
import os, sys

def main_git_completion_path():
    'Get path to git completion file, used by scripts.'
    print(Path(__file__).parent / 'git_completion.bash')

def main_git_functions_path():
    'Get path to git functions file, used by scripts.'
    print(Path(__file__).parent / 'git_functions.bash')

def main_insertshlvl():
    'Insert SHLVL indicator into given prompt.'
    ps1, = sys.argv[1:]
    colon = ps1.rindex(':')
    n = int(os.environ['SHLVL'])
    indicator = '"' * (n // 2) + ("'" if n % 2 else '')
    print(f"{ps1[:colon]}{indicator}{ps1[colon + 1:]}")
