#HALP Reinstall corda gradle plugins.

from common import findproject, runpy
import os

def main_pluginst():
    projectdir = findproject()
    runpy(['gradle', '-u', 'clean', 'install'], cwd = os.path.join(projectdir, 'publish-utils'))
    runpy(['gradle', 'clean', 'install'], cwd = os.path.join(projectdir))
