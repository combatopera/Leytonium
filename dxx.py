#HALP Short diff from parent branch or of passed-in commit number.

from common import args as getargs, AllBranches, showmenu, pb, stderr, chain

def main_dxx():
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
