from .common import nicely, publicbranches
from lagoon import git

def main_autopull():
    'Pull master and releases with automatic stash and switch.'
    def pullthem():
        for b in publicbranches():
            git.checkout.print(b)
            git.pull.print()
    nicely(pullthem)
