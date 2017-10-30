import subprocess, os, sys

infodirname = '.pb'

def pb():
    path = os.path.join(findproject(), infodirname, thisbranch())
    if os.path.exists(path):
        with open(path) as f:
            line = f.readline()
    else:
        line = run(['git', 'rev-list', '--max-parents=0', 'HEAD'], stdout = subprocess.PIPE).stdout.decode()
    line, = line.splitlines()
    return line

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
