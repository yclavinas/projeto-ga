"""
Module ForecastGroupTest
"""

__version__ = "$Revision: 3769 $"
__revision__ = "$Id: ForecastGroupTest.py 3769 2012-07-24 20:37:27Z liukis $"


import sys, os, unittest, shutil, datetime

import CSEP

from Environment import *
from CSEPTestCase import CSEPTestCase
from ForecastGroup import ForecastGroup
from RELMAftershockPostProcess import RELMAftershockPostProcess
from OneDayModelPostProcess import OneDayModelPostProcess
from BogusForecastModel1 import BogusForecastModel1
from BogusForecastModel2 import BogusForecastModel2
from HybridForecast import HybridForecast


 #--------------------------------------------------------------------
 #
 # Validate that ForecastGroup class is working properly.
 #
class ForecastGroupTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'forecastGroup')

   
   #--------------------------------------------------------------------
   #
   # This test verifies that ForecastGroup class identifies existing 
   # forecast files properly.
   #
   def testExistingFiles(self):
      """ Confirm that ForecastGroup identifies existing \
forecast files properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, "ForecastGroupExistingFiles")

      # Use csep/data/forecasts
      forecast_dir = os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                  "data", "forecasts")
      
      group = ForecastGroup(forecast_dir, RELMAftershockPostProcess.Type)

      ### Validate results
      # 13 forecast files are expected in specified directory
      expected_num_files = 13
      error_message = "ForecastGroupTest: failed to get expected %s \
forecast files." %expected_num_files

      self.assertEqual(len(group.files()),
                       expected_num_files, 
                       error_message)
        

   #--------------------------------------------------------------------
   #
   # This test verifies that ForecastGroup class properly parses 
   # initialization file.
   #
   def testInitializationFile(self):
      """ Confirm that ForecastGroup properly parses initialization file."""

      # Setup test name
      CSEPTestCase.setTestName(self, "ForecastGroupInitFile")

      # Copy reference init file to the test directory
      init_file = "forecast.init.xml"
      shutil.copyfile(os.path.join(self.__referenceDataDir, init_file),
                      os.path.join(CSEPTestCase.TestDirPath, init_file))    

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)

      ### Validate results
      
      # Forecast directory
      forecast_dir = os.path.join(CSEPTestCase.TestDirPath, 
                                  "forecasts")
      self.assertEqual(group.dir(),
                       forecast_dir, 
                       "Expected '%s' forecast directory, got %s." %(forecast_dir,
                                                                     group.dir()))

      # PostProcess object
      post_processing = group.postProcess()
      self.assertIsNotNone(post_processing,
                           "Expected valid PostProcessing object.")
      
      type = RELMAftershockPostProcess.Type
      self.assertEqual(post_processing.type(),
                       type, 
                       "Expected '%s' type of postProcessing object, got %s" %(type,
                                                                               post_processing.type()))
    
      # Check for start date of post-processing 
      expected_date = datetime.datetime(2006, 6, 1)
      self.assertEqual(post_processing.start_date, 
                       expected_date, 
                       "Expected startDate='%s', got '%s'" %(expected_date, 
                                                             post_processing.start_date))
      
      # Check for expiration date of post-processing
      expire_date = datetime.datetime(2011, 6, 1)
      self.assertTrue(post_processing.expires(expire_date),
                      "Expected to expire on '%s'" %expire_date)      


      # Models 
      self.assertTrue(group.hasModels(), 
                      "Expected forecast models in initialization file")

      # Existing forecast files
      self.assertEqual(len(group.files()), 0,
                       "There should not be any forecast files, found %s" %group.files())
      
      # Catalog directory
      catalog_dir = os.path.join(CSEPTestCase.TestDirPath, 
                                 "observations")
      self.assertEqual(group.catalogDir(),
                       catalog_dir,
                       "Expected '%s' catalog directory, got %s" %(catalog_dir,
                                                                   group.catalogDir()))
                  
      # Evaluation tests
      tests = "N L ROC MASS"
      
      file_tests = []
      for each_test in group.tests:
         file_tests.append(each_test.type())
      file_tests_str = ' '.join(file_tests)
      
      self.assertEqual(file_tests_str,
                       tests, 
                       "Expected '%s' evaluation tests, got '%s'" %(tests, 
                                                                    file_tests_str))


   #--------------------------------------------------------------------
   #
   # This test verifies that ForecastGroup class properly parses 
   # initialization file that contains HybridForecast configuration.
   #
   def testHybridModel(self):
      """ Confirm that ForecastGroup properly parses initialization file which \
