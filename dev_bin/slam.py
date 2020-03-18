from .common import AllBranches, args as getargs, showmenu, chain, pb, savecommits, savedcommits

def main_slam():
    'Reset branch to given commit number.'
    items = AllBranches().branchcommits() + [[pb(), '']]
    args = getargs()
    if '-f' == args[0]:
        save = False
        n, = args[1:]
    else:
        save = True
        n, = args
    n = int(n)
    if n > 0:
        commit = showmenu(items, False)[n - 1] + '^'
        if save:
            savecommits([item[0] for item in items[:n - 1]])
        chain(['git', 'reset', '--hard', commit])
    else:
        saved = savedcommits()
        i = len(saved) - 1 + n
        commit = saved[i]
        if save:
            savecommits(saved[:i], True)
        chain(['git', 'cherry-pick'] + list(reversed(saved[i:])))
