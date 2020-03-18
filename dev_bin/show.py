from .common import args, showmenu, AllBranches, savedcommits
from lagoon import git

def main_show():
    'Show a commit that was listed by st.'
    items = AllBranches().branchcommits()
    n, = args()
    n = int(n)
    if n > 0:
        commit = showmenu(items, False)[n]
    else:
        saved = savedcommits()
        commit = saved[len(saved) - 1 + n]
    git.show.exec(commit)
