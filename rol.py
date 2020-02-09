#HALP Move given slammed commit (default top) to the bottom.

from common import savedcommits, savecommits, args as getargs

def main_rol():
    v = savedcommits()
    args = getargs()
    if args:
        n, = args
        n = int(n)
        if n < 0:
            raise Exception("Don't bother with the minus.")
        i = len(v) - int(n) - 1
    else:
        i = 0
    savecommits(v[:i] + v[i + 1:] + [v[i]], True)
