#HALP Pull master and releases with automatic stash and switch.

from dev_bin.common import nicely, isgitpol, publicbranches, run, stderr

def main_autopull():
    def pullthem():
        for b in publicbranches():
            # TODO LATER: Also pull ticket branches owned by others.
            if isgitpol(b):
                stderr("Skip: %s" % b)
            else:
                run(['git', 'checkout', b])
                run(['git', 'pull'])
    nicely(pullthem)
