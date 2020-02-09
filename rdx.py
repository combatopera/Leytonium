#HALP Run git rm on conflicted path, with completion.

from dev_bin.common import chain, args

def main_rdx():
    chain(['git', 'rm'] + args())
