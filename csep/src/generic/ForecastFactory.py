"""
Module ForecastFactory
"""

__version__ = "$Revision: 3769 $"
__revision__ = "$Id: ForecastFactory.py 3769 2012-07-24 20:37:27Z liukis $"


import os, sys, glob

from CSEPFactory import CSEPFactory
from Forecast import Forecast
from HybridForecast import HybridForecast

from Environment import *


#--------------------------------------------------------------------------------
#
# ForecastFactory.
#
# This class represents an interface for the factory of existing forecast modules
# that are defined for the CSEP Natural Laboratory (NL).
# It is implemented as a singleton.
# 
class ForecastFactory (CSEPFactory):

    # Static data of the class

    Type = "ForecastFactory"
    
    # Instances of the class will be sharing the same state 
    # (see CSEPBorgIdiom class)
    _shared_state = {}      
    
    # Default configuration file is not specified by the caller  
    __configFilePattern = '*ForecastFactory.init.xml'
    
    # Parent class for installed models that will be loaded at runtime
    __parentClass = Forecast
    
    # Remember configuration files used to initialize the factory (to avoid
    # re-initialization using the same files)
    __configFiles = set()
    
   
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        config_file - Configuration file with installed Python forecasts 
    #                      modules. Default is None. 
    # 
    def __init__ (self, 
                  config_file=None):
        """ Initialization for ForecastFactory class"""

        CSEPFactory.__init__(self, 
                             config_file, 
                             parent_class = ForecastFactory.__parentClass)

        # Check for files that satisfy the pattern for factory configuration file
        existing_config_files =  glob.glob(os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                        ForecastFactory.__configFilePattern))

        if config_file is not None:
            ForecastFactory.__configFiles.add(config_file)

        for each_file in existing_config_files:
            
           if each_file not in ForecastFactory.__configFiles:
               
               self.loadPythonModules(each_file,
                                      ForecastFactory.__parentClass)
                   
               ForecastFactory.__configFiles.add(each_file)
        

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
              
        return ForecastFactory.Type
     

    #----------------------------------------------------------------------------
    #
    # Add hybrid models to the factory if any are provided in configuration file
    # 
    # Input: forecast_group - Forecast group for the hybrid model 
    #        init_file - DOM element representing ForecastGroup configuration
    #                    file with configuration for hybrid models if any.
    #        root_tag - Name of root XML element for the hybrid model
    #                   configuration  
    # 
    # Output:
    #        List of Forecast objects that represent HybridForecast models
    # 
    @staticmethod
    def addHybridModels(forecast_group,
                        init_file,
                        tag_name):
        """ Add hybrid models to the factory if any are provided in 
            configuration file."""
              
        # Configuration file contain more than one hybrid model, iterate through
        # all
        hybrid_models = []
        
        if init_file.exists():
            for each_hybrid_elem in init_file.next(tag_name):
                hybrid_models.append(HybridForecast(each_hybrid_elem,
                                                    init_file,
                                                    forecast_group))
            
        return hybrid_models
        

