#HALP Switch to the given branch, with completion.

from common import run, args, AllBranches, addparents, getpublic

def main_co():
    name, = args()
    new = name not in AllBranches().names
    run(['git', 'checkout', name])
    if new:
        addparents(name, getpublic())
