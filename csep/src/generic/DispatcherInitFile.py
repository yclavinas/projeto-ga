"""
Module DispatcherInitFile
"""

__version__ = "$Revision: 3489 $"
__revision__ = "$Id: DispatcherInitFile.py 3489 2011-11-03 22:19:40Z liukis $"

import os, datetime, copy

import CSEP, Environment, CSEPInitFile, DataSourceFactory, ForecastFactory, \
       PostProcessFactory, CatalogDataSource, CSEPLogging


#--------------------------------------------------------------------------------
#
# DispatcherInitFile
#
# This module is designed to open and parse XML format files that represent
# initialization parameters for the Dispatcher.
# These files consist of any combination of the following elements:
#    - RootDirectory - Top level directory for all dispatcher runs.
#    - ForeacastGroup - Directory path for the forecast group. There should be
#                       one element per each forecast group Dispatcher need to 
#                       handle.
#
class DispatcherInitFile (CSEPInitFile.CSEPInitFile):

    # Static data members

    # Name of top level directory for all dispatcher runs and attributes
    RootDirectoryElement = 'directory'
     
    # Attribute to specify location of existing raw data file - used only
    # by acceptance tests of CSEP testing framework for now
    RawDataDirAttribute = 'rawDataDir'  
    PreProcessedDataDirAttribute = 'preProcessedDataDir'
    InputCatalogAttribute = 'inputCatalog'
    
    # Name of ForecastGroup element Dispatcher should handle.
    ForecastGroupElement = 'forecastGroup'

    # Name of forecast factory configuration file element and attributes - optional
    ForecastFactoryElement = 'forecastFactoryConfigFile'
    
    # Name of catalog post-processing modules configuration file - optional
    # ATTN: this is to overwrite static data of existing PostProcess classes 
    #       that are set up by default for California testing region
    PostProcessFactoryElement = 'postProcessFactoryConfigFile'
    
    # Name of catalog data source element and attributes - optional
    __dataSourceElement = 'catalogDataSource'
    __catalogStartDateAttribute = 'startDate'
    __catalogMinMagnitudeAttribute = 'minMagnitude'
    __dataSourceOptionsAttribute = 'options'
    
    # Name of environment element and attributes specific to the configuration
    __environmentElement = "environment"
    
    # Names for XML format elements
    __XMLTopLevelElements = [RootDirectoryElement,
                             ForecastGroupElement]

    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #       filename - Filename for the input parameters. Default is
    #                  "dispatcher.init.xml".
    # 
    def __init__ (self, filename):    
        """ Initialization for ForecastGroupInitFile class."""

        CSEPInitFile.CSEPInitFile.__init__(self,
                                           filename, 
                                           DispatcherInitFile.__XMLTopLevelElements)
        
        # Load Python modules for factories as specified by corresponding 
        # configuration file (if any) or any directories that are specific
        # to the configuration
        self.__initEnvironment()
        

    #----------------------------------------------------------------------------
    #
    # Accessor for DataSource object represented by the initialization file. 
    #
    # Input: download_raw_data - Flag if raw data should be downloaded from
    #                            authorized data source. Default is True.
    #       
    # Output: CatalogDataSource object that represents data source for catalog. 
    #         It defaults to ANSS data source if none was provided by the file.
    # 
    def dataSource(self,
                   download_raw_data = True,
                   pre_process_raw_data = True):
       """ Returns CatalogDataSource object that represents data source for the
           catalog. It defaults to ANSS data source if none was provided by the 
           file. """
           

       # If default behavior to download raw catalog data needs 
       # to be overwritten, specify such option   
       __default_args = {'download_data' : download_raw_data,
                         'pre_process_data' : pre_process_raw_data}


       # Is data source element provided by the file? - use default source (ANSS)
       # if it's not provided
       data_sources = self.elements(DispatcherInitFile.__dataSourceElement)

       if len(data_sources) != 0:

           DataSourceFactory.DataSourceFactory.composite().clear()
           
           for data_source_elem in self.elements(DispatcherInitFile.__dataSourceElement): 
            
              args = copy.deepcopy(__default_args)
              
              # Data source is provided
              attribs = data_source_elem.attrib
              source_type = data_source_elem.text.strip()
              
              # Start date is provided
              if DispatcherInitFile.__catalogStartDateAttribute in attribs:
                 
                 # Get string representation of the start date for catalog data 
                 start_date_str = attribs[DispatcherInitFile.__catalogStartDateAttribute]
                 
                 # convert start date to datetime.date() object          
                 args['start_date'] = datetime.datetime.strptime(start_date_str, 
                                                                 CSEP.Time.DateFormat)
                 
              if DispatcherInitFile.__catalogMinMagnitudeAttribute in attribs:
                 
                 # Set minimum magnitude for downloaded catalog data
                 args['min_magnitude'] = float(attribs[DispatcherInitFile.__catalogMinMagnitudeAttribute])
              
    
              if DispatcherInitFile.__dataSourceOptionsAttribute in attribs:
                 
                 # Set optional parameters to by used by data source
                 args['args']  = attribs[DispatcherInitFile.__dataSourceOptionsAttribute]
              
              DataSourceFactory.DataSourceFactory().object(source_type,
                                                           args)
                  
       else:
            # Create default data source for processing - ANSS
            DataSourceFactory.DataSourceFactory().object(input_variables = __default_args)
       
       # Return all data source objects as generated by the factory 
       return DataSourceFactory.DataSourceFactory.composite()


    #----------------------------------------------------------------------------
    #
    # Initiate runtime loading of installed forecast models if specified by
    # the initialization file, and initialize directories paths used by
    # current configuration
    #
    # Input: None. 
    #       
    # Output: None.
    # 
    def __initEnvironment(self):
       """ Initiate runtime loading of installed forecast models if specified by
           the initialization file, and set up configuration environment. """
           
       # If configuration file is provided for the ForecastFactory
       config_file_list = self.elements(DispatcherInitFile.ForecastFactoryElement)
        
       # Configuration file(s) is(are) provided ---> load modules
       for each_file in config_file_list:
          ForecastFactory.ForecastFactory(Environment.replaceVariableReference(Environment.CENTER_CODE_ENV,
                                                                               each_file.text.strip()))

       # If configuration file is provided for the PostProcessFactory 
       # ATTN: this is to overwrite static data of existing PostProcess classes 
       #       that are set up by default for California testing region
       config_file_list = self.elements(DispatcherInitFile.PostProcessFactoryElement)
       for each_file in config_file_list:
          PostProcessFactory.PostProcessFactory(Environment.replaceVariableReference(Environment.CENTER_CODE_ENV,
                                                                                     each_file.text.strip()))
          
       # Check if directories are specified
       for each_elem in self.elements(DispatcherInitFile.__environmentElement):

          attribs = each_elem.attrib

          # Check for specific attributes:
          if Environment.GMT_HOME_ENV in attribs:
             os.environ[Environment.GMT_HOME_ENV] = attribs[Environment.GMT_HOME_ENV]
             
          if Environment.NETCDF_HOME_ENV in attribs:
             os.environ[Environment.NETCDF_HOME_ENV] = attribs[Environment.NETCDF_HOME_ENV]
             
          if Environment.IMAGE_MAGICK_HOME_ENV in attribs:
             os.environ[Environment.IMAGE_MAGICK_HOME_ENV] = attribs[Environment.IMAGE_MAGICK_HOME_ENV]


# Invoke the module
if __name__ == '__main__':

   import CSEPLogging, DispatcherOptionParser
   

   parser = DispatcherOptionParser.DispatcherOptionParser()
   init_file = DispatcherInitFile(parser.options().config_file)
   
   CSEPLogging.CSEPLogging.getLogger(DispatcherInitFile.__name__).debug("Init file exists: %s" \
                                                                        %init_file.exists())

# end of main
