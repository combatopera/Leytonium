#HALP Restore given file to parent branch version.

from common import run, pb, args

def main_rx():
    run(['git', 'checkout', pb()] + args())
