#!/usr/bin/env python3

#HALP Update the kitchen-sink branch with all that have been published.

from common import run, findproject, nicely, runpy, showexception, runlines, stderr, pb, allbranches, githubuser, publicbranches, touchmsg
import os

def merge(b):
    return runlines(['git', 'merge', b, '--no-edit'])

def report(b):
    status = merge(b)
    conflicts = sum(1 for line in status if 'CONFLICT' in line)
    if not conflicts:
        for line in status:
            print(line)
    else:
        result = conflicts, b
        stderr("%s %s" % result)
        run(['git', 'reset', '--hard'])
        return result

def iter(task):
    prefix = "%s-" % githubuser()
    for b in publicbranches():
        stderr(b)
        if b == 'master' or (b.startswith(prefix) and 'master' == pb(b)):
            # TODO: Use branch name if it's the same as this commit.
            b, = runlines(['git', 'rev-parse', "origin/%s" % b]) # Skip unpushed commits, as I may yet undo them.
            yield task(b)
        else:
            stderr('Skip divergent branch.')
    for b in allbranches():
        if b.startswith('controversial-'):
            stderr(b)
            yield task(b)

def updateks():
    ks = 'kitchen-sink'
    try:
        runpy(['co', ks])
    except:
        showexception()
        run(['git', 'checkout', '-b', ks, 'master'])
    while True:
        for _ in iter(report): pass # Do all automatic merges up-front for accurate conflict counts.
        reports = sorted(r for r in iter(report) if r is not None)
        if not reports:
            break
        _, b = reports[0]
        stderr("Merging: %s", b)
        merge(b)
    if [touchmsg()] == runlines(['git', 'log', '-1', '--pretty=format:%B']):
        stderr('No changes, touch not needed.')
    else:
        runpy(['touchb'])

def main():
    os.chdir(findproject()) # XXX: Why?
    nicely(updateks)

if '__main__' == __name__:
    main()
