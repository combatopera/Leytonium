from .common import findproject
from lagoon import autopep8, sed
import subprocess, re

cols = 120

def main_brown():
    'Satisfy PEP 8 with minimal impact.'
    command = autopep8._rv.partial('--max-line-length', cols, findproject())
    result = command._d(stdout = subprocess.DEVNULL, stderr = subprocess.PIPE)
    def paths():
        for line in result.splitlines():
            m = re.fullmatch(r'\[file:(.+)]', line)
            if m is not None:
                yield m.group(1)
    sed._ni.print(r'/\S/p', *paths())
    command._i.print()
