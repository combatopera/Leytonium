#!/usr/bin/env python3

#HALP Create a kitchen-sink branch.

from common import run, githubuser, addparents

def main():
    master, ks = 'master', 'kitchen-sink'
    run(['git', 'checkout', '-b', ks, master])
    addparents(ks, master, 'controversial-*', "public/%s-*" % githubuser())

if '__main__' == __name__:
    main()
