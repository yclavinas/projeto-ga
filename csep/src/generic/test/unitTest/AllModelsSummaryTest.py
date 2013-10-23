"""
Module AllModelsSummaryTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, datetime, filecmp
from xml.etree.cElementTree import parse, ElementTree

from Environment import *
from CSEPInitFile import CSEPInitFile
from CSEPTestCase import CSEPTestCase
from EvaluationTest import EvaluationTest
from EvaluationTestFactory import EvaluationTestFactory
from AllModelsSummary import AllModelsSummary
import CSEPFile


 #-------------------------------------------------------------------------------
 #
 # Validate that AllModelsSummary module is working properly.
 #
class AllModelsSummaryTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'allModelsSummary')


   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation N-test
   # are created and updated properly.
   #
   def testNEvaluationTest(self):
      """ Confirm that AllModelsSummary.py module generates and \
updates evaluation N-test cumulative results file for all participating in the
group models properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      summary_file = 'N-Test_all.xml'               
      test_date = datetime.datetime(2009, 12, 29)
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file -----------------------------------------------
         # Order of result files being added to the summary is important during 
         # validation of cumulative results
         reference_files = ['rTest_N-Test_STEP_12_29_2009-fromXML.xml',
                            'rTest_N-Test_ETAS_12_29_2009-fromXML.xml',
                            'rTest_N-Test_KJSSOneDayCalifornia_12_29_2009-fromXML.xml']
   
         for each_result in reference_files:
             
             test_type = EvaluationTest.typeFromFilename(each_result)
             eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
             
             self.__update(summary_file, 
                           eval_test_class_ref, 
                           test_date, 
                           each_result) 

         ### Validate results --------------------------------------------------
         reference_file = os.path.join(AllModelsSummaryTest.__referenceDataDir,
                                       'all.rTest_N-Test.xml')
         self.failIf(filecmp.cmp(summary_file, reference_file) is False, 
                    'Failed to compare reference file %s to %s' %(reference_file,
                                                                  summary_file))
         

         ###--------------------------------------------------------------------
         ### Update cumulative file with the new test results for already 
         ### existing model
         reference_files = ['rTest_N-Test_STEP_12_30_2009-fromXML.xml',
                            'rTest_N-Test_ETAS_12_30_2009-fromXML.xml',
                            'rTest_N-Test_KJSSOneDayCalifornia_12_30_2009-fromXML.xml']
   
         test_date = datetime.datetime(2009, 12, 30)
         
         for each_result in reference_files:
             
             # Should generate an exception
             try:
                 
                 sys.exc_clear()
                 
                 test_type = EvaluationTest.typeFromFilename(each_result)
                 eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
                 
                 self.__update(summary_file, 
                               eval_test_class_ref, 
                               test_date, 
                               each_result)
                 
             except RuntimeError, error: 
                 self.failIf("Result element exists" not in error.args[0], 
                             "Failed to raise exception of expected content for existing entry %s, got exception '%s'"
                             %(each_result,
                               error.args[0]))
                 
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
        

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation L-test
   # are created and updated properly.
   #
   def testLEvaluationTest(self):
      """ Confirm that AllModelsSummary.py module generates and \
updates evaluation L-test cumulative results file for all participating in the
group models properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      summary_file = 'L-Test_all.xml'               
      test_date = datetime.datetime(2009, 12, 29)
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file -----------------------------------------------
         # Order of result files being added to the summary is important during 
         # validation of cumulative results
         reference_files = ['rTest_L-Test_ETAS_12_29_2009-fromXML.xml',
                            'rTest_L-Test_KJSSOneDayCalifornia_12_29_2009-fromXML.xml',
                            'rTest_L-Test_STEP_12_29_2009-fromXML.xml']
   
         for each_result in reference_files:
             
             test_type = EvaluationTest.typeFromFilename(each_result)
             eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
             
             self.__update(summary_file, 
                           eval_test_class_ref, 
                           test_date, 
                           each_result) 

         ### Validate results --------------------------------------------------
         reference_file = os.path.join(AllModelsSummaryTest.__referenceDataDir,
                                       'all.rTest_L-Test.xml')
         self.failIf(filecmp.cmp(summary_file, reference_file) is False, 
                    'Failed to compare reference file %s to %s' %(reference_file,
                                                                  summary_file))
         

         ###--------------------------------------------------------------------
         ### Update cumulative file with the new test results for already 
         ### existing model
         reference_files = ['rTest_L-Test_ETAS_12_30_2009-fromXML.xml',
                            'rTest_L-Test_KJSSOneDayCalifornia_12_30_2009-fromXML.xml',
                            'rTest_L-Test_STEP_12_30_2009-fromXML.xml']
   
         test_date = datetime.datetime(2009, 12, 30)
         
         for each_result in reference_files:
             
             # Should generate an exception
             try:
                 
                 sys.exc_clear()
                 
                 test_type = EvaluationTest.typeFromFilename(each_result)
                 eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
                 
                 self.__update(summary_file, 
                               eval_test_class_ref, 
                               test_date, 
                               each_result)
                 
             except RuntimeError, error: 
                 self.failIf("Result element exists" not in error.args[0], 
                             "Failed to raise exception of expected content for existing entry %s, got exception '%s'"
                             %(each_result,
                               error.args[0]))
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
        

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation R-test
   # are created and updated properly.
   #
   def testREvaluationTest(self):
      """ Confirm that AllModelsSummary.py module generates and \
