"""
Module RTestAsymptoticResults
"""

__version__ = "$Revision: 3315 $"
__revision__ = "$Id: RTestAsymptoticResults.py 3315 2011-05-20 23:32:13Z  $"


import sys, os, shutil
from xml.etree.cElementTree import parse, ElementTree

import CSEPGeneric, CSEPXML, EvaluationTest, CSEP
from Environment import *
from CSEPTestCase import CSEPTestCase
from OneDayModelPostProcess import OneDayModelPostProcess
from PostProcess import PostProcess
from ForecastGroup import ForecastGroup
from RELMLikelihoodRatioTest import RELMLikelihoodRatioTest


 #--------------------------------------------------------------------
 #
 # Validate that R-test RELM evaluation test generates results asymptotically.
 #
class RTestAsymptoticResults (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 
                                     'asymptoticResults')

   # Use one day model post-processing to avoid scaling of the forecast rates
   __postProcess = OneDayModelPostProcess()


   #--------------------------------------------------------------------
   #
   # Overwrite CSEPTestCase initialization routine for Matlab.
   #
   def initialize(self):
       """ Initialize Matlab related variables for the test."""

       CSEPTestCase.initialize(self)
       EvaluationTest.EvaluationTest.initialize(num_test_simulations = 1)

   
   #--------------------------------------------------------------------
   #
   # This test confirms that R-test is generating results asymptotically: R12 = -R21.
   # It parses XML format result data to extract simulation values for the result evaluation.
   #
   def test(self):
      """ Confirm that R-test produces the same result asymptotically (R12 = -R21)."""

      # Setup test name
      CSEPTestCase.setTestName(self, "RTestAsymptoticResults")

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)

      
      try:
         # Reference catalog data file for the test - observations
         reference_catalog = "RTestAsymptoticResultsCatalog.dat"
         
         ### Generate R12 results  
         
         # Names of the forecasts models
         forecast1_name = os.path.join(self.__referenceDataDir, "forecast1.dat")
         forecast2_name = os.path.join(self.__referenceDataDir, "forecast2.dat")
         
         # Name of the file with random numbers for the test
         random_dir = "R-Test_forecast1_forecast2"
         result_dir = "rTest_R-Test_forecast1_forecast2_results"

         [R12_simulation1, R12_simulation2] = self.__getRTestResults(forecast1_name,
                                                                     forecast2_name,
                                                                     reference_catalog,
                                                                     random_dir, 
                                                                     result_dir)

         ### Generate R21 results  
         
         # Name of the file with random numbers for the test
         random_dir = "R-Test_forecast2_forecast1"
         result_dir = "rTest_R-Test_forecast2_forecast1_results"
         
         [R21_simulation1, R21_simulation2] = self.__getRTestResults(forecast2_name,
                                                                     forecast1_name,
                                                                     reference_catalog,
                                                                     random_dir, 
                                                                     result_dir)

         ### Compare results: R12 = R21
         error_message = "Failed to compare R12_simulation1 and \
R21_simulation2: %s vs. %s" %(R12_simulation1, R21_simulation2)
         self.failUnlessEqual(R12_simulation1, R21_simulation2, 
                              error_message)
         

         error_message = "Failed to compare R12_simulation2 and \
R21_simulation1: %s vs. %s" %(R12_simulation2, R21_simulation1)
         self.failUnlessEqual(R12_simulation2, R21_simulation1, 
                              error_message)

      finally:
         # Go back to the original directory
         os.chdir(cwd)         
         
         
   #--------------------------------------------------------------------
   #
   # Invoke R-test and extract results of simulations for both models.
   #
   # Input:
   #           forecast1 - Name of the file that represents 1st forecast model.
   #           forecast2 - Name of the file that represents 2nd forecast model.     
   #           catalog - Observation catalog.
   #           random_dir - Directory with files that represent simulations seed 
   #                        values for random number generator.
   #           result_dir - Directory with test results.
   #
   # Output:
   #           [list1, list2] - Two lists that represent simulation values for input forecasts models.
   #
   def __getRTestResults(self, 
                         forecast1, 
                         forecast2, 
                         catalog,
                         random_dir, 
                         result_dir):
      """ Invoke R-test and return sorted result arrays for both models simulations."""

      # Copy random seed files used by evaluation test to the test directory
      shutil.copytree(os.path.join(self.__referenceDataDir,
                                   random_dir),
                      result_dir)

      shutil.copyfile(os.path.join(self.__referenceDataDir,
                                   catalog),
                     os.path.join(result_dir,
                                  self.__postProcess.files.catalog))
            
      __post_process  = PostProcess(OneDayModelPostProcess.MinMagnitude,
                                    OneDayModelPostProcess.MaxDepth,
                                    catalogs = PostProcess.Files(catalog))
                                    
      self.__postProcess.startDate(CSEPTestCase.Date) 


      # Instantiate forecast group for the tests
      forecast_group = ForecastGroup(self.__referenceDataDir,
                                     self.__postProcess)

      test = RELMLikelihoodRatioTest(forecast_group)

      test.prepare(CSEPTestCase.Date,
                   result_dir,
                   result_dir)
          
      (scaled_forecast1, area_flag) = test.prepareForecast(forecast1)
      (scaled_forecast2, area_flag) = test.prepareForecast(forecast2)
      
      test.prepareCatalog()
      
      result = test._invoke(scaled_forecast1,
                            scaled_forecast2,
                            os.path.join(result_dir,
                                         random_dir))

      return  result[RELMLikelihoodRatioTest.Result.SimulationData1], \
              result[RELMLikelihoodRatioTest.Result.SimulationData2]
              

# Invoke the module
if __name__ == '__main__':

   import unittest
       
   # Invoke all tests
   unittest.main()
        
# end of main
