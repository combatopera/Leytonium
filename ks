#!/bin/bash

#HALP Update the kitchen-sink branch with all that have been published.

set -e

. git_functions

ks=kitchen-sink

function mergeb {
    git merge $b --no-edit
}

function reportb {
    local status="$(mergeb)"
    local conflicts=$(grep -c CONFLICT <<<"$status")
    if [[ $conflicts -eq 0 ]]; then
        echo "$status" >&2
    else
        echo $conflicts $b | tee /dev/stderr
        git reset --hard >/dev/null
    fi
}

function iter {
    local b
    for b in $(publicbranches); do
        echo $b >&2
        if [[ $b = master || $b = $(githubuser)-* ]]; then
            # TODO: Skip commits that haven't been pushed, as I may yet abandon/squash them.
            $1
        else
            echo Skip divergent branch. >&2
        fi
    done
    for b in $(allbranches); do
        [[ $b = controversial-* ]] || continue
        echo $b >&2
        $1
    done
}

function updateks {
    co $ks || git checkout -b $ks master
    while true; do
        iter reportb >/dev/null # Do all automatic merges up-front for accurate conflict counts.
        read conflicts b <<<"$(iter reportb | sort -n | head -1)"
        [[ "$b" ]] || break
        echo Merging: $b >&2
        mergeb
    done
    if [[ $(touchmsg) = $(git log -1 --pretty=%B) ]]; then
        echo No changes, touch not needed. >&2
    else
        touchb
    fi
}

nicely updateks
