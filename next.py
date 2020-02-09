#HALP Go to next step in current git workflow.

from common import findproject, run, runlines
import os

def main_next():
    gitdir = os.path.join(findproject(), '.git')
    if os.path.isdir(os.path.join(gitdir, 'rebase-apply')):
        if runlines(['git', 'status', '--porcelain']):
            run(['git', 'rebase', '--continue'])
        else:
            run(['git', 'rebase', '--skip'])
    elif os.path.isfile(os.path.join(gitdir, 'MERGE_HEAD')):
        run(['git', 'commit', '--no-edit'])
    elif os.path.isfile(os.path.join(gitdir, 'CHERRY_PICK_HEAD')):
        run(['git', 'cherry-pick', '--continue'])
    elif os.path.isfile(os.path.join(gitdir, 'REVERT_HEAD')):
        run(['git', 'revert', '--continue'])
    else:
        raise Exception('Unknown git workflow, giving up.')
