# runj

_I just want to run a shell command from Python!_

[![Version](https://img.shields.io/docker/v/fnndsc/runj?sort=semver)](https://hub.docker.com/r/fnndsc/runj)
[![MIT License](https://img.shields.io/github/license/fnndsc/runj)](https://github.com/FNNDSC/runj/blob/main/LICENSE)
[![ci](https://github.com/FNNDSC/runj/actions/workflows/ci.yml/badge.svg)](https://github.com/FNNDSC/runj/actions/workflows/ci.yml)

```
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░
```

## Abstract

The accepted method for running underlying system or shell commands via python is using the `subprocess` module and specifically the `Popen()` function. While this method exposes considerable flexibility, it can be complex, requiring some tedious boilerplate for capturing `stdout` and `stderr`, return values, etc. Moreover, depending on context (foreground vs background for example), some of the `Popen()` semantics and supporting boilerplate differ.

If the need is simply to have a straightforward pythonic way to just call a CLI string on the underlying system that uses `Popen()`, can handle real time `stdout` echoing, can easily background tasks, does `stderr` capturing, etc, `runj` can help.

`runj` offers a same-named script, and a `RunJ()` class. Using the `RunJ()` class provides a much simpler and cleaner API compared to `Popen()` and boilerplate. Additionally, the `runj` script can run CLI commands and return a JSON formatted result by default.

## Installation

### Using ``PyPI``

The best method of installing `runj` and all of its dependencies is by fetching it from PyPI

```bash
pip3 install runj
```

## Usage

A good set of exemplars is provided in the [`test_core.py`](https://github.com/FNNDSC/runj/blob/master/tests/test_core.py) test code.

### Python API

In the simplest case where some CLI string, say `ls /tmp | wc -l` needs to be evaluated:

```python
from runj.runj  import RunJ, json_representation
from runj.models.data import ShellRet

shell:RunJ      = RunJ()
ret:ShellRet    = shell('ls /tmp | wc -l')
print(json_representation(ret))
```

### script

The equivalent from the `runj` script would be

```bash
runj --exec 'ls /tmp | wc -l'
```

While it might be debatable as to the utility of running a CLI string from the CLI via some intermediary like `runj`, one use case is simply that it captures results in a useful JSON return, so would be suited as a possible interface to communications over web, for example. 

## CLI Synopsis

```html
        --exec <CLIcmdToExec>
        The command line expression to exeute.

        [--spawnScript]
        If specified, create a script around the <CLIcmdToExec> and execute
        the script. This is particularly useful for jobs that need to be run
        in the background.

        [--scriptDir <dir>]
        If specified, write any spawnedScripts to <dir>. If not specified, will
        autogenerate the <dir> given current date, typically in
        `/tmp/runj-history`

        [--background]
        If specified, and in conjunction with --spawnScript, will open the
        subprocess and not wait/block on stdout/stderr.

        IMPORTANT: Even if the <CLIcmdToExec> ends with a "background" '&'
        character, this script will still block until the child has completed.
        To detach and not wait, for the child, you MUST specify this flag.

        In fact, the "&" is not needed in the <CLIcmdToExec>.

        [--log <dir>]
        If specified, create in <dir> a log snapshot of various env/exec
        values (uid, pid, etc).

        [--logPrefix <prefix>]
        If specified, prepend log snapshots with <prefix>.

        [--version]
        If specified, print the version and exit.

        [--man]
        If specified, print a detail man page and exit.

        [--synopsis]
        If specified, print only an overview synposis and exit.

```

## Examples

_Watch this space!_

_-30-_
