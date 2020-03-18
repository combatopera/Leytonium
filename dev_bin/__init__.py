from lagoon import bash
from pathlib import Path
import inspect, os, sys

effectivehome = Path("~%s" % os.environ.get('SUDO_USER', '')).expanduser()

class Interpreter:

    def bash(path):
        with path.open('rb') as f:
            text = f.read()
        bash._c.exec(text, *sys.argv)

def delegate(*relpath):
    path = Path(Path(inspect.stack()[1].filename).parent, *relpath)
    name = path.name
    getattr(Interpreter, name[name.rindex('.') + 1:])(path)
