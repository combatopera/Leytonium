#HALP Add the top commit to the list of slammed commits.

from common import AllBranches, savecommits

def main_dup():
    savecommits([AllBranches().branchcommits()[0][0]])
