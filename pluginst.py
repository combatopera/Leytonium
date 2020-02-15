from dev_bin.common import findproject, runpy
import os

def main_pluginst():
    'Reinstall corda gradle plugins.'
    projectdir = findproject()
    runpy(['gradle', '-u', 'clean', 'install'], cwd = os.path.join(projectdir, 'publish-utils'))
    runpy(['gradle', 'clean', 'install'], cwd = os.path.join(projectdir))
