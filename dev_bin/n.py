from .common import runlines
from lagoon import co, st

def main_n():
    'Switch to the next branch and run st.'
    lines = runlines(['git', 'branch'])
    for i, line in enumerate(lines):
        if line.startswith('*'):
            b = lines[i + 1].strip()
            break
    co.print(b)
    st.exec()
