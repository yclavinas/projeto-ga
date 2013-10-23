"""
Module IntermediateResultsTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, datetime
from xml.etree.cElementTree import parse, ElementTree

from Environment import *
from CSEPInitFile import CSEPInitFile
from CSEPTestCase import CSEPTestCase
from EvaluationTest import EvaluationTest
from EvaluationTestFactory import EvaluationTestFactory
from ResultsSummary import ResultsSummary
from ResultsSummaryFactory import ResultsSummaryFactory
import CSEPFile


 #-------------------------------------------------------------------------------
 #
 # Validate that ResultsSummary module is working properly.
 #
class IntermediateResultsTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'intermediateResults')

   # Name of summary file for the test
   __file = None
   
   # CSEPInitFile object that represents current summary file for the test
   __tree = None

   # Flag to use string representation of values for result validation
   __useStringRep = True
   
   __startForecastDate = datetime.date(2007, 1, 1)
   __endForecastDate = datetime.date(2007, 12, 31)
   
      
   #-----------------------------------------------------------------------------
   #
   # This test verifies that intermediate test results for RELM evaluation N-test
   # are created and updated properly.
   #
   def testNEvaluationTest(self):
      """ Confirm that ResultsSummary.py module generates and \
updates evaluation N-test cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      IntermediateResultsTest.__file = 'N-Test_intermediate.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file ------------------------------------------------
         reference_file = 'rTest_N-Test_wiemer-schorlemmer.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)

         # Input arguments for summary file object
         args = [IntermediateResultsTest.__file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2007, 6, 25)
         self.__update(args, 
                       test_date_1,
                       reference_file)
         

         ### Validate results ---------------------------------------------------
         
         # Check delta value of cumulative 
         element_name = 'delta1'
         expected_values = "0"
         self.__validate(element_name, expected_values)         

         element_name = 'delta2'
         expected_values = "0.5"
         self.__validate(element_name, expected_values)         
         
         # Check eventCount value of cumulative 
         element_name = 'eventCount'
         expected_values = "2"
         self.__validate(element_name, expected_values)         

         ###---------------------------------------------------------------------
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2007, 6, 30)         
         reference_file = 'rTest_N-Test_wiemer-schorlemmer-lastDate.xml'         
         self.__update(args, 
                       test_date_2,
                       reference_file)

         ### Validate results----------------------------------------------------
         
         # Search for date values
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)
         
         # Check delta value of cumulative 
         element_name = 'delta1'
         expected_values = "0 0.6"
         self.__validate(element_name, expected_values)         

         element_name = 'delta2'
         expected_values = "0.5 0.8"
         self.__validate(element_name, expected_values)         

         # Check eventCount value of cumulative 
         element_name = 'eventCount'
         expected_values = "2 4"
         self.__validate(element_name, expected_values)         

         ### Insert missing test date in the middle of processed dates ----------
         test_date_3 = datetime.date(2007, 6, 27)         
         reference_file = 'rTest_N-Test_wiemer-schorlemmer-missed.xml'
         self.__update(args, 
                       test_date_3, 
                       reference_file)

         ### Validate results----------------------------------------------------
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)
   
         # Validate delta's
         element_name = 'delta1'
         expected_values = "0 1.0 0.6"
         self.__validate(element_name, expected_values)         

         element_name = 'delta2'
         expected_values = "0.5 0.8 0.8"
         self.__validate(element_name, expected_values)         

         # Check eventCount value of cumulative 
         element_name = 'eventCount'
         expected_values = "2 4 4"
         self.__validate(element_name, expected_values)         

         
         ### Replace test date results in the middle of processing --------------
         reference_file = 'rTest_N-Test_wiemer-schorlemmer-replaced.xml'
         self.__update(args, 
                       test_date_3, 
                       reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)

         # Validate delta's
         element_name = 'delta1'
         expected_values = "0 0.8 0.6"
         self.__validate(element_name, expected_values)         

         element_name = 'delta2'
         expected_values = "0.5 0.2 0.8"
         self.__validate(element_name, expected_values)         


         # Check eventCount value of cumulative 
         element_name = 'eventCount'
         expected_values = "2 2 4"
         self.__validate(element_name, expected_values)         

      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
        

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation L-test
   # are created and updated properly.
   #
   def testLEvaluationTest(self):
      """ Confirm that ResultsSummary.py module generates and \
updates evaluation L-test cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      IntermediateResultsTest.__file = 'L-Test_intermediate.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:
         
         ### Create summary file ------------------------------------------------
         reference_file = 'rTest_L-Test_wiemer-schorlemmer.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)
         
         # Input arguments for summary file object
         args = [IntermediateResultsTest.__file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2007, 10, 1)
         self.__update(args, 
                       test_date_1,
                       reference_file)
         
         ### Validate results----------------------------------------------------         
         
         # Validate gamma of cumulative result
         element_name = 'gamma'
         expected_values = "0.8"
         self.__validate(element_name, expected_values)         

         # Check log-likelihood value of cumulative 
         element_name = 'logLikelihood'
         expected_values = "0"
         self.__validate(element_name, expected_values)         
         
         
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2007, 10, 5)         
         self.__update(args, 
                       test_date_2,
                       reference_file)
         
         ### Validate results----------------------------------------------------         
         
         # Validate test dates
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)
         
         # Validate gamma -------------------------------------------------------
         element_name = 'gamma'
         expected_values = "0.8 0.8"
         self.__validate(element_name, expected_values)         

         # Check log-likelihood value of cumulative 
         element_name = 'logLikelihood'
         expected_values = "0 0"
         self.__validate(element_name, expected_values)         
         

         ### Update with missed date --------------------------------------------
         test_date_3 = datetime.date(2007, 10, 2)         
         reference_file = 'rTest_L-Test_wiemer-schorlemmer-missed.xml'
         self.__update(args, 
                       test_date_3,
                       reference_file)

         ### Validate results----------------------------------------------------         
         
         # Validate processed test dates
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)
   
         # Validate gamma's
         element_name = 'gamma'
         expected_values = "0.8 0.2 0.8"
         self.__validate(element_name, expected_values)          

         # Check log-likelihood value of cumulative 
         element_name = 'logLikelihood'
         expected_values = "0 20 0"
         self.__validate(element_name, expected_values)         
         
                           
         ### Replace test date results in the middle of processing --------------
         reference_file = 'rTest_L-Test_wiemer-schorlemmer-replaced.xml'
         self.__update(args, 
                       test_date_3, 
                       reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)

         # Validate delta's
         element_name = 'gamma'
         expected_values = "0.8 0.2 0.8"
         self.__validate(element_name, expected_values)         

         # Check log-likelihood value of cumulative 
         element_name = 'logLikelihood'
         expected_values = "0 4 0"
         self.__validate(element_name, expected_values)         
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         
         

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation R-test
   # are created and updated properly.
   #
   def testREvaluationTest(self):
      """ Confirm that ResultsSummary.py module generates and \
