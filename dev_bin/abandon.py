from lagoon import git

def main_abandon():
    'Discard all local changes, with confirmation step.'
    git.status.print()
    input('Press enter to permanently lose all these changes.')
    git.reset.__hard.print()
