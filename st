#!/usr/bin/env python3

#HALP Show list of branches and outgoing changes.

from common import run, showmenu, UnknownParentException, showexception, unchecked_run, runlines, stripansi, getpublic, savedcommits, AllBranches
import subprocess, re

limit = 20

class Row:

    def __init__(self, allbranches, line):
        name = stripansi(re.search('[\S]+', line).group())
        if '(no' == name:
            self.parent = '(void)'
        else:
            parents = allbranches.parents(name)
            if parents:
                self.parent = '[...]' if parents[0] == getpublic(name) else parents[0]
                if len(parents) > 1:
                    self.parent += "+%s" % (len(parents) - 1)
            else:
                self.parent = '<!>'
        self.line = line

def main():
    run(['clear'])
    try:
        allbranches = AllBranches()
    except subprocess.CalledProcessError:
        run(['ls', '-l', '--color=always'])
        return
    rows = [Row(allbranches, l[2:]) for l in runlines(['git', '-c', 'color.ui=always', 'branch', '-vv'])]
    fmt = "%%-%ss %%s" % max(len(r.parent) for r in rows)
    for r in rows:
        print(fmt % (r.parent, r.line))
    for c in savedcommits():
        print(c)
    try:
        entries = allbranches.branchcommits()
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
