import subprocess, os, sys

infodirname = '.pb'

class UnknownParentException(Exception): pass

def pb():
    b = thisbranch()
    path = os.path.join(findproject(), infodirname, b)
    if not os.path.exists(path):
        raise UnknownParentException(b)
    with open(path) as f:
        parent, = f.read().splitlines()
    return parent

def run(*args, **kwargs):
    return subprocess.run(*args, check = True, **kwargs)

def chain(*args, **kwargs):
    sys.exit(subprocess.run(*args, **kwargs).returncode)

def thisbranch():
    line, = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout = subprocess.PIPE).stdout.decode().splitlines()
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
