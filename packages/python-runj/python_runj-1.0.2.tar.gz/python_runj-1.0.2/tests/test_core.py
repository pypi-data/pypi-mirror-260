import  os
import  shlex
import  shutil
from    _pytest.capture         import capsys
from    runj.__main__           import main
from    runj.runj               import RunJ, json_respresentation, dir_create
os.environ['XDG_CONFIG_HOME'] = '/tmp'
from    argparse                import Namespace
from    runj.models.data        import ShellRet, ScriptRet
from    pathlib                 import Path

def CLIcall_parseForStringAndRet(capsys, cli:str, contains:str, exitCode:int) -> None:
    """ helper for running main module simulating CLI call
    """
    ret:int     = main(shlex.split(cli))
    captured    = capsys.readouterr()
    assert contains in captured.out
    assert ret  == exitCode

def historyDir_remove(dir:Path) -> None:
    shutil.rmtree(str(dir))

def test_main_manCore(capsys) -> None:
    """ core man page
    """
    CLIcall_parseForStringAndRet(capsys, "--man", "--exec", 1)

def test_main_version(capsys) -> None:
    """ version CLI reporting
    """
    CLIcall_parseForStringAndRet(capsys, "--version", "Name", 2)

def test_main_count_to_10(capsys) -> None:
    """ count to 10 calling the main method simulating CLI access
        (careful with quoting)!
    """
    CLIcall_parseForStringAndRet(capsys,
        "--exec 'seq 1 10 | tr -d \"\n\"'", '12345678910', 0)

def test_module_count_to_10(capsys) -> None:
    """ count to 10 on the shell in a more pythonic way
    """
    shell:RunJ      = RunJ()
    ret:ShellRet    = shell("seq 1 10 | tr -d '\n'")
    print(json_respresentation(ret))
    captured        = capsys.readouterr()
    assert "12345678910" in captured.out

def test_main_script_count_to_10(capsys) -> None:
    """ count to 10 calling the main method in CLI 'script'
        mode
    """
    CLIcall_parseForStringAndRet(capsys,
        "--scriptDir /tmp/runj-testing --spawnScript --exec 'seq 1 10 | tr -d \"\n\"'", '12345678910', 0)
    shutil.rmtree('/tmp/runj-testing')

def test_module_script_count_to_10(capsys) -> None:
    """ count to 10 on the shell in a more pythonic way
    """
    shell:RunJ                  = RunJ()
    shell.options.spawnScript   = True
    shell.histlogPath           = dir_create(Path('/tmp/runj-testing'))
    ret:ShellRet                = shell("seq 1 10 | tr -d '\n'")
    print(json_respresentation(ret))
    captured                    = capsys.readouterr()
    assert "12345678910" in captured.out
    shutil.rmtree('/tmp/runj-testing')

