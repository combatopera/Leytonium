import subprocess

def run(*args, **kwargs):
    return subprocess.run(*args, check = True, **kwargs)

def thisbranch():
    line, = run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout = subprocess.PIPE).stdout.decode().splitlines()
    return line
