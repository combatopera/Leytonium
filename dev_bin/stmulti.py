from . import checkremotes
from lagoon import clear, co, git, hg, hgcommit, md5sum
from pathlib import Path
import glob, logging, os

log = logging.getLogger(__name__)
reponame = 'Seagate3'
repo = Path('/mnt', reponame)
effectivehome = Path(f"~{os.environ.get('SUDO_USER', '')}").expanduser()

class Project:

    kindwidth = 3
    kindformat = "%%-%ss" % kindwidth

    @classmethod
    def forprojects(cls, action):
        for path in sorted(d.parent for d in Path('.').glob(f"*/{glob.escape(cls.dirname)}")):
            print(cls.kindformat % cls.dirname[1:1 + cls.kindwidth], path)
            getattr(cls(path), action)()

    def __init__(self, path):
        for command in self.commands:
            setattr(self, Path(command.path).name, command.cd(path))
        self.repopath = path.resolve().relative_to(effectivehome)
        self.path = path

class Mercurial(Project):

    dirname = '.hg'
    commands = hg, hgcommit

    def pull(self):
        self.hg.print('pull', repo / 'arc' / self.repopath)
        self.hg.print('update')

    def push(self):
        self.hgcommit.print()

    def status(self):
        self.hg.print('st')

class Git(Project):

    dirname = '.git'
    commands = co, git, hgcommit, md5sum

    def _allbranches(self, task):
        restore, = self.git('rev-parse', '--abbrev-ref', 'HEAD').splitlines()
        for branch in (l[2:] for l in self.git('branch').splitlines()):
            self.co.print(branch)
            task(branch)
        self.co.print(restore)

    def pull(self):
        self._allbranches(lambda branch: self.git.print('pull', '--ff-only', repo / 'arc' / self.repopath, branch))

    def push(self):
        self._allbranches(lambda branch: self.hgcommit.print())

    def status(self):
        self.git.print('branch', '-vv')
        self.git.print('status', '-s')
        if repo.is_dir():
            checkremotes.check(self.path, self.repopath)
            if self.md5sum('.git/hooks/post-commit', check = False).stdout[:32] != 'd92ab6d4b18b4bf64976d3bae7b32bd7':
                log.error('Bad hook: post-commit')
        self.git.print('stash', 'list')

class Rsync(Project):

    dirname = '.rsync'
    commands = ()

    def pull(self):
        '''
        lhs=(rsync -avzu --exclude /.rsync)
        rhs=(lave.local::$reponame/$1/ .)
        ${lhs[@]} ${rhs[@]}
        lhs+=(--del)
        ${lhs[@]} --dry-run ${rhs[@]}
        echo "(cd $PWD && ${lhs[@]} ${rhs[@]})"
        '''

    def push(self):
        '''
        hgcommit
        '''

    def status(self):
        '''
        tput setf 1
        tput bold
        find -newer .rsync
        tput sgr0
        '''

def main(action):
    clear.print()
    for projecttype in Mercurial, Git, Rsync:
        projecttype.forprojects(action)

def main_stmulti():
    'Short status of all shallow projects in directory.'
    main('status')

def main_pullall():
    main('pull')

def main_pushall():
    main('push')
