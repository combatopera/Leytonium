from .common import args, chain, pb, run
from pathlib import Path
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

def main_rdx():
    'Run git rm on conflicted path, with completion.'
    chain(['git', 'rm'] + args())

def main_rx():
    'Restore given file to parent branch version.'
    run(['git', 'checkout', pb()] + args())

def main_gag():
    'Run ag on all build.gradle files.'
    chain(['find', '-name', 'build.gradle', '-exec', 'ag'] + args() + ['{}', '+'])

def main_git_completion_path():
    print(Path(__file__).parent / 'git_completion')

def main_git_functions_path():
    print(Path(__file__).parent / 'git_functions')
