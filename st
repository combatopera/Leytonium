#!/usr/bin/env pyven

#HALP Show list of branches and outgoing changes.

from common import run, showmenu, UnknownParentException, showexception, unchecked_run, runlines, stripansi, getpublic, savedcommits, AllBranches, highlight, findproject, infodirname
from termcolor import colored
from pathlib import Path
import subprocess, re, tempfile, aridity, yaml

limit = 20

class Row:

    def __init__(self, allbranches, line):
        name = stripansi(re.search('[\S]+', line).group())
        if '(no' == name:
            self.parent = '(void)'
        else:
            parents = allbranches.parents(name)
            if parents:
                self.parent = '[...]' if parents[0] == getpublic(name) else parents[0]
                if len(parents) > 1:
                    self.parent += "+%s" % (len(parents) - 1)
            else:
                self.parent = '<!>'
        self.line = line

    def branch(self):
        return self.line[:self.line.index(' ')]

    def colorline(self, ispr):
        return colored(self.line, 'green', attrs = ['reverse']) if ispr else self.line

def title(commit):
    return runlines(['git', 'log', '-n', '1', '--pretty=format:%B', commit])[0]

def getprstatuses(branches):
    context = aridity.Context()
    with aridity.Repl(context) as repl:
        repl.printf(". %s", Path.home() / '.settings.arid')
    org = context.resolved('organization').unravel()
    projectdir = Path(findproject()).resolve()
    cachepath = projectdir / infodirname / 'cache.yml'
    if cachepath.exists():
        with cachepath.open() as f:
            cache = yaml.safe_load(f)
    else:
        cache = {}
    with tempfile.NamedTemporaryFile() as cookiesfile:
        subprocess.run([str(Path(__file__).parent / 'extract_cookies.sh')], stdout = cookiesfile, check = True)
        for branch, wget in zip(branches, [None if branch in cache else subprocess.Popen(['wget', '-q', '-O', '-', "https://github.com/%s/%s/tree/%s" % (org, projectdir.name, branch), '--load-cookies', cookiesfile.name], stdout = subprocess.PIPE) for branch in branches]):
            if wget is not None:
                cache[branch] = 'View #' in wget.communicate()[0].decode()
            yield cache[branch]
    cachepath.parent.mkdir(exist_ok = True)
    with cachepath.open('w') as f:
        yaml.dump(cache, f)

def main():
    run(['clear'])
    try:
        allbranches = AllBranches()
    except subprocess.CalledProcessError:
        run(['ls', '-l', '--color=always'])
        return
    prstatuses = getprstatuses(allbranches.names)
    rows = [Row(allbranches, l[2:]) for l in runlines(['git', '-c', 'color.ui=always', 'branch', '-vv'])]
    fmt = "%%-%ss %%s" % max(len(r.parent) for r in rows)
    for r, ispr in zip(rows + [None], prstatuses):
        print(fmt % (r.parent, r.colorline(ispr)))
    saved = savedcommits()
    showmenu([(c, title(c)) for c in saved], xform = lambda i: i - len(saved) + 1, print = highlight)
    try:
        entries = allbranches.branchcommits()
        showmenu(entries[:limit])
        count = len(entries) - limit
        if count > 0:
            print("(%s more)" % count)
    except UnknownParentException:
        showexception()
    unchecked_run(['git', 'status', '-v'])
    run(['git', 'stash', 'list'])

if '__main__' == __name__:
    main()
