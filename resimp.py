#HALP Resolve conflicts in imports and adjacent-line conflicts.

from common import stderr, findproject, runlines
import itertools, os, re

def resimp(path):
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
            handler = handler(line) or handler
    if chunks[0]:
        with open(path, 'w') as g:
            for line in output:
                g.write(line)
        stderr("[%s] Merged %s chunks of imports." % (path, chunks[0]))

def getconflictinfos(path):
    conflictinfos = []
    def outer(line):
        if line.startswith('+<<<<<<< '):
            return ConflictInfo()
    class ConflictInfo:
        def __init__(self):
            self.current = self.upper = []
            self.lower = []
        def __call__(self, line):
            if line.startswith('+>>>>>>> '):
                conflictinfos.append(self)
                return outer
            elif line.splitlines()[0] == '+=======':
                self.current = self.lower
            else:
                self.current.append(line)
        def shape(self):
            return [''.join(l[0] for l in part) for part in [self.upper, self.lower]]
    handler = outer
    for line in runlines(['git', 'diff', '--base', '--', path], keepends = True):
        handler = handler(line) or handler
    return conflictinfos

def resadj(path):
    conflictinfos = getconflictinfos(path)
    output = []
    resolved = [0]
    def outer(line):
        if line.startswith('<<<<<<< '):
            info = conflictinfos.pop(0) # FIXME: Pop from empty list has happened! Suspect when both sides added the path so there is no base.
            cls = BlankPlusPlusBlank.forshape(info.shape()) or PassConflict
            return cls(line)
        else:
            output.append(line)
    class PassConflict:
        def __init__(self, intro):
            output.append(intro)
        def __call__(self, line):
            output.append(line)
            if line.startswith('>>>>>>> '):
                return outer
    class BlankPlusPlusBlank:
        shapepatterns = [re.compile(s) for s in [' +[+]+', '[+]+ +']]
        @classmethod
        def forshape(cls, shape):
            for p, s in zip(cls.shapepatterns, shape):
                if p.fullmatch(s) is None:
                    return
            return lambda intro: cls(shape, intro)
        def __init__(self, shape, intro):
            self.currentshape = self.uppershape = list(shape[0])
            self.lowershape = list(shape[1])
            self.current = self.upper = []
            self.lower = []
        def __call__(self, line):
            if line.startswith('>>>>>>> '):
                output.extend(self.lower)
                output.extend(self.upper)
                resolved[0] += 1
                return outer
            elif line.splitlines()[0] == '=======':
                self.currentshape = self.lowershape
                self.current = self.lower
            elif '+' == self.currentshape.pop(0):
                self.current.append(line)
    handler = outer
    with open(path) as f:
        for line in f:
            handler = handler(line) or handler
    if resolved[0]:
        with open(path, 'w') as g:
            for line in output:
                g.write(line)
        stderr("[%s] Auto-resolved %s adjacent-line conflicts." % (path, resolved[0]))

def main_resimp():
    os.chdir(findproject()) # Paths below are relative to project root.
    for path in runlines(['git', 'diff', '--name-only', '--diff-filter=U']):
        for task in resimp, resadj:
            task(path)
