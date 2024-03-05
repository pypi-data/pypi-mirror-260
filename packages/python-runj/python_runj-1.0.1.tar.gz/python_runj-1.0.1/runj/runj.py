str_description = """
    This module provides some very simple shell-based job running
    methods.
"""


import  subprocess
import  os
import  pudb
import  uuid
import  json
import  sys
from    pudb.remote                 import set_trace
from    pathlib                     import Path
from    datetime                    import datetime
from    argparse                    import Namespace, ArgumentParser, RawTextHelpFormatter
from    runj.models.data            import Space, ShellRet, ScriptRet
from    multiprocessing             import Process, Manager
from    multiprocessing.managers    import DictProxy
from    typing                      import Any

def logHistoryPath_create(basePath:Path = Path('/tmp')) -> Path:
    """Creates the log directory structure and returns the path."""

    today:datetime  = datetime.today()
    year_dir:str    = str(today.year)
    date_dir:str    = today.strftime("%Y-%m-%d")
    log_path:Path   = basePath/"runj-history"/year_dir/date_dir
    try:
        log_path.mkdir(parents=True, exist_ok=True)  # Create parent dirs if needed
    except Exception as e:
        print(f"An error in creating the logHistoryPath occurred: {e}")
        log_path    = Path('/tmp')
    return log_path

def dir_create(dir:Path = Path('/tmp')) -> Path:
    try:
        dir.mkdir(parents = True, exist_ok = True)
    except Exception as e:
        print(f"An error occured in creating {dir}: {e}. Setting path to '/tmp'")
        dir     = Path('/tmp')
    return dir

def json_respresentation(obj:ShellRet|ScriptRet|None) -> str:
    if obj:
        return json.dumps(obj.model_dump(), indent = 4)
    else:
        return ""

def parser_setup(desc:str, add_help:bool = True) -> ArgumentParser:
    parserSelf = ArgumentParser(
                description         = desc,
                formatter_class     = RawTextHelpFormatter,
                add_help            = add_help
            )

    parserSelf.add_argument("--exec",
                help    = "command line execution string to perform",
                dest    = 'exec',
                default = '')

    parserSelf.add_argument("--spawnScript",
                help    = "if specified, embed the exec cmd in a script and run the script",
                dest    = 'spawnScript',
                default = False,
                action  = 'store_true')

    parserSelf.add_argument("--scriptDir",
                help    = "if specified, use the passed directory for saving scripts",
                dest    = 'scriptDir',
                default = '')

    parserSelf.add_argument("--background",
                help    = "if specified, run the shell command in background",
                dest    = 'background',
                default = False,
                action  = 'store_true')

    parserSelf.add_argument("--log",
                help    = "if specified, log various runtime info to the passed dir",
                dest    = 'log',
                default = '')

    parserSelf.add_argument("--prefix",
                help    = "if specified, add prefix to log outputs",
                dest    = 'prefix',
                default = '')

    parserSelf.add_argument("--version",
                help    = "if specified, print name and version",
                dest    = 'version',
                default = False,
                action  = 'store_true')

    parserSelf.add_argument("--man",
                help    = "if specified, print detailed man page",
                dest    = 'man',
                default = False,
                action  = 'store_true')

    parserSelf.add_argument("--synopsis",
                help    = "if specified, print help synopsis",
                dest    = 'synopsis',
                default = False,
                action  = 'store_true')

    return parserSelf

def parser_interpret(parser, args = None) -> tuple:
    """
    Interpret the list space of *args, or sys.argv[1:] if
    *args is empty
    """
    if args:
        args, unknown    = parser.parse_known_args(args)
    else:
        args, unknown    = parser.parse_known_args(sys.argv[1:])
    return args, unknown

def parser_JSONinterpret(parser, d_JSONargs) -> tuple:
    """
    Interpret a JSON dictionary in lieu of CLI.

    For each <key>:<value> in the d_JSONargs, append to
    list two strings ["--<key>", "<value>"] and then
    argparse.
    """
    l_args  = []
    for k, v in d_JSONargs.items():
        if type(v) == type(True):
            if v: l_args.append('--%s' % k)
            continue
        l_args.append('--%s' % k)
        l_args.append('%s' % v)
    return parser_interpret(parser, l_args)

def namespace_isempty(namespace: Namespace) -> bool:
    return all(value is None for value in vars(namespace).values())

