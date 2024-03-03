"""CLI for 'Python Transcoding' package.

# Autocompletion

https://click.palletsprojects.com/en/8.1.x/shell-completion/

_PYTRANSCODING_COMPLETE=IGNORE_WINGDEBUG=0 bash_source pytranscoding > ~/.pytranscoding-complete.bash

. ~/.pytranscoding-complete.bash

"""
# ==============================================================
# Implementation of 1st ports interface for CLI 
# ==============================================================
import sys
import os
ACTIVE_WINGDEBUG = os.environ.get('ACTIVE_WINGDEBUG', 'False').lower()
    
if ACTIVE_WINGDEBUG in ('true', 'yes', '1'):
    try:
        # print(f"Trying to connect to a remote debugger..")
        sys.path.append(os.path.dirname(__file__))
        from . import wingdbstub
    except Exception as why:
        print(f"{why}")
        print("Remote debugging is not found or configured: Use ACTIVE_WINGDEBUG=True to activate")
else:
    #print("Remote debugging is not selected") # don't show: problem with bash_source autocompletion
    pass



# -----------------------------------------------
# import main cli interface (root)
# -----------------------------------------------

from .main import *
from .config import *
from .workspace import *

# -----------------------------------------------
# import other project submodules/subcommands
# -----------------------------------------------

from .convert import convert

# from .plan import plan
# from .real import real
# from .roles import role
# from .run import run
# from .target import target
# from .test import test
# from .users import user
# from .watch import watch
