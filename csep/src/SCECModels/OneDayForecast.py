"""
OneDayForecast module
"""

__version__ = "$Revision: 3484 $"
__revision__ = "$Id: OneDayForecast.py 3484 2011-09-07 20:23:40Z liukis $"


import os, datetime

import Forecast, Environment, OneDayModelInputPostProcess


#-------------------------------------------------------------------------------------
#
# OneDayForecast forecast model.
#
# This class is designed to invoke a one-day forecast model. It prepares 
# input catalog data, formats input file with model parameters, and invokes
# the model. It places forecast file under the user specified directory.
# This is a base class with virtual 'create()' method that should be 
# overloaded by children classes.
#
class OneDayForecast (Forecast.Forecast):

    # Static data of the class 

    # Keyword identifying type of the class
    Type = 'OneDay'
    
    # Forecast template file to be used by the model
    TemplateFile = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                'data', 
                                'templates', 
                                'csep-forecast-template-M4.xml')
    
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        dir_path - Directory to store forecast file to.
    # 
    def __init__ (self, 
                  dir_path, 
                  template_file = None,
                  post_process_type = OneDayModelInputPostProcess.OneDayModelInputPostProcess.Type):
         """ Initialization for OneDayForecast class"""
        
         # Can't set default value for 'template_file' input argument to the  
         # class's static TemplateFile: in case the static data member is reset 
         # through configuration file, it will still use default value for 
         # California template file
         model_template_file = template_file 
         
         if model_template_file is None:
             model_template_file = OneDayForecast.TemplateFile
             
         Forecast.Forecast.__init__(self, dir_path, 
                                    model_template_file,
                                    post_process_type)


    #----------------------------------------------------------------------------
    #
    # Set start and end date for the forecast period. 
    #
    # Input: 
    #        test_date - Forecast period start date.
    # 
    # Output:
    #         None.
    # 
    def setPeriod (self, 
                   start_date, 
                   num_years=None, 
                   num_months=None, 
                   num_days=1):
        """ Calculate end date for the forecast period."""

        Forecast.Forecast.setPeriod(self, 
                                    start_date, 
                                    num_years, 
                                    num_months, 
                                    num_days)
        
