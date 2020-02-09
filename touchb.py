#HALP Give the current branch its own identity.

from common import touchmsg, run, findproject, thisbranch
import os, time

def main_touchb():
    path = os.path.join(findproject(), 'TOUCHME')
    with open(path, 'w') as f:
        print("%s %s" % (time.strftime('%c %Z'), thisbranch()), file = f)
    run(['git', 'add', path])
    run(['git', 'commit', '-m', touchmsg()])
