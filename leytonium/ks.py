from .common import addparents
from lagoon import git
import os, re

def githubuser():
    with open(os.path.join(os.path.expanduser('~'), '.git-credentials')) as f:
        return re.search('//([^:]+):.*github', f.read()).group(1)

def main_ks():
    'Create a kitchen-sink branch.'
    master, ks = 'master', 'kitchen-sink'
    git.checkout._b.print(ks, master)
    addparents(ks, master, 'controversial/*', "public/%s-*" % githubuser())
