"""
Module PostProcessFactory
"""

__version__ = "$Revision: 3805 $"
__revision__ = "$Id: PostProcessFactory.py 3805 2012-08-16 23:40:40Z liukis $"

import PostProcess
from CSEPFactory import CSEPFactory
from RELMAftershockPostProcess import RELMAftershockPostProcess
from RELMMainshockPostProcess import RELMMainshockPostProcess
from OneDayModelPostProcess import OneDayModelPostProcess
from OneDayModelInputPostProcess import OneDayModelInputPostProcess
from ThreeMonthsModelPostProcess import ThreeMonthsModelPostProcess
from OneYearModelPostProcess import OneYearModelPostProcess
from OneDayModelDeclusInputPostProcess import OneDayModelDeclusInputPostProcess


#--------------------------------------------------------------------------------
#
# PostProcessFactory.
#
# This class represents an interface for the factory of post-processing modules that are 
# defined for the CSEP Natural Laboratory (NL).
# It is implemented as a singleton.
# 
class PostProcessFactory (CSEPFactory):

    # Static data of the class 

    Type = "PostProcessFactory"
    
    # Parent class for registered classes
    __parentClass = PostProcess.PostProcess
    
    # Instances of the class will be sharing the same state 
    # (see CSEPBorgIdiom class)
    _shared_state = {}      
    
      
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:     
    #        config_file - Configuration file for the factory. Default is None.
    # 
    def __init__ (self, config_file = None):
        """ Initialization for PostProcessFactory class"""

        # Dictionary of known post-processing modules.
        my_modules = {RELMMainshockPostProcess.Type : RELMMainshockPostProcess,
                      RELMAftershockPostProcess.Type : RELMAftershockPostProcess,
                      OneDayModelPostProcess.Type : OneDayModelPostProcess,
                      OneDayModelInputPostProcess.Type : OneDayModelInputPostProcess,
                      OneDayModelDeclusInputPostProcess.Type : OneDayModelDeclusInputPostProcess,
                      ThreeMonthsModelPostProcess.Type : ThreeMonthsModelPostProcess,
                      OneYearModelPostProcess.Type : OneYearModelPostProcess}
        
        CSEPFactory.__init__(self, 
                             config_file, 
                             my_modules,
                             PostProcessFactory.__parentClass)
        

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
              
        return PostProcessFactory.Type
     
