import subprocess, os, sys, traceback, re, collections

infodirname = '.pb'

class UnknownParentException(Exception): pass

def stderr(*args, **kwargs):
    return print(*args, file = sys.stderr, **kwargs)

def pb():
    b = thisbranch()
    path = os.path.join(findproject(), infodirname, b)
    if not os.path.exists(path):
        raise UnknownParentException(b)
    with open(path) as f:
        parent, = f.read().splitlines()
    return parent

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

def findproject():
    name = path = '.git'
    while not os.path.exists(path):
        parent = '..' + os.sep + path
        if os.path.abspath(parent) == os.path.abspath(path):
            raise Exception('No project found.')
        path = parent
    return '.' if path == name else path[:-len(os.sep + name)]

def args():
    return sys.argv[1:]

def showmenu(entries):
    for i, (k, v) in enumerate(entries):
        print("%3d %s %s" % (1 + i, k, v), file = sys.stderr)
    return {1 + i: k for i, (k, _) in enumerate(entries)}

def showexception():
    for line in traceback.format_exception_only(*sys.exc_info()[:2]):
        sys.stderr.write(line)

def githubuser():
    with open(os.path.join(os.path.expanduser('~'), '.git-credentials')) as f:
        return re.search('//([^:]+):.*github', f.read()).group(1)