contains HybridModel configuration."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      init_file = "forecast_with_hybrid_model.init.xml"
      shutil.copyfile(os.path.join(self.__referenceDataDir, init_file),
                      os.path.join(CSEPTestCase.TestDirPath, 
                                   "forecast.init.xml"))    

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)

      ### Validate results
      
      # Models within the group should include HybridForecast
      self.assertEqual(len(group.models), 3,
                       "Expected 3 forecasts models within the group, got %s models" %group.models)
      
      # One of the models should be HybridModels
      self.assertTrue(any(isinstance(model, HybridForecast) for model in group.models),
                  "One of group's forecasts must by of HybridForecast type, got %s objects" %group.models)
      
      


   #-----------------------------------------------------------------------------
   #
   # This test verifies that ForecastGroup class is properly initialized
   # by configuration file with missing evaluation tests.
   #
   def testInitializationFileNoTests(self):
      """ Confirm that ForecastGroup properly initialized by configuration file."""

      # Setup test name
      CSEPTestCase.setTestName(self, "ForecastGroupInitFileNoTests")

      # Copy reference init file to the test directory
      init_file = "forecast_no_tests.init.xml"
      shutil.copyfile(os.path.join(self.__referenceDataDir, init_file),
                      os.path.join(CSEPTestCase.TestDirPath, 'forecast.init.xml'))    

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)

      ### Validate results
      
      # Tests are not specified for the date
      self.assertFalse(group.hasTests(CSEPTestCase.Date),
                      "Group should not have any evaluation tests specified")


   #-----------------------------------------------------------------------------
   #
   # Fix for Trac ticket #94
   # This test verifies that ForecastGroup class stages archived XML format of 
   # the forecast file to create Matlab format file used by evaluation tests.
   #
   def testXMLForecastStaging(self):
      """ Confirm that ForecastGroup stages archived XML format of the forecast \
file to generate final Matlab format file used by evaluation tests."""

      # Setup test name
      CSEPTestCase.setTestName(self, "ForecastGroupStageXMLFile")

      # Copy forecast group directory to the runtime test directory
      group_dir = "forecasts"
      shutil.copytree(os.path.join(self.__referenceDataDir, group_dir),
                      os.path.join(CSEPTestCase.TestDirPath, group_dir))

      # Copy input catalog to the test directory
      input_catalog = 'OneDayModelInputCatalog.mat'
      shutil.copyfile(os.path.join(self.__referenceDataDir, 
                                   input_catalog),
                      os.path.join(CSEPTestCase.TestDirPath, 
                                   input_catalog))    
      
      CSEP.Forecast.UseXMLMasterTemplate = True
      
      try:
         
         group = ForecastGroup(os.path.join(CSEPTestCase.TestDirPath,
                                            group_dir),
                               post_process = OneDayModelPostProcess.Type,
                               model_list = '%s %s' %(BogusForecastModel1.Type,
                                                      BogusForecastModel2.Type))
         
         group.create(datetime.datetime(2008, 6, 1),
                      CSEPTestCase.TestDirPath)
         
      finally:
         
         CSEP.Forecast.UseXMLMasterTemplate = False
         
      # Validate that XML format files in top-level forecast directory are links
      # to archived files
      xml_files = ['BogusForecastModel1_6_1_2008.xml', 
                   'BogusForecastModel2_6_1_2008.xml']
      
      for each_file in xml_files:
         self.assertTrue(os.path.islink(os.path.join(CSEPTestCase.TestDirPath, 
                                                     group_dir,
                                                     each_file)),
                         "Expected '%s' link for archived forecast file." %each_file)
      

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
