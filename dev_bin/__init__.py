from pathlib import Path
import inspect, os, sys

class Interpreter:

    def bash(path):
        with path.open('rb') as f:
            text = f.read()
        command = ['bash', '-c', text] + sys.argv
        os.environ['GIT_FUNCTIONS'] = str(path.parent / 'git_functions')
        os.execvp(command[0], command)

def delegate(*relpath):
    path = Path(Path(inspect.stack()[1].filename).parent, *relpath)
    name = path.name
    getattr(Interpreter, name[name.rindex('.') + 1:])(path)
