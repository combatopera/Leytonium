from . import effectivehome
from lagoon import clear, co, find, git, hg, hgcommit, md5sum, rsync, tput
from pathlib import Path
import aridity, glob, logging, re, shlex

log = logging.getLogger(__name__)

class Config:

    @classmethod
    def load(cls):
        context = aridity.Context()
        with aridity.Repl(context) as repl, (Path.home() / '.settings.arid').open() as f:
            for line in f:
                repl(line)
        return cls(context)

    def __init__(self, context):
        self.repohost = context.resolved('stmulti', 'repohost').value
        self.netremotename = context.resolved('stmulti', 'netremotename').value
        self.reponame = context.resolved('stmulti', 'reponame').value
        self.repomount = Path(context.resolved('stmulti', 'repomount').value)
        self.hookmd5 = context.resolved('stmulti', 'hookmd5').value

class Project:

    kindwidth = 3
    kindformat = "%%-%ss" % kindwidth

    @classmethod
    def forprojects(cls, config, action):
        for path in sorted(d.parent for d in Path('.').glob("*/%s" % glob.escape(cls.dirname))):
            print(cls.kindformat % cls.dirname[1:1 + cls.kindwidth], path)
            getattr(cls(config, path), action)()

    def __init__(self, config, path):
        for command in self.commands:
            setattr(self, Path(command.path).name, command.cd(path))
        self.homerelpath = path.resolve().relative_to(effectivehome)
        self.netpath = config.repomount / effectivehome.name / self.homerelpath
        self.config = config
        self.path = path

class Mercurial(Project):

    dirname = '.hg'
    commands = hg, hgcommit

    def pull(self):
        self.hg.pull.print(self.netpath)
        self.hg.update.print()

    def push(self):
        self.hgcommit.print()

    def status(self):
        self.hg.st.print()

class Git(Project):

    dirname = '.git'
    commands = co, git, hgcommit, md5sum
    remotepattern = re.compile('(.+)\t(.+) [(].+[)]')
    hookname = 'post-commit'

    def _checkremotes(self):
        d = {}
        for l in self.git.remote('-v').splitlines():
            name, loc = self.remotepattern.fullmatch(l).groups()
            if name in d:
                assert d[name] == loc
            else:
                d[name] = loc
        netremotepath = d.get(self.config.netremotename)
        if "%s.git" % self.netpath != netremotepath:
            log.error("Bad %s: %s", self.config.netremotename, netremotepath)
        for name, loc in d.items():
            if name != self.config.netremotename and not loc.startswith('git@'):
                log.error("Non-SSH remote: %s %s", name, loc)

    def _allbranches(self, task):
        restore, = self.git('rev-parse', '--abbrev-ref', 'HEAD').splitlines()
        for branch in (l[2:] for l in self.git.branch().splitlines()):
            self.co.print(branch)
            task(branch)
        self.co.print(restore)

    def pull(self):
        # TODO: Only fetch once.
        self._allbranches(lambda branch: self.git.pull.print('--ff-only', self.netpath, branch))

    def push(self):
        self._allbranches(lambda branch: self.hgcommit.print())

    def status(self):
        self.git.branch.print('-vv')
        self.git.status.print('-s')
        if self.config.repomount.is_dir(): # Needn't actually be mounted.
            self._checkremotes()
            if self.md5sum(Path('.git', 'hooks', self.hookname), check = False).stdout[:32] != self.config.hookmd5:
                log.error("Bad hook: %s", self.hookname)
        self.git.stash.list.print()

class Rsync(Project):

    dirname = '.rsync'
    commands = find, hgcommit, rsync, tput

    def pull(self):
        lhs = '-avzu', '--exclude', "/%s" % self.dirname
        rhs = "%s::%s/%s/" % (self.config.repohost, self.config.reponame, self.homerelpath), '.'
        self.rsync.print(*lhs, *rhs)
        lhs += '--del',
        self.rsync.print(*lhs, '--dry-run', *rhs)
        print("(cd %s && rsync %s)" % (shlex.quote(str(self.path)), ' '.join(map(shlex.quote, lhs + rhs))))

    def push(self):
        self.hgcommit.print()

    def status(self):
        self.tput.print('setaf', 4)
        self.tput.print('bold')
        self.find.print('-newer', self.dirname)
        self.tput.print('sgr0')

def main(action):
    config = Config.load()
    clear.print()
    for projecttype in Mercurial, Git, Rsync:
        projecttype.forprojects(config, action)

def main_stmulti():
    'Short status of all shallow projects in directory.'
    main('status')

def main_pullall():
    main('pull')

def main_pushall():
    main('push')
