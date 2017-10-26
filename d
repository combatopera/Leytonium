#!/usr/bin/env python3

#HALP Show local changes.

import subprocess

def main():
    subprocess.run(['clear'], check = True)
    subprocess.run(['git', 'diff'], check = True)

if '__main__' == __name__:
    main()
