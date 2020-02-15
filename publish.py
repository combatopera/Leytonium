from dev_bin.common import thisbranch, pb, run, args, runlines

def main_publish():
    'Publish this branch, accepts push options.'
    remote, = runlines(['git', 'config', '--get', "branch.%s.remote" % pb()])
    run(['git', 'push', '-u', remote, thisbranch()] + args())
