from .common import thisbranch, args, findproject, infodirname
from lagoon import git
import os

def main_ren():
    'Rename current branch.'
    fromname = thisbranch()
    git.branch._m.print(*args())
    d = os.path.join(findproject(), infodirname)
    target = os.path.join(d, thisbranch())
    os.makedirs(os.path.dirname(target), exist_ok = True)
    os.rename(os.path.join(d, fromname), target)
