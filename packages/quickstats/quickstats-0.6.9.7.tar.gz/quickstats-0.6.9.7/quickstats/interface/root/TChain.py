from typing import Optional, Union, List, Dict
import numpy as np

from .TObject import TObject
from .TFile import TFile

class TChain(TObject):
    
    def __init__(self, treename:str,
                 source:Optional[Union[str, List[str]]],
                 **kwargs):
        super().__init__(treename=treename, source=source, **kwargs)
        
    def initialize(self, treename:str,
                   source:Optional[Union[str, List[str]]]):
        import ROOT
        obj = ROOT.TChain(treename)
        filenames = TFile.list_files(source)
        for filename in filenames:
            obj.AddFile(filename)
        self.obj = obj

    def get_entries(self, sel:Optional[str]=None):
        if sel:
            return self.obj.GetEntries(sel)
        return self.obj.GetEntries()