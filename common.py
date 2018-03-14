import subprocess, os, sys, traceback, re, collections, importlib.machinery, termcolor

infodirname = '.pb'
publicprefix = 'public/'

def runpy(command, **kwargs):
    name = command[0]
    m = importlib.machinery.SourceFileLoader(name, os.path.join(os.path.dirname(__file__), name)).load_module()
    sys.argv[1:] = command[1:]
    m.main(**kwargs)

class UnknownParentException(Exception): pass

def stderr(*args, **kwargs):
    return termcolor.cprint(*args + ('red',), file = sys.stderr, **kwargs)

def addparents(branch, *parents, clobber = False):
    path = os.path.join(findproject(), infodirname, branch) # Note branch may contain slashes.
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, 'w' if clobber else 'a') as f:
        for p in parents:
            print(p, file = f)

def savecommits(commits):
    path = os.path.join(findproject(), infodirname, "%s slammed" % thisbranch())
    os.makedirs(os.path.dirname(path), exist_ok = True)
    with open(path, 'a') as f:
        for c in commits:
            print(c, file = f)

def savedcommits():
    path = os.path.join(findproject(), infodirname, "%s slammed" % thisbranch())
    if not os.path.exists(path):
        return []
    with open(path) as f:
        return f.read().splitlines()

def pb(b = None):
    if b is None:
        b = thisbranch()
    path = os.path.join(findproject(), infodirname, b)
    if not os.path.exists(path):
        raise UnknownParentException(b)
    with open(path) as f:
        return f.readline().splitlines()[0]

class AllBranches:

    def published(self, name):
        try:
            lines = runlines(['git', 'rev-parse', "origin/%s" % name], stderr = subprocess.DEVNULL)
        except:
            return None
        published, = lines # May be a merge.
        # Find parent of the first unpublished non-merge commit:
        nonmerges = set(id for id, _ in self.branchcommits(name))
        allcommits = runlines(['git', 'log', '--format=%H', name])
        mergeableindex = 0
        for i, commit in enumerate(allcommits):
            if commit == published:
                return allcommits[mergeableindex] if mergeableindex else name
            if commit in nonmerges:
                mergeableindex = i + 1
        return published # What commit is this?

    def __init__(self):
        self.names = [line[2:] for line in runlines(['git', 'branch'])]
        self.remotenames = set(runlines(['git', 'remote']))

    def matching(self, glob):
        regex = re.compile('.*'.join(re.escape(text) for text in re.split('[*]', glob)))
        for name in self.names:
            if regex.fullmatch(name):
                yield name

    def parents(self, b):
        def g():
            path = os.path.join(findproject(), infodirname, b)
            if not os.path.exists(path):
                return
            with open(path) as f:
                for line in f:
                    line, = line.splitlines()
                    if '*' in line:
                        public = line.startswith(publicprefix)
                        glob = line[len(publicprefix):] if public else line
                        for match in self.matching(glob):
                            if public:
                                mergeable = self.published(match)
                                if mergeable is not None:
                                    yield mergeable
                            else:
                                yield match
                    else:
                        yield line
        return list(g())

    def isremote(self, b):
        i = b.find('/')
        if -1 != i:
            return b[:i] in self.remotenames

    def branchcommits(self, b = None):
        if b is None:
            b = thisbranch()
        intersection = None # Logically this is the set of all commits.
        for pb in self.parents(b):
            nextinter = collections.OrderedDict()
            for line in reversed(runlines(['git', 'cherry', '-v', pb, b])):
                if intersection is None or line in intersection:
                    nextinter[line] = None
            intersection = nextinter
        if intersection is None:
            raise UnknownParentException(b) # Rebasing?
        def g():
            for line in intersection:
                commit, message = line.split(' ', 2)[1:]
                stat = ''.join("%%%sd%%s" % w % (n, u) for n, w, u in zip(map(int, re.findall('[0-9]+', runlines(['git', 'show', '--shortstat', commit])[-1])), [2, 3, 3], 'f+-'))
                yield commit, "%s %s" % (stat, message)
        return list(g())

