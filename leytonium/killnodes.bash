set -ex

kill "$@" $(ps -ef | egrep '[C]orda|[I]rsDemoWebApplication' | awk '{ print $2 }')
