#HALP Diff from parent branch.

from dev_bin.common import pb, args, chain, stderr

def main_dx():
    parent = pb()
    stderr("Parent branch: %s" % parent)
    chain(['git', 'diff', '-M25'] + args() + [parent])
