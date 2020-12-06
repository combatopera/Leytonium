from lagoon import git
from pathlib import Path
import ast

projectdir = Path(git.rev_parse.__show_toplevel(cwd = Path(__file__).parent).rstrip())
mainprefix = 'main_'

def main_halp():
    '''You're looking at it!'''
    halps = []
    for path in projectdir.rglob('*.py'):
        if path.relative_to(projectdir).parts[0] in {'.pyven', 'build'}:
            continue
        with path.open() as f:
            m = ast.parse(f.read())
        for obj in m.body:
            if isinstance(obj, ast.FunctionDef) and obj.name.startswith(mainprefix):
                doc = ast.get_docstring(obj)
                if doc is not None:
                    halps.append((obj.name[len(mainprefix):], doc))
    format = "%%-%ss %%s" % max(len(halp[0]) for halp in halps)
    for halp in sorted(halps):
        print(format % halp)
