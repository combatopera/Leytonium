from . import effectivehome
from aridity.config import Config
from lagoon import clear, co, find, git, hg, hgcommit, md5sum, rsync, test, tput
from pathlib import Path
from pyven.projectinfo import ProjectInfo
import glob, logging, re, shlex, sys

log = logging.getLogger(__name__)

def loadconfig():
    config = Config.blank()
    config.load(Path.home() / '.settings.arid')
    return config.stmulti

class Project:

    kindwidth = 3
    kindformat = "%%-%ss" % kindwidth

    @classmethod
    def forprojects(cls, config, action):
        for path in sorted(d.parent for d in Path('.').glob("*/%s" % glob.escape(cls.dirname))):
            print(cls.kindformat % cls.dirname[1:1 + cls.kindwidth], "%s%s%s" % (tput.setaf(7), path, tput.sgr0()))
            getattr(cls(config, path), action)()

    def __init__(self, config, path):
        for command in self.commands:
            setattr(self, Path(command.path).name, command.cd(path))
        self.homerelpath = path.resolve().relative_to(effectivehome)
        self.netpath = Path(config.repomount, effectivehome.name, self.homerelpath)
        self.config = config
        self.path = path

class Mercurial(Project):

    dirname = '.hg'
    commands = hg, hgcommit

    def fetch(self):
        pass

    def pull(self):
        self.hg.pull.print(self.netpath)
        self.hg.update.print()

    def push(self):
        self.hgcommit.print()

    def status(self):
        self.hg.st.print()

class Git(Project):

    dirname = '.git'
    commands = co, git, hgcommit, md5sum, test
    remotepattern = re.compile('(.+)\t(.+) [(].+[)]')
    hookname = 'post-commit'

    def _checkremotes(self):
        d = {}
        for l in self.git.remote._v().splitlines():
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
        restore, = self.git.rev_parse.__abbrev_ref.HEAD().splitlines()
        for branch in (l[2:] for l in self.git.branch().splitlines()):
            self.co.print(branch)
            task(branch)
        self.co.print(restore)

    def fetch(self):
        self.git.fetch.__all.print()

    def pull(self):
        # TODO: Only fetch once.
        # FIXME: The public branch does not normally exist in netpath.
        self._allbranches(lambda branch: self.git.pull.__ff_only.print(self.netpath, branch))

    def push(self):
        self._allbranches(lambda branch: self.hgcommit.print())

    def status(self):
        if (self.path / 'project.arid').exists():
            if Path(self.config.repomount).is_dir(): # Needn't actually be mounted.
                self._checkremotes()
                hookpath = Path('.git', 'hooks', self.hookname)
                if self.md5sum(hookpath, check = False).stdout[:32] != self.config.hookmd5:
                    log.error("Bad hook: %s", self.hookname)
                if self.test._x.print(hookpath, check = False):
                    log.error("Unexecutable hook: %s", self.hookname)
            if not ProjectInfo.seek(self.path)['proprietary']:
                lastrelease = max((t for t in self.git.tag().splitlines() if t.startswith('v')), default = None, key = lambda t: int(t[1:]))
                if lastrelease is None:
                    lastrelease, = self.git.rev_list('--max-parents=0', 'HEAD').splitlines() # Assume trivial initial commit.
                shortstat = self.git.diff.__shortstat(lastrelease, '--', '.', *(":(exclude,glob)%s" % glob for glob in ['.travis.yml', 'project.arid', '**/test_*.py', '.gitignore']))
                if shortstat:
                    sys.stdout.write(f"{tput.rev()}{tput.setaf(5)}{lastrelease}{tput.sgr0()}{shortstat}")
        sys.stdout.write(re.sub(r':[^]\n]+]', lambda m: f"{tput.setaf(3)}{tput.rev()}{m.group()}{tput.sgr0()}", self.git.branch._vv('--color=always')))
        self.git.status._s.print()
        self.git.stash.list.print()

class Rsync(Project):

    dirname = '.rsync'
    commands = find, hgcommit, rsync

    def fetch(self):
        pass

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
        tput.setaf.print(4)
        tput.bold.print()
        self.find._newer.print(self.dirname)
        tput.sgr0.print()

def main(action):
    config = loadconfig()
    clear.print()
    for projecttype in Mercurial, Git, Rsync:
        projecttype.forprojects(config, action)

def main_stmulti():
    'Short status of all shallow projects in directory.'
    main('status')

def main_fetchall():
    main('fetch')

def main_pullall():
    main('pull')

def main_pushall():
    main('push')
