from dev_bin.common import run

def main_abandon():
    'Discard all local changes, with confirmation step.'
    run(['git', 'status'])
    input('Press enter to permanently lose all these changes.')
    run(['git', 'reset', '--hard'])
