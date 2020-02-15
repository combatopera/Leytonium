from dev_bin.common import findproject, run, infodirname

def main_scrub():
    'Remove all untracked items, including the git-ignored.'
    run(['git', 'clean', '-xdi', '-e', infodirname], cwd = findproject())
