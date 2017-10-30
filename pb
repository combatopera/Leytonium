#!/usr/bin/env python3

#HALP Find parent branch.

from common import *

def pb():
    path = os.path.join(findproject(), infodirname, thisbranch())
    with open(path) as f:
        line, = f.readline().splitlines()
        return line

if '__main__' == __name__:
    print(pb())
