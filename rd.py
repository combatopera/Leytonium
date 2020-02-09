#HALP Run git add on conflicted path, with completion.

from dev_bin.common import chain, args

def main_rd():
    # FIXME: Reject directory args.
    chain(['git', 'add'] + args())
