#HALP Show a commit that was listed by st.

from common import args, showmenu, chain, AllBranches, savedcommits

def main_show():
    items = AllBranches().branchcommits()
    n, = args()
    n = int(n)
    if n > 0:
        commit = showmenu(items, False)[n]
    else:
        saved = savedcommits()
        commit = saved[len(saved) - 1 + n]
    chain(['git', 'show', commit])
