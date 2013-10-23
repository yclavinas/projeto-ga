"""
Module ForecastHandlerFactory
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

from CSEPFactory import CSEPFactory
from ForecastHandler import ForecastHandler


#--------------------------------------------------------------------------------
#
# ForecastHandlerFactory.
#
# This class represents an interface for the factory of forecast handler modules
# that support different kinds of forecats: rate-based and polygon-based forecasts
# within CSEP testing framework.
# 
class ForecastHandlerFactory (CSEPFactory):

    # Static data of the class 

    Type = "ForecastHandlerFactory"
    
    # Parent class for registered classes
    __parentClass = ForecastHandler
    
    # Instances of the class will be sharing the same state 
    # (see CSEPBorgIdiom class)
    _shared_state = {}      

    CurrentHandler = None
    
      
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:     
    #        config_file - Configuration file for the factory. Default is None.
    # 
    def __init__ (self, config_file = None):
        """ Initialization for PostProcessFactory class"""

        from RateForecastHandler import RateForecastHandler
        from PolygonForecastHandler import PolygonForecastHandler

        # Dictionary of known post-processing modules.
        my_modules = {RateForecastHandler.Type : RateForecastHandler,
                      PolygonForecastHandler.Type : PolygonForecastHandler}
        
        CSEPFactory.__init__(self, 
                             config_file, 
                             my_modules,
                             ForecastHandlerFactory.__parentClass)
        
        if ForecastHandlerFactory.CurrentHandler is None:
           ForecastHandlerFactory.CurrentHandler = RateForecastHandler()
        

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
              
        return ForecastHandlerFactory.Type
     

    def object (self, class_type, input_variables = None):
        """ Instantiate object of specified type."""
        
        # Set forecast handler to the last object created by the factory
        ForecastHandlerFactory.CurrentHandler = CSEPFactory.object(self, 
                                                                   class_type, 
                                                                   input_variables)
        return ForecastHandlerFactory.CurrentHandler
        
        

if __name__ == '__main__':
    
    ### Stand-alone functionality to be used by miniCSEP distribution
    from ForecastHandlerOptionParser import ForecastHandlerOptionParser
    

    parser = ForecastHandlerOptionParser()
    options = parser.options()
    
    
    ### Invoke ASCII to XML conversion
    if options.convert_to_xml is True:
        
        # Forecast filename will be used to populate 'name' element of the 
        # XML template
        template = ForecastHandlerFactory().CurrentHandler.XML(options.xml_template)
        result_file = template.toXML(options.forecast, 
                                     datetime.datetime.strptime(options.start_date, 
                                                               CSEP.Time.ISO8601Format),
                                     datetime.datetime.strptime(options.end_date,
                                                               CSEP.Time.ISO8601Format),                                                                
                                     os.path.basename(options.forecast))
        _moduleLogger().info('%s forecast, converted to XML format, is stored in %s file.' %(options.forecast,
                                                                                             result_file)) 

    ### Invoke ASCII to XML conversion
    elif options.convert_to_ascii is True:
        
        forecast_file = ForecastHandlerFactory().CurrentHandler.XML(options.forecast)
        result_file = forecast_file.toASCII()
        _moduleLogger().info('%s forecast, converted to ASCII format, is stored in %s file.' %(options.forecast,
                                                                                               result_file)) 