updates evaluation R-test cumulative results file for all participating in the
group models properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      summary_file = 'R-Test_all.xml'               
      test_date = datetime.datetime(2009, 12, 29)
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file -----------------------------------------------
         # Order of result files being added to the summary is important during 
         # validation of cumulative results
         reference_files = ['rTest_R-Test_ETAS_12_29_2009-fromXML_KJSSOneDayCalifornia_12_29_2009-fromXML.xml',
                            'rTest_R-Test_STEP_12_29_2009-fromXML_KJSSOneDayCalifornia_12_29_2009-fromXML.xml',
                            'rTest_R-Test_STEP_12_29_2009-fromXML_ETAS_12_29_2009-fromXML.xml']
   
         for each_result in reference_files:
             
             test_type = EvaluationTest.typeFromFilename(each_result)
             eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
             
             self.__update(summary_file, 
                           eval_test_class_ref, 
                           test_date, 
                           each_result) 

         ### Validate results --------------------------------------------------
         reference_file = os.path.join(AllModelsSummaryTest.__referenceDataDir,
                                       'all.rTest_R-Test.xml')
         self.failIf(filecmp.cmp(summary_file, reference_file) is False, 
                    'Failed to compare reference file %s to %s' %(reference_file,
                                                                  summary_file))
         

         ###--------------------------------------------------------------------
         ### Update cumulative file with the new test results for already 
         ### existing model
         reference_files = ['rTest_R-Test_ETAS_12_30_2009-fromXML_KJSSOneDayCalifornia_12_30_2009-fromXML.xml',
                            'rTest_R-Test_STEP_12_30_2009-fromXML_KJSSOneDayCalifornia_12_30_2009-fromXML.xml',
                            'rTest_R-Test_STEP_12_30_2009-fromXML_ETAS_12_30_2009-fromXML.xml']
   
         test_date = datetime.datetime(2009, 12, 30)
         
         for each_result in reference_files:
             
             # Should generate an exception
             try:
                 
                 sys.exc_clear()
                 
                 test_type = EvaluationTest.typeFromFilename(each_result)
                 eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
                 
                 self.__update(summary_file, 
                               eval_test_class_ref, 
                               test_date, 
                               each_result)
                 
             except RuntimeError, error: 
                 self.failIf("Result element exists" not in error.args[0], 
                             "Failed to raise exception of expected content for existing entry %s, got exception '%s'"
                             %(each_result,
                               error.args[0]))
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
        

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation S-test
   # are created and updated properly.
   #
   def testSEvaluationTest(self):
      """ Confirm that AllModelsSummary.py module generates and \
updates evaluation S-test cumulative results file for all participating in the
group models properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      summary_file = 'S-Test_all.xml'               
      test_date = datetime.datetime(2009, 12, 29)
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file -----------------------------------------------
         # Order of result files being added to the summary is important during 
         # validation of cumulative results
         reference_files = ['rTest_S-Test_ETAS_12_29_2009-fromXML.xml',
                            'rTest_S-Test_STEP_12_29_2009-fromXML.xml',
                            'rTest_S-Test_KJSSOneDayCalifornia_12_29_2009-fromXML.xml']
   
         for each_result in reference_files:
             
             test_type = EvaluationTest.typeFromFilename(each_result)
             eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
             
             self.__update(summary_file, 
                           eval_test_class_ref, 
                           test_date, 
                           each_result) 

         ### Validate results --------------------------------------------------
         reference_file = os.path.join(AllModelsSummaryTest.__referenceDataDir,
                                       'all.rTest_S-Test.xml')
         self.failIf(filecmp.cmp(summary_file, reference_file) is False, 
                    'Failed to compare reference file %s to %s' %(reference_file,
                                                                  summary_file))
         

         ###--------------------------------------------------------------------
         ### Update cumulative file with the new test results for already 
         ### existing model
         reference_files = ['rTest_S-Test_ETAS_12_30_2009-fromXML.xml',
                            'rTest_S-Test_KJSSOneDayCalifornia_12_30_2009-fromXML.xml',
                            'rTest_S-Test_STEP_12_30_2009-fromXML.xml']
   
         test_date = datetime.datetime(2009, 12, 30)
         
         for each_result in reference_files:
             
             # Should generate an exception
             try:
                 
                 sys.exc_clear()
                 
                 test_type = EvaluationTest.typeFromFilename(each_result)
                 eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
                 
                 self.__update(summary_file, 
                               eval_test_class_ref, 
                               test_date, 
                               each_result)
                 
             except RuntimeError, error: 
                 self.failIf("Result element exists" not in error.args[0], 
                             "Failed to raise exception of expected content for existing entry %s, got exception '%s'"
                             %(each_result,
                               error.args[0]))
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
        

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation M-test
   # are created and updated properly.
   #
   def testMEvaluationTest(self):
      """ Confirm that AllModelsSummary.py module generates and \
