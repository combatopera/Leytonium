#HALP Run git rm on conflicted path, with completion.

from common import chain, args

def main_rdx():
    chain(['git', 'rm'] + args())
