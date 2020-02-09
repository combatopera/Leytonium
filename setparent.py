#HALP Change declared parent of current branch.

from dev_bin.common import args as getargs, addparents, thisbranch, getpublic

def main_setparent():
    args = getargs()
    if args:
        newparent, = args
    else:
        newparent = getpublic()
        if newparent is None:
            raise Exception('Please specify a branch to be parent.')
    addparents(thisbranch(), newparent, clobber = True)
