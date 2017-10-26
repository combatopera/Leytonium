#!/bin/bash

#HALP Show list of branches and outgoing changes.

set -e

clear

git branch -vv

. git_functions

lines="$(git cherry -v $(pb) | tac | while read _ rest; do echo "$rest"; done)"
limit=20
function recents {
    head -$limit <<<"$lines"
}
showmenu recents >/dev/null
count=$(tail -n +$((limit+1)) <<<"$lines" | wc -l)
[[ $count -eq 0 ]] || echo "($count more)"

git status -v

git stash list
