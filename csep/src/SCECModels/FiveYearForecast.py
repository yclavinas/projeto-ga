"""
FiveYearForecast module
"""

__version__ = "$Revision: 2966 $"
__revision__ = "$Id: FiveYearForecast.py 2966 2010-05-27 23:25:42Z liukis $"


import sys, os, datetime

import Environment, Forecast, OneDayModelInputPostProcess


#-------------------------------------------------------------------------------------
#
# FiveYearForecast forecast model.
#
# This class is designed to invoke a five-year forecast model. It prepares 
# input catalog data, formats input file with model parameters, and invokes
# the model. It places forecast file under the user specified directory.
# This is a base class with virtual 'create()' method that should be 
# overloaded by children classes.
#
class FiveYearForecast (Forecast.Forecast):

    # Static data of the class 
    Type = "FiveYear"

    # Forecast template file to be used by the model - if the model populates
    # the template instead of using it's own one
    TemplateFile = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                "data", "templates", "csep-forecast-template-M5.xml")
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        dir_path - Directory to store forecast file to.
    # 
    def __init__ (self, dir_path):
         """ Initialization for FiveYearForecast class"""
        
         Forecast.Forecast.__init__(self, dir_path, 
                                    FiveYearForecast.TemplateFile,
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
                   num_years=5, 
                   num_months=None, 
                   num_days=None):
        """ Set start and end date for the forecast period."""

        Forecast.Forecast.setPeriod(self, 
                                    start_date, 
                                    num_years, 
                                    num_months, 
                                    num_days)

