from .common import nicely, isgitpol, publicbranches, run, stderr

def main_autopull():
    'Pull master and releases with automatic stash and switch.'
    def pullthem():
        for b in publicbranches():
            # TODO LATER: Also pull ticket branches owned by others.
            if isgitpol(b):
                stderr("Skip: %s" % b)
            else:
                run(['git', 'checkout', b])
                run(['git', 'pull'])
    nicely(pullthem)
