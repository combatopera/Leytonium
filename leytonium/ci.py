from .common import args
from lagoon import git

def main_ci():
    'Commit with the given args as message.'
    message = ' '.join(args())
    git.commit._m.print(message)
