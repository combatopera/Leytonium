from .common import args, findproject
from lagoon import ag
import os

def main_agi():
    'Search for identifier.'
    ag._ws.print(*args(), findproject())

def main_agil():
    'Edit files containing identifier.'
    command = [os.environ['EDITOR']] + ag._wsl(*args(), findproject()).splitlines()
    os.execvp(command[0], command)
