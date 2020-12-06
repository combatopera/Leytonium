from .common import getpublic, args, stderr
from lagoon import git

def main_dp():
    'Diff from public branch.'
    parent = getpublic()
    stderr("Public branch: %s" % parent)
    git.diff._M25.exec(*args(), parent)

def main_pd():
    'Diff from public branch, the other way.'
    parent = getpublic()
    stderr("Public branch: %s" % parent)
    git.diff._M25.exec(*args(), 'HEAD', parent)
