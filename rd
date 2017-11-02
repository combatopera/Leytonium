#!/usr/bin/env python3

#HALP Run git add on conflicted path, with completion.

from common import *

def main():
    chain(['git', 'add'] + args())

if '__main__' == __name__:
    main()
