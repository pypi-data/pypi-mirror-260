"""
Some models used by Jobber
"""

from pydantic_settings          import BaseSettings
from pathlib                    import Path

from argparse                   import Namespace
from multiprocessing.managers   import BaseManager

class Space(Namespace):
    """ A namespace that can check if it has an attribute """
    def has(self, attrib:str) -> bool:
        return hasattr(self, attrib)

    def rm(self, attrib:str) -> bool:
        if not self.has(attrib):
            return False
        delattr(self, attrib)
        return True

class ShellRet(BaseSettings):
    """ Return from running through shell directly """
    stdout:str              = ""
    stderr:str              = ""
    cmd:str                 = ""
    cwd:str                 = ""
    pid:int|None            = -1
    returncode:int          = 0

class ScriptRet(ShellRet):
    """ Return from running a script """
    uid:int             = -1
    script:str          = ""

