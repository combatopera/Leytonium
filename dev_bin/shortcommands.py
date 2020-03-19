from . import st
from .common import AllBranches, args, findproject, infodirname, pb, savecommits, savedcommits
from lagoon import clear, find, git
from pathlib import Path

def main_showstash():
    'Show stash as patch.'
    git.stash.show._p.exec()

def main_pb():
    'Find parent branch.'
    print(pb())

def main_d():
    'Show local changes.'
    clear.print()
    git.diff.print()

def main_rdx():
    'Run git rm on conflicted path, with completion.'
    git.rm.exec(*args())

def main_rx():
    'Restore given file to parent branch version.'
    git.checkout.print(pb(), *args())

def main_gag():
    'Run ag on all build.gradle files.'
    find._name.exec('build.gradle', '-exec', 'ag', *args(), '{}', '+')

def main_git_completion_path():
    print(Path(__file__).parent / 'git_completion')

def main_git_functions_path():
    print(Path(__file__).parent / 'git_functions')

def main_rd():
    'Run git add on conflicted path, with completion.'
    # FIXME: Reject directory args.
    # FIXME: Refuse to add file with outstanding conflicts.
    git.add.exec(*args())

def main_dup():
    'Apply the last slammed commit.'
    git.cherry_pick.__no_commit.print(savedcommits()[-1])
    git.reset.print()
    st.main_st()

def main_scrub():
    'Remove all untracked items, including the git-ignored.'
    git.clean._xdi.print('-e', infodirname, cwd = findproject())
