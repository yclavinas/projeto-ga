"""
Module EvaluationTests
"""

__version__ = "$Revision: 4200 $"
__revision__ = "$Id: EvaluationTests.py 4200 2013-02-05 19:31:32Z liukis $"


import sys, os, unittest, shutil, datetime

import CSEPFile, CSEPInitFile, CSEP

from CSEPTestCase import CSEPTestCase
from EvaluationTest import EvaluationTest
from RELMAftershockPostProcess import RELMAftershockPostProcess
from RELMMainshockPostProcess import RELMMainshockPostProcess
from OneDayModelPostProcess import OneDayModelPostProcess
from ThreeMonthsModelPostProcess import ThreeMonthsModelPostProcess
from RELMCatalog import RELMCatalog
from RELMTest import RELMTest
from RELMNumberTest import RELMNumberTest, Delta1, Delta2
from RELMLikelihoodTest import RELMLikelihoodTest, Gamma
from RELMLikelihoodRatioTest import RELMLikelihoodRatioTest, Alpha, Beta
from RELMMagnitudeTest import RELMMagnitudeTest, Kappa
from RELMSpaceTest import RELMSpaceTest, Zeta
from RELMConditionalLikelihoodTest import RELMConditionalLikelihoodTest, Xi
from RELMMagnitudeTest import RELMMagnitudeTest
from PostProcessFactory import PostProcessFactory
from ForecastGroup import ForecastGroup
from CSEPLogging import CSEPLogging
from ForecastHandlerFactory import ForecastHandlerFactory
from PolygonForecastHandler import PolygonForecastHandler


# Logger object for the module
__logger = None


#-------------------------------------------------------------------------------
# Function to access logger object for the module.
#-------------------------------------------------------------------------------
def _moduleLogger():
    """ Get logger object for the module, initialize one if it does not exist"""
    
    global __logger
    if __logger is None:
        __logger = CSEPLogging.getLogger(__name__)
    
    return __logger


 #--------------------------------------------------------------------
 #
 # Test RELM evaluation tests for the forecasts models. This module tests
 # reproducibility of tests results. All tests are reading random numbers from
 # provided files.
 #
