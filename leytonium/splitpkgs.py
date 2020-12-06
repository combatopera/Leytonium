import os

def relativise(context, path):
    if context == path:
        return []
    else:
        return path[len(context + os.sep):].split(os.sep)

def main_splitpkgs():
    'Show packages that exist in more than one module.'
    packagetomodules = {}
    def register(module, package):
        try:
            packagetomodules[package].add(module)
        except KeyError:
            packagetomodules[package] = set([module])
    def findpackages(langpath):
        for dirpath, dirnames, filenames in os.walk(langpath):
            if filenames:
                package = relativise(langpath, dirpath)
                if not package:
                    yield '<unnamed>'
                elif 'META-INF' != package[0]:
                    yield '.'.join(package)
            dirnames.sort()
    def process(module, modulepath):
        srcpath = os.path.join(modulepath, 'src')
        if os.path.exists(srcpath):
            for scope in sorted(os.listdir(srcpath)):
                scopepath = os.path.join(srcpath, scope)
                for lang in sorted(os.listdir(scopepath)):
                    for package in findpackages(os.path.join(scopepath, lang)):
                        register(module, package)
    projectpath = '.'
    for dirpath, dirnames, filenames in os.walk(projectpath):
        if 'build.gradle' in filenames:
            process(''.join(":%s" % w for w in relativise(projectpath, dirpath)), dirpath)
        dirnames.sort()
    for package, modules in sorted(packagetomodules.items()):
        if 1 != len(modules):
            print(package)
            for m in modules:
                print("\t%s" % m)