from .common import pb, args as getargs, stderr, AllBranches, showmenu
from lagoon import git

def main_dx():
    'Diff from parent branch.'
    parent = pb()
    stderr("Parent branch: %s" % parent)
    git.diff._M25.exec(*getargs(), parent)

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
    git.diff._M25.__name_status.exec(*commits)
