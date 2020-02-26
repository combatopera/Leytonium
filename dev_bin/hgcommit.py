from diapyr.util import singleton
from lagoon import git
import os, subprocess, multiprocessing as mp, queue, logging

log = logging.getLogger(__name__)
projectsdir = os.path.expanduser('~' + os.environ.get('SUDO_USER', ''))

def trypath(path, q):
    q.put(subprocess.call(['ls', path], stdout = subprocess.DEVNULL)) # Must actually attempt NFS communication.

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

    def __init__(self, drive, reldir):
        self.clonespath = "/mnt/%s/arc" % drive
        self.path = os.path.join(self.clonespath, reldir)
        self.drive = drive
        self.reldir = reldir

    def check(self):
        return checkpath(self.clonespath)

    def exists(self):
        return os.path.exists(self.path)

@singleton
class Git:

    def mangle(self, reldir): return reldir + '.git'

    def pushorclone(self, dest):
        if dest.exists():
            self.push(dest)
        else:
            subprocess.check_call(['git', 'clone', '--bare', '.', dest.path])

    def push(self, dest):
        command = ['git', 'push']
        if dest is not None:
            command += [dest.path, self.currentbranch()]
        subprocess.check_call(command)

    @staticmethod
    def currentbranch():
        branch, = git('rev-parse', '--abbrev-ref', 'HEAD').splitlines()
        return branch

@singleton
class Rsync:

    def mangle(self, reldir): return reldir

    def pushorclone(self, dest):
        self.push(dest)

    def push(self, dest):
        lhs = ['rsync', '-avzu', '--exclude', '/.rsync']
        rhs = [".%s" % os.sep, "lave.local::%s/%s" % (dest.drive, dest.reldir)]
        subprocess.check_call(lhs + rhs)
        os.utime('.rsync')
        lhs += ['--del']
        subprocess.check_call(lhs + ['--dry-run'] + rhs)
        print("(cd %s && %s %s)" % (os.getcwd(), ' '.join(lhs), ' '.join(rhs)))

def main_hgcommit():
    logging.basicConfig(level = logging.DEBUG, format = "[%(levelname)s] %(message)s")
    projectdir = os.getcwd()
    if not projectdir.startswith(projectsdir + os.sep):
        raise Exception("Not under %s: %s" % (projectsdir, projectdir))
    reldir = projectdir[len(projectsdir + os.sep):]
    if os.path.exists('.git'):
        command = Git
    elif os.path.exists('.rsync'):
        command = Rsync
    if os.environ.get('LOCAL'):
        return
    dest = PathDest('Seagate3', command.mangle(reldir))
    if dest.check():
        command.pushorclone(dest)
    else:
        log.error("Bad path: %s", dest.clonespath)
