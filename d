#!/usr/bin/env python3

#HALP Show local changes.

from common import *

def main():
    run(['clear'])
    run(['git', 'diff'])

if '__main__' == __name__:
    main()
