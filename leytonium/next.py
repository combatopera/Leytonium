from lagoon import git
from pathlib import Path

def main_next():
    'Go to next step in current git workflow.'
    gitdir = Path(git.rev_parse.__git_dir().rstrip())
    if (gitdir / 'rebase-apply').is_dir():
        if git.status.__porcelain().splitlines():
            git.rebase.__continue.print()
        else:
            git.rebase.__skip.print()
    elif (gitdir / 'MERGE_HEAD').is_file():
        git.commit.__no_edit.print()
    elif (gitdir / 'CHERRY_PICK_HEAD').is_file():
        git.cherry_pick.__continue.print()
    elif (gitdir / 'REVERT_HEAD').is_file():
        git.revert.__continue.print()
    else:
        raise Exception('Unknown git workflow, giving up.')
