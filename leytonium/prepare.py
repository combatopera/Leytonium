from .common import thisbranch, pb, AllBranches, addparents
from lagoon import git, ren

def main_prepare():
    'Create a master-based branch from this non-master-based one.'
    master = 'master'
    parent = pb()
    if parent == master:
        raise Exception("Parent is already %s!" % master)
    name = thisbranch()
    allbranches = AllBranches()
    commits = [commit for commit, _ in allbranches.branchcommits(name)]
    ren.print("%s.bak" % name)
    git.checkout._b.print(name, master)
    addparents(name, master)
    git.cherry_pick.print(*commits)
