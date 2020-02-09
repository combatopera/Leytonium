#HALP Cherry-pick commits lost in a previous slam.

from common import findproject, thisbranch, infodirname, chain, os, stderr

def main_unslam():
    path = os.path.join(findproject(), infodirname, "%s slammed" % thisbranch())
    with open(path) as f:
        commits = f.read().splitlines()
    commits.reverse()
    command = ['git', 'cherry-pick'] + commits
    stderr("Command: %s" % ' '.join(command))
    os.remove(path)
    chain(command)