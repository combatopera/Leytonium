from dev_bin.common import run, pb, args

def main_rx():
    'Restore given file to parent branch version.'
    run(['git', 'checkout', pb()] + args())
