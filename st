#!/usr/bin/env python3

#HALP Show list of branches and outgoing changes.

from common import run, showmenu, UnknownParentException, showexception, unchecked_run, branchcommits, runlines
import subprocess

limit = 20

def main():
    run(['clear'])
    try:
        lines = runlines(['git', '-c', 'color.ui=always', 'branch', '-vv'])
    except subprocess.CalledProcessError:
        run(['ls', '-l', '--color=always'])
        return
    for line in lines:
        print(line)
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
