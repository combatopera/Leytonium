set -ex

. "$GIT_FUNCTIONS"

[[ "$1" != '-f' && "$(dxx)" ]] && {
    echo 'Unmerged changes!' >&2
    exit 1
}

git rebase --abort || true

[[ "$(git status --porcelain)" ]] && abandon

todrop=$(thisbranch)

unset b

v="$(allbranches)"

for next in $v $v; do

    [[ $b = $todrop ]] && break

    b=$next

done

co $next

git branch -D $todrop

cdtoproject

rm -fv .pb/$todrop
