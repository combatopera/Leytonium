#!/bin/bash

#HALP Update the kitchen-sink branch with all that have been published.

set -e

. git_functions

ks=kitchen-sink

function mergeb {
    git merge $b --no-edit
}

function updateks {
    co $ks || git checkout -b $ks master
    local b
    # TODO LATER: This permutation may raise conflicts while some other would not.
    for b in $(publicbranches); do
        echo $b >&2
        if [[ $b = master || $b = $(githubuser)-* ]]; then
            # TODO: Skip commits that haven't been pushed, as I may yet abandon/squash them.
            mergeb
        else
            echo Skip divergent branch. >&2
        fi
    done
    for b in $(allbranches); do
        [[ $b = controversial-* ]] || continue
        echo $b >&2
        mergeb
    done
    if [[ $(touchmsg) = $(git log -1 --pretty=%B) ]]; then
        echo No changes, touch not needed. >&2
    else
        touchb
    fi
}

nicely updateks
