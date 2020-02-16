from . import delegate

def main_stmulti():
    'Short status of all shallow projects in directory.'
    delegate('stmulti.bash')

def main_pullall():
    delegate('stmulti.bash')

def main_pushall():
    delegate('stmulti.bash')

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
