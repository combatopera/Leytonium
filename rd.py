from dev_bin.common import chain, args

def main_rd():
    'Run git add on conflicted path, with completion.'
    # FIXME: Reject directory args.
    chain(['git', 'add'] + args())
