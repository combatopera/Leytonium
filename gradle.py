#HALP Run the context gradlew.

from dev_bin.common import chain, findproject, args
import os

def main_gradle(cwd = None):
    chain([os.path.join(findproject(cwd), 'gradlew')] + args(), cwd = cwd)
