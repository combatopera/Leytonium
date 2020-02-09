#HALP Diff from public branch.

from common import getpublic, args, chain, stderr

def main_dp():
    parent = getpublic()
    stderr("Public branch: %s" % parent)
    chain(['git', 'diff', '-M25'] + args() + [parent])
