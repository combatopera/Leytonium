from dev_bin.common import thisbranch, pb, AllBranches, runpy, run, addparents

def main_prepare():
    'Create a master-based branch from this non-master-based one.'
    master = 'master'
    parent = pb()
    if parent == master:
        raise Exception("Parent is already %s!" % master)
    name = thisbranch()
    allbranches = AllBranches()
    commits = [commit for commit, _ in allbranches.branchcommits(name)]
    runpy(['ren', "%s.bak" % name])
    run(['git', 'checkout', '-b', name, master])
    addparents(name, master)
    run(['git', 'cherry-pick'] + commits)
