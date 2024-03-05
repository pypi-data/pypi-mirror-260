#!/usr/bin/env python3
#
# (c) 2024 Fetal-Neonatal Neuroimaging & Developmental Science Center
#                   Boston Children's Hospital
#
#              http://childrenshospital.org/FNNDSC/
#                        dev@babyMRI.org
#

import  sys, os


from    runj.__init__       import __version__

from    argparse            import RawTextHelpFormatter
from    argparse            import ArgumentParser
import  pudb

from    pfmisc._colors      import Colors
from    pfmisc              import other

from    runj.runj           import RunJ, json_respresentation, parser_setup, parser_interpret

CY      = Colors.CYAN
YL      = Colors.YELLOW
NC      = Colors.NO_COLOUR
GR      = Colors.GREEN
PL      = Colors.PURPLE
RD      = Colors.RED

str_desc = Colors.CYAN + f"""{CY}
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░       ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░
░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░
{NC}
                        run CLI "jobs" from python

                             -- version {YL}{__version__}{NC} --

    {GR}runj{NC} is python module and script for executing arbitrary CLI strings on
    the underlying system. In script mode its utility is somewhat limited (since
    running a script from the CLI to run a CLI string seems rather contorted);
    however from within python it allows for an easy mechanism to run CLI apps
    and capture output.


""" + Colors.NO_COLOUR

package_CLIself = f'''
        {CY} --exec {PL}<CLIcmdToExec>{NC}              \\
        [{CY}--spawnScript{NC}]                     \\
        [{CY}--scriptDir {PL}<dir>{NC}]                 \\
        [{CY}--background{NC}]                      \\
        [{CY}--log {PL}<logDir>{NC}]                    \\
        [{CY}--logPrefix {PL}<prefix>{NC}]              \\
        [{CY}--version{NC}]                         \\
        [{CY}--man{NC}]                             \\
        [{CY}--synopsis{NC}]                        \\
'''

package_argSynopsisSelf = f'''
        {CY}--exec {PL}<CLIcmdToExec>{NC}
        The command line expression to exeute.

        [{CY}--spawnScript{NC}]
        If specified, create a script around the <CLIcmdToExec> and execute
        the script. This is particularly useful for jobs that need to be run
        in the background.

        [{CY}--scriptDir {PL}<dir>{NC}]
        If specified, write any spawnedScripts to <dir>. If not specified, will
        autogenerate the <dir> given current date, typically in
        `/tmp/runj-history`

        [{CY}--backgroundi{NC}]
        If specified, and in conjunction with --spawnScript, will open the
        subprocess and not wait/block on stdout/stderr.

        {RD}IMPORTANT{NC}: Even if the <CLIcmdToExec> ends with a "background" '&'
        character, this script will still block until the child has completed.
        To detach and not wait, for the child, you MUST specify this flag.

        In fact, the "&" is not needed in the <CLIcmdToExec>.

        [{CY}--log {PL}<logDir>{NC}]
        If specified, create in <dir> a log snapshot of various env/exec
        values (uid, pid, etc).

        [{CY}--logPrefix {PL}<prefix>{NC}]
        If specified, prepend log snapshots with <prefix>.

        [{CY}--version{NC}]
        If specified, print the version and exit.

        [{CY}--man{NC}]
        If specified, print a detail man page and exit.

        [{CY}--synopsis{NC}]
        If specified, print only an overview synposis and exit.

'''

package_CLItagHelp          = """
"""

package_CLIfull             = package_CLIself
package_CLIDS               = package_CLIself
package_argsSynopsisFull    = package_argSynopsisSelf
package_argsSynopsisDS      = package_argSynopsisSelf

def synopsis(ab_shortOnly = False):
    scriptName = os.path.basename(sys.argv[0])
    shortSynopsis = f"""
    {YL}NAME{NC}

        {GR}runj{NC}

    {YL}SYNOPSIS

        {GR}runj{NC} """ + package_CLIfull + f"""

    {YL}BRIEF EXAMPLE

        {GR}runj {CY}--exec {YL}"ls /"{NC}

    """

    description =  f'''
    {YL}DESCRIPTION

        {GR}runj{NC} runs some user specified CLI either "directly"
        or from a created script.


    {YL}ARGS{NC}
    ''' +  package_argsSynopsisFull     +\
                package_CLItagHelp + f'''

    {YL}EXAMPLES{NC}

    Perform  `ls -1 /tmp | wc -l`

    <python>
        {PL}from{NC} runj.runj  import {CY}RunJ, json_representation
        {PL}from{NC} runj.models.data import {CY}ShellRet

        shell:{CY}RunJ{NC}      = {PL}RunJ(){NC}
        ret:{CY}ShellRet{NC}    = {GR}shell{NC}({YL}'ls /tmp | wc -l'{NC})
        {PL}print({GR}json_representation{NC}(ret))

    <CLI>
        {GR}runj {CY}--exec {YL}'ls -1 /tmp | wc -l'{NC}

    '''

    if ab_shortOnly:
        return shortSynopsis
    else:
        return shortSynopsis + description


def earlyExit_check(args) -> int:
    """Perform some preliminary checks
    """
    if args.man or args.synopsis:
        print(str_desc)
        if args.man:
            str_help     = synopsis(False)
        else:
            str_help     = synopsis(True)
        print(str_help)
        return 1
    if args.version:
        print("Name:    %s\nVersion: %s" % (__pkg.name, __version__))
        return 2
    return 0

def main(argv:list[str]=[]) -> int:
    add_help:bool           = False
    parserSA:ArgumentParser = parser_setup(
                                    'A command line python helper',
                                    add_help
                                )
    args, extra              = parser_interpret(parserSA, argv)

    if (exit:=earlyExit_check(args)): return exit

    args.version            = __version__
    args.desc               = synopsis(True)

    shell                   = RunJ(args)()
    print(json_respresentation(shell))
    return shell.returncode

if __name__ == "__main__":
    sys.exit(main())
