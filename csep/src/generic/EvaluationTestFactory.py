"""
Module EvaluationTestFactory
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import glob, os 

import CSEP
from Environment import *
from CSEPFactory import CSEPFactory
from EvaluationTest import EvaluationTest
from RELMNumberTest import RELMNumberTest
from RELMLikelihoodTest import RELMLikelihoodTest
from RELMLikelihoodRatioTest import RELMLikelihoodRatioTest
from RELMMagnitudeTest import RELMMagnitudeTest
from RELMSpaceTest import RELMSpaceTest
from RELMConditionalLikelihoodTest import RELMConditionalLikelihoodTest

# Alarm-based tests by Jeremy Zechar
from MASSTest import MASSTest
from ROCTest import ROCTest

# Diagnostics test by Robert Clements
from CenteredWeightedLFunctionTest import CenteredWeightedLFunctionTest
from PearsonResidualsTest import PearsonResidualsTest
from DevianceResidualsTest import DevianceResidualsTest
from SuperThinnedResidualsTest import SuperThinnedResidualsTest
from SuperThinnedResidualsTestingTest import SuperThinnedResidualsTestingTest

# Statistical tests by David Rhoades
from TStatisticalTest import TStatisticalTest
from WStatisticalTest import WStatisticalTest


#--------------------------------------------------------------------------------
#
# EvaluationTestFactory.
#
# This class represents an interface for the factory of evaluation tests
# modules that are defined for the CSEP Natural Laboratory (NL).
# It is implemented as a singleton.
# 
class EvaluationTestFactory (CSEPFactory):

    # Static data of the class

    Type = "EvaluationTestFactory"
    
    # Parent class for registered classes within the factory
    __parentClass = EvaluationTest
    
    # Instances of the class will be sharing the same state 
    # (see CSEPBorgIdiom class)
    _shared_state = {}      
      
    # Default configuration file is not specified by the caller  
    __configFilePattern = '*EvaluationTestFactory.init.xml'
    
    # Remember configuration files used to initialize the factory (to avoid
    # re-initialization using the same files)
    __configFiles = set()
      
   
    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    #        config_file - Configuration file with installed Python evaluation 
    #                      tests modules. Default is None. 
    # 
    def __init__ (self,
                  config_file = None):
        """ Initialization for EvaluationTestFactory class"""

        # Dictionary of registered evaluation tests in the testing center
        my_modules = {RELMNumberTest.Type : RELMNumberTest,
                      RELMLikelihoodTest.Type : RELMLikelihoodTest,
                      RELMLikelihoodRatioTest.Type : RELMLikelihoodRatioTest,
                      RELMMagnitudeTest.Type : RELMMagnitudeTest,
                      RELMSpaceTest.Type : RELMSpaceTest,
                      RELMConditionalLikelihoodTest.Type : RELMConditionalLikelihoodTest,
                      
                      # Alarm-based tests by Jeremy Zechar
                      MASSTest.Type : MASSTest,
                      ROCTest.Type : ROCTest,
                      
                      # Diagnostics tests by Robert Clements introduced in CSEP V11.1.0
                      CenteredWeightedLFunctionTest.Type : CenteredWeightedLFunctionTest,
                      PearsonResidualsTest.Type : PearsonResidualsTest,
                      DevianceResidualsTest.Type: DevianceResidualsTest,
                      SuperThinnedResidualsTest.Type: SuperThinnedResidualsTest,
                      SuperThinnedResidualsTestingTest.Type: SuperThinnedResidualsTestingTest,
                      
                      # Statistical tests by David Rhoades introduced in CSEP V11.7.0
                      TStatisticalTest.Type: TStatisticalTest,
                      WStatisticalTest.Type: WStatisticalTest}

        CSEPFactory.__init__(self, 
                             config_file, 
                             my_modules,
                             EvaluationTestFactory.__parentClass)
        
        # Check for files that satisfy the pattern for factory configuration file
        existing_config_files = glob.glob(os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                       CSEP.TestingCenterConfigDir,
                                                       EvaluationTestFactory.__configFilePattern))

        if config_file is not None:
            EvaluationTestFactory.__configFiles.add(config_file)

        for each_file in existing_config_files:
            
           if each_file not in EvaluationTestFactory.__configFiles:
               
               self.loadPythonModules(each_file,
                                      EvaluationTestFactory.__parentClass)
                   
               EvaluationTestFactory.__configFiles.add(each_file)
        

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
              
        return EvaluationTestFactory.Type

