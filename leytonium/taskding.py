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

from aridity.config import ConfigCtrl
from diapyr.util import innerclass
from lagoon import pgrep
from lagoon.program import bg
from pathlib import Path
import os, subprocess, sys, time

sleeptime = .5
threshold = 5
alwaysinteractive = {'Concern', 'diffuse', 'gt', 'man', 'showstash', 'top', 'vim'}

class ChildFactory:

    def __init__(self, config):
        self.sound_path = Path(config.sound.path)

    @innerclass
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
            if self.start + threshold <= now and self.armed and self.sound_path.exists() and not os.fork():
                paplay[exec](self.sound_path)

def main_taskding():
    'Play a sound when a long-running child of shell terminates.'
    config = ConfigCtrl().loadappconfig(main_taskding, 'taskding.arid')
    if 'SSH_CLIENT' in os.environ:
        return
    factory = ChildFactory(config)
    shpidstr, = sys.argv[1:]
    children = {}
    while True:
        nowchildren = {}
        now = time.time()
        try:
            with pgrep[bg]('-P', shpidstr) as stdout:
                for line in stdout:
                    nowchildren[int(line)] = factory.Child(now)
        except subprocess.CalledProcessError:
            break
        for pid in children.keys() - nowchildren.keys():
            children.pop(pid).fire(now)
        for pid, child in nowchildren.items():
            if pid not in children and child.fetch(pid):
                children[pid] = child
        time.sleep(sleeptime)
