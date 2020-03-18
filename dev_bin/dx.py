from .common import pb, args as getargs, chain, stderr, AllBranches, showmenu

def main_dx():
    'Diff from parent branch.'
    parent = pb()
    stderr("Parent branch: %s" % parent)
    chain(['git', 'diff', '-M25'] + getargs() + [parent])

def main_dxx():
    'Short diff from parent branch or of passed-in commit number.'
    args = getargs()
    if args:
        n, = args
        n = int(n)
        commit = showmenu(AllBranches().branchcommits(), False)[n]
        commits = ["%s^" % commit, commit]
    else:
        parent = pb()
        stderr("Parent branch: %s" % parent)
        commits = [parent]
    chain(['git', 'diff', '-M25', '--name-status'] + commits)
