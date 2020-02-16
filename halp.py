from pathlib import Path
import ast, os

prefix = '#HALP '

def main_halp():
    '''You're looking at it!'''
    halps = []
    dirpath = os.path.dirname(__file__)
    for script in os.listdir(dirpath):
        path = os.path.join(dirpath, script)
        if script.startswith('.') or os.path.islink(path) or os.path.isdir(path):
            continue
        with open(path) as f:
            for line in f:
                if line.startswith(prefix):
                    line, = line.splitlines()
                    halps.append((script, line[len(prefix):]))
                    break
    mainprefix = 'main_'
    for path in Path(dirpath).rglob('*.py'):
        if path.relative_to(dirpath).parts[0] in {'.pyven', 'build'}:
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