class RunJ:

    def __init__(self, options:Namespace = Namespace()):
        """Constructor for the runj class.

        Args:
            d_args (dict): a dictionary of "arguments" (parameters) for the
                           object.
        """
        if namespace_isempty(options):
            options, extra          = parser_interpret(
                                        parser_setup(
                                            'A command line python helper',
                                            True
                                        )
                                    )
        # pudb.set_trace()
        self.options:Space          = Space(**vars(options))
        if not self.options.scriptDir:
            self.histlogPath:Path   = logHistoryPath_create(Path('/tmp'))
        else:
            self.histlogPath:Path   = dir_create(Path(self.options.scriptDir))
        self.execCmd:Path           = Path("")
        self.desc                   = "" if not self.options.has('desc') else self.options.desc
        if self.options.has('desc'):
            self.options.rm('desc')
        if not self.options.has('verbosity'):
            self.options.verbosity      = 0
        if not self.options.has('jobLogging'):
            self.options.jobLogging     = False

    def v2JSONcli(self, v:str) -> str:
        """
        attempts to convert a JSON string serialization explicitly into a string
        with enclosed single quotes. If the input is not a valid JSON string, simply
        return it unchanged.

        An input string of

            '{ "key1": "value1", "key2": N, "key3": true }'

        is explicitly enclosed in embedded single quotes:

            '\'{ "key1": "value1", "key2": N, "key3": true }\''

        args:
            v(str): a value to process

        returns:
            str: cli equivalent string.
        """
        vb:str      = ""
        try:
            d_dict  = json.loads(v)
            vb      = f"'{v}'"
        except:
            vb      = '%s' % v
        return vb

    def dict2cli(self, d_dict : dict) -> str:
        """convert a dictionary into a cli conformant json string.

        an input dictionary of

            {
                'key1': 'value1',
                'key2': 'value2',
                'key3': true,
                'key4': false
            }

        is converted to a string:

            "--key1 value1 --key2 value2 --key3"

        args:
            d_dict (dict): a python dictionary to convert

        returns:
            str: cli equivalent string.
        """
        str_cli     : str = ""
        for k,v in d_dict.items():
            if type(v) == bool:
                if v:
                    str_cli += '--%s ' % k
            elif len(v):
                v = self.v2JSONcli(v)
                str_cli += '--%s %s ' % (k, v)
        return str_cli

    def __call__(self, *args, **kwargs) -> ShellRet | ScriptRet:
        cli:str         = ""
        if self.options.has('exec'):
            cli         = self.options.exec
        ret:ShellRet|ScriptRet
        if len(args):
            cli         = str(args[0])
        if not cli:
            return ShellRet()
        runFrom:str     = ""
        for k,v in kwargs.items():
            if k == 'runFrom':  runFrom = v.tolower()
        if not self.options.has('spawnScript'):
            self.options.spawnScript        = False
        if runFrom:
            if runFrom == 'shell':
                self.options.spawnScript    = False
            else:
                self.options.spawnScript    = True
        match self.options.spawnScript:
            case False: ret =  self.shell_run(cli)
            case True:  ret =  self.script_run(cli)
            case _:     ret =  self.shell_run(cli)
        if self.options.log:
            self.job_stdwrite(ret, self.options.log, self.options.prefix)
        return ret

    def shell_run(self, str_cmd:str) -> ShellRet:
        """
        running some cli process via python is cumbersome. the typical/easy
        path of

                            os.system(str_cmd)

        is deprecated and prone to hidden complexity. The preferred
        method is via subprocess, which has a cumbersome processing
        syntax. Still, this method runs the `str_cmd` and returns the
        stderr and stdout strings as well as a returncode.
        Providing readtime output of both stdout and stderr seems
        problematic. The approach here is to provide realtime
        output on stdout and only provide stderr on process completion.
        """
        ret:ShellRet        = ShellRet()
        stdoutbytes:bytes   = b''
        stdoutline:str      = ""
        stdout:str          = ""
        p = subprocess.Popen(
                    str_cmd,
                    start_new_session = True,
                    shell   = True,
                    stdout  = subprocess.PIPE,
                    stderr  = subprocess.PIPE,
        )
        if p.stdout and not self.options.background:
            for stdoutbytes in iter(p.stdout.readline, b''):
                stdoutline  = stdoutbytes.decode()
                if int(self.options.verbosity):
                    print(stdoutline)
                stdout      += stdoutline
        ret.cmd             = str_cmd
        ret.cwd             = os.getcwd()
        ret.pid             = p.pid
        ret.stdout          = stdout
        if p.stderr and not self.options.background:
            ret.stderr      = p.stderr.read().decode()
        poll                = p.poll()
        if poll is not None:
            ret.returncode = poll
        if int(self.options.verbosity) and len(ret.stderr):
            print('\nstderr: \n%s' % ret.stderr)
        return ret

    def script_run(self, str_cmd:str) -> ScriptRet:
        """run a job from a script.

        This method will:
            * create a shell script around <str_cmd> on the underlying system
              and execute that scripts in a subprocess.popen.
            * if the <str_cmd> is explicitly meant to be background process
              append a "&" to the <str_cmd>
            * this method is more reliable in running a <str_cmd> "in the background"
              than a direct Popen

        args:
            str_cmd (str): cli string to run

        returns:
            dict: a dictionary of exec state
        """

        def txscript_content(message:str) -> str:
            nonlocal baseFileName
            str_script:str  = ""
            str_script      = f"""#!/bin/bash

            {message}
            """
            str_script = ''.join(str_script.split(r'\r'))
            return str_script

        def txscript_save(str_content:str) -> None:
            with open(self.execCmd, "w") as f:
                f.write(f'%s' % str_content)
            self.execCmd.chmod(0o755)

        def execstr_build(input:Path) -> str:
            """ the path might have spaces, esp on non-Linux systems """
            ret:str             = ""
            t_parts:tuple       = input.parts
            ret                 = '/'.join(['"{0}"'.format(arg)\
                                    if ' ' in arg else arg for arg in t_parts])
            return ret[1:] # remove the leading and extraneous '/'

        baseFileName:Path   = self.histlogPath / Path(f"job-{uuid.uuid4().hex}")
        self.execCmd        = baseFileName.with_suffix(".sh")
        txscript_save(txscript_content(str_cmd))
        # pudb.set_trace()
        shellRet:ShellRet   = self.shell_run(execstr_build(self.execCmd))
        scriptRet:ScriptRet = ScriptRet(**shellRet.model_dump())
        scriptRet.script    = str(self.execCmd)
        scriptRet.uid       = os.getuid()
        return scriptRet

    def job_stdwrite(self, d_job:ShellRet|ScriptRet, str_outputDir:str, str_prefix:str = "") -> dict:
        """
        Capture the d_job entries to respective files.
        """
        if self.options.log:
            for key, value in d_job.__dict__.items():
                with open(
                    '%s/%s%s' % (str_outputDir, str_prefix, key), "w"
                ) as f:
                    f.write(str(value))
                    f.close()
        return {
            'status': True
        }
