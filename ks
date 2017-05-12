#!/bin/bash

#HALP Update the kitchen-sink branch with all that have been published.

set -e

. git_functions

ks=$(githubuser)-kitchen-sink

co $ks

for b in $(git branch -vv | grep '\[origin/' | awk '{ print $1 }'); do

    echo $b >&2

    git merge $b --no-edit

done

touchmsg=touch

[[ $touchmsg = $(git log -1 --pretty=%B) ]] || {

    date >TOUCHME

    git add TOUCHME

    git commit -m $touchmsg

}
