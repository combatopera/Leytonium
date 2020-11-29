from lagoon import paplay, pgrep
from pathlib import Path
import os, subprocess, sys, time

sleeptime = .5
soundpath = Path('/usr/share/sounds/freedesktop/stereo/complete.oga')
threshold = 5
interactivecommands = {'diffuse', 'vim'}

class Child:

    def __init__(self, start):
        self.start = start

    def fetch(self, pid):
        try:
            with open(f"/proc/{pid}/cmdline") as f:
                self.armed = f.read().split('\0')[0].split(os.sep)[-1] not in interactivecommands
                return True
        except FileNotFoundError:
            pass

    def fire(self, now):
        if self.start + threshold <= now and self.armed and soundpath.exists() and not os.fork():
            paplay.exec(soundpath)

def main_taskding():
    shpidstr, = sys.argv[1:]
    children = {}
    while True:
        nowchildren = {}
        now = time.time()
        try:
            with pgrep.bg('-P', shpidstr) as stdout:
                for line in stdout:
                    nowchildren[int(line)] = Child(now)
        except subprocess.CalledProcessError:
            break
        for pid in children.keys() - nowchildren.keys():
            children.pop(pid).fire(now)
        for pid, child in nowchildren.items():
            if pid not in children and child.fetch(pid):
                children[pid] = child
        time.sleep(sleeptime)
