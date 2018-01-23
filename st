#!/usr/bin/env python3

#HALP Show list of branches and outgoing changes.

from common import run, showmenu, UnknownParentException, showexception, unchecked_run, branchcommits, runlines, pb, stripansi, getpublic
import subprocess, re

limit = 20

class Row:

    def __init__(self, line):
        self.name = stripansi(re.search('[\S]+', line).group())
        p = pb(self.name)
        self.parent = '[...]' if p == getpublic(self.name) else p
        self.line = line

def main():
    run(['clear'])
    try:
        rows = [Row(l[2:]) for l in runlines(['git', '-c', 'color.ui=always', 'branch', '-vv'])]
    except subprocess.CalledProcessError:
        run(['ls', '-l', '--color=always'])
        return
    fmt = "%%-%ss %%s" % max(len(r.parent) for r in rows)
    for r in rows:
        print(fmt % (r.parent, r.line))
    try:
        entries = branchcommits()
        showmenu(entries[:limit])
        count = len(entries) - limit
        if count > 0:
            print("(%s more)" % count)
    except UnknownParentException:
        showexception()
    unchecked_run(['git', 'status', '-v'])
    run(['git', 'stash', 'list'])

if '__main__' == __name__:
    main()
