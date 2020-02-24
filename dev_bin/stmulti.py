from lagoon import clear
from pathlib import Path

reponame = 'Seagate3'
repo = Path('/mnt', reponame)
'''
effectivehome=$(eval echo ~$SUDO_USER)

function kind {
    printf '%-3s' ${1%task} | cut -c -3
}
'''

class Project:

    @classmethod
    def forprojects(cls, action):
        '''
        local contextdir="$PWD"
        for d in $(find -mindepth 2 -maxdepth 2 -name $1 | sort); do
            cd ${d%/*}
            echo "$(kind $2) ${PWD#$contextdir/}:"
            $2 ${PWD#$effectivehome/}
            cd - >/dev/null
        '''

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
        '''
        git branch -vv
        git status -s
        checkremotes($PWD, $1)
        [[ "$(md5sum .git/hooks/post-commit)" = d92ab6d4b18b4bf64976d3bae7b32bd7* ]] || {
            echo Bad hook: post-commit >&2
        }
        git stash list
        '''

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
