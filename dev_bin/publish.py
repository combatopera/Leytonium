from .common import thisbranch, pb, args, runlines
from lagoon import git

def main_publish():
    'Publish this branch, accepts push options.'
    remote, = runlines(['git', 'config', '--get', "branch.%s.remote" % pb()])
    git.push._u.print(remote, thisbranch(), *args())
