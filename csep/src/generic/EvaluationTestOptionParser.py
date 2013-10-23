"""
Module EvaluationTestOptionParser
"""

__version__ = "$Revision: 3812 $"
__revision__ = "$Id: EvaluationTestOptionParser.py 3812 2012-08-17 04:04:55Z liukis $"


import sys, logging, datetime

import CSEPOptionParser, CSEP
from PostProcessFactory import PostProcessFactory
from DataSourceFactory import DataSourceFactory
from CatalogDataSource import CatalogDataSource
from ForecastFactory import ForecastFactory
from EvaluationTestFactory import EvaluationTestFactory
from CSEPOptions import CommandLineOptions


#--------------------------------------------------------------------------------
#
# EvaluationTestOptionParser.
#
# This class is designed to parse command line options specific to Dispatcher.
# This class is inherited from CSEPOptionParser.
#
class EvaluationTestOptionParser (CSEPOptionParser.CSEPOptionParser):

    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None.     
    # 
    def __init__ (self):
        """ Initialization for EvaluationTestOptionParser class."""
        
        CSEPOptionParser.CSEPOptionParser.__init__(self)
        
        # Define options
        self.add_option(CommandLineOptions.CREATE_CATALOG, 
                        action="store_false", 
                        dest="create_catalog", 
                        default=True, 
                        help="Do not create catalog, re-use \
existent one under directory as specified by '%s' option. \
Default is to generate the catalog." %CommandLineOptions.TEST_DIR)

        self.add_option(CommandLineOptions.CATALOG_SOURCE, 
                        dest="data_source", 
                        type="string",
                        default=DataSourceFactory.DefaultType,                        
                        help="Catalog data source, one of %s'. Default is '%s' catalog." \
                             %(DataSourceFactory().composite().keys(), 
                               DataSourceFactory.DefaultType))
        
        self.add_option(CommandLineOptions.CATALOG_START_DATE, 
                        dest="catalog_start_date", 
                        type="string",
                        default=None,                        
                        help="Catalog start date in 'YYYY-MM-DD' format. \
Default is None.")

        self.add_option(CommandLineOptions.CATALOG_MIN_MAGNITUDE, 
                        dest="catalog_min_magnitude", 
                        type="float",
                        default=None,                        
                        help="Catalog minimum magnitude. Default is None.")

        self.add_option(CommandLineOptions.CATALOG_SOURCE_INPUTS, 
                        dest="data_source_options", 
                        type="string",
                        default=None,                        
                        help="Optional inputs for catalog data source. Default \
is None.")
        
        self.add_option(CommandLineOptions.POST_PROCESS_FACTORY,
                        dest="post_process_factory",
                        type="string",
                        default=None,
                        help="Configuration file to reset static data attributes of \
available PostProcess modules registered within a factory. Default is None.",
                        metavar="FILE")
    
        self.add_option(CommandLineOptions.FORECAST_FACTORY,
                        dest="forecast_factory",
                        type="string",
                        default=None,
                        help="Configuration file to add new forecast modules or \
reset static data attributes of available Forecast modules registered within \
a factory. Default is None.",
                        metavar="FILE")

        self.add_option(CommandLineOptions.EVALUATION_TEST_FACTORY,
                        dest="evaluation_test_factory",
                        type="string",
                        default=None,
                        help="Configuration file to add new evaluation test modules \
or to reset static data attributes of available EvaluationTest modules registered \
within a factory. Default is None.",
                        metavar="FILE")


    #--------------------------------------------------------------------
    #
    # Get command line options values.
    #
    # Input:
    #       required_options - List of required options for the parser. 
    #                          Default is None.
    # 
    # Output:
    #        Map of command line options and their values.
    #
    def options (self, required_options = None):
        """Get command line options and their values."""

        values = CSEPOptionParser.CSEPOptionParser.options(self, required_options)

        if values.post_process_factory is not None:
           # Reset post-processing static attributes if any are specified
           PostProcessFactory(values.post_process_factory)

        if values.forecast_factory is not None:
           # Reset forecast classes static attributes if any are specified
           ForecastFactory(values.forecast_factory)

        if values.evaluation_test_factory is not None:
           # Reset forecast classes static attributes if any are specified
           EvaluationTestFactory(values.evaluation_test_factory)
        
        args = {'download_data' : values.download_raw_data,
                'pre_process_data' : values.preprocess_raw_data}
        
        if values.data_source_options is not None:
            args['args'] = values.data_source_options

        if values.catalog_min_magnitude is not None:
            args['min_magnitude'] = values.catalog_min_magnitude

        if values.catalog_start_date is not None:
            args['start_date'] = datetime.datetime.strptime(values.catalog_start_date, 
                                                            CSEP.Time.DateFormat)

        DataSourceFactory.composite().clear()
        print 'DATASOURCE=', values.data_source
        DataSourceFactory().object(values.data_source, 
                                   args)
        return values
        
           
# Invoke the module
if __name__ == '__main__':

   import CSEPLogging
   
   
   parser = EvaluationTestOptionParser()
        
   # List of requred options
   required_options = [CommandLineOptions.YEAR,
                       CommandLineOptions.MONTH,
                       CommandLineOptions.DAY,
                       CommandLineOptions.FORECASTS]
   options = parser.options(required_options)
  
   CSEPLogging.CSEPLogging.getLogger(EvaluationTestOptionParser.__name__).info("Options: %s" 
                                                                               %options)
   logging.shutdown()
     
# end of class
