from dev_bin.common import AllBranches, savecommits

def main_dup():
    'Add the top commit to the list of slammed commits.'
    savecommits([AllBranches().branchcommits()[0][0]])
