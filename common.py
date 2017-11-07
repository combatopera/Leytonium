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

def pb(b = None):
    if b is None:
        b = thisbranch()
    path = os.path.join(findproject(), infodirname, b)
    if not os.path.exists(path):
        raise UnknownParentException(b)
    with open(path) as f:
        parent, = f.read().splitlines()
    return parent

class AllBranches:

    @staticmethod
    def published(name):
        try:
            lines = runlines(['git', 'rev-parse', "origin/%s" % name], stderr = subprocess.DEVNULL)
        except:
            return None
        line, = lines
        return line

    def __init__(self):
        self.names = [line[2:] for line in runlines(['git', 'branch'])]

    def matching(self, glob):
        regex = re.compile('.*'.join(re.escape(text) for text in re.split('[*]', glob)))
        for name in self.names:
            if regex.fullmatch(name):
                yield name

    def parents(self, b):
        def g():
            with open(os.path.join(findproject(), infodirname, b)) as f:
                for line in f:
                    line, = line.splitlines()
                    if '*' in line:
                        public = line.startswith(publicprefix)
                        glob = line[len(publicprefix):] if public else line
                        for match in self.matching(glob):
                            if public:
                                match = self.published(match)
                                if match is not None:
                                    yield match
                            else:
                                yield match
                    else:
                        yield line
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
    return unchecked_run(*args, check = True, **kwargs)

def runlines(*args, **kwargs):
    return run(*args, stdout = subprocess.PIPE, **kwargs).stdout.decode().splitlines()

def chain(*args, **kwargs):
    sys.exit(unchecked_run(*args, **kwargs).returncode)

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
            if '[origin/' not in line:
                continue
            yield re.search(r'\S+', line[2:]).group()
    return list(g())

def ispublic():
    return '...origin/' in runlines(['git', 'status', '-sb'])[0]

def nicely(task):
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
