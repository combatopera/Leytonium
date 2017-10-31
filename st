#!/usr/bin/env python3

#HALP Show list of branches and outgoing changes.

from common import *

limit = 20

def main():
    run(['clear'])
    run(['git', 'branch', '-vv'])
    try:
        parent = pb()
        lines = runlines(['git', 'cherry', '-v', parent])
        lines.reverse()
        entries = [line.split(' ', 2)[1:] for line in lines[:limit]]
        showmenu(entries)
        count = len(lines) - limit
        if count > 0:
            print("(%s more)" % count)
    except UnknownParentException:
        showexception()
    subprocess.run(['git', 'status', '-v']) # Ignore returncode.
    run(['git', 'stash', 'list'])

if '__main__' == __name__:
    main()
