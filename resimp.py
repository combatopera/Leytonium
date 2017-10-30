#!/usr/bin/env python3

#HALP Resolve conflicts in imports in one file.

from common import *
import itertools

def main():
    path, = args()
    output = []
    chunks = [0]
    def outer(line):
        if line.startswith('<<<<<<< '):
            return Conflict(line)
        else:
            output.append(line)
    class Conflict:
        def __init__(self, intro):
            self.current = self.upper = []
            self.lower = []
            self.intro = intro
        def __call__(self, line):
            if line.startswith('>>>>>>> '):
                for l in itertools.chain(self.upper, self.lower):
                    if not l.startswith('import '):
                        break
                else:
                    output.extend(self.upper)
                    output.extend(self.lower)
                    chunks[0] += 1
                    return outer
                output.append(self.intro)
                output.extend(self.upper)
                output.append(self.sep)
                output.extend(self.lower)
                output.append(line)
                return outer
            elif line.splitlines()[0] == '=======':
                self.sep = line
                self.current = self.lower
            else:
                self.current.append(line)
    handler = outer
    with open(path) as f:
        for line in f:
            newhandler = handler(line)
            if newhandler is not None: handler = newhandler
    if chunks[0]:
        with open(path, 'w') as g:
            for line in output:
                g.write(line)
        print("Merged %s chunks of imports in: %s" % (chunks[0], path), file = sys.stderr)

if '__main__' == __name__:
    main()
