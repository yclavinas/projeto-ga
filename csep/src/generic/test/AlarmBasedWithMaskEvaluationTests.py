"""
Module AlarmBasedWithMaskEvaluationTests
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
 # Test alarm-based evaluation tests that take masking bit into account for 
 # the forecasts models. This module tests
 # reproducibility of tests results. All tests are reading random numbers from
 # provided files.
 #
class AlarmBasedWithMaskEvaluationTests (CSEPTestCase):

    # Static data of the class
    
    # Path to the reference data for the tests
    __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                      'alarm_based_tests')
    
    # XML elements to validate for the MASS test: if attirubute is provided in the 
    # value of each pair, then compare elements that have matching 
    # attribute value
    __XMLElementsMASS = {'molchanNu' : None,
                         'molchanTrajectory' : 'forecast',
                         'molchanLowerConfidence' : None,
                         'molchanUpperConfidence' : None,
                         'assTau' : None,
                         'assTrajectory' : 'forecast',
                         'assLowerConfidence' : None,
                         'assUpperConfidence' : None}
    
    # XML elements to validate for the ROC test    
    __XMLElementsROC = {'hitRate' : None,
                        'falseAlarmRate' : None,
                        'lowerConfidence' : None,
                        'upperConfidence' : None}


    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for NW Pacific forecasts, and validate the results.
    #
    def testNWPacificMASSTestWithMask(self):
        """ Run MASS test for the NW Pacific forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'KJSSOneYearNWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = MASSTest.Type

        # Reference file with test results
        result_filename = 'KJMASSResultsNWPacific_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,
                              'nw_pacific',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsMASS,
                              OneYearModelPostProcess.Type,
                              post_process_args)
          

    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for SW Pacific forecasts, and validate the results.
    #
    def testSWPacificMASSTestWithMask(self):
        """ Run MASS test for the SW Pacific forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'KJSSOneYearSWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = MASSTest.Type

        # Reference file with test results
        result_filename = 'KJMASSResultsSWPacific_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,
                              'sw_pacific',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsMASS,
                              OneYearModelPostProcess.Type,
                              post_process_args)


    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for SW Pacific forecasts, and validate the results.
    #
    def testSWPacificROCTestWithMask(self):
        """ Run ROC test for the SW Pacific forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'KJSSOneYearSWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = ROCTest.Type

        # Reference file with test results
        result_filename = 'KJROCResultsSWPacific_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,
                              'sw_pacific',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsROC,
                              OneYearModelPostProcess.Type,
                              post_process_args)
        

    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for NW Pacific forecasts, and validate the results.
    #
    def testNWPacificROCTestWithMask(self):
        """ Run ROC test for the NW Pacific forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'KJSSOneYearNWPacific_7_1_2008.xml'
        post_process_args = [datetime.datetime(2008, 7, 1), 
                             datetime.datetime(2009, 7, 1)]
        test_list = ROCTest.Type

        # Reference file with test results
        result_filename = 'KJROCResultsNWPacific_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,                              
                              'nw_pacific',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsROC,
                              OneYearModelPostProcess.Type,
                              post_process_args)


    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for RELM Mainshock forecasts, and validate the 
    # results.
    #
    def testRELMMainshockMASSTestWithMask(self):
        """ Run MASS test for the RELM Mainshock forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'ebel.mainshock.xml'
        test_list = MASSTest.Type

        # Reference file with test results
        result_filename = 'EbelMASSResultsRELMMainshock_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,
                              'relm-mainshock',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsMASS,
                              RELMMainshockPostProcess.Type)
          

    #----------------------------------------------------------------------------
    #
    # Run MASS test evaluation for RELM Mainshock/Aftershock forecasts, and 
    # validate the results.
    #
    def testRELMMainshockAftershockMASSTestWithMask(self):
        """ Run MASS test for the RELM Mainshock/Aftershock forecast evaluation 
            and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'ebel.aftershock.xml'
        test_list = MASSTest.Type

        # Reference file with test results
        result_filename = 'EbelMASSResultsRELMMainshockAftershock_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,
                              'relm-mainshock-aftershock',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsMASS,
                              RELMAftershockPostProcess.Type)


    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for RELM Mainshock forecasts, and validate the 
    # results.
    #
    def testRELMMainshockROCTestWithMask(self):
        """ Run ROC test for the RELM Mainshock forecast evaluation and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'ebel.mainshock.xml'
        test_list = ROCTest.Type

        # Reference file with test results
        result_filename = 'EbelROCResultsRELMMainshock_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,
                              'relm-mainshock',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsROC,
                              RELMMainshockPostProcess.Type)


    #----------------------------------------------------------------------------
    #
    # Run ROC test evaluation for RELM Mainshock/Aftershock forecasts, and 
    # validate the results.
    #
    def testRELMMainshockAftershockROCTestWithMask(self):
        """ Run ROC test for the RELM Mainshock/Aftershock forecast evaluation 
            and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        
        model = 'ebel.aftershock.xml'
        test_list = ROCTest.Type

        # Reference file with test results
        result_filename = 'EbelROCResultsRELMMainshockAftershock_masked.xml'        

        self.__evaluationTest(model,
                              test_list,
                              result_filename,
                              'relm-mainshock-aftershock',
                              AlarmBasedWithMaskEvaluationTests.__XMLElementsROC,
                              RELMAftershockPostProcess.Type)
        

    #----------------------------------------------------------------------------
    #
    # Run evaluation test for the forecast, and validate the results.
    #
    # Inputs:
    #            model - Forecast file for which to invoke the test.
    #            test_list - List of evaluation tests to invoke.
    #            result_file - Name of the result file in XML format used for
    #                          test validation.
    #            reference_dir - Directory that stores input files, forecasts and
    #                            expected results files for evaluation.
    #            xml_tags - Dictionary of XML elements from result file and optional
    #                       attribute that should match for each pair of elements to be 
    #                       validated.
    #            post_process_type - Keyword identifying PostProcessing that
    #                                has been applied to the catalog data.
    #            post_process_args - Input arguments for post-processing. Default
    #                                is None.
    #            random_seed - Name of the file with seed for random numbers used by the 
    #                          evaluation test. Default is 'seed.dat'.
    #
    def __evaluationTest(self, 
                         model,
                         test_list,
                         result_file,
                         reference_dir,
                         xml_tags,
                         post_process_type, 
                         post_process_args = None,
                         random_seed = 'seed.dat'):                               
        """ Run specified evaluation test for the forecast and succeed."""


        ### Generate test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath)
        catalog_file = PostProcessFactory().object(post_process_type,
                                                   post_process_args).files.catalog
        catalog_file = CSEPFile.Name.ascii(catalog_file)

        ### Copy reference catalog data file to the test directory
        shutil.copyfile(os.path.join(AlarmBasedWithMaskEvaluationTests.__referenceDataDir,
                                     reference_dir,
                                     catalog_file),
                        os.path.join(CSEPTestCase.TestDirPath, catalog_file))    

        ### Path to the random seed file
        random_seed_path = os.path.join(AlarmBasedWithMaskEvaluationTests.__referenceDataDir,
                                        random_seed)

        # Copy forecast group directory to the runtime test directory
        group_dir = "forecasts"
        shutil.copytree(os.path.join(AlarmBasedWithMaskEvaluationTests.__referenceDataDir,
                                     reference_dir, 
                                     group_dir),
                        os.path.join(CSEPTestCase.TestDirPath, group_dir))
        
        # Format input parameters for the test
        test_inputs = "forecast=%s, randomSeedFile=%s" %(model,
                                                         random_seed_path)
        

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

        
        ### Evaluate test results
        reference_file = os.path.join(AlarmBasedWithMaskEvaluationTests.__referenceDataDir,
                                      reference_dir, 
                                      'results',
                                      result_file)
        test_file = glob.glob('%s/*%s' %(CSEPTestCase.TestDirPath,
                                         CSEPFile.Extension.XML))[0]
        
        CSEPLogging.getLogger(AlarmBasedWithMaskEvaluationTests.__name__).info("Comparing reference evaluation \
test file %s with generated evaluation test file %s..." \
                                               %(reference_file, test_file)) 
                          
        # Extract values of specified XML elements from both files and compare
        reference_xml = CSEPInitFile(reference_file)
        test_xml = CSEPInitFile(test_file)
        
        # Use percent difference validating results        
        percent_diff = 0.01
                
        for each_tag, tag_attribute in xml_tags.iteritems():
           ref_elements = reference_xml.elements(each_tag)
           test_elements = test_xml.elements(each_tag)           
           
           # If attribute for the XML element is provided, make sure to compare
           # elements that have matching values for that attribute
           if tag_attribute is not None:
              
              ref_dict = {}
              test_dict = {}
              for r_elem, t_elem in zip(ref_elements, 
                                        test_elements):
                 ref_dict[r_elem.attrib[tag_attribute]] = r_elem
                 test_dict[t_elem.attrib[tag_attribute]] = t_elem

              # Reset list of elements to the sorted by attribute list 
              ref_elements = ref_dict.values()
              test_elements = test_dict.values()
              
           
           for each_ref_elem, each_test_elem in zip(ref_elements,
                                                    test_elements):

              CSEPLogging.getLogger(AlarmBasedWithMaskEvaluationTests.__name__).info("Comparing %s \
XML element: %s to %s" %(each_tag, tostring(each_ref_elem), tostring(each_test_elem))) 
              
              self.failIf(CSEPFile.compareLines(each_ref_elem.text,
                                                each_test_elem.text,
                                                percent_diff,
                                                True) is False,
                          "Failed to compare %s XML elements: expected '%s', received '%s'"
                          %(each_tag, tostring(each_ref_elem), tostring(each_test_elem)))
              

        # Make sure plots are generated for each test result
        for each_test in forecast_group.tests:
           plot_files = each_test.plot(test_file)
           
           for each_plot in plot_files:
              self.failIf(os.path.exists(each_plot) is False,
                          "Failed to generate plot file '%s'")
        
           # Fix for Trac ticket #150: Make sure result file is renamed to 
           # unique filename (malformed filename won't be renamed) 
           each_test.resultData()
            
           # Make sure that all results in XML files are renamed:
           xml_files = glob.glob('%s/*%s' %(CSEPTestCase.TestDirPath,
                                            CSEPFile.Extension.XML))
           self.failIf(len(xml_files) != 0,
                       "Copies of XML files with unique filenames were not generated for: %s" \
                       %xml_files)

           # Make sure that all results in XML files are renamed:
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
