"""
Module DiagnosticsEvaluationTests
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, datetime

import CSEPFile

from CSEPTestCase import CSEPTestCase
from EvaluationTest import EvaluationTest
from RELMCatalog import RELMCatalog
from RELMAftershockPostProcess import RELMAftershockPostProcess
from PostProcessFactory import PostProcessFactory
from ForecastGroup import ForecastGroup
from CSEPLogging import CSEPLogging
from CenteredWeightedLFunctionTest import CenteredWeightedLFunctionTest
from PearsonResidualsTest import PearsonResidualsTest
from DevianceResidualsTest import DevianceResidualsTest
from SuperThinnedResidualsTest import SuperThinnedResidualsTest
from SuperThinnedResidualsTestingTest import SuperThinnedResidualsTestingTest


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


 #------------------------------------------------------------------------------
 #
 # Test diagnostics evaluation tests for the forecasts models. This module tests
 # reproducibility of tests results. Evaluation tests that are dependent on
 # random numbers will be provided with random seed value for the test case.
 #
class DiagnosticsEvaluationTests (CSEPTestCase):

    # Directory with reference data for the tests
    __referenceDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                  'diagnostics_tests')
    
    __referenceResultDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                        'diagnostics_tests',
                                        'results')

    __referenceEmptyCatalogResultDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                                    'diagnostics_tests',
                                                    'empty_catalog_results')
    
    # Test date for three-months models
    __testDay = datetime.datetime(2009, 1, 1)


    #---------------------------------------------------------------------------
    #
    # Run LW-Test evaluation for the RELM mainshock/aftershock forecast, 
    # and validate the results.
    #
    def testRELMAftershockWeightedLTest(self):
        """ Run LW-test for the RELM mainshock/aftershock forecast \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = CenteredWeightedLFunctionTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'one_forecast'
        
        # Reference file with test results as provided by Robert
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "wl_test_upd.dat")        
        result_filename = 'dTest_LW-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename)


    #---------------------------------------------------------------------------
    #
    # Run LW-Test evaluation for SW Pacific forecast with catalog 
    # of less than 16 columns, and validate the results.
    #
    def testSWPacificLWTest(self):
        """ Run LW-test for the SW-Pacific one-day forecast \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = CenteredWeightedLFunctionTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'swp_forecasts'
        
        # Reference file with test results as provided by Robert
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "dTest_LW-Test_KJSSOneDaySWPacific_result.dat")        
        result_filename = 'dTest_LW-Test_KJSSOneDaySWPacific_2_18_2013-fromXML_result.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              observation_catalog = 'swp.catalog.nodecl.dat')


    #---------------------------------------------------------------------------
    #
    # Run LW-Test evaluation for SW Pacific forecast, 
    # and validate the results.
    #
    def testExtendedForecastRPTest(self):
        """ Run RP-test for one-day forecast (with more than 10 columns of data) \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = PearsonResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'Md2_forecast'
        
        # Reference file with test results as provided by Robert
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "dTest_RP-Test_JANUSOneDay_result.dat")        
        result_filename = 'dTest_RP-Test_JANUSOneDay_result.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              observation_catalog = 'Md2.catalog.nodecl.dat')

          
    #---------------------------------------------------------------------------
    #
    # Run PEARSONRESIDUALS-Test evaluation for the RELM mainshock/aftershock 
    # forecast, and validate the results.
    #
    def testRELMAftershockPearsonResidualsTest(self):
        """ Run RP-test for the RELM mainshock/aftershock forecast \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = PearsonResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'one_forecast'
        
        # Reference file with test results as provided by Robert
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "pearson_test_upd.dat")        
        result_filename = 'dTest_RP-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename)
          

    #---------------------------------------------------------------------------
    #
    # Run DEVIANCERESIDUALS-Test evaluation for the RELM mainshock/aftershock  
    # forecast, and validate the results.
    #
    def testRELMAftershockDevianceResidualsTest(self):
        """ Run RD-test for the RELM mainshock/aftershock forecast \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = DevianceResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'forecasts'
        
        # Reference file with test results as provided by Robert
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "deviance_test_upd.dat")        
        result_filename = 'dTest_RD-Test_helmstetter_et_al.hkj.aftershock-fromXML_shen_et_al.geodetic.aftershock-fromXML_result.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename)


    #---------------------------------------------------------------------------
    #
    # Run SUPERTHINNEDRESIDUAL-Test evaluation for the RELM mainshock/aftershock 
    # forecast, and validate the results.
    #
    def testRELMAftershockSuperThinnedResidualsTest(self):
        """ Run STRD-test for the RELM mainshock/aftershock forecast \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = SuperThinnedResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'one_forecast'
        
        # Reference file with test results as provided by Robert
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "superthin_test_upd.dat")        
        result_filename = 'dTest_RT-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        input_args = 'seedValue=20'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              input_args)
          
        test_list = SuperThinnedResidualsTestingTest.Type

        # Reference file with test results as provided by Robert
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "superthintest_test_upd.dat")        
        result_filename = 'dTest_RTT-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename)


    #---------------------------------------------------------------------------
    #
    # Run SUPERTHINNEDRESIDUAL-Test evaluation for the RELM mainshock/aftershock 
    # forecast, and validate the results.
    #
    def testRELMAftershockSuperThinnedResidualsTestRandom(self):
        """ Run STRD-test for the RELM mainshock/aftershock forecast \
