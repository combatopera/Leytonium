from dev_bin.common import findproject
from lagoon import autopep8, sed
import subprocess, re

cols = 120

def main_brown():
    'Satisfy PEP 8 with minimal impact.'
    command = '-rv', '--max-line-length', cols, findproject()
    result = autopep8(*command, '-d', stdout = subprocess.DEVNULL, stderr = subprocess.PIPE)
    def paths():
        for line in result.splitlines():
            m = re.fullmatch(r'\[file:(.+)]', line)
            if m is not None:
                yield m.group(1)
    sed.print('-ni', r'/\S/p', *paths())
    autopep8.print(*command, '-i')