class EvaluationTests (CSEPTestCase):

    # Directory with reference data for the tests
    __referenceDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                  'evaluationTests')
    
    # Static data of the class
    __evaluateXMLVars = {RELMNumberTest.Type: [Delta1, 
                                               Delta2,
                                               RELMTest.Result.ModificationCount,
                                               RELMTest.Result.Modification,
                                               RELMNumberTest.Result.EventCount,
                                               RELMNumberTest.Result.EventCountForecast,
                                               RELMNumberTest.Result.CDFEventCount,
                                               RELMNumberTest.Result.CDFCount,
                                               RELMNumberTest.Result.CDFValues],
                                               
                         RELMLikelihoodTest.Type: [Gamma, 
                                                   RELMTest.Result.ModificationCount,
                                                   RELMTest.Result.Modification,
                                                   RELMLikelihoodTest.Result.LogLikelihood,
                                                   RELMTest.Result.Simulation,
                                                   RELMTest.Result.SimulationCount],

                         RELMConditionalLikelihoodTest.Type: [Xi, 
                                                              RELMTest.Result.ModificationCount,
                                                              RELMTest.Result.Modification,
                                                              RELMConditionalLikelihoodTest.Result.LogLikelihood,
                                                              RELMTest.Result.Simulation,
                                                              RELMTest.Result.SimulationCount],
                                                   
                         RELMMagnitudeTest.Type: [Kappa, 
                                                  RELMTest.Result.ModificationCount,
                                                  RELMTest.Result.Modification,
                                                  RELMMagnitudeTest.Result.LogLikelihood,
                                                  RELMTest.Result.Simulation,
                                                  RELMTest.Result.SimulationCount],

                         RELMSpaceTest.Type: [Zeta, 
                                              RELMTest.Result.ModificationCount,
                                              RELMTest.Result.Modification,
                                              RELMSpaceTest.Result.LogLikelihood,
                                              RELMTest.Result.Simulation,
                                              RELMTest.Result.SimulationCount],

                         RELMLikelihoodRatioTest.Type: [Alpha,
                                                        Beta, 
                                                        RELMTest.Result.ModificationCount,
                                                        RELMTest.Result.Modification,
                                                        RELMLikelihoodRatioTest.Result.LogLikelihoodRatio,
                                                        RELMTest.Result.Simulation,
                                                        RELMTest.Result.SimulationCount]}

    
    # Test date for three-months models
    __threeMonthsModelsTestDay = datetime.datetime(2007, 12, 10)


    #--------------------------------------------------------------------
    #
    # Run N-Test evaluation for the shortterm forecast, and validate the results.
    #
    def testOneDayModelNTest(self):
        """ Run N-test for the shortterm forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'shortterm_forecasts'
        
        # New implementation does not use random numbers
        random_filename = None
        
        # Reference file with test results
        result_filename = "rTest_N-Test_STEP_daily_11_2_2006.xml"        

        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename)
          

    #--------------------------------------------------------------------
    #
    # Run L-Test evaluation for the shortterm forecast, and validate the results.
    #
    def testOneDayModelLTest(self):
        """ Run L-test for the shortterm forecast evaluation and succeed."""

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


    #--------------------------------------------------------------------
    #
    # Run CL-Test evaluation for the shortterm forecast, and validate the results.
    #
    def testOneDayModelCLTest(self):
        """ Run CL-test for the shortterm forecast evaluation and succeed."""

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
    def testRELMMainshockSTest(self):
        """ Run S-test for 5-year RELMMainshock forecast evaluation and succeed."""

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
    def testRELMMainshockMTest(self):
        """ Run M-test for 5-year RELMMainshock forecast evaluation and succeed."""

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
    def testRELMAftershockNTest(self):
        """ Run N-test for the longterm forecast evaluation and succeed."""

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
    def testRELMAftershockLTest(self):
        """ Run L-test for the longterm forecast evaluation and succeed."""

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
    def testRELMAftershockCLTest(self):
        """ Run CL-test for the longterm forecast evaluation and succeed."""

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
    def testRELMAftershockRTest(self):
        """ Run R-test for the longterm forecast evaluation and succeed."""

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
    def testThreeMonthsNTest(self):
        """ Run N-test for the three-months forecast evaluation and succeed."""

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
                              EvaluationTests.__threeMonthsModelsTestDay)


    #----------------------------------------------------------------------------
    #
    # Run L-Test evaluation for the three-months forecast, and validate the 
    # results.
    #
    def testThreeMonthsLTest(self):
        """ Run L-test for the three-months forecast evaluation and succeed."""

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
                              EvaluationTests.__threeMonthsModelsTestDay)


    #----------------------------------------------------------------------------
    #
    # Run CL-Test evaluation for the three-months forecast, and validate the 
    # results.
    #
    def testThreeMonthsCLTest(self):
        """ Run CL-test for the three-months forecast evaluation and succeed."""

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
                              EvaluationTests.__threeMonthsModelsTestDay)


    #----------------------------------------------------------------------------
    #
    # Run R-Test evaluation for the three-months forecast, and validate the 
    # results.
    #
    def testThreeMonthsRTest(self):
        """ Run R-test for the three-months forecast evaluation and succeed."""

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
                              EvaluationTests.__threeMonthsModelsTestDay)


    #---------------------------------------------------------------------------
    #
    # Run N-Test evaluation for the polygon-based forecast, and validate the 
    # results.
    #
    def testOneDayPolygonModelNTest(self):
        """ Run N-test for one-day polygon-based forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'polygon-based-forecasts'
        
        # New implementation does not use random numbers
        random_filename = None
        
        # Reference file with test results
        result_filename = "rTest_N-Test_OneDayPolygonForecast.xml"        

        ForecastHandlerFactory().object(PolygonForecastHandler.Type)
        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'PolygonForecast.catalog.nodecl.dat',
                              datetime.datetime(2012, 1, 1))


    #---------------------------------------------------------------------------
    #
    # Run N-Test evaluation for the polygon-based forecast, and validate the 
    # results.
    #
    def testOneDayPolygonModelWithVertexExclusionNTest(self):
        """ Run N-test for one-day polygon-based forecast (with vertex exclusions) 
            evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'polygon-based-vertex-exclude-forecasts'
        
        # New implementation does not use random numbers
        random_filename = None
        
        # Reference file with test results
        result_filename = "rTest_N-Test_OneDayPolygonForecastVertexExclude.xml"

        ForecastHandlerFactory().object(PolygonForecastHandler.Type)
        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'PolygonForecastExcludeVertex.catalog.nodecl.dat',
                              datetime.datetime(2012, 1, 1))


    #---------------------------------------------------------------------------
    #
    # Run N-Test evaluation for the polygon-based forecast, and validate the 
    # results.
    #
    def testOneDayPolygonModelWithSideExclusionNTest(self):
        """ Run N-test for one-day polygon-based forecast (with side exclusions) 
            evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'polygon-based-side-exclude-forecasts'
        
        # New implementation does not use random numbers
        random_filename = None
        
        # Reference file with test results
        result_filename = "rTest_N-Test_OneDayPolygonForecastSideExclude.xml"

        ForecastHandlerFactory().object(PolygonForecastHandler.Type)
        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'PolygonForecastExcludeSide.catalog.nodecl.dat',
                              datetime.datetime(2012, 1, 1))


    #---------------------------------------------------------------------------
    #
    # Run N-Test evaluation for the polygon-based forecast, and validate the 
    # results.
    #
    def testOneDayPolygonModelWithVertexSideExclusionNTest(self):
        """ Run N-test for one-day polygon-based forecast (with vertex and side exclusions) 
            evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = RELMNumberTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'polygon-based-vertex-side-exclude-forecasts'
        
        # New implementation does not use random numbers
        random_filename = None
        
        # Reference file with test results
        result_filename = "rTest_N-Test_OneDayPolygonForecastVertexSideExclude.xml"

        ForecastHandlerFactory().object(PolygonForecastHandler.Type)
        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'PolygonForecastExcludeVertexSide.catalog.nodecl.dat',
                              datetime.datetime(2012, 1, 1))


    #---------------------------------------------------------------------------
    #
    # Run N-Test evaluation for the polygon-based forecast, and validate the 
    # results.
    #
    def testOneDayPolygonModelLTest(self):
        """ Run L-test for one-day polygon-based forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'polygon-based-forecasts'
        test_list = RELMLikelihoodTest.Type

        # Name of the file with random numbers for the test
        #from cseprandom import CSEPRandom
        #CSEPRandom.ReadSeedFromFile = False
        random_filename = "L-Test_OneDayPolygonForecast"
                
        # Reference file with test results
        result_filename = "rTest_L-Test_OneDayPolygonForecast.xml"        

        ForecastHandlerFactory().object(PolygonForecastHandler.Type)
        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'PolygonForecast.catalog.nodecl.dat',
                              datetime.datetime(2012, 1, 1))


    #---------------------------------------------------------------------------
    #
    # Run N-Test evaluation for the polygon-based forecast, and validate the 
    # results.
    #
    def testOneDayPolygonModelCLTest(self):
        """ Run CL-test for one-day polygon-based forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'polygon-based-forecasts'
        test_list = RELMConditionalLikelihoodTest.Type

        # Name of the file with random numbers for the test
        random_filename = "CL-Test_OneDayPolygonForecast"
                
        # Reference file with test results
        result_filename = "rTest_CL-Test_OneDayPolygonForecast.xml"        

        ForecastHandlerFactory().object(PolygonForecastHandler.Type)
        self.__evaluationTest(test_list,
                              OneDayModelPostProcess.Type,
                              random_filename,
                              forecast_dir,
                              result_filename,
                              'PolygonForecast.catalog.nodecl.dat',
                              datetime.datetime(2012, 1, 1))


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
        RELMCatalog(CSEPTestCase.TestDirPath)

        reference_catalog = catalog_file
        
        if catalog_file is None:
           catalog_file = PostProcessFactory().object(post_process_type).files.catalog

           ### Copy reference catalog data file to the test directory
           reference_catalog = "%s.%s" %(post_process_type, catalog_file)
           
        else:
           # If reference file is given, strip post-processing part of it
           # to get original catalog filename
           catalog_file = catalog_file[(catalog_file.find('.')+1):]   
        

        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(CSEPTestCase.ReferenceDataDir, reference_catalog),
                                                                   os.path.join(CSEPTestCase.TestDirPath, catalog_file)))
        shutil.copyfile(os.path.join(CSEPTestCase.ReferenceDataDir, reference_catalog),
                        os.path.join(CSEPTestCase.TestDirPath, catalog_file))    

        ### Copy random numbers seed files (if used by evaluation test) to 
        ### the test directory
        if random_file is not None:
           
           seed_dir = os.path.join(CSEPTestCase.TestDirPath, '%s-randomSeed' \
                                                               %random_file)
           os.makedirs(seed_dir)                                                    
                              
           num_seed_files = 2     
           if test_list == RELMLikelihoodRatioTest.Type:
              num_seed_files = 4
           elif test_list == RELMSpaceTest.Type or \
                test_list == RELMMagnitudeTest.Type or \
                test_list == RELMConditionalLikelihoodTest.Type:
              num_seed_files = 1 
              
           for index in xrange(1, EvaluationTest.NumberSimulations+1):
              
              # Format expected filename for the simulation random seed file
              # (there are 2 random seed files per simulation)
              for iter_index in xrange(1, num_seed_files+1):
                 seed_file = "%s-simulation%s_%s-randomSeed.txt" %(random_file, 
                                                                   index,
                                                                   iter_index)
      
                 shutil.copyfile(os.path.join(EvaluationTests.__referenceDir, 
                                              seed_file),
                                 os.path.join(seed_dir, seed_file))    

        # ForecastGroup object that represents forecast models for the test
        forecast_group = ForecastGroup(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                                    forecast_dir),
                                       post_process_type,
                                       test_list)

        # Use the same directory for catalog data and test results
        for each_test in forecast_group.tests:
           each_test.run(test_date, 
                         CSEPTestCase.TestDirPath,
                         CSEPTestCase.TestDirPath)

        
        ### Evaluate test results
        reference_file = os.path.join(EvaluationTests.__referenceDir, 
                                      result_file)
        test_file = os.path.join(CSEPTestCase.TestDirPath, result_file)
        
        CSEPLogging.getLogger(EvaluationTests.__name__).info("Comparing reference evaluation \
test file %s with generated evaluation test file %s..." %(reference_file, 
                                                          test_file)) 

        # If result filename in XML format, extract variables names  to evaluate
        if CSEPFile.Extension.toFormat(result_file) == CSEPFile.Format.XML:
            
            diff_precision = 5E-5 
            for each_test in forecast_group.tests:
                
                # Open reference file
                ref_obj = CSEPInitFile.CSEPInitFile(reference_file)
                
                # Open test result file
                test_obj = CSEPInitFile.CSEPInitFile(test_file)
                
                # Evaluate variables specific to the test
                for each_var in EvaluationTests.__evaluateXMLVars[each_test.Type]:
                    
                    # There might be multiple elements with the same tag name:
                    # validation relies on the fact that reference and generated
                    # result data will have the corresponding elements listed in the
                    # same order
                    num_var_elements = ref_obj.elements(each_var)
                    for var_index in xrange(len(num_var_elements)):
                         
                        # Reference data was generated by Matlab and written with at 
                        # most 8 digits of precision
                        ref_data = ref_obj.elementValue(each_var,
                                                        index = var_index)
                        
                        # Round up test data to be compatible with at most 8 digits
                        # of precision for reference data
                        test_data = test_obj.elementValue(each_var,
                                                          index = var_index)
                        
                        CSEPLogging.getLogger(EvaluationTests.__name__).info(\
    "Comparing reference var %s: %s vs. %s" %(each_var, ref_data, test_data)) 
    
                        self.failIf(CSEPFile.compareLines(ref_data, 
                                                          test_data,
                                                          diff_precision) is False,
                                    "Failed to compare evaluation test results for %s: expected %s, got %s"
                                    %(each_var, 
                                      ref_data,
                                      test_data))
                                   
        else:
            error = "Failed to compare evaluation test results."
            self.failIf(CSEPFile.compare(reference_file, test_file) is False, error)


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
