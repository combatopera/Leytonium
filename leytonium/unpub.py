from .common import thisbranch
from lagoon import git

def main_unpub():
    'Unpublish this branch.'
    git.push.origin.__delete.print(thisbranch(), check = False) # Idempotent.
    git.branch.__unset_upstream.exec()
