from lagoon import co, git, st

def main_n():
    'Switch to the next branch and run st.'
    lines = git.branch().splitlines()
    for i, line in enumerate(lines):
        if line.startswith('*'):
            b = lines[i + 1].strip()
            break
    co.print(b)
    st.exec()
