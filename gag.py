from dev_bin.common import chain, args

def main_gag():
    'Run ag on all build.gradle files.'
    chain(['find', '-name', 'build.gradle', '-exec', 'ag'] + args() + ['{}', '+'])
