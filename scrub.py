#HALP Remove all untracked items, including the git-ignored.

from common import findproject, run, infodirname

def main_scrub():
    run(['git', 'clean', '-xdi', '-e', infodirname], cwd = findproject())
