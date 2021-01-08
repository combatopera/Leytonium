set -e

path=$(gmktemp --suffix .html || mktemp)

function cleanup {
    rm -fv $path
}

trap cleanup EXIT

pandoc -T "$(basename "${@: -1}")" --toc "$@" >$path

$(which open || which firefox) $path

while true; do sleep 1; done
