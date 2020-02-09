#HALP Merge master into all PRs and carrion.

from dev_bin.common import findproject, nicely, AllBranches, getpublic, stderr, run, runlines, touchmsg, runpy
import os

def merge(b, check = True):
    return runlines(['git', 'merge', b, '--no-edit'], check = check)

def reportornone(b):
    status = merge(b, False)
    conflicts = sum(1 for line in status if 'CONFLICT' in line)
    if conflicts:
        run(['git', 'reset', '--hard'])
        return conflicts, b
    for line in status:
        print(line)

def getreports(branches):
    def g():
        for b in branches:
            r = reportornone(b)
            if r is not None:
                yield r
    return list(g())

def mergeintocurrent(parents):
    while True:
        getreports(parents) # Do all automatic merges up-front for accurate conflict counts.
        reports = getreports(parents)
        if not reports:
            break
        for r in reports:
            stderr("%s %s" % r)
        reports.sort()
        _, b = reports[0]
        stderr("Merging: %s" % b)
        merge(b)

def touchifnecessary():
    if [touchmsg()] == runlines(['git', 'log', '-1', '--pretty=format:%B']):
        stderr('No changes, touch not needed.')
    else:
        runpy(['touchb'])

def ispublished(): # TODO: Really this should check whether PR.
    pb = getpublic()
    return pb is not None and not pb.startswith("origin/%s_" % os.environ['USER'])

def multimerge():
    allbranches = AllBranches()
    remaining = allbranches.names
    branchtoparents = {b: allbranches.parents(b) for b in remaining}
    allparents = {p for parents in branchtoparents.values() for p in parents}
    def update(b):
        run(['git', 'checkout', b])
        parents = branchtoparents[b]
        if b in allparents or ispublished():
            mergeintocurrent(parents)
            if len(parents) > 1: # XXX: Is that right?
                touchifnecessary()
        elif len(parents) > 1:
            raise Exception("Too many parents for rebase: %s" % b)
        else:
            p, = parents
            run(['git', 'rebase', p])
    done = set()
    while remaining:
        stderr("Remaining: %s" % ' '.join(remaining))
        done0 = frozenset(done)
        def g():
            for b in remaining:
                badparents = [p for p in branchtoparents[b] if not (allbranches.isremote(p) or p in done0)]
                if badparents:
                    yield b, badparents
                else:
                    update(b)
                    done.add(b)
        status = list(g())
        remaining2 = [b for b, _ in status]
        if remaining2 == remaining:
            for b, deps in status:
                stderr("%s: %s" % (b, ' '.join(deps)))
            raise Exception("Still remain: %s" % remaining)
        remaining = remaining2

def main_multimerge():
    os.chdir(findproject()) # Don't fail if working directory doesn't exist in some branch.
    nicely(multimerge)
