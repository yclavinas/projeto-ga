"""
Module StatisticalEvaluationTests
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, datetime, glob
from xml.etree.cElementTree import tostring
import numpy as np

import CSEPFile

from CSEPTestCase import CSEPTestCase
from EvaluationTest import EvaluationTest
from RELMCatalog import RELMCatalog
from OneDayModelPostProcess import OneDayModelPostProcess
from ForecastGroup import ForecastGroup
from CSEPLogging import CSEPLogging
from TStatisticalTest import TStatisticalTest
from WStatisticalTest import WStatisticalTest
from RELMAftershockPostProcess import RELMAftershockPostProcess
from CSEPInitFile import CSEPInitFile
from ThreeMonthsModelPostProcess import ThreeMonthsModelPostProcess
from CSEPSchedule import CSEPSchedule
from ForecastHandlerFactory import ForecastHandlerFactory

from BogusForecastModel1 import BogusForecastModel1
from BogusForecastModel2 import BogusForecastModel2
from BogusForecastModel3 import BogusForecastModel3

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
 # Test statistical evaluation tests for the forecasts models. This module tests
 # reproducibility of tests results.
 #
class StatisticalEvaluationTests (CSEPTestCase):

    # Directory with reference data for the tests
    __referenceDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                  'statistical_tests')
    
    # Test date 
    __testDate = datetime.datetime(2011, 3, 8)

    # XML elements to validate for each test
    __XMLElements = {TStatisticalTest.Type: ['meanInformationGain',
                                             'lowerConfidenceLimits',
                                             'upperConfidenceLimits',
                                             'numberEvents'],
                     WStatisticalTest.Type: ['WilcoxonSignificance']}

    __referenceData = {TStatisticalTest.Type: 'sTest_T-Test.xml',
                       WStatisticalTest.Type: 'sTest_W-Test.xml'}


    #---------------------------------------------------------------------------
    #
    # Run T and W evaluation tests for already prepared forecasts rates (Canterbury
    # aftershock sequence is used) and validate the results.
    #
    def testPreparedDataForTWTests(self):
        """ Run T and W evaluation tests for the already prepared forecast \
