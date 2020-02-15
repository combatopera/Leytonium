from dev_bin.common import run, findproject, runlines
from pathlib import Path
import subprocess, sys, aridity, st

def main_gt():
    'Stage all outgoing changes and show them.'
    projectdir = Path(findproject()).resolve()
    paths = [projectdir / line[line.index("'") + 1:-1] for line in runlines(['git', 'add', '-n', str(projectdir)])]
    context = aridity.Context()
    with aridity.Repl(context) as repl:
        repl.printf('formattedprojects := $list()')
        repl.printf(". %s", Path.home() / '.settings.arid')
    stderrbytes = b''
    if projectdir.name in context.resolved('formattedprojects').unravel():
        toformat = [path for path in paths if path.exists() and path.name.endswith('.py')]
        if toformat:
            stderrbytes = run(['black', '--line-length', '120'] + toformat, stderr = subprocess.PIPE).stderr
    run(['git', 'add'] + [str(p) for p in paths])
    st.main_st()
    sys.stderr.buffer.write(stderrbytes)