try:
    unchecked_run = subprocess.run
except AttributeError:
    def unchecked_run(*args, **kwargs):
        if 'check' in kwargs:
            popenkwargs = kwargs.copy()
            del popenkwargs['check']
        else:
            popenkwargs = kwargs
        process = subprocess.Popen(*args, **popenkwargs)
        stdout, stderr = process.communicate()
        returncode = process.wait()
        if kwargs.get('check', False) and returncode:
            raise subprocess.CalledProcessError(returncode, args[0])
        return collections.namedtuple('CompletedProcess', 'returncode stdout stderr')(returncode, stdout, stderr)

def run(*args, **kwargs):
    if 'check' not in kwargs:
        kwargs = dict(kwargs, check = True)
    return unchecked_run(*args, **kwargs)

def runlines(*args, keepends = False, **kwargs):
    return run(*args, stdout = subprocess.PIPE, **kwargs).stdout.decode().splitlines(keepends)

def chain(*args, **kwargs):
    status = unchecked_run(*args, **kwargs).returncode
    if status:
        sys.exit(status)

def thisbranch():
    line, = runlines(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
    return line

def findproject(context = None):
    context = [] if context is None else [context]
    name = ['.git']
    k = 0
    path = os.path.join(*context + name)
    while not os.path.exists(path):
        k += 1
        parent = os.path.join(*context + k * ['..'] + name)
        if os.path.abspath(parent) == os.path.abspath(path):
            raise Exception('No project found.')
        path = parent
    return os.path.join(*k * ['..']) if k else '.'

def args():
    args = sys.argv[1:]
    del sys.argv[1:] # In case we call another main function.
    return args

def showmenu(entries, show = True):
    if show:
        for i, (k, v) in enumerate(entries):
            print("%3d %s %s" % (1 + i, k, v), file = sys.stderr)
    return {1 + i: k for i, (k, _) in enumerate(entries)}

def menu(entries, prompt):
    ids = showmenu(entries)
    n = int(input("%s? " % prompt))
    return n, ids[n]

def showexception():
    for line in traceback.format_exception_only(*sys.exc_info()[:2]):
        sys.stderr.write(line)

def githubuser():
    with open(os.path.join(os.path.expanduser('~'), '.git-credentials')) as f:
        return re.search('//([^:]+):.*github', f.read()).group(1)

def publicbranches():
    def g():
        for line in runlines(['git', 'branch', '-vv']):
            if re.search(r' \[[^/]+/', line) is None:
                continue
            yield re.search(r'\S+', line[2:]).group()
    return list(g())

def getpublic(b = None):
    if b is None:
        b = thisbranch()
    lines = runlines(
        ['git', 'rev-parse', '--abbrev-ref', "%s@{upstream}" % b],
        check = False,
        stderr = subprocess.DEVNULL)
    if not lines:
        return None
    pub, = lines
    return pub

def nicely(task):
    killide = lambda sig: unchecked_run(['pkill', '-f', "-%s" % sig, 'com.intellij.idea.Main'])
    killide('STOP')
    try:
        nicelyimpl(task)
    finally:
        killide('CONT')

def nicelyimpl(task):
    stashed = ['No local changes to save'] != runlines(['git', 'stash'])
    branch = thisbranch()
    try:
        task()
    except:
        if stashed:
            run(['toilet', '-w', '500', '-f', 'smmono12', '--metal', 'You have a new stash:'])
            run(['git', 'stash', 'list'])
        raise
    run(['git', 'checkout', branch])
    if stashed:
        run(['git', 'stash', 'pop'])

def touchmsg():
    return "touch %s" % thisbranch()

def stripansi(text):
    return re.sub('\x1b[[][\x30-\x3f]*[\x20-\x2f]*[\x40-\x7e]', '', text)
