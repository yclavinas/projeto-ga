"""
Module RandomAlarmBasedEvaluationTests
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, datetime, glob
from xml.etree.cElementTree import tostring

import CSEPFile

from CSEPTestCase import CSEPTestCase
from RELMMainshockPostProcess import RELMMainshockPostProcess
from RELMAftershockPostProcess import RELMAftershockPostProcess
from OneYearModelPostProcess import OneYearModelPostProcess
from MASSTest import MASSTest
from ROCTest import ROCTest
from RELMCatalog import RELMCatalog
from PostProcessFactory import PostProcessFactory
from ForecastGroup import ForecastGroup
from CSEPInitFile import CSEPInitFile
from CSEPLogging import CSEPLogging


 #-------------------------------------------------------------------------------
 #
 # Test alarm-based evaluation tests for the forecasts models. This module tests
 # system ability to generate new seed for random number generator.
 #
class RandomAlarmBasedEvaluationTests (CSEPTestCase):

    # Static data of the class
    
    # Path to the reference data for the tests
    __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                      'alarm_based_tests')
    

    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for NW Pacific forecasts, and validate the results.
    #
    def testNWPacificMASSTest(self):
        """ Create random seed file, and run MASS test for the NW Pacific \
forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomMASSTestNWPacific")
        
        model = 'KJSSOneYearNWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = MASSTest.Type

        self.__evaluationTest(model,
                              test_list,
                              'nw_pacific',
                              OneYearModelPostProcess.Type,
                              post_process_args)
          

    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for SW Pacific forecasts, and validate the results.
    #
    def testSWPacificMASSTest(self):
        """ Create random seed file, and run MASS test for the SW Pacific \
forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomMASSTestSWPacific")
        
        model = 'KJSSOneYearSWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = MASSTest.Type

        self.__evaluationTest(model,
                              test_list,
                              'sw_pacific',
                              OneYearModelPostProcess.Type,
                              post_process_args)


    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for SW Pacific forecasts, and validate the results.
    #
    def testSWPacificROCTest(self):
        """ Create random seed file, and run ROC test for the SW Pacific forecast \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomROCTestSWPacific")
        
        model = 'KJSSOneYearSWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = ROCTest.Type

        self.__evaluationTest(model,
                              test_list,
                              'sw_pacific',
                              OneYearModelPostProcess.Type,
                              post_process_args)
        

    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for NW Pacific forecasts, and validate the results.
    #
    def testNWPacificROCTest(self):
        """ Create random seed file, and run ROC test for the NW Pacific forecast \
evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomROCTestNWPacific")
        
        model = 'KJSSOneYearNWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = ROCTest.Type

        self.__evaluationTest(model,
                              test_list,
                              'nw_pacific',
                              OneYearModelPostProcess.Type,
                              post_process_args)


    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for RELM Mainshock forecasts, and validate the 
    # results.
    #
    def testRELMMainshockMASSTest(self):
        """ Create random seed file, and run MASS test for the RELM Mainshock \
forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomMASSTestRELMMainshock")
        
        model = 'ebel.mainshock.xml'
        test_list = MASSTest.Type

        self.__evaluationTest(model,
                              test_list,
                              'relm-mainshock',
                              RELMMainshockPostProcess.Type)
          

    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for RELM Mainshock/Aftershock forecasts, and 
    # validate the results.
    #
    def testRELMMainshockAftershockMASSTest(self):
        """ Create random seed file, and run MASS test for the \
RELM Mainshock/Aftershock forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomMASSTestRELMMainshockAftershock")
        
        model = 'ebel.aftershock.xml'
        test_list = MASSTest.Type

        # Reference file with test results
        result_filename = 'EbelMASSResultsRELMMainshockAftershock.xml'        

        self.__evaluationTest(model,
                              test_list,
                              'relm-mainshock-aftershock',
                              RELMAftershockPostProcess.Type)


    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for RELM Mainshock forecasts, and validate the 
    # results.
    #
    def testRELMMainshockROCTest(self):
        """ Create random seed file, and run ROC test for the RELM Mainshock \
forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomROCTestRELMMainshock")
        
        model = 'ebel.mainshock.xml'
        test_list = ROCTest.Type

        self.__evaluationTest(model,
                              test_list,
                              'relm-mainshock',
                              RELMMainshockPostProcess.Type)


    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for RELM Mainshock/Aftershock forecasts, and 
    # validate the results.
    #
    def testRELMMainshockAftershockROCTest(self):
        """ Create random seed file, and run ROC test for the \
RELM Mainshock/Aftershock forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, "RandomROCTestRELMMainshockAftershock")
        
        model = 'ebel.aftershock.xml'
        test_list = ROCTest.Type

        self.__evaluationTest(model,
                              test_list,
                              'relm-mainshock-aftershock',
                              RELMAftershockPostProcess.Type)
        

    #----------------------------------------------------------------------------
    #
    # Run evaluation test for the forecast, and validate the results.
    #
    # Inputs:
    #            model - Forecast file for which to invoke the test.
    #            test_list - List of evaluation tests to invoke.
    #            reference_dir - Directory that stores input files, forecasts and
    #                            expected results files for evaluation.
    #            post_process_type - Keyword identifying PostProcessing that
    #                                has been applied to the catalog data.
    #            post_process_args - Input arguments for post-processing. Default
    #                                is None.
    #
    def __evaluationTest(self, 
                         model,
                         test_list,
                         reference_dir,
                         post_process_type, 
                         post_process_args = None):
        """ Run specified evaluation test for the forecast and succeed."""


        ### Generate test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath)
        catalog_file = PostProcessFactory().object(post_process_type,
                                                   post_process_args).files.catalog
        catalog_file = CSEPFile.Name.ascii(catalog_file)

        ### Copy reference catalog data file to the test directory
        shutil.copyfile(os.path.join(RandomAlarmBasedEvaluationTests.__referenceDataDir,
                                     reference_dir,
                                     catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath, catalog_file))    

        # Copy forecast group directory to the runtime test directory
        group_dir = "forecasts"
        shutil.copytree(os.path.join(RandomAlarmBasedEvaluationTests.__referenceDataDir,
                                     reference_dir, 
                                     group_dir),
                        os.path.join(CSEPTestCase.TestDirPath, group_dir))
        
        # Format input parameters for the test
        test_inputs = "forecast=%s" %(model)

        # ForecastGroup object that represents forecast models for the test
        forecast_group = ForecastGroup(os.path.join(CSEPTestCase.TestDirPath, 
                                                    group_dir),
                                       post_process_type,
                                       test_list,
                                       test_inputs,
                                       post_process_inputs = post_process_args)

        # Use the same directory for catalog data and test results
        for each_test in forecast_group.tests:
           each_test.run(CSEPTestCase.Date, 
                         CSEPTestCase.TestDirPath,
                         CSEPTestCase.TestDirPath)

           test_file = glob.glob('%s/*%s' %(CSEPTestCase.TestDirPath,
                                            CSEPFile.Extension.XML))[0]

           # Make sure plots are generated for each test result
#           plot_files = each_test.plot(test_file)
#           
#           for each_plot in plot_files:
#              self.failIf(os.path.exists(each_plot) is False,
#                          "Failed to generate plot file '%s'")

        
        ### Evaluate test results - seed file exists
        seed_file = glob.glob('%s/*randomSeed%s*' %(CSEPTestCase.TestDirPath,
                                                   CSEPFile.Extension.ASCII))
        
        self.failIf(len(seed_file) == 0,
                    "Failed to generate seed file for the test.")
        

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
