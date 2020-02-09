#HALP Create a kitchen-sink branch.

from dev_bin.common import run, addparents
import os, re

def githubuser():
    with open(os.path.join(os.path.expanduser('~'), '.git-credentials')) as f:
        return re.search('//([^:]+):.*github', f.read()).group(1)

def main_ks():
    master, ks = 'master', 'kitchen-sink'
    run(['git', 'checkout', '-b', ks, master])
    addparents(ks, master, 'controversial/*', "public/%s-*" % githubuser())
