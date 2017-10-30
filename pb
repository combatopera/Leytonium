#!/usr/bin/env python3

#HALP Find parent branch.

from common import *

def pb():
    path = os.path.join(findproject(), infodirname, thisbranch())
    if os.path.exists(path):
        with open(path) as f:
            line = f.readline()
    else:
        line = run(['git', 'rev-list', '--max-parents=0', 'HEAD'], stdout = subprocess.PIPE).stdout.decode()
    line, = line.splitlines()
    return line

if '__main__' == __name__:
    print(pb())
