"""
Module RandomEvaluationTests
"""

__version__ = "$Revision: 3315 $"
__revision__ = "$Id: RandomEvaluationTests.py 3315 2011-05-20 23:32:13Z  $"


import sys, string, os, unittest, shutil, filecmp, datetime

import CSEPFile, EvaluationTest

from CSEPTestCase import CSEPTestCase
from RELMAftershockPostProcess import RELMAftershockPostProcess
from RELMMainshockPostProcess import RELMMainshockPostProcess
from OneDayModelPostProcess import OneDayModelPostProcess
from ThreeMonthsModelPostProcess import ThreeMonthsModelPostProcess
from RELMCatalog import RELMCatalog
from RELMNumberTest import RELMNumberTest
from RELMLikelihoodTest import RELMLikelihoodTest
from RELMConditionalLikelihoodTest import RELMConditionalLikelihoodTest
from RELMLikelihoodRatioTest import RELMLikelihoodRatioTest
from RELMSpaceTest import RELMSpaceTest
from RELMMagnitudeTest import RELMMagnitudeTest
from PostProcessFactory import PostProcessFactory
from ForecastGroup import ForecastGroup
from cseprandom import CSEPRandom


 #--------------------------------------------------------------------
 #
 # Test RELM evaluation tests for the forecasts models.
 # This module verifies that we can run evaluation tests in "production" mode,
 # meaning that we draw random numbers for simulations by the system.
 #
