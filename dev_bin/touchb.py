from .common import touchmsg, findproject, thisbranch
from lagoon import git
import os, time

def main_touchb():
    'Give the current branch its own identity.'
    path = os.path.join(findproject(), 'TOUCHME')
    with open(path, 'w') as f:
        print("%s %s" % (time.strftime('%c %Z'), thisbranch()), file = f)
    git.add.print(path)
    git.commit._m.print(touchmsg())
