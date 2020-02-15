from dev_bin.common import run, args, AllBranches, addparents, getpublic

def main_co():
    'Switch to the given branch, with completion.'
    name, = args()
    new = name not in AllBranches().names
    run(['git', 'checkout', name])
    if new:
        addparents(name, getpublic())
