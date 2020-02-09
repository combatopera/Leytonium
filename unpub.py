#HALP Unpublish this branch.

from common import unchecked_run, thisbranch, chain

def main_unpub():
    unchecked_run(['git', 'push', 'origin', '--delete', thisbranch()]) # Idempotent.
    chain(['git', 'branch', '--unset-upstream'])
