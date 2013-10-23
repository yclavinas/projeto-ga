"""
ThreeMonthsForecast module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os, datetime

import Environment, Forecast, OneDayModelInputPostProcess


#-------------------------------------------------------------------------------------
#
# ThreeMonthsForecast forecast model.
#
# This class is designed to invoke a three-months forecast model. It prepares 
# input catalog data, formats input file with model parameters, and invokes
# the model. It places forecast file under the user specified directory.
# This is a base class with virtual 'create()' method that should be 
# overloaded by children classes.
#
class ThreeMonthsForecast (Forecast.Forecast):

    # Static data of the class
    
    Type = 'ThreeMonth' 

    # Forecast template file to be used by the model - if the model populates
    # the template instead of using it's own one
    TemplateFile = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                "data", "templates", "forecast.qs.dat")
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        dir_path - Directory to store forecast file to.
    # 
    def __init__ (self, dir_path):
         """ Initialization for ThreeMonthsForecast class"""
        
         Forecast.Forecast.__init__(self, dir_path, 
                                    ThreeMonthsForecast.TemplateFile,
                                    OneDayModelInputPostProcess.OneDayModelInputPostProcess.Type)
         

    #----------------------------------------------------------------------------
    #
    # Calculate end date for the forecast period. 
    #
    # Input: 
    #        start_date - Forecast period start date.
    # 
    # Output:
    #         None.
    # 
    def setPeriod (self, 
                   start_date,
                   num_years=None, 
                   num_months=3, 
                   num_days=None):
        """ Set start and end date for the forecast period."""

        Forecast.Forecast.setPeriod(self, 
                                    start_date, 
                                    num_years, 
                                    num_months, 
                                    num_days)

