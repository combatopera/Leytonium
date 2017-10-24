#!/bin/bash

#HALP Show list of branches and outgoing changes.

set -e

clear

git branch -vv

. git_functions

lines="$(git cherry -v $(pb) | tac)"
head -10 <<<"$lines"
count=$(tail -n +11 <<<"$lines" | wc -l)
[[ $count -eq 0 ]] || echo $count more

git status -v

git stash list