updates evaluation R-test cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      IntermediateResultsTest.__file = 'R-Test_intermediate.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:
         
         ### Create summary file ------------------------------------------------
         reference_file = 'rTest_R-Test_ward.seismic81_wiemer-schorlemmer.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)
         
         # Input arguments for summary file object
         args = [IntermediateResultsTest.__file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2007, 9, 15)
         self.__update(args, 
                       test_date_1,
                       reference_file)
         
         ### Validate results----------------------------------------------------         
         
         # Validate alpha and beta of cumulative result
         element_name = 'alpha'
         expected_values = "0.0"
         self.__validate(element_name, expected_values)         
         
         element_name = 'beta'
         expected_values = "0.5"
         self.__validate(element_name, expected_values)         

         # Check log-likelihood ratio value of cumulative 
         element_name = 'logLikelihoodRatio'
         expected_values = "1.5"
         self.__validate(element_name, expected_values)         

         
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2007, 9, 17)         
         self.__update(args, 
                       test_date_2,
                       reference_file)
         
         ### Validate results----------------------------------------------------         
         
         # Validate test dates
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)
         
         # Validate alpha and beta
         element_name = 'alpha'
         expected_values = "0.0 0.0"
         self.__validate(element_name, expected_values)         
         
         element_name = 'beta'
         expected_values = "0.5 0.5"
         self.__validate(element_name, expected_values)         

         # Check log-likelihood ratio value of cumulative 
         element_name = 'logLikelihoodRatio'
         expected_values = "1.5 1.5"
         self.__validate(element_name, expected_values)         

         
         ### Update with missed date --------------------------------------------
         test_date_3 = datetime.date(2007, 9, 16)         
         reference_file = 'rTest_R-Test_ward.seismic81_wiemer-schorlemmer-missed.xml'
         self.__update(args, 
                       test_date_3,
                       reference_file)

         ### Validate results----------------------------------------------------         
         
         # Validate processed test dates
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)
   
         # Validate alpha and beta
         element_name = 'alpha'
         expected_values = "0.0 0.0 0.0"
         self.__validate(element_name, expected_values)         
         
         element_name = 'beta'
         expected_values = "0.5 0.5 0.5"
         self.__validate(element_name, expected_values)         

         # Check log-likelihood ratio value of cumulative 
         element_name = 'logLikelihoodRatio'
         expected_values = "1.5 1.0 1.5"
         self.__validate(element_name, expected_values)         
         
                           
         ### Replace test date results in the middle of processing --------------
         reference_file = 'rTest_R-Test_ward.seismic81_wiemer-schorlemmer-replaced.xml'
         self.__update(args, 
                       test_date_3, 
                       reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         IntermediateResultsTest.__useStringRep)

         # Validate alpha and beta
         element_name = 'alpha'
         expected_values = "0.0 1.0 0.0"
         self.__validate(element_name, expected_values)         
         
         element_name = 'beta'
         expected_values = "0.5 1.0 0.5"
         self.__validate(element_name, expected_values)         

         # Check log-likelihood ratio value of cumulative 
         element_name = 'logLikelihoodRatio'
         expected_values = "1.5 2.0 1.5"
         self.__validate(element_name, expected_values)         
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         
         

   #-----------------------------------------------------------------------------
   #
   # This is a helper method to create/update cumulative file based on given
   # result data file for a specific test date.
   #
   # Input:
   #        args - List of input arguments for summary object
   #        test_date - Test date for result file
   #        result_file - Test date result file
   #        
   # Output:
   #        CSEPInitFile object representing the summary file
   #
   def __update(self, args, test_date, result_file):
      """ Create/update intermediate file with given test results."""

      summary = ResultsSummaryFactory().object(ResultsSummary.Type,
                                               args)

      ### Initialize/update summary file with results:
      reference_path = os.path.join(IntermediateResultsTest.__referenceDataDir,
                                    result_file)
      
      summary.update(reference_path, 
                     test_date,
                     IntermediateResultsTest.__startForecastDate,
                     IntermediateResultsTest.__endForecastDate)
      
      ### Validate results ------------------------------------------------------
      error_message = "IntermediateResultsTest: expected cumulative file %s." \
                      %IntermediateResultsTest.__file
      
      ### Check that summary file is generated
      self.failIf(os.path.exists(IntermediateResultsTest.__file) == False, 
                  error_message)

      IntermediateResultsTest.__tree = CSEPInitFile(IntermediateResultsTest.__file)
      return


   #-----------------------------------------------------------------------------
   #
   # This is a helper method to validate content of intermediate file based on given
   # reference data.
   #
   # Input:
   #        element_name - Tag of summary file element to validate.
   #        expected_values - Expected value for the element.
   #        use_string_rep - Flag to indicate if validation should be done on
   #                         numerical values of the results. Default is False, 
   #                         that means to use string representation of results
   #                         for validation.
   #        
   # Output:
   #        None
   #
   def __validate(self, 
                  element_name, 
                  expected_values, 
                  use_string_rep = False):
      """ Validate content of intermediate file."""

      nodes = IntermediateResultsTest.__tree.elements(element_name)
      simulation_results = nodes[0].text

      error_message = "'%s' element in '%s' file: expected %s values, got %s." \
                      %(element_name, 
                        IntermediateResultsTest.__file, 
                        expected_values, 
                        simulation_results)
      if use_string_rep == False:                
         self.failIf(CSEPFile.compareLines(expected_values, 
                                           simulation_results) == False,
                     error_message)    
      else:
         self.failIf(simulation_results.strip() != expected_values,
                     error_message)
            
      return
   
 
# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
