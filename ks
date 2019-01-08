#!/usr/bin/env python3

#HALP Create a kitchen-sink branch.

from common import run, addparents
import os, re

def githubuser():
    with open(os.path.join(os.path.expanduser('~'), '.git-credentials')) as f:
        return re.search('//([^:]+):.*github', f.read()).group(1)

def main():
    master, ks = 'master', 'kitchen-sink'
    run(['git', 'checkout', '-b', ks, master])
    addparents(ks, master, 'controversial/*', "public/%s-*" % githubuser())

if '__main__' == __name__:
    main()