class RandomEvaluationTests (CSEPTestCase):

    # Static data of the class
    
    # Test date for three-months models
    __threeMonthsModelsTestDay = datetime.datetime(2007, 12, 10)


    #--------------------------------------------------------------------
    #
    # Overwrite CSEPTestCase initialization routine for Matlab to force 
    # the system to draw random numbers for the tests.
    #
    def initialize(self):
        """ Initialize Matlab related variables for the test."""

        CSEPTestCase.initialize(self)
        
        CSEPRandom.ReadSeedFromFile = False
        EvaluationTest.EvaluationTest.NumberSimulations = 15


    #--------------------------------------------------------------------
    #
    # Run N-Test evaluation for the shortterm forecast, and validate that
    # result and random numbers file are generated. 
    #
    def testOneDayModelNTestRandom(self):
        """ Run N-test for the shortterm forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'shortterm_forecasts'
        
        # Reference file with test results
        result_filename = "rTest_N-Test_STEP_daily_11_2_2006.xml"     
        # New implementation does not use random numbers
        random_filename = None   

        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)
          

    #--------------------------------------------------------------------
    #
    # Run L-Test evaluation for the shortterm forecast, and validate the results.
    #
    def testOneDayModelLTestRandom(self):
        """ Run L-test for the shortterm forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMLikelihoodTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'shortterm_forecasts'
        
        # Name of the file with random numbers for the test
        random_filename = "L-Test_STEP_daily_11_2_2006"
        
        # Reference file with test results
        result_filename = "rTest_L-Test_STEP_daily_11_2_2006.xml"        

        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)


    #---------------------------------------------------------------------------
    #
    # Run CL-Test evaluation for the shortterm forecast, and validate the results.
    #
    def testOneDayModelCLTestRandom(self):
        """ Run CL-test for the shortterm forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMConditionalLikelihoodTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'shortterm_forecasts'
        
        # Name of the file with random numbers for the test
        random_filename = "CL-Test_STEP_daily_11_2_2006"
        
        # Reference file with test results
        result_filename = "rTest_CL-Test_STEP_daily_11_2_2006.xml"        

        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)


    #---------------------------------------------------------------------------
    #
    # Run S-Test evaluation for 5-year RELM Mainshock forecast, 
    # and validate the results.
    #
    def testRELMMainshockSTestRandom(self):
        """ Run S-test for 5-year RELMMainshock forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMSpaceTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'S_M_evaluationTestsForecasts'
        
        # Name of the file with random numbers for the test
        random_filename = "S-Test_spatialForecast"
        
        # Reference file with test results
        result_filename = "rTest_S-Test_spatialForecast.xml"        

        # Store default values for RELMMainshockPostProcess
        min_magnitude = RELMMainshockPostProcess.MinMagnitude
        RELMMainshockPostProcess.MinMagnitude = 1.0
        
        try:
            self.__evaluationTest(test_list,
                                  RELMMainshockPostProcess.Type,
                                  random_filename,
                                  forecast_dir,
                                  result_filename,
                                  'S_M_evaluationTests.catalog.decl.dat',
                                  datetime.datetime(2011, 1, 1))
        finally:
            # Restore defaults
            RELMMainshockPostProcess.MinMagnitude = min_magnitude
            

    #---------------------------------------------------------------------------
    #
    # Run M-Test evaluation for 5-year RELM Mainshock forecast, 
    # and validate the results.
    #
    def testRELMMainshockMTestRandom(self):
        """ Run M-test for 5-year RELMMainshock forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMMagnitudeTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'S_M_evaluationTestsForecasts'
        
        # Name of the file with random numbers for the test
        random_filename = "M-Test_spatialForecast"
        
        # Reference file with test results
        result_filename = "rTest_M-Test_spatialForecast.xml"        

        # Store default values for RELMMainshockPostProcess
        min_magnitude = RELMMainshockPostProcess.MinMagnitude
        RELMMainshockPostProcess.MinMagnitude = 1.0
        
        try:
            self.__evaluationTest(test_list,
                                  RELMMainshockPostProcess.Type,
                                  random_filename,
                                  forecast_dir,
                                  result_filename,
                                  'S_M_evaluationTests.catalog.decl.dat',
                                  datetime.datetime(2011, 1, 1))
        finally:
            # Restore defaults
            RELMMainshockPostProcess.MinMagnitude = min_magnitude


    #--------------------------------------------------------------------
    #
    # Run N-Test evaluation for the longterm forecast, and validate the results.
    #
    def testRELMAftershockNTestRandom(self):
        """ Run N-test for the longterm forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files
        forecast_dir = 'forecasts'

        # New implementation does not use random numbers
        random_filename = None
        
        # Reference file with test results
        result_filename = "rTest_N-Test_wiemer_schorlemmer[1].alm.xml"        

        self.__evaluationTest(test_list,
                              RELMAftershockPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)
         

    #--------------------------------------------------------------------
    #
    # Run L-Test evaluation for the longterm forecast, and validate the results.
    #
    def testRELMAftershockLTestRandom(self):
        """ Run L-test for the longterm forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMLikelihoodTest.Type

        # Directory with forecast model files
        forecast_dir = 'forecasts'
        
        # Name of the file with random numbers for the test
        random_filename = "L-Test_wiemer_schorlemmer[1].alm"
        
        # Reference file with test results
        result_filename = "rTest_L-Test_wiemer_schorlemmer[1].alm.xml"        

        self.__evaluationTest(test_list,
                              RELMAftershockPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)
        

    #--------------------------------------------------------------------
    #
    # Run CL-Test evaluation for the longterm forecast, and validate the results.
    #
    def testRELMAftershockCLTestRandom(self):
        """ Run CL-test for the longterm forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMConditionalLikelihoodTest.Type

        # Directory with forecast model files
        forecast_dir = 'forecasts'
        
        # Name of the file with random numbers for the test
        random_filename = "CL-Test_wiemer_schorlemmer[1].alm"
        
        # Reference file with test results
        result_filename = "rTest_CL-Test_wiemer_schorlemmer[1].alm.xml"        

        self.__evaluationTest(test_list,
                              RELMAftershockPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)

        
    #--------------------------------------------------------------------
    #
    # Run R-Test evaluation for the longterm forecast, and validate the results.
    #
    def testRELMAftershockRTestRandom(self):
        """ Run R-test for the longterm forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMLikelihoodRatioTest.Type

        # Directory with forecast model files
        forecast_dir = 'rtest-forecasts'
        
        # Name of the file with random numbers for the test
        random_filename = "R-Test_holliday[1].pi_wiemer_schorlemmer[1].alm"
        
        # Reference file with test results
        result_filename = "rTest_R-Test_holliday[1].pi_wiemer_schorlemmer[1].alm.xml"        

        self.__evaluationTest(test_list,
                              RELMAftershockPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)


    #----------------------------------------------------------------------------
    #
    # Run N-Test evaluation for the three-months forecast, and validate the 
    # results.
    #
    def testThreeMonthsNTestRandom(self):
        """ Run N-test for the three-months forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files
        forecast_dir = 'three_months_forecasts'

        # New implementation does not use random numbers
        random_filename = None
        
        # Reference file with test results
        result_filename = "rTest_N-Test_EEPAS-0F_12_1_2007.xml"        
        
        # The forecast directory has configuration file with post-processing type
        # and start and end time for evaluation period
        self.__evaluationTest(test_list,
                              None,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'ThreeMonthsModel.catalog.nodecl.dat',
                              RandomEvaluationTests.__threeMonthsModelsTestDay)


    #----------------------------------------------------------------------------
    #
    # Run L-Test evaluation for the three-months forecast, and validate the 
    # results.
    #
    def testThreeMonthsLTestRandom(self):
        """ Run L-test for the three-months forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMLikelihoodTest.Type

        # Directory with forecast model files
        forecast_dir = 'three_months_forecasts'

        # Name of the file with random numbers for the test
        random_filename = "L-Test_EEPAS-0F_12_1_2007"
        
        # Reference file with test results
        result_filename = "rTest_L-Test_EEPAS-0F_12_1_2007.xml"        
        
        # The forecast directory has configuration file with post-processing type
        # and start and end time for evaluation period
        self.__evaluationTest(test_list,
                              None,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'ThreeMonthsModel.catalog.nodecl.dat',
                              RandomEvaluationTests.__threeMonthsModelsTestDay)


    #----------------------------------------------------------------------------
    #
    # Run CL-Test evaluation for the three-months forecast, and validate the 
    # results.
    #
    def testThreeMonthsCLTestRandom(self):
        """ Run CL-test for the three-months forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMConditionalLikelihoodTest.Type

        # Directory with forecast model files
        forecast_dir = 'three_months_forecasts'

        # Name of the file with random numbers for the test
        random_filename = "CL-Test_EEPAS-0F_12_1_2007"
        
        # Reference file with test results
        result_filename = "rTest_CL-Test_EEPAS-0F_12_1_2007.xml"        
        
        # The forecast directory has configuration file with post-processing type
        # and start and end time for evaluation period
        self.__evaluationTest(test_list,
                              None,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'ThreeMonthsModel.catalog.nodecl.dat',
                              RandomEvaluationTests.__threeMonthsModelsTestDay)


    #----------------------------------------------------------------------------
    #
    # Run R-Test evaluation for the three-months forecast, and validate the 
    # results.
    #
    def testThreeMonthsRTestRandom(self):
        """ Run R-test for the three-months forecast evaluation (draw random \
numbers by the system)."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMLikelihoodRatioTest.Type

        # Directory with forecast model files
        forecast_dir = 'rtest_three_months_forecasts'

        # Name of the file with random numbers for the test
        random_filename = "R-Test_EEPAS-0F_12_1_2007_EEPAS-0R_12_1_2007"
        
        # Reference file with test results
        result_filename = "rTest_R-Test_EEPAS-0F_12_1_2007_EEPAS-0R_12_1_2007.xml"        
        
        # The forecast directory has configuration file with post-processing type
        # and start and end time for evaluation period
        self.__evaluationTest(test_list,
                              None,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'ThreeMonthsModel.catalog.nodecl.dat',
                              RandomEvaluationTests.__threeMonthsModelsTestDay)


    #--------------------------------------------------------------------
    #
    # Run evaluation test for the forecast, and validate the results.
    #
    # Inputs:
    #            test_list - List of evaluation tests to invoke.
    #            post_process_type - Keyword identifying PostProcessing that
    #                                         has been applied to the catalog data.
    #            random_file - Name of the file with random numbers used by the 
    #                                 evaluation test.
    #            forecast_dir - Directory that stores forecast files for evaluation.
    #            result_file - Name of the result file in ascii format used for
    #                             test validation.
    #            catalog_file - Observation catalog for the test (default is PostProcess.files.catalog)
    #            test_date - Date for evaluation. Default is as defined by the
    #                        CSEPTestCase.Date.
    #            
    #
    def __evaluationTest(self, test_list,
                               post_process_type, 
                               random_file,
                               forecast_dir,
                               result_file,
                               catalog_file = None,
                               test_date = CSEPTestCase.Date):
        """ Run evaluation test for the forecast and succeed."""


        ### Generate test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath)

        reference_catalog = catalog_file
        
        if catalog_file is None:
           catalog_file = PostProcessFactory().object(post_process_type).files.catalog

           ### Copy reference catalog data file to the test directory
           reference_catalog = "%s.%s" %(post_process_type, catalog_file)
           
        else:
           # If reference file is given, strip post-processing part of it
           # to get original catalog filename
           catalog_file = catalog_file[(catalog_file.find('.')+1):]   
        

        shutil.copyfile(os.path.join(CSEPTestCase.ReferenceDataDir, reference_catalog),
                        os.path.join(CSEPTestCase.TestDirPath, catalog_file))    

        # ForecastGroup object that represents forecast models for the test
        forecast_group = ForecastGroup(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                                    forecast_dir),
                                       post_process_type,
                                       test_list)

        for each_test in forecast_group.tests:
           # Use the same directory for catalog data and test results
           each_test.run(test_date, 
                         CSEPTestCase.TestDirPath,
                         CSEPTestCase.TestDirPath)

        
        ### Check existence of test results and random numbers files
        self.failIf(os.path.exists(os.path.join(CSEPTestCase.TestDirPath, 
                                                result_file)) == False, 
                    "Test result file does not exist.")

        # Check for random seed files only for evaluation tests that use 
        # random numbers
        if random_file is not None:
           
           seed_dir = os.path.join(CSEPTestCase.TestDirPath, '%s-randomSeed' \
                                                               %random_file)
   
           num_seed_files = 2     
           if test_list == RELMLikelihoodRatioTest.Type:
              num_seed_files = 4
           elif test_list == RELMSpaceTest.Type or \
                test_list == RELMMagnitudeTest.Type or \
                test_list == RELMConditionalLikelihoodTest.Type:
              num_seed_files = 1 
              
              
           for index in xrange(1, EvaluationTest.EvaluationTest.NumberSimulations+1):
              
              # Format expected filename for the simulation random seed file
              # (there are 2 random seed files per simulation)
              for iter_index in xrange(1, num_seed_files+1):
                 seed_file = "%s-simulation%s_%s-randomSeed.txt" %(random_file, 
                                                                   index,
                                                                   iter_index)

                 self.failIf(os.path.exists(os.path.join(seed_dir, seed_file)) == False, 
                             "Random seed file '%s' does not exist." %seed_file)
        

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
