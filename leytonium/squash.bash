set -e

base=$(pb)

ids=($(git cherry $base | tac | while read _ id; do echo $id; done))

function commitmessage {
    git log -n 1 --pretty=format:%B "$@"
}

function cherry {
    local id
    for id in ${ids[@]}; do
        echo $id "$(commitmessage $id | head -1)"
    done
}

. "$(git-functions-path)"

menu cherry Which commit should absorb all newer commits

index=$((MENU_NUMBER-1))

id=${ids[$index]}

git reset --hard $id

git cherry-pick $(for i in $(seq $((index-1)) -1 0); do echo ${ids[$i]}; done)

git reset --soft $id~1

message="$(for i in $(seq $((index)) -1 0); do echo "$((index-i+1)). $(commitmessage ${ids[$i]})"; done)"

git commit -em "$message"
