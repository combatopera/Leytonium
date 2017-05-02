#!/bin/bash

#HALP Find parent branch.

set -e

function tip {
    git cherry $root $1 | tail -1 | cut -c 3-
}

root=master

current=$(git branch | grep '^[*]' | cut -c 3-)

echo Current branch: $current >&2

parent=$(git cherry $root | tac | while read _ id; do

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
