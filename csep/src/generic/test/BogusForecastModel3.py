"""
Module BogusForecastModel3
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, datetime, string

import Environment, CSEPFile
from OneDayForecast import OneDayForecast
from Forecast import Forecast


#--------------------------------------------------------------------------------
#
# BogusForecastModel3 forecast model.
#
# This class is designed to test CSEP functionality of properly handling forecast
# models in the running system.
#
class BogusForecastModel3 (OneDayForecast):

    # Static data of the class
    
    # Keyword identifying type of the class
    Type = "BogusForecastModel3"
    

    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        dir_path - Directory to store forecast file to.
    #        args - Optional arguments for the model. Default is None.    
    # 
    def __init__ (self, dir_path, args = None):
        """ Initialization for BogusForecastModel3 class"""
        
        OneDayForecast.__init__(self, dir_path)
        

    #--------------------------------------------------------------------
    #
    # Return keyword identifying the model.
    #
    # Input: None.
    #
    # Output:
    #           String identifying the type
    #
    def type (self):
        """ Returns keyword identifying the forecast model type."""
        
        return self.Type


    #--------------------------------------------------------------------
    #
    # Write input parameter file for the model.
    #
    # Input: None
    #        
    def writeParameterFile (self):
        """ Format input parameter file for the model.
            Created file will be used by R script that invokes the
            model."""

        fhandle = Forecast.writeParameterFile(self)

        # Close the file
        fhandle.close()

    #---------------------------------------------------------------------------
    #
    # Invoke the model (simulate forecast generation by touching the file
    #
    # Input: None
    #        
    def run (self):
        """ Run forecast: 'touch' forecast file"""
        
        Environment.invokeCommand('touch %s' %self.filename())
