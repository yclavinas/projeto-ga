"""
Module DispatcherInitFileTest
"""

__version__ = "$Revision: 3448 $"
__revision__ = "$Id: DispatcherInitFileTest.py 3448 2011-08-12 17:05:35Z liukis $"


import sys, os, unittest, shutil, datetime

import CSEP, OneDayModelInputPostProcess, GeographicalRegions
from Environment import *
from CSEPTestCase import CSEPTestCase
from DispatcherInitFile import DispatcherInitFile
from CMTDataSource import CMTDataSource
from ANSSDataSource import ANSSDataSource
from CatalogDataSource import CatalogDataSource


 #--------------------------------------------------------------------
 #
 # Validate that DispatcherInitFile class is working properly.
 #
class DispatcherInitFileTest (CSEPTestCase):

   # Static data of the class

   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'dispatcherInitFile')

   __referenceDataFile = os.path.join(__referenceDataDir,
                                     'dispatcher.init.xml')

   __postProcessConfigFile = os.path.join(__referenceDataDir,
                                          'TestPostProcessFactory.init.xml')
   
   
   #--------------------------------------------------------------------
   #
   # This test verifies that DispatcherInitFile class identifies  
   # element values properly.
   #
   def testElementsValues(self):
      """ Confirm that DispatcherInitFile identifies \
elements values properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, "DispatcherInitFileValues")
   
      # cd to the test directory, remember current directory 
      # (done to locate configuration files Dispatcher file is refering to)
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      # Copy ForecastFactory config file that Dispatcher configuration is 
      # referring to
      shutil.copyfile(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                   CSEPTestCase.ForecastFactoryConfigFile),
                      os.path.join(CSEPTestCase.TestDirPath, 
                                   CSEPTestCase.ForecastFactoryConfigFile))    

      # Copy PostProcessFactory config file that Dispatcher configuration is
      # referring to
      shutil.copyfile(DispatcherInitFileTest.__postProcessConfigFile,
                      os.path.join(CSEPTestCase.TestDirPath, 
                                   os.path.basename(DispatcherInitFileTest.__postProcessConfigFile)))    

      # Remember original values for environment variables
      original_gmt_home = os.environ[GMT_HOME_ENV]
      original_netcdf_home = os.environ[NETCDF_HOME_ENV]
      original_image_magick_home = os.environ[IMAGE_MAGICK_HOME_ENV]

      # Remember data members of PostProcessing classes that are overwritten
      # by configuration file - to be re-set back to original values after 
      # test validation
      one_day_input_min_magnitude = OneDayModelInputPostProcess.OneDayModelInputPostProcess.MinMagnitude
      one_day_input_max_depth = OneDayModelInputPostProcess.OneDayModelInputPostProcess.MaxDepth
      
      try:   
         init_file = DispatcherInitFile(self.__referenceDataFile)
   
         ### Validate results
         
         # Geographical region - California
         region = GeographicalRegions.Region.info()
         
         reference_data = os.path.join(Environment.Variable[CENTER_CODE_ENV], 
                                       'data', 'areas', 'RELMCollectionArea.dat')
         self.failIf(reference_data != region.collectionArea,
                     "Expected %s, got %s for the geographical region" %(reference_data,
                                                                         region.collectionArea))

         reference_data = os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                       'data', 'areas', 'RELMTestArea.dat')
         self.failIf(reference_data != region.testArea,
                     "Expected %s, got %s for the geographical region" %(reference_data,
                                                                         region.testArea))
                                       
         reference_data = os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                       'src', 
                                       'GMTScripts')
         self.failIf(reference_data != region.mapScriptLocation,
                     "Expected %s, got %s for the geographical region" %(reference_data,
                                                                         region.mapScriptLocation))
         
         reference_data = 'forecast.gmt -p bf'
         self.failIf(reference_data != region.mapScript,
                     "Expected %s, got %s for the geographical region" %(reference_data,
                                                                         region.mapScript))
                                        
         reference_value = "dispatcher_runs"  
         root_dir = init_file.elementValue(DispatcherInitFile.RootDirectoryElement)    
         
         error_message = "DispatcherInitFileTest: expected '%s' \
value, got '%s'." %(reference_value, root_dir)
         self.failIf(root_dir != reference_value, error_message)        
         
         reference_value = "data/forecasts/foo"  
         group_dir = init_file.elementValue(DispatcherInitFile.ForecastGroupElement)    
         
         error_message = "DispatcherInitFileTest: expected '%s' \
value, got '%s'." %(reference_value, group_dir)
         self.failIf(group_dir != reference_value, error_message)        

         ### Email values are testes by separate unit test - CSEPEmailTest.py
         
         ### Check values for catalog data source
         all_data_sources = init_file.dataSource()
         
         # Validate ANSS data source settings:
         data_source = all_data_sources[ANSSDataSource.Type]
         
         self.failIf(data_source.type() != ANSSDataSource.Type, 
                     "DispatcherInitFileTest: expected %s, received %s data source" \
                     %(ANSSDataSource.Type, data_source.type()))
         
         expected_start_date = datetime.datetime(1934, 1, 1)
         self.failIf(data_source.StartDate != expected_start_date,
                     "DispatcherInitFileTest: expected %s, received %s start date for \
data source" %(expected_start_date, data_source.StartDate))
         
         expected_min_magnitude = 0.1
         self.failIf(data_source.MinMagnitude != expected_min_magnitude,
                     "DispatcherInitFileTest: expected %s, received %s min magnitude for \
data source" %(expected_min_magnitude, data_source.MinMagnitude))
         

         # Validate ANSS data source settings:
         data_source = all_data_sources[CMTDataSource.Type]
         
         self.failIf(data_source.type() != CMTDataSource.Type, 
                     "DispatcherInitFileTest: expected %s, received %s data source" \
                     %(CMTDataSource.Type, data_source.type()))
         
         expected_start_date = datetime.datetime(1977, 1, 1)
         self.failIf(data_source.StartDate != expected_start_date,
                     "DispatcherInitFileTest: expected %s, received %s start date for \
data source" %(expected_start_date, data_source.StartDate))
         
         expected_options = {'includePreliminary' : 'True'}
         self.failIf(data_source.Options != expected_options,
                     "DispatcherInitFileTest: expected %s, received %s options for \
data source" %(expected_options, data_source.Options))
             
         
         ### Check value for forecast factory configuration file
         factory_config_file = init_file.elements(DispatcherInitFile.ForecastFactoryElement)[0]
         file_path, file_name = os.path.split(factory_config_file.text.strip())
         self.failIf(file_name != CSEPTestCase.ForecastFactoryConfigFile,
                     "DispatcherInitFileTest: Expected %s for forecast factory element" %
                     CSEPTestCase.ForecastFactoryConfigFile)
         
         # Check for updated Python path
         path_value = 'user/fooTestPath1'
         self.failIf(sys.path.count(path_value) != 1,
                     "DispatcherInitFileTest: expected %s in sys.path" %path_value)
         
         path_value = 'user/fooTestPath2'
         self.failIf(sys.path.count(path_value) != 1,
                     "DispatcherInitFileTest: expected %s in sys.path" %path_value)

         expected_value = "other/gmt/path"
         self.failIf(os.environ[GMT_HOME_ENV] != expected_value,
                     "Expected '%s', received %s" \
                     %(expected_value, os.environ[GMT_HOME_ENV]))
         
         expected_value = "other/netCDF/path"
         self.failIf(os.environ[NETCDF_HOME_ENV] != expected_value,
                     "Expected '%s', received %s" \
                     %(expected_value, os.environ[NETCDF_HOME_ENV]))

         expected_value = "other/imageMagick/path"
         self.failIf(os.environ[IMAGE_MAGICK_HOME_ENV] != expected_value,
                     "Expected '%s', received %s" \
                     %(expected_value, os.environ[IMAGE_MAGICK_HOME_ENV]))
         
         
         self.__validatePostProcessing()
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd) 
         
         # Set variables to original values
         os.environ[GMT_HOME_ENV] = original_gmt_home
         os.environ[NETCDF_HOME_ENV] = original_netcdf_home
         os.environ[IMAGE_MAGICK_HOME_ENV] = original_image_magick_home
         
         # Set PostProcess classes data to original values
         OneDayModelInputPostProcess.OneDayModelInputPostProcess.MinMagnitude = one_day_input_min_magnitude
         OneDayModelInputPostProcess.OneDayModelInputPostProcess.MaxDepth = one_day_input_max_depth
         

   #-----------------------------------------------------------------------------
   #
   # This method verifies that PostProcessingFactoryConfigFile as specified in 
   # DispatcherInitFile sets static data values of the classes properly.
   #
   def __validatePostProcessing(self):
      """ Validate PostProcessing static data members."""
      

      # OneDayModelInputPostProcess class
      expected_value = 2.95
      self.failIf(OneDayModelInputPostProcess.OneDayModelInputPostProcess.MinMagnitude != expected_value,
                  "Expected '%s' for OneDayModelInputPostProcess.MinMagnitude, received %s" \
                  %(expected_value, 
                    OneDayModelInputPostProcess.OneDayModelInputPostProcess.MinMagnitude))
      
      expected_value = 40
      self.failIf(OneDayModelInputPostProcess.OneDayModelInputPostProcess.MaxDepth != expected_value,
                  "Expected '%s' for OneDayModelInputPostProcess.MaxDepth, received %s" \
                  %(expected_value, 
                    OneDayModelInputPostProcess.OneDayModelInputPostProcess.MaxDepth))


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
