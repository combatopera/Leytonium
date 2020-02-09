#HALP Discard all local changes, with confirmation step.

from common import run

def main_abandon():
    run(['git', 'status'])
    input('Press enter to permanently lose all these changes.')
    run(['git', 'reset', '--hard'])
