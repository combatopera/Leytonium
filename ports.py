#!/usr/bin/env python3

#HALP Show listen ports of all Corda nodes.

import subprocess, re

def lineport(line):
    return int(re.search(':([0-9]+)', line).group(1))

def minport(lines):
    return min(p for p in (lineport(line) for line in lines) if p >= 10000)

def main():
    def pidstrs():
        for line in subprocess.check_output(['ps', '-ef']).decode().splitlines():
            if 'Corda' in line:
                yield re.search('[0-9]+', line).group()
    pattern = re.compile("(%s)/java" % '|'.join(pidstrs()))
    def g():
        for line in subprocess.check_output(['netstat', '-lnp']).decode().splitlines():
            m = pattern.search(line)
            if m is not None:
                yield int(m.group(1)), line
    nodes = {}
    for pid, line in g():
        try:
            nodes[pid].append(line)
        except KeyError:
            nodes[pid] = [line]
    sep = lambda: None
    for lines in sorted(nodes.values(), key = minport):
        sep()
        for line in sorted(lines, key = lineport):
            print(line)
        sep = print

if '__main__' == __name__:
    main()
