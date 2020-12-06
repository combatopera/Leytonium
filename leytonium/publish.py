from .common import thisbranch, pb, args
from lagoon import git

def main_publish():
    'Publish this branch, accepts push options.'
    remote, = git.config.__get("branch.%s.remote" % pb()).splitlines()
    git.push._u.print(remote, thisbranch(), *args())
