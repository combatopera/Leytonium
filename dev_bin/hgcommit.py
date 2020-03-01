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
        self.drive = config.reponame
        self.reldir = reldir

    def check(self):
        return checkpath(self.clonespath)

    def exists(self):
        return self.path.exists()

@singleton
class Git:

    def mangle(self, reldir):
        return reldir.parent / ("%s.git" % reldir.name)

    def pushorclone(self, dest):
        if dest.exists():
            self.push(dest)
        else:
            git.clone.print('--bare', '.', dest.path)

    def push(self, dest):
        git.push.print(*[] if dest is None else [dest.path, self.currentbranch()])

    @staticmethod
    def currentbranch():
        branch, = git('rev-parse', '--abbrev-ref', 'HEAD').splitlines()
        return branch

@singleton
class Rsync:

    def mangle(self, reldir):
        return reldir

    def pushorclone(self, dest):
        self.push(dest)

    def push(self, dest):
        lhs = '-avzu', '--exclude', '/.rsync'
        rhs = ".%s" % os.sep, "lave.local::%s/%s" % (dest.drive, dest.reldir)
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
