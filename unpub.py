from dev_bin.common import unchecked_run, thisbranch, chain

def main_unpub():
    'Unpublish this branch.'
    unchecked_run(['git', 'push', 'origin', '--delete', thisbranch()]) # Idempotent.
    chain(['git', 'branch', '--unset-upstream'])
