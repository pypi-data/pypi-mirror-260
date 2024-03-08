from typing import Optional, Union, List, Dict
import os
import re
import glob

import numpy as np

from quickstats import semistaticmethod
from .TObject import TObject

class TFile(TObject):

    FILE_PATTERN = re.compile(r"^.+\.root(?:\.\d+)?$")

    def __init__(self, source:Union[str, "ROOT.TFile"],
                 **kwargs):
        super().__init__(source=source, **kwargs)

    def initialize(self, source:Union[str, "ROOT.TFile"]):
        self.obj = self._open(source)
        
    @staticmethod
    def is_corrupt(f:"ROOT.TFile"):
        if f.IsZombie():
            return True
        if f.GetNkeys() == 0:
            return True
        import ROOT
        if f.TestBit(ROOT.TFile.kRecovered):
            return True
        return False

    @semistaticmethod
    def _is_valid_filename(self, filename:str):
        return self.FILE_PATTERN.match(filename) is not None

    @semistaticmethod
    def list_files(self, paths:Union[List[str], str],
                   strict_format:Optional[bool]=True):
        if isinstance(paths, str):
            return self.list_files([paths])
        filenames = []
        for path in paths:
            if os.path.isdir(path):
                filenames.extend(glob.glob(os.path.join(path, "*")))
            else:
                filenames.extend(glob.glob(path))
        filenames = [filename for filename in filenames if os.path.isfile(filename)]
        if strict_format:
            filenames = [filename for filename in filenames if self._is_valid_filename(filename)]
        if not filenames:
            return []
        import ROOT
        invalid_filenames = []
        for filename in filenames:
            try:
                rfile = ROOT.TFile(filename)
                if self.is_corrupt(rfile):
                    invalid_filenames.append(filename)
            except:
                invalid_filenames.append(filename)
        if invalid_filenames:
            fmt_str = "\n".join(invalid_filenames)
            raise RuntimeError(f'Found empty/currupted file(s):\n{fmt_str}')
        return filenames
    
    @staticmethod
    def _open(source:Union[str, "ROOT.TFile"]):
        # source is path to a root file
        if isinstance(source, str):
            import ROOT
            source = ROOT.TFile(source)
            
        if TFile.is_corrupt(source):
            raise RuntimeError(f'empty or currupted root file: "{source.GetName()}"')
            
        return source
        
    """
    def make_branches(self, branch_data):
        branches = {}
        return branches
    
    def fill_branches(self, treename:str, branch_data):
        if self.obj is None:
            raise RuntimeError("no active ROOT file instance defined")
        tree = self.obj.Get(treename)
        if not tree:
            raise RuntimeError(f"the ROOT file does not contain the tree named \"{treename}\"")
        n_entries = tree.GetEntriesFast()
        
        for i in range(n_entries):
            for branch in branches:
                
        tree.SetDirectory(self.obj)
        # save only the new version of the tree
        tree.GetCurrentFile().Write("", ROOT.TObject.kOverwrite)
    """
    
    def get_tree(self, name:str, strict:bool=True):
        tree = self.obj.Get(name)
        if not tree:
            if strict:
                raise RuntimeError(f'In TFile.Get: Tree "{name}" does not exist')
            return None
        return tree

    def close(self):
        self.obj.Close()
        self.obj = None