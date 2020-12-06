from .common import addparents, args, AllBranches, menu
from lagoon import git

def main_br():
    'Create given branch with completion and dashes, show menu for parent.'
    _, base = menu([[n, ''] for n in AllBranches().names], 'From')
    name = '-'.join(args())
    git.checkout._b.print(name, base)
    addparents(name, base)
