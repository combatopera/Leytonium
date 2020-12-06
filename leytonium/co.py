from .common import args, AllBranches, addparents, getpublic
from lagoon import git

def main_co():
    'Switch to the given branch, with completion.'
    name, = args()
    new = name not in AllBranches().names
    git.checkout.print(name)
    if new:
        addparents(name, getpublic())
