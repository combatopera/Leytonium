from lagoon import git
import logging, re

log = logging.getLogger(__name__)
pattern = re.compile('(.+)\t(.+) [(].+[)]')
lave = 'lave'

def check(dirpath, relpath):
    d = {}
    for l in git('remote', '-v', cwd = dirpath).splitlines():
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