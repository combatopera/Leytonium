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

'Play a sound when a long-running child of shell terminates.'
from argparse import ArgumentParser
from aridity.config import ConfigCtrl
from foyndation import inf, innerclass
from lagoon.program import partial
from lagoon.text import pgrep
from pathlib import Path
from subprocess import CalledProcessError
import os, time

class TaskDing:

    def __init__(self, config):
        self.always_interactive = set(config.always.interactive)
        self.pgrep = pgrep[partial]('-P', config.shpidstr)
        self.sleep_time = float(config.sleep.time)
        self.sound_path = Path(config.sound.path)
        self.threshold = config.threshold

    @innerclass
    class Child:

        armed = False

        def __init__(self, mark):
            self.mark = mark

        def tick(self, now, pid):
            if self.mark <= now:
                self.mark = inf
                try:
                    self.armed = Path(f"/proc/{pid}/comm").read_text().rstrip() not in self.always_interactive
                except (FileNotFoundError, ProcessLookupError):
                    pass

        def fire(self):
            from lagoon.text import paplay
            if self.armed and self.sound_path.exists():
                if (pid := os.fork()):
                    return pid
                paplay[exec](self.sound_path)

    def run(self):
        children = {}
        soundpids = set()
        while True:
            nowchildren = {}
            now = time.time()
            try:
                with self.pgrep as stdout:
                    for line in stdout:
                        nowchildren[int(line)] = self.Child(now + self.threshold)
            except CalledProcessError:
                break
            for pid in soundpids - nowchildren.keys():
                os.waitpid(pid, 0)
            soundpids &= nowchildren.keys()
            for pid in children.keys() - nowchildren.keys():
                q = children.pop(pid).fire()
                if q is not None:
                    soundpids.add(q)
            for pid, child in nowchildren.items():
                if pid not in children:
                    children[pid] = child
            for pid, child in children.items():
                child.tick(now, pid)
            time.sleep(self.sleep_time) # FIXME LATER: I suspect keyboard interrupt can kill script when not asleep.

def main():
    if 'SSH_CLIENT' in os.environ:
        return
    config = ConfigCtrl().loadappconfig(main, 'taskding.arid')
    parser = ArgumentParser()
    parser.add_argument('shpidstr')
    parser.parse_args(namespace = config.cli)
    TaskDing(config).run()

if '__main__' == __name__:
    main()
