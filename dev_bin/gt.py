from . import st
from .common import findproject
from aridity.config import ConfigCtrl
from lagoon import git
from pathlib import Path
import subprocess, sys

def main_gt():
    'Stage all outgoing changes and show them.'
    projectdir = Path(findproject()).resolve()
    paths = [projectdir / line[line.index("'") + 1:-1] for line in git.add._n(projectdir).splitlines()]
    config = ConfigCtrl()
    config.printf('formattedprojects := $list()')
    config.loadsettings()
    stderr = ''
    if projectdir.name in config.node.formattedprojects:
        toformat = [path for path in paths if path.exists() and path.name.endswith('.py')]
        if toformat:
            from lagoon import black
            stderr = black.print('--line-length', 120, *toformat, stderr = subprocess.PIPE)
    git.add.print(*paths)
    st.main_st()
    sys.stderr.write(stderr)
