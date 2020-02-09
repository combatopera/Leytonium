#HALP Remove all untracked items, including the git-ignored.

from dev_bin.common import findproject, run, infodirname

def main_scrub():
    run(['git', 'clean', '-xdi', '-e', infodirname], cwd = findproject())
