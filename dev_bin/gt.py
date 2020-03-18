from . import st
from .common import findproject
from lagoon import git
from pathlib import Path
import subprocess, sys, aridity

def main_gt():
    'Stage all outgoing changes and show them.'
    projectdir = Path(findproject()).resolve()
    paths = [projectdir / line[line.index("'") + 1:-1] for line in git.add._n(projectdir).splitlines()]
    context = aridity.Context()
    with aridity.Repl(context) as repl:
        repl.printf('formattedprojects := $list()')
        repl.printf(". %s", Path.home() / '.settings.arid')
    stderr = ''
    if projectdir.name in context.resolved('formattedprojects').unravel():
        toformat = [path for path in paths if path.exists() and path.name.endswith('.py')]
        if toformat:
            from lagoon import black
            stderr = black.print('--line-length', 120, *toformat, stderr = subprocess.PIPE)
    git.add.print(*paths)
    st.main_st()
    sys.stderr.write(stderr)
