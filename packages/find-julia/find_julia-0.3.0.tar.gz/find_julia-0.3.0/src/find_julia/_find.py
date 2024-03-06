import os
import shutil
import subprocess
import itertools
import julia_semver
from . import juliaup
from . import _jill
from . import install_julia
from . import util
from . import julia_version


def is_julia_executable(exe):
    """
    Return True if exe is the path to a Julia exectuable, otherwise False.

    The test consists of checking the output of "julia --version".
    """
    try:
        words = subprocess.run(
            [exe, '--version'], check=True, capture_output=True, encoding='utf8'
        ).stdout.strip().split()
    except Exception:
        return False
    return len(words) == 3 and words[0] == "julia" and words[1] == "version"


# Check if `path` exists and is a julia executable.
# Strange to take the argument to skip check. But it makes call site much simpler.
def _check_path(path, check_exe=True):
    if not check_exe:
        return True
    if not os.path.isfile(path):
        return False
    return is_julia_executable(path)


def _to_semver(versions_paths):
    semver_list = [(julia_semver.version(v), p) for (v, p) in versions_paths if v is not None]
    if len(semver_list) == len(versions_paths):
        return semver_list
    for (v, p) in versions_paths: # slower, less common branch
        if v is None:
            print(f"Skipping path '{p}', unable to get julia version.")
    return semver_list

# There are several ways or locations to look for julia. This returns a dict
# whose keys are these ways to find julia and whose values are bool s.
# 'jill' looks in default locations that `jill.py` installs to
# 'juliaup' queries the juliaup program for installed julias
# 'which' uses `shutil.which` to search the user's PATH for julia.
# 'env' checks the environment variable `JULIA`.
def _default_locations(default=True):
    return {'jill': default, 'juliaup': default, 'which': default, 'env': default}

# Collect paths to julia executables found by searching `locations`.
# `locations` is a `dict` of the form returned by `_default_locations`.
# `no_dist` means skip `/usr/bin/julia`.
def _collect_paths(locations, no_dist=True):
    all_paths = []
    # Finding juliaup versions is fast because they are cached in the filesystem.
    if locations['juliaup']:
        paths_juliaup = _to_semver(juliaup.version_path_list())
        all_paths.append(paths_juliaup)
    if locations['which']:
        wpath = shutil.which("julia")
        if no_dist and _is_linux_dist_julia(wpath):
            print(f"Excluding julia found on PATH: {wpath}. Distribution-installations are usually broken.")
        # Exclude ~/.juliaup/bin/julia . It actually links to julialauncher. This program
        # is not really julia. Eg, if DEPOT_PATH[1] has been changed, julialauncher will error.
        elif wpath is not None:
            if os.path.realpath(wpath).endswith("julialauncher"):
                pass
                # Log this instead? print("Excluding symlink from 'julialauncher' to 'julia'.")
            else:
                paths_which = _to_semver(julia_version.to_version_path_list([wpath]))
                all_paths.append(paths_which)
    if locations['jill']:
        paths_jill = _to_semver(_jill.version_path_list())
        all_paths.append(paths_jill)
    return all_paths


# If the environment variable (usually `JULIA`) exists,
# check if the path exists and find the version of the executable
# at that path. Return the version and the path.
# Return None, None, if any of this fails.
def _env_var_julia(var_name):
    path = os.getenv(var_name)
    if path is None:
        return None, None
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Executable {var_name} = {path} does not exist.")
    version = julia_version.julia_version(path)
    return version, path


_LINUX_DIST_JULIA = os.path.join(os.sep, "usr", "bin", "julia")
_LINUX_DIST_SBIN_JULIA = os.path.join(os.sep, "usr", "sbin", "julia")

# Try to determine whether `julia_path` is a system installed
# julia. If so return `true`. We assume that executables in
# `/usr/bin` and `/usr/sbin` have been installed by linux package
# managers.
def _is_linux_dist_julia(julia_path):
    if julia_path is None:
        return False
    rjulia_path = os.path.realpath(julia_path)
    return (julia_path == _LINUX_DIST_JULIA
            or rjulia_path == _LINUX_DIST_JULIA
            or julia_path == _LINUX_DIST_SBIN_JULIA
            or rjulia_path == _LINUX_DIST_SBIN_JULIA
            )


