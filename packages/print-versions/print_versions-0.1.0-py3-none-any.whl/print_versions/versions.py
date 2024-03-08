from importlib.metadata import version

_skip = ["IPython", "print_versions"]


def get_versions(_globals, skip=_skip):
    skip_modules = set(["__main__", "importlib", *(skip or [])])
    versions = {}
    for m in [*_globals.values()]:
        if getattr(m, "__version__", None):
            versions[m.__name__] = m.__version__
        elif getattr(m, "__module__", None):
            n = m.__module__.split(".")[0]
            if not n in skip_modules:
                skip_modules.add(n)
                try:
                    versions[n] = version(n)
                except:
                    pass
    return versions


def print_versions(_globals, skip=_skip):
    for [n, v] in get_versions(_globals, skip=skip).items():
        print(f"{n}=={v}")
