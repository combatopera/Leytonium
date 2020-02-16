function summary {
    git log --pretty="%an %ae%n%cn %ce" | sort -u
}

summary

git filter-branch --env-filter '

if [ "$GIT_AUTHOR_NAME" = "Andrzej Cichocki" ]; then
    GIT_AUTHOR_EMAIL=andrzej.cichocki@gmail.com
fi

if [ "$GIT_COMMITTER_NAME" = "Andrzej Cichocki" ]; then
    GIT_COMMITTER_EMAIL=andrzej.cichocki@gmail.com
fi

' -- --all

summary
