#!/bin/bash

#HALP Update the kitchen-sink branch with all that have been published.

set -e

. git_functions

ks=$(githubuser)-kitchen-sink

function updateks {
    co $ks || git checkout -b $ks master
    local b
    for b in $(git branch -vv | grep '\[origin/' | awk '{ print $1 }'); do
        echo $b >&2
        if [[ $b = master || $b = $(githubuser)-* ]]; then
            git merge $b --no-edit
        else
            echo Skip divergent branch. >&2
        fi
    done
    if [[ $(touchmsg) = $(git log -1 --pretty=%B) ]]; then
        echo No changes, touch not needed. >&2
    else
        touchb
    fi
}

nicely updateks
