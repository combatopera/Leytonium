from pathlib import Path
import ast

projectdir = Path(__file__).parent
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
