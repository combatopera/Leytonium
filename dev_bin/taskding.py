from lagoon import pgrep
from pathlib import Path
import os, sys, time

sleeptime = .5
threshold = 5
soundpath = Path('/usr/share/sounds/freedesktop/stereo/complete.oga')

class Child:

    def __init__(self, pid, start):
        self.pid = pid
        self.start = start

    def fire(self, now):
        if self.start + threshold <= now and soundpath.exists() and not os.fork():
            command = 'paplay', soundpath
            os.execvp(command[0], command)

def main_taskding():
    shpidstr, = sys.argv[1:]
    procdir = Path('/proc', shpidstr)
    children = {}
    while procdir.exists():
        newchildren = {}
        now = time.time()
        with pgrep.bg('-P', shpidstr, check = False) as p:
            for line in p.stdout:
                c = Child(int(line), now)
                newchildren[c.pid] = c
        for pid in children.keys() - newchildren.keys():
            children.pop(pid).fire(now)
        for c in newchildren.values():
            if c.pid not in children:
                children[c.pid] = c
        time.sleep(sleeptime)
