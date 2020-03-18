from dev_bin.common import thisbranch, chain
import subprocess

def main_unpub():
    'Unpublish this branch.'
    subprocess.run(['git', 'push', 'origin', '--delete', thisbranch()]) # Idempotent.
    chain(['git', 'branch', '--unset-upstream'])
