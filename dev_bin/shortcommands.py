from .common import pb, run
import os

def main_showstash():
    'Show stash as patch.'
    command = 'git', 'stash', 'show', '-p'
    os.execvp(command[0], command)

def main_pb():
    'Find parent branch.'
    print(pb())

def main_d():
    'Show local changes.'
    run(['clear'])
    run(['git', 'diff'])
