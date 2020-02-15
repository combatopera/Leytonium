from dev_bin.common import chain, args

def main_rdx():
    'Run git rm on conflicted path, with completion.'
    chain(['git', 'rm'] + args())