data and succeed. This test is using already collected forecasts rates for \
observed events, and verifies that Python impelementation of the test is \
working properly."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        test_list = '%s %s' %(TStatisticalTest.Type, 
                              WStatisticalTest.Type)

        # Directory with forecasts files
        forecast_dir = 'forecasts-rates'
        cumulative_start_date = '2010-09-04'
        forecast_group = ForecastGroup(os.path.join(StatisticalEvaluationTests.__referenceDir,
                                                    forecast_dir),
                                       OneDayModelPostProcess.Type,
                                       test_list,
                                       post_process_inputs = cumulative_start_date)
        
        # Create matrix of total forecasts rates (as it was used by original R code)
        np_rates = np.array([[66.611278,  66.611278,  4.608372,  4.608372],
                             [288.523330, 288.523330, 19.960993, 19.960993],
                             [4.648330,   4.648330,   4.648330,  4.648330],
                             [2.091676,   2.091676,   2.091676,  2.091676]])
        
        test_obj = forecast_group.tests[0]
        test_rates = test_obj.rates(forecast_group)
        
        test_rates.np_sum_rates = np_rates
        
        all_models = ['PPEETAS-rates-fromXML.dat',
                      'ETAS-rates-fromXML.dat',
                      'PPEEEPAS-0F-rates-fromXML.dat',
                      'ppe5yrnzdec-fromXML.dat.RATES-fromXML.dat']
        
        test_rates.all_models = all_models
        
        np_event_rates = np.zeros((len(all_models),),
                                  dtype = np.object)
        
        for index, model in enumerate(all_models):
             np_event_rates[index] = ForecastHandlerFactory().CurrentHandler.load(os.path.join(StatisticalEvaluationTests.__referenceDir,
                                                                                             forecast_dir,
                                                                                             model))
        test_rates.np_event_rates = np_event_rates
        
        shutil.copyfile(os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                     OneDayModelPostProcess().files.catalog),
                        os.path.join(CSEPTestCase.TestDirPath,
                                     OneDayModelPostProcess().files.catalog))
        
        catalog = RELMCatalog.load(os.path.join(CSEPTestCase.TestDirPath,
                                                OneDayModelPostProcess().files.catalog))
        
        for each_test in forecast_group.tests:
            each_test.cumulativeCatalogFile.npObject = catalog
            each_test.testDir = CSEPTestCase.TestDirPath
            each_test.testDate = StatisticalEvaluationTests.__testDate
       
        for each_test in forecast_group.tests:
            for each_forecast in all_models:
                each_test.evaluate(each_forecast)

            # Evaluate result data
            self.__evaluateResults(each_test)


    #---------------------------------------------------------------------------
    #
    # Run T and W evaluation tests for file-based forecasts and validate 
    # the results.
    #
    def testFileBasedForecastsTests(self):
        """ Run T and W evaluation tests for file-based forecasts \
and succeed. This test collects forecasts rates for the whole testing period \
and per each observed event, invokes T and W evaluation tests and verifies \
results."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        catalog_file = '2006_01_01.catalog.nodecl.dat'

        # Copy over catalog file to the test directory
        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                                                                 catalog_file),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 RELMAftershockPostProcess().files.catalog)))
        shutil.copyfile(os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                     catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath,
                                     RELMAftershockPostProcess().files.catalog))    
                
        # Tests to invoke
        test_list = '%s %s' %(TStatisticalTest.Type, 
                              WStatisticalTest.Type)

        # Directory with forecasts files
        forecast_dir = 'file_forecasts'
        test_date = datetime.datetime(2011, 5, 2)

        forecast_group = ForecastGroup(os.path.join(StatisticalEvaluationTests.__referenceDir,
                                                    forecast_dir),
                                       RELMAftershockPostProcess.Type,
                                       test_list)
        
        
        for each_test in forecast_group.tests:
            each_test.run(test_date,
                          CSEPTestCase.TestDirPath,
                          CSEPTestCase.TestDirPath)

            # Evaluate result data
            self.__evaluateResults(each_test,
                                   os.path.join(StatisticalEvaluationTests.__referenceDir,
                                                'file_forecasts_results'))


    #---------------------------------------------------------------------------
    #
    # Run T and W evaluation tests for one-day forecasts and validate 
    # the results.
    #
    def testOneDayForecasts(self):
        """ Run T and W evaluation tests for one-day forecasts \
