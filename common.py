import subprocess, os

def run(*args, **kwargs):
    return subprocess.run(*args, check = True, **kwargs)

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
