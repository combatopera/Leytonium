#!/bin/bash

#HALP Find parent branch.

set -e

function tip {
    git cherry $root $1 | tail -1 | cut -c 3-
}

root=master

. git_functions

current=$(thisbranch)

echo Current branch: $current >&2

cdtocorda

[[ -e ".pb/$current" ]] && {
    cat .pb/$current
    exit
}

for pub in $(publicbranches); do
    [[ $current = $pub ]] && {
        parent=$root
        break
    }
done

[[ "$parent" ]] || parent=$(git cherry $root | tac | while read _ id; do

    branches=($(git branch --contains $id | grep -v '^[*]' || true))

    parents=($(for b in ${branches[@]}
        do if [[ $id = $(tip $b) ]]
            then echo $b
        else
            echo Changed since fork: $b >&2
        fi
    done))

    [[ 0 = ${#parents[@]} ]] && continue

    [[ 1 = ${#parents[@]} ]] || {
        echo Too many parents: ${parents[@]} >&2
        exit 1
    }

    echo ${parents[0]}

    break

done)

echo ${parent:-$root}
