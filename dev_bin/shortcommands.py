from .common import AllBranches, args, chain, findproject, infodirname, pb, run, savecommits
from pathlib import Path
import os

def main_showstash():
    'Show stash as patch.'
    command = 'git', 'stash', 'show', '-p'
    os.execvp(command[0], command)

def main_pb():
    'Find parent branch.'
    print(pb())

def main_d():
    'Show local changes.'
    run(['clear'])
    run(['git', 'diff'])

def main_rdx():
    'Run git rm on conflicted path, with completion.'
    chain(['git', 'rm'] + args())

def main_rx():
    'Restore given file to parent branch version.'
    run(['git', 'checkout', pb()] + args())

def main_gag():
    'Run ag on all build.gradle files.'
    chain(['find', '-name', 'build.gradle', '-exec', 'ag'] + args() + ['{}', '+'])

def main_git_completion_path():
    print(Path(__file__).parent / 'git_completion')

def main_git_functions_path():
    print(Path(__file__).parent / 'git_functions')

def main_rd():
    'Run git add on conflicted path, with completion.'
    # FIXME: Reject directory args.
    # FIXME: Refuse to add file with outstanding conflicts.
    chain(['git', 'add'] + args())

def main_dup():
    'Add the top commit to the list of slammed commits.'
    savecommits([AllBranches().branchcommits()[0][0]])

def main_gradle(cwd = None):
    'Run the context gradlew.'
    chain([os.path.join(findproject(cwd), 'gradlew')] + args(), cwd = cwd)

def main_scrub():
    'Remove all untracked items, including the git-ignored.'
    run(['git', 'clean', '-xdi', '-e', infodirname], cwd = findproject())
