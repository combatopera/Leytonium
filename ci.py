from dev_bin.common import args, isgitpol
from lagoon import git

def main_ci():
    'Commit with the given args as message.'
    message = ' '.join(args())
    if isgitpol():
        message = 'WIP ' + message[0].upper() + message[1:]
    git.commit._m(message)
