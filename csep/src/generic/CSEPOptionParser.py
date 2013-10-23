"""
Module CSEPOptionParser
"""

__version__ = "$Revision: 4150 $"
__revision__ = "$Id: CSEPOptionParser.py 4150 2012-12-19 03:08:43Z liukis $"


import optparse, sys, logging

import CSEPLogging, EvaluationTestFactory, GeographicalRegions, \
       CSEP, CSEPInputParams, CSEPStorage, EvaluationTest
from PostProcessFactory import PostProcessFactory
from ForecastFactory import ForecastFactory
from ForecastHandlerFactory import ForecastHandlerFactory
from RateForecastHandler import RateForecastHandler
from CSEPOptions import CommandLineOptions
from cseprandom import CSEPRandom


#--------------------------------------------------------------------------------
#
# CSEPOptionParser.
#
# This class is designed to parse command line options. This class is inherited
# from optparse.OptionParser.
#
class CSEPOptionParser (optparse.OptionParser):

    # Static data
    
    # Dictionary of reporting levels for the logging module
    __reportLevels = {'critical': logging.CRITICAL,
                      'error': logging.ERROR,
                      'warning': logging.WARNING,
                      'debug': logging.DEBUG,
                      'info': logging.INFO,
                      'notset': logging.NOTSET}


    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None.     
    # 
    def __init__ (self):
        """ Initialization for CSEPOptionParser class"""
        
        
        # Report CSEP version on request (--version option)        
        optparse.OptionParser.__init__(self, version = CSEP.Version)
        
        
        # Define generic options
        # This option is added to support Python generic 
        # 'verbose' mode used by PyUnit
        self.add_option("-v", "--verbose", 
                        dest="verbose", 
                        action="store_true",
                        default=False,
                        help="Enable verbose reporting. Added to support Python's \
'verbose' mode used by CSEP acceptance tests only. Please see %s option to \
configure progress report level." %CommandLineOptions.LOG_LEVEL) 
     
        self.add_option(CommandLineOptions.YEAR, 
                        dest="year", 
                        type="int",
                        help="Year of the test date", 
                        metavar="YEAR")
        
        self.add_option(CommandLineOptions.MONTH, 
                        dest="month",
                        type="int",
                        help="Month of the test date", 
                        metavar="MONTH")
        
        self.add_option(CommandLineOptions.DAY, 
                        dest="day",
                        type="int",
                        help="Day of the test date",
                        metavar="DAY")

        self.add_option(CommandLineOptions.REGION, 
                        dest="region",
                        type="string",
                        help="Geographical region for the forecast models and \
evaluation tests. One of %s. Default is %s." %(GeographicalRegions.Region.all(),
                                               GeographicalRegions.Region.Selected),
                        metavar="REGION")
        
        self.add_option(CommandLineOptions.TEST_DIR,
                        dest="test_dir", 
                        type="string",
                        default="catalog",
                        help="Directory to store test results to. Default is 'catalog'.", 
                        metavar="DIR") 

        help_message = "Set of evaluation tests to invoke. \
Any combination of %s keywords." %(EvaluationTestFactory.EvaluationTestFactory().keys())
        self.add_option(CommandLineOptions.TESTS,
                        dest="test_list", 
                        type="string",
                        default=None,
                        help=help_message,
                        metavar="TEST LIST")
        
        help_message = "Input arguments for evaluation tests to invoke. \
Default is None. Arguments for the same test are comma-separated \"key=value\" \
pairs. A '%s'-character separator is used to separate \
arguments for different tests." %(CSEPInputParams.CSEPInputParams.InputSeparator)
        self.add_option(CommandLineOptions.TESTS_INPUTS,
                        dest="test_inputs", 
                        type="string",
                        default=None,
                        help=help_message,
                        metavar="TEST INPUTS")

        help_message = "Keyword for registered python module to \
use for catalog post-processing or to provide proper initialization \
for the evaluation tests. One of %s."  \
%(PostProcessFactory().keys())

        self.add_option(CommandLineOptions.POST_PROCESS, 
                        dest="post_process",
                        type="string",
                        default=None,
                        help=help_message, 
                        metavar="PYTHON MODULE")

        help_message = "Space-separated input arguments for specified post-processing: \
start and end date for the testing period in 'YYYY-MM-DD' format. Default is an empty string."
        self.add_option(CommandLineOptions.POST_PROCESS_ARGS, 
                        dest="post_process_args",
                        type="string",
                        help=help_message, 
                        default=None,
                        metavar="\"YYYY1-MM1-DD1 YYYY2-MM2-DD2\"")

        self.add_option(CommandLineOptions.DOWNLOAD_RAW, 
                        action="store_false", 
                        dest="download_raw_data",
                        default=True, 
                        help="Do not download raw catalog data, re-use \
existent raw data in the test directory as specified by the '%s' option. \
Default is to download the data." %CommandLineOptions.TEST_DIR)    

        self.add_option(CommandLineOptions.PREPROCESS_RAW, 
                        action="store_false", 
                        dest="preprocess_raw_data",
                        default=True, 
                        help="Do not pre-process downloaded raw catalog data, re-use \
existent pre-processed data in the test directory as specified by the '%s' option. \
Default is to pre-process the data." %CommandLineOptions.TEST_DIR)    
        
        self.add_option(CommandLineOptions.STAGING, 
                        action="store_false", 
                        dest="stage_data",
                        default=True, 
                        help="Do not stage existing data products, generate \
new data products instead. Default is to stage existing data products \
(forecasts, observation catalogs).")
        
        
        self.add_option(CommandLineOptions.RANDOM_FILES, 
                        action="store_true", 
                        dest="use_random_num_files",
                        default=False, 
                        help="Extract random seed numbers from the files. \
Default is to create new seed for random number generator.")
        
        
        self.add_option(CommandLineOptions.FORECASTS,
                        dest="forecast_dir",
                        type="string",
                        default=None,
                        help="Directory to read from or to store files \
generated by forecast models to. Default is None.", 
                        metavar="DIR")

        help_message = "Keywords for registered forecast models to invoke. One of %s. \
 Default is None which means to use file-based models in directory as specified by the \
 '%s' option." %(ForecastFactory().keys(), CommandLineOptions.FORECASTS)
        self.add_option(CommandLineOptions.GENERATE_FORECAST, 
                        dest="generate_forecast",
                        type="string",
                        default=None, 
                        help=help_message,
                        metavar="FORECAST LIST")        

        help_message = "Input arguments for the forecasts models to invoke. \
Default is None. Arguments for the same model are comma-separated \"key=value\" \
pairs. A '%s'-character separator is used to separate \
arguments for different models." %(CSEPInputParams.CSEPInputParams.InputSeparator)
        self.add_option(CommandLineOptions.FORECASTS_INPUTS, 
                        dest="forecasts_inputs",
                        type="string",
                        default=None, 
                        help=help_message,
                        metavar="\"arg1=value1, arg2=value2,...[|...]\"")        

        help_message = "Forecasts type for the experiment. \
One of %s, with default type of '%s'." %(ForecastHandlerFactory().keys(),
                                         ForecastHandlerFactory().CurrentHandler.Type)
        self.add_option(CommandLineOptions.FORECASTS_TYPE, 
                        dest="forecast_handler_type",
                        type="string",
                        default=RateForecastHandler.Type, 
                        help=help_message,
                        metavar="TYPE")        

        help_message = "Do not use forecast weights for evaluation tests. \
Default behavior is to use model weights." 
        self.add_option(CommandLineOptions.WEIGHTS, 
                        action="store_false", 
                        dest="forecast_weights",
                        default=True, 
                        help=help_message)        

        help_message = "Enable master XML forecast template for evaluation tests. \
The master template is populated by the forecast values to guarnatee the same \
models dimensions and bin order for evalation tests. Default behavior is NOT to use \
the template." 
        self.add_option(CommandLineOptions.FORECAST_TEMPLATE, 
                        action="store_true", 
                        dest="forecast_xml_template",
                        default=False, 
                        help=help_message)        

        help_message = "Disable validation of XML forecast file as generated \
by the model code by passing it through master XML forecast template. \
Default behavior is to validate XML format of the forecast by the CSEP Testing\
Framework." 
        self.add_option(CommandLineOptions.VALIDATE_XML_FORECAST, 
                        action="store_false", 
                        dest="validate_xml_forecast",
                        default=True, 
                        help=help_message)        

        help_message = "Enable generation of forecasts maps. Default behavior is \
to skip map generation for forecasts."
        self.add_option(CommandLineOptions.FORECAST_MAP, 
                        action="store_true", 
                        dest="forecast_map",
                        default=False, 
                        help=help_message)        

        self.add_option(CommandLineOptions.TEST_RESULT_PLOT, 
                        action="store_false", 
                        dest="result_plot", 
                        default=True, 
                        help="Create plot for each evaluation test result \
located under directory specified by '%s' option. \
Default is to generate test result plot." %CommandLineOptions.FORECASTS)


        self.add_option(CommandLineOptions.NUM_DECLUSTER_SIMULATIONS, 
                        dest="num_decluster_simulations", 
                        default=1000, 
                        type='int',
                        metavar = "NUM",
                        help="Number of simulations for declustering. \
Default is 1000.")
        
        self.add_option(CommandLineOptions.NUM_TEST_SIMULATIONS, 
                        dest="num_test_simulations", 
                        default=1000, 
                        type="int",
                        metavar = "NUM",                        
                        help="Number of simulations for evaluation test. \
Default is 1000.")
        
        self.add_option(CommandLineOptions.NUM_CATALOG_VARIATIONS, 
                        dest="num_catalog_variations", 
                        default=1000, 
                        type='int',
                        metavar = "NUM",                        
                        help="Number of catalogs with applied uncertainties. \
Default is 1000.")

        self.add_option(CommandLineOptions.HORIZONTAL_ERROR, 
                        action="store_false", 
                        dest="horizontal_error",
                        default=True, 
                        help="Disable horizontal error for catalog uncertainties. \
Default is to apply horizontal error.")

        self.add_option(CommandLineOptions.DEPTH_ERROR, 
                        action="store_false", 
                        dest="depth_error",
                        default=True, 
                        help="Disable depth error for catalog uncertainties. \
Default is to apply depth error.")

        self.add_option(CommandLineOptions.MAGNITUDE_ERROR, 
                        action="store_false", 
                        dest="magnitude_error",
                        default=True, 
                        help="Disable magnitude error for catalog uncertainties. \
Default is to apply magnitude error.")
        
        self.add_option(CommandLineOptions.LOG_FILE, 
                        dest="log_file", 
                        type="string",
                        help="Log file used to capture progress and error \
messages to. This option is used only to make the software aware of the file \
where it's output was redirected to. Caller has to explicitly redirect output \
and error streams to the specified file. Default is stdout stream handler.", 
                        metavar="FILE",
                        default=None)
        
        self.add_option(CommandLineOptions.LOG_LEVEL, 
                        dest="log_level", 
                        type="string",
                        help="Level for progress reporting. One of %s. \
Default is 'info'." %CSEPOptionParser.__reportLevels.keys(), 
                        metavar="INT",
                        default='info')


    #--------------------------------------------------------------------
    #
    # Check for a specific required option.
    #
    # Input: 
    #        opt - Name of the required option.
    # 
    def __checkRequired (self, opt):
       """ Check for existence of required options."""
       
       option = self.get_option(opt)

       # Assumes the option's default value to be None
       if getattr(self.values, option.dest) is None:
           self.print_help()
           self.error("Required %s option is missing." %option)
    
    
    #===========================================================================
    # Overwrite error handler to allow use of 'Error' keyword to trigger failure
    # in CSEP testing framework if python's optparse.error occurs (uses 'error'
    # keyword which is not specified in the CSEP set of possible error tokens - 
    # some forecasts use '*error*' pattern in stdout to report progress) 
    #===========================================================================
    def error(self, msg):
        """Overwrite error handler to allow use of CSEP error token to trigger
           CSEP-type of failure report"""
        
        sys.stderr.write('%s Error: %s\n' %(CSEPOptionParser.__name__, msg))
        optparse.OptionParser.error(self, msg)
         
       
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

        # Parse command line arguments
        (values, args) = self.parse_args()

        # Check for required options
        if required_options != None:
            for option in required_options:
               self.__checkRequired(option)
       
        # Initialize forecast settings
        CSEP.Forecast.initialize(values.forecast_weights,
                                 values.forecast_xml_template,
                                 values.validate_xml_forecast,
                                 values.forecast_map)
        
        # Testing framework supports rate-based and polygon-based forecasts
        ForecastHandlerFactory().object(values.forecast_handler_type)

        CSEPRandom.ReadSeedFromFile = values.use_random_num_files

        # Initialize evaluation test settings
        EvaluationTest.EvaluationTest.initialize(values.num_test_simulations,
                                                 values.result_plot)
        
        # Initialize catalog settings
        CSEP.Catalog.initialize(values.num_decluster_simulations,
                                values.num_catalog_variations,
                                values.horizontal_error,
                                values.depth_error,
                                values.magnitude_error)
        
        # Set geographical region if it's specified
        GeographicalRegions.Region().set(values.region)
        
        # Set flag for staging of existing data products (forecasts, observation
        # catalogs)
        CSEPStorage.CSEPStorage.allowStaging(values.stage_data)
        
        # Set up the root logger
        root_logger_name = ''
        CSEPLogging.CSEPLogging.getLogger(root_logger_name, 
                                          CSEPOptionParser.__reportLevels[values.log_level])
                                          # Don't redirect messages to the file, it should
                                          # be explicitly redirected by the caller
                                          # values.log_file)
        
        return values
     

# Invoke the module
if __name__ == '__main__':

   import Environment
   
   
   parser = CSEPOptionParser()
        
   # List of requred options
   required_options = [CommandLineOptions.YEAR,
                       CommandLineOptions.MONTH,
                       CommandLineOptions.DAY]
   
   options = parser.options(required_options)
   
   # Test logging
   logger = CSEPLogging.CSEPLogging.getLogger()
   logger.warning("Test warning message")
   logger.debug("Test debug message")  
   logger.error("Test error message")
   logger.exception("Test exception")  
   logger.info("Test info message")
   logger.info("userName = %s" %Environment.commandOutput('whoami'))
   logger.debug("Command line options: %s" %options)
     
# end of class
