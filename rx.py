#HALP Restore given file to parent branch version.

from dev_bin.common import run, pb, args

def main_rx():
    run(['git', 'checkout', pb()] + args())
