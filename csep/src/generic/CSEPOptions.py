"""
Module CSEPOptions
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


# Collection of command-line options used by the CSEP Testing Framework
class CommandLineOptions (object):
    
    # The reason of storing these data attributes outside of the *OptionParser.py
    # modules is to avoid module dependency problems during imports
    
    # Generic command-line options
    YEAR = "--year"
    MONTH = "--month"
    DAY = "--day"
    
    ### Use '--testDir' directory where to find raw data if its download is 
    ### disabled
    DOWNLOAD_RAW = "--disableRawDataDownload"
    PREPROCESS_RAW = "--disableRawDataPreProcess"
    
    STAGING = "--disableExistingDataStaging"
    TEST_DIR = "--testDir"
    
    # Evaluation tests options
    TESTS = "--tests"
    TESTS_INPUTS = "--testsInputs"
    RANDOM_FILES = "--withRandomNumbersFiles"
    
    # Catalog post-processing options
    POST_PROCESS = "--postProcessing"
    POST_PROCESS_ARGS = "--postProcessingArgs"
    
    # Forecasts options
    FORECASTS = "--forecasts"
    GENERATE_FORECAST = "--generateForecasts"
    FORECASTS_INPUTS = "--forecastsInputs"
    FORECASTS_TYPE = "--forecastType"
    WEIGHTS = "--disableForecastWeights"
    FORECAST_TEMPLATE = "--enableForecastXMLTemplate"
    VALIDATE_XML_FORECAST = "--disableXMLForecastValidation"
    FORECAST_MAP = "--enableForecastMap"
    TEST_RESULT_PLOT = "--disableTestResultPlot"
    
    # RELM evaluation tests options
    NUM_DECLUSTER_SIMULATIONS = "--numDeclusterSimulations"
    NUM_TEST_SIMULATIONS = "--numTestSimulations"
    NUM_CATALOG_VARIATIONS = "--numVariationsSimulations"
    
    # Catalog uncertainties fields
    HORIZONTAL_ERROR = "--disableGeographicalError"
    DEPTH_ERROR = "--disableDepthError"
    MAGNITUDE_ERROR = "--disableMagnitudeError"
    
    
    LOG_FILE = "--logFile"
    LOG_LEVEL = "--logLevel"
    REGION = "--geographicalRegion"

    # Dispatcher specific options
    CONFIG_FILE = "--configFile"
    WAITING_PERIOD = "--waitingPeriod"
    PUBLISH_SERVER = "--publishServer"
    PUBLISH_DIR = "--publishDirectory"
    PUBLISH_RUNTIME_SERVER = '--publishRuntimeInfoServer'
    PUBLISH_RUNTIME_DIR = '--publishRuntimeInfoDir'

    # Authorized data source specific options
    CREATE_CATALOG = "--disableCatalogGeneration"
    CATALOG_SOURCE = "--catalogDataSource"
    CATALOG_START_DATE = "--catalogStartDate"
    CATALOG_MIN_MAGNITUDE = "--catalogMinMagnitude"
    CATALOG_SOURCE_INPUTS = "--catalogDataSourceOptions"
    
    # Factories specific options
    POST_PROCESS_FACTORY = "--postProcessFactory"
    FORECAST_FACTORY = "--forecastFactory"
    EVALUATION_TEST_FACTORY = "--evaluationTestFactory"


