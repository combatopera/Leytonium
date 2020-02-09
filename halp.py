#HALP You're looking at it!

import os

prefix = '#HALP '

def main_halp():
    halps = []
    dirpath = os.path.dirname(__file__)
    for script in sorted(os.listdir(dirpath)):
        path = os.path.join(dirpath, script)
        if script.startswith('.') or os.path.islink(path) or os.path.isdir(path):
            continue
        with open(path) as f:
            for line in f:
                if line.startswith(prefix):
                    line, = line.splitlines()
                    halps.append((script, line[len(prefix):]))
                    break
    format = "%%-%ss %%s" % max(len(halp[0]) for halp in halps)
    for halp in halps:
        print(format % halp)
