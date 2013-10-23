"""
Module ResultsSummaryFactory
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import glob, os

import CSEP
from Environment import *
from CSEPFactory import CSEPFactory
from ResultsSummary import ResultsSummary
from ResultsCumulativeSummary import ResultsCumulativeSummary
from DiagnosticsSummary import DiagnosticsSummary


#--------------------------------------------------------------------------------
#
# ResultsSummaryFactory
#
# This class represents an interface for the factory of results summary objects
# that are based on type of summary (intermediate or cumulative) and test type
# of the results (N, L, or R).
# It is implemented as a singleton.
# 
class ResultsSummaryFactory (CSEPFactory):

    # Static data of the class 

    Type = "ResultsSummaryFactory"
    
    # Parent class for registered classes within the factory
    __parentClass = ResultsSummary
    
    # Instances of the class will be sharing the same state 
    # (see CSEPBorgIdiom class)
    _shared_state = {}      
    
    # Default configuration file is not specified by the caller  
    __configFilePattern = '*ResultsSummaryFactory.init.xml'
    
    # Remember configuration files used to initialize the factory (to avoid
    # re-initialization using the same files)
    __configFiles = set()
      
      
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None.
    # 
    def __init__ (self,
                  config_file = None):
        """ Initialization for ResultsSummaryFactory class"""

        # Dictionary of known post-processing modules.
        my_modules = {ResultsCumulativeSummary.Type : ResultsCumulativeSummary, 
                      ResultsSummary.Type : ResultsSummary,
                      DiagnosticsSummary.Type : DiagnosticsSummary}
        
        CSEPFactory.__init__(self, config_file, my_modules)
        
        # Check for files that satisfy the pattern for factory configuration file
        existing_config_files = glob.glob(os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                       CSEP.TestingCenterConfigDir,
                                                       ResultsSummaryFactory.__configFilePattern))

        if config_file is not None:
            ResultsSummaryFactory.__configFiles.add(config_file)

        for each_file in existing_config_files:
            
           if each_file not in ResultsSummaryFactory.__configFiles:
               
               self.loadPythonModules(each_file,
                                      ResultsSummaryFactory.__parentClass)
                   
               ResultsSummaryFactory.__configFiles.add(each_file)
        

    #----------------------------------------------------------------------------
    #
    # Return factory string identifier.
    # 
    # Input: None
    # 
    # Output:
    #         Keyword identifying the factory.
    # 
    def type (self):
        """ Return type of the factory."""
              
        return ResultsSummaryFactory.Type
     
