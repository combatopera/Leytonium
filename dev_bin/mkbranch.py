from .common import menu, run, addparents, AllBranches
import sys, subprocess, os, tempfile, re

wordpattern = re.compile(r'[^\s/]+')

def main_mkbranch():
    'Create a branch for the given ticket(s) named according to git policy.'
    tickets = sys.argv[1:]
    with tempfile.NamedTemporaryFile() as cookiesfile:
        subprocess.run([os.path.join(os.path.dirname(__file__), 'extract_cookies.sh')], stdout = cookiesfile, check = True)
        wget = subprocess.Popen(['wget', '-O', '-', "%s/browse/%s" % (os.environ['JIRA_URL'], tickets[0]), '--load-cookies', cookiesfile.name], stdout = subprocess.PIPE)
        words = [w.lower() for w in wordpattern.findall(subprocess.run([os.path.join(os.environ['GOPATH'], 'bin', 'pup'), 'h1 text{}'], stdin = wget.stdout, stdout = subprocess.PIPE).stdout.decode())]
        wget.wait()
    prefix = ''.join("%s_" % t.translate({ord('-'): None}).lower() for t in tickets)
    options = [prefix + '_'.join(words[:i + 1]) for i in range(len(words))]
    _, name = menu([[o, ''] for o in options], 'Branch name')
    _, base = menu([[n, ''] for n in AllBranches().names], 'From')
    run(['git', 'checkout', '-b', name, base])
    addparents(name, base)