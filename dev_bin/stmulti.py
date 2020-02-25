from . import checkremotes
from lagoon import clear, git
from pathlib import Path
import glob, os

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
            getattr(cls(path.resolve()), action)()

    def __init__(self, path):
        pass

class Mercurial(Project):

    dirname = '.hg'

    def pull(self):
        '''
        hg pull $repo/arc/$1 && hg update
        '''

    def push(self):
        '''
        hgcommit
        '''

    def status(self):
        '''
        hg st
        '''

class Git(Project):

    dirname = '.git'

    def __init__(self, path):
        self.git = git.cd(path)
        self.path = path

    def pull(self):
        '''
        local restore="$(git rev-parse --abbrev-ref HEAD)"
        git branch | cut -c 3- | while read branch; do
            co "$branch"
            git pull --ff-only $repo/arc/$1 "$branch"
        done
        co "$restore"
        '''

    def push(self):
        '''
        local restore="$(git rev-parse --abbrev-ref HEAD)"
        git branch | cut -c 3- | while read branch; do
            co "$branch"
            hgcommit
        done
        co "$restore"
        '''

    def status(self):
        self.git.print('branch', '-vv')
        self.git.print('status', '-s')
        checkremotes.check(self.path, self.path.relative_to(effectivehome))
        '''
        [[ "$(md5sum .git/hooks/post-commit)" = d92ab6d4b18b4bf64976d3bae7b32bd7* ]] || {
            echo Bad hook: post-commit >&2
        }
        '''
        self.git.print('stash', 'list')

class Rsync(Project):

    dirname = '.rsync'

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
