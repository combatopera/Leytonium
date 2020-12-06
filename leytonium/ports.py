from lagoon import netstat, ps
import re

def lineport(line):
    return int(re.search(':([0-9]+)', line).group(1))

def minport(lines):
    return min(p for p in (lineport(line) for line in lines) if p >= 10000)

def main_ports():
    'Show listen ports of all Corda nodes.'
    def pidstrs():
        for line in ps._ef().splitlines():
            if 'Corda' in line:
                yield re.search('[0-9]+', line).group()
    pattern = re.compile("(%s)/java" % '|'.join(pidstrs()))
    def g():
        for line in netstat._lnp.splitlines():
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