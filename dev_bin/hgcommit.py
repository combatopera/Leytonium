from . import effectivehome
from .stmulti import loadconfig
from diapyr.util import singleton
from lagoon import git, ls, rsync
from pathlib import Path
import os, subprocess, multiprocessing as mp, queue, logging

log = logging.getLogger(__name__)

def trypath(path, q):
    q.put(ls(path, check = False, stdout = subprocess.DEVNULL)) # Must actually attempt NFS communication.

def checkpath(path):
    q = mp.Queue()
    p = mp.Process(target = trypath, args = (path, q))
    p.daemon = True
    p.start()
    try:
        q.get(timeout = .5)
        return True
    except queue.Empty:
        pass

class PathDest:

    def __init__(self, config, reldir):
        self.clonespath = Path(config.repomount, effectivehome.name)
        self.path = self.clonespath / reldir
        self.repohost = config.repohost
        self.reponame = config.reponame
        self.netremotename = config.netremotename
        self.reldir = reldir

    def check(self):
        return checkpath(self.clonespath)

    def exists(self):
        return self.path.exists()

@singleton
class Git:

    dirname = '.git'

    def mangle(self, reldir):
        return reldir.parent / f"{reldir.name}.git"

    def pushorclone(self, dest):
        if dest.exists():
            branch, = git.rev_parse.__abbrev_ref.HEAD().splitlines()
            git.push.print(dest.netremotename, branch)
        else:
            git.clone.__bare.print('.', dest.path)
        branches = set(git.branch().splitlines())
        if '  public' in branches:
            currentbranch = {'* master', '* trunk'} & branches
            if currentbranch:
                mainbranch, = (b[2:] for b in currentbranch)
                git.update_ref.print('refs/heads/public', mainbranch)

@singleton
class Rsync:

    dirname = '.rsync'

    def mangle(self, reldir):
        return reldir

    def pushorclone(self, dest):
        lhs = '-avzu', '--exclude', '/.rsync'
        rhs = ".%s" % os.sep, "%s::%s/%s" % (dest.repohost, dest.reponame, dest.reldir)
        rsync.print(*lhs, *rhs)
        os.utime('.rsync')
        lhs += '--del',
        rsync.print(*lhs, '--dry-run', *rhs)
        print("(cd %s && rsync %s %s)" % (Path.cwd(), ' '.join(lhs), ' '.join(rhs)))

def main_hgcommit():
    logging.basicConfig(level = logging.DEBUG, format = "[%(levelname)s] %(message)s")
    config = loadconfig()
    reldir = Path.cwd().relative_to(effectivehome)
    for c in Git, Rsync:
        if Path(c.dirname).exists():
            command = c
            break
    dest = PathDest(config, command.mangle(reldir))
    if dest.check():
        command.pushorclone(dest)
    else:
        log.error("Bad path: %s", dest.clonespath)
