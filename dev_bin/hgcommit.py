from . import effectivehome
from .stmulti import Config
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
        self.clonespath = config.repomount / effectivehome.name
        self.path = self.clonespath / reldir
        self.repohost = config.repohost
        self.reponame = config.reponame
        self.reldir = reldir

    def check(self):
        return checkpath(self.clonespath)

    def exists(self):
        return self.path.exists()

@singleton
class Git:

    def mangle(self, reldir):
        return reldir.parent / f"{reldir.name}.git"

    def pushorclone(self, dest):
        if dest.exists():
            branch, = git('rev-parse', '--abbrev-ref', 'HEAD').splitlines()
            git.push.print(dest.path, branch)
        else:
            git.clone.print('--bare', '.', dest.path)

@singleton
class Rsync:

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
    config = Config.load()
    reldir = Path.cwd().relative_to(effectivehome)
    if Path('.git').exists():
        command = Git
    elif Path('.rsync').exists():
        command = Rsync
    if os.environ.get('LOCAL'):
        return
    dest = PathDest(config, command.mangle(reldir))
    if dest.check():
        command.pushorclone(dest)
    else:
        log.error("Bad path: %s", dest.clonespath)
