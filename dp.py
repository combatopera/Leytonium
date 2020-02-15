from dev_bin.common import getpublic, args, chain, stderr

def main_dp():
    'Diff from public branch.'
    parent = getpublic()
    stderr("Public branch: %s" % parent)
    chain(['git', 'diff', '-M25'] + args() + [parent])
