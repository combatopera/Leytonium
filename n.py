from dev_bin.common import runlines, chain, run

def main_n():
    'Switch to the next branch and run st.'
    lines = runlines(['git', 'branch'])
    for i, line in enumerate(lines):
        if line.startswith('*'):
            b = lines[i + 1].strip()
            break
    run(['co', b])
    chain(['st'])
