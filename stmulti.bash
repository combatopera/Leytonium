#HALP Short status of all shallow projects in directory.

set -e

IFS=$'\n'

reponame=Seagate3
repo=/mnt/$reponame
effectivehome=$(eval echo ~$SUDO_USER)

function pull {
    [[ pullall = "$(basename "$0")" ]]
}

function push {
    [[ pushall = "$(basename "$0")" ]]
}

function kind {
    printf '%-3s' ${1%task} | cut -c -3
}

function forprojects {
    for d in $(find -mindepth 2 -maxdepth 2 -name $1 | sort); do
        cd ${d%/*}
        echo -n "$(kind $2) "
        $2 ${PWD#$effectivehome/}
        cd - >/dev/null
    done
}

function hgtask {
    echo $1:
    if pull; then
        hg pull $repo/arc/$1 && hg update
    elif push; then
        hgcommit
    else
        hg st
    fi
}

function gittask {
    echo $1:
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
        git status -s
        git remote -v | while read line; do
            if [[ "$line" =~ ^lave$'\t'"$repo/arc/$1.git"' ' ]]; then
                echo Remote lave OK.
            elif [[ "$line" != *$'\tgit@'* ]]; then
                echo Remote is not SSH: "$line"
            fi >&2
        done
        [[ "$(md5sum .git/hooks/post-commit)" = d92ab6d4b18b4bf64976d3bae7b32bd7* ]] || {
            echo Bad hook: post-commit >&2
        }
        git stash list
    fi
}

function rsynctask {
    echo $1:
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

clear
forprojects .hg hgtask
forprojects .git gittask
forprojects .rsync rsynctask