updates evaluation M-test cumulative results file for all participating in the
group models properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      summary_file = 'M-Test_all.xml'               
      test_date = datetime.datetime(2009, 12, 29)
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file -----------------------------------------------
         # Order of result files being added to the summary is important during 
         # validation of cumulative results
         reference_files = ['rTest_M-Test_ETAS_12_29_2009-fromXML.xml',
                            'rTest_M-Test_KJSSOneDayCalifornia_12_29_2009-fromXML.xml',
                            'rTest_M-Test_STEP_12_29_2009-fromXML.xml']
   
         for each_result in reference_files:
             
             test_type = EvaluationTest.typeFromFilename(each_result)
             eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
             
             self.__update(summary_file, 
                           eval_test_class_ref, 
                           test_date, 
                           each_result) 

         ### Validate results --------------------------------------------------
         reference_file = os.path.join(AllModelsSummaryTest.__referenceDataDir,
                                       'all.rTest_M-Test.xml')
         self.failIf(filecmp.cmp(summary_file, reference_file) is False, 
                    'Failed to compare reference file %s to %s' %(reference_file,
                                                                  summary_file))
         

         ###--------------------------------------------------------------------
         ### Update cumulative file with the new test results for already 
         ### existing model
         reference_files = ['rTest_M-Test_ETAS_12_30_2009-fromXML.xml',
                            'rTest_M-Test_KJSSOneDayCalifornia_12_30_2009-fromXML.xml',
                            'rTest_M-Test_STEP_12_30_2009-fromXML.xml']
   
         test_date = datetime.datetime(2009, 12, 30)
         
         for each_result in reference_files:
             
             # Should generate an exception
             try:
                 
                 sys.exc_clear()
                 
                 test_type = EvaluationTest.typeFromFilename(each_result)
                 eval_test_class_ref = EvaluationTestFactory().classReference(test_type)
                 
                 self.__update(summary_file, 
                               eval_test_class_ref, 
                               test_date, 
                               each_result)
                 
             except RuntimeError, error: 
                 self.failIf("Result element exists" not in error.args[0], 
                             "Failed to raise exception of expected content for existing entry %s, got exception '%s'"
                             %(each_result,
                               error.args[0]))
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
        

   #-----------------------------------------------------------------------------
   #
   # This is a helper method to create/update cumulative file based on given
   # result data file for a specific test date.
   #
   # Input:
   #        summary_file - Path to the summary file
   #        class_ref - Reference to the class that represents evaluation test
   #        test_date - Test date for result file
   #        result_file - Test date result file
   #        
   # Output:
   #        CSEPInitFile object representing the summary file
   #
   def __update(self, summary_file, class_ref, test_date, result_file):
      """ Create/update cumulative file with given test results."""

      summary = AllModelsSummary(summary_file,
                                 class_ref)

      ### Initialize/update summary file with results:
      reference_path = os.path.join(AllModelsSummaryTest.__referenceDataDir,
                                    result_file)
      
      forecast_end_date = test_date + datetime.timedelta(days=1)
      
      summary.update(reference_path, 
                     test_date,
                     test_date,
                     forecast_end_date)
      
      ### Validate results ------------------------------------------------------
      error_message = "AllModelsSummaryTest: expected cumulative file %s." \
                      %summary_file
      
      ### Check that summary file is generated
      self.failIf(os.path.exists(summary_file) is False, 
                  error_message)

      return summary

 
# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