evaluation using random number generator and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = SuperThinnedResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'one_forecast'
        
        result_filename = 'dTest_RT-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'

        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename)
          
        test_list = SuperThinnedResidualsTestingTest.Type

        result_filename = 'dTest_RTT-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename)


    #---------------------------------------------------------------------------
    #
    # Run WEIGHTEDL-Test evaluation for the RELM mainshock/aftershock forecast
    # with empty catalog, and verify that test is not invoked.
    #
    def testRELMAftershockWeightedLTestWithEmptyCatalog(self):
        """ Run LW-test for the RELM mainshock/aftershock forecast \
evaluation with empty catalog and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = CenteredWeightedLFunctionTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'one_forecast'
        
        # Test result file if it would be generated by the test
        result_filename = 'dTest_LW-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        catalog_filename = 'empty.catalog.nodecl.dat'

        # Reference file with test results (as generated by the acceptance test with new R codes)
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceEmptyCatalogResultDir,
                                          result_filename)        
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              observation_catalog = catalog_filename)

          
    #---------------------------------------------------------------------------
    #
    # Run PEARSONRESIDUALS-Test evaluation for the RELM mainshock/aftershock 
    # forecast with empty catalog, and verify that test is not invoked.
    #
    def testRELMAftershockPearsonResidualsTestWithEmptyCatalog(self):
        """ Run RP-test for the RELM mainshock/aftershock forecast \
evaluation with empty catalog and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = PearsonResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'one_forecast'

        # Test result file if it would be generated by the test        
        result_filename = 'dTest_RP-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        catalog_filename = 'empty.catalog.nodecl.dat'
        
        # Reference file with test results (as generated by the acceptance test with new R codes)
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceEmptyCatalogResultDir,
                                          result_filename)        
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              observation_catalog = catalog_filename)
          

    #---------------------------------------------------------------------------
    #
    # Run DEVIANCERESIDUALS-Test evaluation for the RELM mainshock/aftershock  
    # forecast with empty catalog, and verify that test is not invoked.
    #
    def testRELMAftershockDevianceResidualsTestWithEmptyCatalog(self):
        """ Run RD-test for the RELM mainshock/aftershock forecast \
evaluation with empty catalog and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = DevianceResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'forecasts'
        
        # Test result file if it would be generated by the test 
        result_filename = 'dTest_RD-Test_helmstetter_et_al.hkj.aftershock-fromXML_shen_et_al.geodetic.aftershock-fromXML_result.dat'
        catalog_filename = 'empty.catalog.nodecl.dat' 
        
        # Reference file with test results (as generated by the acceptance test with new R codes)
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceEmptyCatalogResultDir,
                                          result_filename)        
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              observation_catalog = catalog_filename)


    #---------------------------------------------------------------------------
    #
    # Run SUPERTHINNEDRESIDUAL-Test evaluation for the RELM mainshock/aftershock 
    # forecast with empty catalog, and verify that test is not invoked.
    #
    def testRELMAftershockSuperThinnedResidualsTestWithEmptyCatalog(self):
        """ Run STRD-test for the RELM mainshock/aftershock forecast \
