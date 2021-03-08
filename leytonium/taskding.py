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

from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from diapyr.util import innerclass
from lagoon import pgrep
from lagoon.program import bg
from pathlib import Path
import os, subprocess, time

class TaskDing:

    def __init__(self, config):
        self.always_interactive = set(config.always.interactive)
        self.shpidstr = config.shpidstr
        self.sleep_time = float(config.sleep.time)
        self.sound_path = Path(config.sound.path)
        self.threshold = config.threshold

    @innerclass
    class Child:

        def __init__(self, start):
            self.start = start

        def fetch(self, pid):
            try:
                with open(f"/proc/{pid}/comm") as f:
                    self.armed = f.read().rstrip() not in self.always_interactive
                    return True
            except (FileNotFoundError, ProcessLookupError):
                pass

        def fire(self, now):
            from lagoon import paplay
            if self.start + self.threshold <= now and self.armed and self.sound_path.exists() and not os.fork():
                paplay[exec](self.sound_path) # FIXME: These leak as zombie processes.

    def run(self):
        children = {}
        while True:
            nowchildren = {}
            now = time.time()
            try:
                with pgrep[bg]('-P', self.shpidstr) as stdout:
                    for line in stdout:
                        nowchildren[int(line)] = self.Child(now)
            except subprocess.CalledProcessError:
                break
            for pid in children.keys() - nowchildren.keys():
                children.pop(pid).fire(now)
            for pid, child in nowchildren.items():
                if pid not in children and child.fetch(pid):
                    children[pid] = child
            time.sleep(self.sleep_time) # FIXME LATER: I suspect keyboard interrupt can kill script when not asleep.

def main_taskding():
    'Play a sound when a long-running child of shell terminates.'
    if 'SSH_CLIENT' in os.environ:
        return
    config = ConfigCtrl().loadappconfig(main_taskding, 'taskding.arid')
    parser = ArgumentParser()
    parser.add_argument('shpidstr')
    parser.parse_args(namespace = config)
    TaskDing(config).run()
