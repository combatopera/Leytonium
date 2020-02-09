#HALP Run ag on all build.gradle files.

from dev_bin.common import chain, args

def main_gag():
    chain(['find', '-name', 'build.gradle', '-exec', 'ag'] + args() + ['{}', '+'])
