from dev_bin.common import chain, findproject, args
import os

def main_gradle(cwd = None):
    'Run the context gradlew.'
    chain([os.path.join(findproject(cwd), 'gradlew')] + args(), cwd = cwd)
