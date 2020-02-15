from dev_bin.common import run, addparents, args, AllBranches, menu

def main_br():
    'Create given branch with completion and dashes, show menu for parent.'
    _, base = menu([[n, ''] for n in AllBranches().names], 'From')
    name = '-'.join(args())
    run(['git', 'checkout', '-b', name, base])
    addparents(name, base)
