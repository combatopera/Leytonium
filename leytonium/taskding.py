# Copyright 2020 Andrzej Cichocki

# This file is part of Leytonium.
#
# Leytonium is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Leytonium is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Leytonium.  If not, see <http://www.gnu.org/licenses/>.

from lagoon import pgrep
from pathlib import Path
import os, subprocess, sys, time

sleeptime = .5
soundpath = Path('/usr/share/sounds/freedesktop/stereo/complete.oga')
threshold = 5
alwaysinteractive = {'Concern', 'diffuse', 'man', 'top', 'vim'}

class Child:

    def __init__(self, start):
        self.start = start

    def fetch(self, pid):
        try:
            with open(f"/proc/{pid}/comm") as f:
                self.armed = f.read().rstrip() not in alwaysinteractive
                return True
        except (FileNotFoundError, ProcessLookupError):
            pass

    def fire(self, now):
        from lagoon import paplay
        if self.start + threshold <= now and self.armed and soundpath.exists() and not os.fork():
            paplay.exec(soundpath)

def main_taskding():
    if 'SSH_CLIENT' in os.environ:
        return
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
