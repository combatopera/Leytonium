from pathlib import Path
import logging, os, re, shutil, subprocess, sys

log = logging.getLogger(__name__)
pattern = re.compile('(.+)\t(.+) [(].+[)]')
lave = 'lave'

def closef(f):
    fileno = f.fileno()
    f.close()
    os.close(fileno)

def main_checkremotes():
    logging.basicConfig(format = "%(message)s")
    control = True
    tempdir, = subprocess.check_output(['mktemp', '-d'], universal_newlines = True).splitlines()
    try:
        fifo = Path(tempdir, 'fifo')
        subprocess.check_call(['mkfifo', str(fifo)])
        print(fifo)
        closef(sys.stdout)
        control = not os.fork()
        if control:
            with fifo.open() as f:
                while True:
                    l = f.readline()
                    if not l:
                        break
                    check(l.rstrip(), f.readline().rstrip())
    finally:
        if control:
            shutil.rmtree(tempdir)

def check(dirpath, relpath):
    d = {}
    for l in subprocess.check_output(['git', 'remote', '-v'], cwd = dirpath, universal_newlines = True).splitlines():
        name, loc = pattern.fullmatch(l).groups()
        if name in d:
            assert d[name] == loc
        else:
            d[name] = loc
    laveloc = d.get(lave)
    if "/mnt/Seagate3/arc/%s.git" % relpath != laveloc:
        log.error("Bad %s: %s", lave, laveloc)
    for name, loc in d.items():
        if name != lave and not loc.startswith('git@'):
            log.error("Non-SSH remote: %s %s", name, loc)