and succeed. This test collects forecasts rates for the whole testing period \
and per each observed event, invokes T and W evaluation tests and verifies \
results."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        # Observation catalogs
        catalog_ref_dir = os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                       'one_day_catalogs')

        # Observation catalog for test date        
        catalog_file = 'catalog.nodecl.dat'

        # Copy over catalog file to the test directory
        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(catalog_ref_dir, 
                                                                                 catalog_file),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 OneDayModelPostProcess().files.catalog)))
        shutil.copyfile(os.path.join(catalog_ref_dir, 
                                     catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     OneDayModelPostProcess().files.catalog))    

        # Observation catalog for test date        
        catalog_file = 'cumulative.catalog.nodecl.dat'

        # Copy over catalog file to the test directory
        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(catalog_ref_dir, 
                                                                                 catalog_file),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 OneDayModelPostProcess().files.cumulativeCatalog)))
        shutil.copyfile(os.path.join(catalog_ref_dir, 
                                     catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     OneDayModelPostProcess().files.cumulativeCatalog))    
        
        # One-day models for the test
        models = '%s %s' %(BogusForecastModel1.Type,
                           BogusForecastModel2.Type)
                
        # Tests to invoke
        test_list = '%s %s' %(TStatisticalTest.Type, 
                              WStatisticalTest.Type)

        # Directory with forecasts files
        group_dir = 'one_day_forecasts'
        
        shutil.copytree(os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                     group_dir),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     group_dir))
        
        test_date = datetime.datetime(2011, 4, 3)

        forecast_group = ForecastGroup(os.path.join(CSEPTestCase.TestDirPath, 
                                                    group_dir),
                                       OneDayModelPostProcess.Type,
                                       test_list,
                                       model_list = models,
                                       post_process_inputs = [datetime.datetime(2011, 3, 28)])
        
        
        for each_test in forecast_group.tests:
            each_test.run(test_date,
                          CSEPTestCase.TestDirPath,
                          CSEPTestCase.TestDirPath)

            # Evaluate result data
            self.__evaluateResults(each_test,
                                   os.path.join(StatisticalEvaluationTests.__referenceDir,
                                                'one_day_forecasts_results'))



    #---------------------------------------------------------------------------
    #
    # Run T and W evaluation tests for three_month forecasts and validate 
    # the results.
    #
    def testThreeMonthForecasts(self):
        """ Run T and W evaluation tests for three-month forecasts \
and succeed. This test collects forecasts rates for the whole testing period \
and per each observed event, invokes T and W evaluation tests and verifies \
results."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        # One-day models for the test
        models = '%s %s %s' %(BogusForecastModel1.Type,
                              BogusForecastModel2.Type,
                              BogusForecastModel3.Type)
                
        # Tests to invoke
        test_list = '%s %s' %(TStatisticalTest.Type, 
                              WStatisticalTest.Type)

        # Directory with forecasts files
        group_dir = 'three_month_forecasts'
        
        shutil.copytree(os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                     group_dir),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     group_dir))
        
        test_date = datetime.datetime(2011, 5, 15)

        forecast_group = ForecastGroup(os.path.join(CSEPTestCase.TestDirPath, 
                                                    group_dir),
                                       ThreeMonthsModelPostProcess.Type,
                                       test_list,
                                       model_list = models,
                                       post_process_inputs = [datetime.datetime(2011, 4, 1),
                                                              datetime.datetime(2011, 7, 1),
                                                              datetime.datetime(2010, 10, 1)])
        
        # Observation catalogs
        catalog_ref_dir = os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                       'three_month_catalogs')

        # Copy over observation catalog file to the test directory
        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(catalog_ref_dir, 
                                                                                 forecast_group.postProcess().files.catalog),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 forecast_group.postProcess().files.catalog)))
        shutil.copyfile(os.path.join(catalog_ref_dir, 
                                     forecast_group.postProcess().files.catalog),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     forecast_group.postProcess().files.catalog))    

        # Copy over cumulative catalog file to the test directory
        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(catalog_ref_dir, 
                                                                                 forecast_group.postProcess().files.cumulativeCatalog),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 forecast_group.postProcess().files.cumulativeCatalog)))
        shutil.copyfile(os.path.join(catalog_ref_dir, 
                                     forecast_group.postProcess().files.cumulativeCatalog),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     forecast_group.postProcess().files.cumulativeCatalog))    
        
        
        models_schedule = CSEPSchedule()
        models_schedule.add('*',
                            '1 4 7 10',
                            '1')
        forecast_group.models.schedule = models_schedule
        
        for each_test in forecast_group.tests:
            each_test.run(test_date,
                          CSEPTestCase.TestDirPath,
                          CSEPTestCase.TestDirPath)

            # Evaluate result data
            self.__evaluateResults(each_test,
                                   os.path.join(StatisticalEvaluationTests.__referenceDir,
                                                'three_month_results'))


    #---------------------------------------------------------------------------
    #
    # Run T and W evaluation tests for one-day forecasts with observation
    # catalog of 1 event to make sure that statistical tests are not invoked.
    #
    def testLessThanTwoEventsCatalogs(self):
        """ Run T and W evaluation tests for less than 2 observed events \
