reponame=Seagate3
repo=/mnt/$reponame
effectivehome=$(eval echo ~$SUDO_USER)

function kind {
    printf '%-3s' ${1%task} | cut -c -3
}

function forprojects {
    local contextdir="$PWD"
    for d in $(find -mindepth 2 -maxdepth 2 -name $1 | sort); do
        cd ${d%/*}
        echo "$(kind $2) ${PWD#$contextdir/}:"
        $2 ${PWD#$effectivehome/}
        cd - >/dev/null
    done
}

function hgtask {
    if pull; then
        hg pull $repo/arc/$1 && hg update
    elif push; then
        hgcommit
    else
        hg st
    fi
}

function gittask {
    if pull; then
        local restore="$(git rev-parse --abbrev-ref HEAD)"
        git branch | cut -c 3- | while read branch; do
            co "$branch"
            git pull --ff-only $repo/arc/$1 "$branch"
        done
        co "$restore"
    elif push; then
        local restore="$(git rev-parse --abbrev-ref HEAD)"
        git branch | cut -c 3- | while read branch; do
            co "$branch"
            hgcommit
        done
        co "$restore"
    else
        git branch -vv
        git status -s
        checkremotes($PWD, $1)
        [[ "$(md5sum .git/hooks/post-commit)" = d92ab6d4b18b4bf64976d3bae7b32bd7* ]] || {
            echo Bad hook: post-commit >&2
        }
        git stash list
    fi
}

function rsynctask {
    if pull; then
        lhs=(rsync -avzu --exclude /.rsync)
        rhs=(lave.local::$reponame/$1/ .)
        ${lhs[@]} ${rhs[@]}
        lhs+=(--del)
        ${lhs[@]} --dry-run ${rhs[@]}
        echo "(cd $PWD && ${lhs[@]} ${rhs[@]})"
    elif push; then
        hgcommit
    else
        tput setf 1
        tput bold
        find -newer .rsync
        tput sgr0
    fi
}

def main(action):
    clear
    forprojects .hg hgtask
    forprojects .git gittask
    forprojects .rsync rsynctask

def main_stmulti():
    'Short status of all shallow projects in directory.'
    main('status')

def main_pullall():
    main('pull')

def main_pushall():
    main('push')
