from .common import thisbranch, chain
from lagoon import git

def main_unpub():
    'Unpublish this branch.'
    git.push.origin.__delete.print(thisbranch(), check = False) # Idempotent.
    chain(['git', 'branch', '--unset-upstream'])
