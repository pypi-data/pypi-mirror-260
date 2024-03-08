import os
import pathlib

from quickstats.core import *
from ._version import __version__

"""
import ROOT
ROOT.gROOT.SetBatch(True) 
ROOT.PyConfig.IgnoreCommandLineOptions = True
"""

# silence cppyy warning
os.environ['CLING_STANDARD_PCH'] = "none"
os.environ['CPPYY_API_PATH'] = "none"

module_path = pathlib.Path(__file__).parent.absolute()
macro_path = os.path.join(module_path, 'macros')
stylesheet_path = os.path.join(module_path, 'stylesheets')
resource_path = os.path.join(module_path, 'resources')

# ROOT.gInterpreter.AddIncludePath(os.path.join(macro_path, "macros"))

MAX_WORKERS = 8

corelib_loaded = False

stdout = AbstractObject.stdout

root_version = get_root_version()