from . import delegate

def main_squash():
    'Semi-interactively squash a most-recent chunk of commits.'
    delegate('squash.bash')

def main_drclean():
    delegate('drclean.bash')

def main_drst():
    delegate('drclean.bash')

def main_examine():
    'Open a shell in a throwaway container of the given image.'
    delegate('examine.bash')

def main_drop():
    'Drop this branch.'
    delegate('drop.bash')

def main_gimports():
    'Stage all imports-only changes and show them.'
    delegate('gimports.bash')

def main_reks():
    'Rebase on a new kitchen-sink branch.'
    delegate('reks.bash')

def main_eb():
    'Rebase on the given branch with completion, or parent with confirmation.'
    delegate('eb.bash')

def main_fixemails():
    delegate('fixemails.bash')

def main_killnodes():
    'Kill all Corda nodes.'
    delegate('killnodes.bash')

def main_mdview():
    delegate('mdview.bash')

def main_upgrade():
    'Upgrade the system and silence the nag.'
    delegate('upgrade.bash')

def main_vpn():
    delegate('vpn.bash')

def main_vunzip():
    'Extract a Docker volume.'
    delegate('vunzip.bash')
