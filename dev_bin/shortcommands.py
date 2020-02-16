import os

def main_showstash():
    'Show stash as patch.'
    command = 'git', 'stash', 'show', '-p'
    os.execvp(command[0], command)