# Search for the best installed julia version that satisfies `version_spec`.
# If locations['env'] is true and a path to acceptable julia executable is found in
# the env variable, then return the version and path
# Otherwise collect paths from the remaining locations and find the best one.
# The best is the highest version satisfying `version_spec`.
def _find_version(version_spec=None, check_exe=False, strict=False, env_var=None, locations=None,
                  no_dist=True):
    if version_spec is None:
        version_spec = julia_semver.semver_spec("^1")
    elif isinstance(version_spec, str):
        version_spec = julia_semver.semver_spec(version_spec)
    if locations is None:
        locations = _default_locations()
    if locations['env']:
        if env_var is None:
            env_var = "JULIA"
        env_version, env_path = _env_var_julia(env_var)
        if _is_linux_dist_julia(env_path) and no_dist:
            print(f"Excluding julia in environment variable {env_var}, set to {env_path}. Distribution-installations are usually broken.")
        elif (env_version is not None and
              julia_semver.match(version_spec, env_version, strict=strict) and
              _check_path(env_path, check_exe)
              ):
            return (env_version, env_path)
    jlists = _collect_paths(locations=locations, no_dist=no_dist)
    paths = set(itertools.chain.from_iterable(jlists))
    maxv = julia_semver.version("0.0.0")
    best = (None, None)
    for vers, path in paths:
        if (vers > maxv and julia_semver.match(version_spec, vers, strict=strict)
            and _check_path(path, check_exe)):
            maxv = vers
            best = (vers, path)
    return best


def find(version_spec=None, check_exe=False, find_all=False, strict=True, env_var=None,
         no_dist=True):
    """
    Search for and return the path to a Julia executable.

    Calling `find()` will use reasonable defaults.

    Parameters:
    env_var : The environment variable to check for a julia path.
        If this variable is set and the exectuable satisfies `version_spec`, then it will be
        preferred to all other paths. Default: "JULIA".
    version_spec : A Julia version specification as a str or object. The returned executable
        must satisfy this specification. Default: "^1".
    strict : If `True` then prerelease (development) versions will be excluded.
    check_exe : If `True` then check that the path is a Julia by querying it for the version.
        Note that this has already been done for most Julias found when the version was extracted.
    find_all : If `False` skip the locations that are slower to search. If no other exectuables
        are found, the slower locations may be searched anyway. The only slow location is the
        jill-installed location.
    no_dist: bool if `True` then a distribution-installed Julia, i.e. /usr/bin/julia under linux,
        will be excluded from the search. Default is `True`. These julia installations are usually
        broken and should almost always be avoided.
    """
    locations = _default_locations()
    if find_all is False: # Finding jill-installed julia versions is a bit slow
        locations['jill'] = False
    _, path = _find_version(
        version_spec=version_spec, check_exe=check_exe, strict=strict,
        env_var=env_var, locations=locations, no_dist=no_dist
    )
    if path is not None:
        return path
    if find_all is not True: # Try other places if no versions were acceptable
        locations = _default_locations(default=False)
        locations['jill'] = True
        _, path = _find_version(
            version_spec=version_spec, check_exe=check_exe, strict=strict, locations=locations
        )
    return path


def find_or_install(version_spec=None, check_exe=False, find_all=False, strict=True,
                    answer_yes=False, post_question_hook=None,
                    env_var=None,
                    no_dist=True
                    ): # , install_root=None):
    """
    Search for and return the path to a Julia executable or install one if none is found.

    Calling `find_or_install()` will use reasonable defaults.

    This function takes all the same parameters as does `find` as well as the following.
    Parameters:
    answer_yes - if `True`, then ask no questions, assume answers are "yes".
    post_question_hook -  a function to run if and after the consumer is asked whether
        to install Julia. This can be used to ask and record more questions rather
        than waiting till after the download. Default: None
    """
    path = find(
        version_spec=version_spec, check_exe=check_exe, find_all=find_all, strict=strict, env_var=env_var,
        no_dist=no_dist
    )
    if path is not None:
        return path
    util.log(f"No Julia version satisfying spec '{str(version_spec)}' found.")
    install_julia.prompt_and_install(
        answer_yes=answer_yes, post_question_hook=post_question_hook, version_spec=version_spec,
        strict=strict)
    # find_all=True !!
    path = find(version_spec=version_spec, check_exe=check_exe, find_all=True, strict=strict)
    return path
