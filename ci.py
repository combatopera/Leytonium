#HALP Commit with the given args as message.

from dev_bin.common import run, args, isgitpol

def main_ci():
    message = ' '.join(args())
    if isgitpol():
        message = 'WIP ' + message[0].upper() + message[1:]
    run(['git', 'commit', '-m', message])