to make sure that tests are not invoked."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        # Observation catalogs
        catalog_ref_dir = os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                       'one_event_catalog')

        # Observation catalog for test date        
        catalog_file = 'catalog.nodecl.dat'

        # Copy over catalog file to the test directory
        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(catalog_ref_dir, 
                                                                                 catalog_file),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 OneDayModelPostProcess().files.catalog)))
        shutil.copyfile(os.path.join(catalog_ref_dir, 
                                     catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     OneDayModelPostProcess().files.catalog))    

        # Observation catalog for test date        
        catalog_file = 'cumulative.catalog.nodecl.dat'

        # Copy over catalog file to the test directory
        _moduleLogger().info('Copying reference catalog %s to %s' %(os.path.join(catalog_ref_dir, 
                                                                                 catalog_file),
                                                                    os.path.join(CSEPTestCase.TestDirPath, 
                                                                                 OneDayModelPostProcess().files.cumulativeCatalog)))
        shutil.copyfile(os.path.join(catalog_ref_dir, 
                                     catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     OneDayModelPostProcess().files.cumulativeCatalog))    
        
        # One-day models for the test
        models = '%s %s' %(BogusForecastModel1.Type,
                           BogusForecastModel2.Type)
                
        # Tests to invoke
        test_list = '%s %s' %(TStatisticalTest.Type, 
                              WStatisticalTest.Type)

        # Directory with forecasts files
        group_dir = 'one_day_forecasts'
        
        shutil.copytree(os.path.join(StatisticalEvaluationTests.__referenceDir, 
                                     group_dir),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     group_dir))
        
        test_date = datetime.datetime(2011, 4, 3)

        forecast_group = ForecastGroup(os.path.join(CSEPTestCase.TestDirPath, 
                                                    group_dir),
                                       OneDayModelPostProcess.Type,
                                       test_list,
                                       model_list = models,
                                       post_process_inputs = [datetime.datetime(2011, 3, 28)])
        
        
        for each_test in forecast_group.tests:
            each_test.run(test_date,
                          CSEPTestCase.TestDirPath,
                          CSEPTestCase.TestDirPath)

            # Evaluate result data
            test_file = os.path.join(CSEPTestCase.TestDirPath,
                                     StatisticalEvaluationTests.__referenceData[each_test.type()])

            self.failIf(os.path.exists(test_file) is True,
                        "Test result file %s is generated for observation catalog of less than 3 events")


    #----------------------------------------------------------------------------
    #
    # Validate results for provided EvaluationTest object
    #
    def __evaluateResults(self, 
                          test_obj,
                          results_dir = None):                               
        """ Validate evaluation test results."""


        ### Evaluate test results
        reference_dir = StatisticalEvaluationTests.__referenceDir
        if results_dir is not None:
            reference_dir = results_dir
            
        reference_file = os.path.join(reference_dir,
                                      StatisticalEvaluationTests.__referenceData[test_obj.type()])

        test_file = os.path.join(CSEPTestCase.TestDirPath,
                                 StatisticalEvaluationTests.__referenceData[test_obj.type()])
        
        CSEPLogging.getLogger(StatisticalEvaluationTests.__name__).info("Comparing reference evaluation \
test file %s with generated evaluation test file %s..." %(reference_file, 
                                                          test_file)) 
                          
        # Extract values of specified XML elements from both files and compare
        reference_xml = CSEPInitFile(reference_file)
        test_xml = CSEPInitFile(test_file)
        
        # Use percent difference validating results        
        percent_diff = 0.01
                
        for each_tag in StatisticalEvaluationTests.__XMLElements[test_obj.type()]:
           ref_elements = reference_xml.elements(each_tag)
           test_elements = test_xml.elements(each_tag)           
           
           for each_ref_elem, each_test_elem in zip(ref_elements,
                                                    test_elements):

              _moduleLogger().info("Comparing %s \
XML element: %s to %s" %(each_tag, tostring(each_ref_elem), tostring(each_test_elem))) 
              
              self.failIf(CSEPFile.compareLines(each_ref_elem.text,
                                                each_test_elem.text,
                                                percent_diff,
                                                True) is False,
                          "Failed to compare %s XML elements: expected '%s', received '%s'"
                          %(each_tag, tostring(each_ref_elem), tostring(each_test_elem)))
              
        
        # Make sure plots are generated for each test result 
        plot_files = test_obj.plot(test_file)
       
        for each_plot in plot_files:
            self.failIf(os.path.exists(each_plot) is False,
                        "Failed to generate plot file '%s'")
    
        # Fix for Trac ticket #150: Make sure result file is renamed to 
        # unique filename (malformed filename won't be renamed) 
        test_obj.resultData()
        
        # Make sure that all results in XML files are renamed:
        xml_files = glob.glob('%s/*%s' %(CSEPTestCase.TestDirPath,
                                         CSEPFile.Extension.XML))
        self.failIf(len(xml_files) != 0,
                    "Copies of XML files with unique filenames were not generated for: %s" \
                    %xml_files)

        # Make sure that all plots in SVG files are renamed:
        svg_files = glob.glob('%s/*%s' %(CSEPTestCase.TestDirPath,
                                         CSEPFile.Extension.SVG))
        self.failIf(len(svg_files) != 0,
                    "Copies of SVG plot files with unique filenames were not generated for: %s" \
                   %svg_files)

          
# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
