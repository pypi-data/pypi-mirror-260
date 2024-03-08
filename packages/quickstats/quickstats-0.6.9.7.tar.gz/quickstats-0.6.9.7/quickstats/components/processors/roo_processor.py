from typing import Optional, List, Dict, Union
import os
import glob
import json
import time
import ROOT

from .builtin_methods import BUILTIN_METHODS
from .actions import *
from .roo_config_parser import RooConfigParser

from quickstats import Timer, AbstractObject, PathManager
from quickstats.interface.root import TFile
from quickstats.utils.root_utils import declare_expression, close_all_root_files

class RooProcessor(AbstractObject):
    def __init__(self, config_path:Optional[str]=None,
                 config_text:Optional[str]=None,
                 flags:Optional[List[str]]=None,
                 multithread:bool=True,
                 cache:bool=False,
                 use_template:bool=False,
                 verbosity:Optional[Union[int, str]]="INFO"):
        super().__init__(verbosity=verbosity)
        self.cache = cache
        self.action_tree = None
        if flags is not None:
            self.flags = list(flags)
        else:
            self.flags = []
        self.rdf_frames = {}
        self.rdf = None
        self.global_variables = {}
        self.external_variables = {}
        self.treename = None
        self.use_template = use_template
        
        self.load_buildin_functions()
        
        if multithread:
            ROOT.EnableImplicitMT()
        
        if config_path is not None:
            self.load_config(config_path=config_path)
        elif config_text is not None:
            self.load_config(config_text=config_text)
            
    def set_cache(self, cache:bool=True):
        self.cache = cache
            
    def load_buildin_functions(self):
        for name, definition in BUILTIN_METHODS.items():
            declare_expression(definition, name)
    
    def load_config(self, config_path:Optional[str]=None,
                    config_text:Optional[str]=None):
        if config_path is not None:
            action_tree = RooConfigParser.parse_file(config_path)
        elif config_text is not None:
            action_tree = RooConfigParser.parse_text(config_text)
        else:
            raise RuntimeError('missing config input')
        action_tree.construct_actions()
        if not action_tree.root_node.has_child:
            raise RuntimeError("no actions found in the process card")
        first_action = action_tree.root_node.first_child.action
        if not isinstance(first_action, RooProcTreeName):
            raise RuntimeError("tree name must be specified at the beginning of the process card")
        self.treename = first_action._params['treename']
        self.action_tree = action_tree
        
    def set_global_variables(self, **kwargs):
        self.global_variables.update(kwargs)
        
    def clear_global_variables(self):
        self.global_variables = {}
    
    def add_flags(self, flags:List[str]):
        self.flags += list(flags)
        
    def set_flags(self, flags:List[str]):
        self.flags = list(flags)        
        
    def cleanup(self):
        close_all_root_files()
        self.rdf_frames = {}
        self.rdf = None
    
    def run_action(self, action:RooProcBaseAction):
        if not self.rdf:
            raise RuntimeError("RDataFrame instance not initialized")
        if isinstance(action, RooProcRDFAction):
            self.rdf = action.execute(self.rdf, self.global_variables)
        elif isinstance(action, RooProcHelperAction):
            action.execute(self, self.global_variables)
        elif isinstance(action, RooProcHybridAction):
            self.rdf, _ = action.execute(self.rdf, self, self.global_variables)
        elif isinstance(action, RooProcNestedAction):
            return_code = action.execute(self, self.global_variables)
            return return_code
        else:
            raise RuntimeError("unknown action type")
        return RooProcReturnCode.NORMAL
            
    def run_all_actions(self, consider_child:bool=True):
        if not self.action_tree:
            raise RuntimeError("action tree not initialized")
        node = self.action_tree.get_next(consider_child=consider_child)
        if node is not None:
            self.stdout.debug(f'Executing node "{node.name}" defined at line {node.data["start_line_number"]}')
            action = node.action
            return_code = self.run_action(action)
            if return_code == RooProcReturnCode.NORMAL:
                self.run_all_actions()
            elif return_code == RooProcReturnCode.SKIP_CHILD:
                self.run_all_actions(consider_child=False)
            else:
                raise RuntimeError("unknown return code")
        else:
            self.stdout.debug('All node executed')
            
    def sanity_check(self):
        if not self.action_tree:
            raise RuntimeError("action tree not initialized")        
        if not self.action_tree.root_node.has_child:
            self.stdout.warning("No actions to be performed.")
            return None
        if self.treename is None:
            raise RuntimeError("tree name is undefined")
    
    def run(self, filenames:Union[List[str], str]):
        self.sanity_check()
        all_files = TFile.list_files(filenames)
        if len(all_files) == 0:
            self.stdout.info('No files to be processed. Skipped.')
            return None
        elif len(all_files) == 1:
            self.stdout.info(f'Processing file "{all_files[0]}".')
        else:
            self.stdout.info("Professing files")
            for f in all_files:
                self.stdout.info(f'\t"{f}"', bare=True)  
        with Timer() as t:
            self.rdf = ROOT.RDataFrame(self.treename, all_files)
            self.action_tree.reset()
            self.run_all_actions()
            self.cleanup()
            
        self.stdout.info(f"Task finished. Total time taken: {t.interval:.3f} s.")