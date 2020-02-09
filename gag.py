#HALP Run ag on all build.gradle files.

from common import chain, args

def main_gag():
    chain(['find', '-name', 'build.gradle', '-exec', 'ag'] + args() + ['{}', '+'])
