from .common import pb, args, chain, stderr

def main_dx():
    'Diff from parent branch.'
    parent = pb()
    stderr("Parent branch: %s" % parent)
    chain(['git', 'diff', '-M25'] + args() + [parent])