evaluation ith empty catalog and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = SuperThinnedResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'one_forecast'
        
        # Test result file if it would be generated by the test
        result_filename = 'dTest_RT-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'
        catalog_filename = 'empty.catalog.nodecl.dat' 
        input_args = 'seedValue=20'

        # Reference file with test results (as generated by the acceptance test with new R codes)
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceEmptyCatalogResultDir,
                                          result_filename)        
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              input_args,
                              observation_catalog = catalog_filename)
          
        test_list = SuperThinnedResidualsTestingTest.Type

        # Test result file if it would be generated by the test
        result_filename = 'dTest_RTT-Test_helmstetter_et_al.hkj.aftershock-fromXML_result.dat'

        # Reference file with test results (as generated by the acceptance test with new R codes)
        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceEmptyCatalogResultDir,
                                          result_filename)        
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              observation_catalog = catalog_filename)


    #---------------------------------------------------------------------------
    #
    # Run PEARSONRESIDUALS-Test evaluation for the RELM mainshock/aftershock 
    # to test fix for Trac ticket #258: Add support for two types of 
    # PearsonResiduals evaluation test output - "P.residual" or "raw.residual"
    #
    def testTrac258(self):
        """ Run RP-test for the RELM mainshock/aftershock forecast \
to test Trac ticket 258 fix (Add support for two types of \
PearsonResiduals evaluation test output - "P.residual" or "raw.residual")."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = PearsonResidualsTest.Type

        # Directory with forecast model files for N and L evaluation tests
        forecast_dir = 'trac258_forecast'

        reference_filename = os.path.join(DiagnosticsEvaluationTests.__referenceResultDir,
                                          "Trac258.dTest_RP-Test_shen_et_al.geodetic.aftershock-fromXML_result.dat")        

        # Test result file if it would be generated by the test        
        result_filename = 'dTest_RP-Test_shen_et_al.geodetic.aftershock-fromXML_result.dat'
        catalog_filename = 'Trac258.catalog.nodecl.dat'
        
        self.__evaluationTest(test_list,
                              forecast_dir,
                              result_filename,
                              reference_filename,
                              observation_catalog = catalog_filename)
          

    #---------------------------------------------------------------------------
    #
    # Run evaluation test for the forecast, and validate the results.
    #
    # Inputs:
    #            test_list - List of evaluation tests to invoke.
    #            forecast_dir - Directory that stores forecast files for evaluation.
    #            result_file - Name of the result file in ascii format used for
    #                             test validation.
    #            
    #
    def __evaluationTest(self, test_list,
                               forecast_dir,
                               result_file,
                               reference_data_file = None,
                               test_inputs = None,
                               observation_catalog = None):
        """ Run evaluation test for the forecast and succeed."""


        ### Generate test directory
        RELMCatalog(CSEPTestCase.TestDirPath)

        __catalog_file = RELMAftershockPostProcess().files.catalog
        if observation_catalog is not None:
            __catalog_file = observation_catalog

        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(DiagnosticsEvaluationTests.__referenceDir, 
                                                                                 __catalog_file),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 RELMAftershockPostProcess().files.catalog)))
        shutil.copyfile(os.path.join(DiagnosticsEvaluationTests.__referenceDir, 
                                     __catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath,
                                     RELMAftershockPostProcess().files.catalog))    

        # ForecastGroup object that represents forecast models for the test
        forecast_group = ForecastGroup(os.path.join(DiagnosticsEvaluationTests.__referenceDir,
                                                    forecast_dir),
                                       RELMAftershockPostProcess.Type,
                                       test_list,
                                       test_inputs)

        # Use the same directory for catalog data and test results
        for each_test in forecast_group.tests:
           each_test.run(DiagnosticsEvaluationTests.__testDay, 
                         CSEPTestCase.TestDirPath,
                         CSEPTestCase.TestDirPath)
           
        
        ### Evaluate test results
        test_data_file = os.path.join(CSEPTestCase.TestDirPath, 
                                      result_file)

        if reference_data_file is None:
            # Non-empty catalog is used for the test ---> test invoked with 
            # random numbers generated by the system
            if observation_catalog is None:
                # Check for existence of result data if no reference data is provided
                self.failIf(os.path.exists(test_data_file) is False,
                            "Failed to generate test result file %s" %test_data_file)
            else:
                # Check that result file was generated when empty catalog
                # is provided
                self.failIf(os.path.exists(test_data_file) is False,
                            "Test result file %s should be generated with empty catalog" %test_data_file)
            
        else:
            CSEPLogging.getLogger(DiagnosticsEvaluationTests.__name__).info("Comparing reference evaluation \
test file %s with generated evaluation test file %s..." %(reference_data_file, 
                                                          test_data_file)) 
        
            error = "Failed to compare evaluation test results."
            self.failIf(CSEPFile.compare(reference_data_file, 
                                         test_data_file,
                                         skip_num_lines=1) is False, error)


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
