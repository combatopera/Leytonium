#HALP Publish this branch, accepts push options.

from dev_bin.common import thisbranch, pb, run, args, runlines

def main_publish():
    remote, = runlines(['git', 'config', '--get', "branch.%s.remote" % pb()])
    run(['git', 'push', '-u', remote, thisbranch()] + args())
