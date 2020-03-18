from .common import AllBranches, args as getargs, showmenu, chain, pb, savecommits, savedcommits, findproject, thisbranch, infodirname, os, stderr

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

def main_unslam():
    'Cherry-pick commits lost in a previous slam.'
    path = os.path.join(findproject(), infodirname, "%s slammed" % thisbranch())
    with open(path) as f:
        commits = f.read().splitlines()
    commits.reverse()
    command = ['git', 'cherry-pick'] + commits
    stderr("Command: %s" % ' '.join(command))
    os.remove(path)
    chain(command)
