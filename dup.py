#HALP Add the top commit to the list of slammed commits.

from dev_bin.common import AllBranches, savecommits

def main_dup():
    savecommits([AllBranches().branchcommits()[0][0]])
