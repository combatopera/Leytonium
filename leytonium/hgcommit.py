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

'Commit hook to push to central clone of repo on local network.'
from . import effectivehome
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from datetime import datetime
from foyndation import initlogging, singleton
from functools import partial
from lagoon.program import ONELINE
from lagoon.text import git, ls, rsync
from multifork import Tasks
from pathlib import Path
from subprocess import DEVNULL
import logging, os, sys

log = logging.getLogger(__name__)

class PathDest:

    def __init__(self, config, reldir):
        self.clonespath = Path(config.repomount, effectivehome.name)
        self.path = self.clonespath / reldir
        self.repohost = config.repohost
        self.reponame = config.reponame
        self.netremotename = config.netremotename
        self.reldir = reldir

    def check(self):
        return ls._d[bool](self.clonespath, stdout = DEVNULL, stderr = DEVNULL)

    def exists(self):
        return self.path.exists()

@singleton
class Git:

    dirname = '.git'

    def mangle(self, reldir):
        return reldir.parent / f"{reldir.name}.git"

    def pushorclone(self, dest):
        if dest.exists(): # TODO: Attempt to mount it.
            git.push[print](dest.netremotename, git.rev_parse.__abbrev_ref.HEAD[ONELINE]())
        else:
            git.clone.__bare[print]('.', dest.path)
        branches = set(git.branch().splitlines())
        if '  public' in branches:
            currentbranch = {f"* {b}" for b in ['main', 'master', 'trunk']} & branches
            if currentbranch:
                mainbranch, = (b[2:] for b in currentbranch)
                git.update_ref[print]('refs/heads/public', mainbranch)

@singleton
class Rsync:

    dirname = '.rsync'

    def mangle(self, reldir):
        return reldir

    def pushorclone(self, dest):
        lhs = '-avzu', '--exclude', '/.rsync'
        rhs = f".{os.sep}", f"{dest.repohost}::{dest.reponame}/{dest.reldir}"
        rsync[print](*lhs, *rhs)
        os.utime('.rsync')
        lhs += '--del',
        rsync[print](*lhs, '--dry-run', *rhs)
        print(f"(cd {Path.cwd()} && rsync {' '.join(lhs)} {' '.join(rhs)})")

def main():
    initlogging()
    config = ConfigCtrl().loadappconfig((__name__, 'stmulti'), 'stmulti.arid')
    parser = ArgumentParser()
    parser.add_argument('--fg', action = 'store_true')
    args = parser.parse_args()
    reldir = Path.cwd().relative_to(effectivehome)
    for command in Git, Rsync:
        if Path(command.dirname).exists():
            break
    else:
        sys.exit('This is not a project root.')
    dest = PathDest(config, command.mangle(reldir))
    if not dest.check():
        sys.exit(f"Bad path: {dest.clonespath}")
    task = partial(command.pushorclone, dest)
    if args.fg:
        task()
    else:
        log.info('Push/clone in background.')
        if not os.fork():
            label = Path.cwd().name
            with (Path.home() / 'var' / 'log' / 'hgcommit.log').open('a') as f:
                tasks = Tasks()
                tasks.append(task)
                tasks.started = lambda _: f.write(f"{label} {datetime.now()}\n")
                tasks.stdout = lambda _, line: f.write(f"{label} o {line}")
                tasks.stderr = lambda _, line: f.write(f"{label} e {line}")
                tasks.stopped = lambda _, code: f.write(f"{label} {code}\n")
                tasks.drain(1)

if '__main__' == __name__:
    main()
