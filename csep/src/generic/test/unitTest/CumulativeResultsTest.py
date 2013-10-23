"""
Module CumulativeResultsTest
"""

__version__ = "$Revision: 4237 $"
__revision__ = "$Id: CumulativeResultsTest.py 4237 2013-03-22 21:03:38Z liukis $"


import sys, os, unittest, datetime, shutil
from xml.etree.cElementTree import parse, ElementTree

from Environment import *
from CSEPInitFile import CSEPInitFile
from CSEPTestCase import CSEPTestCase
from EvaluationTest import EvaluationTest
from EvaluationTestFactory import EvaluationTestFactory
from ResultsCumulativeSummary import ResultsCumulativeSummary
from ResultsSummaryFactory import ResultsSummaryFactory
import CSEPFile
from ForecastGroup import ForecastGroup
from RELMAftershockPostProcess import RELMAftershockPostProcess


 #-------------------------------------------------------------------------------
 #
 # Validate that ResultsCumulativeSummary module is working properly.
 #
class CumulativeResultsTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'cumulativeResults')

   # Flag to use string representation of values for result validation
   __useStringRep = True
   
   
   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation N-test
   # are created and updated properly.
   #
   def testNEvaluationTest(self):
      """ Confirm that ResultsCumulativeSummary.py module generates and \
updates evaluation N-test cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      # Cumulative file for the test
      cum_file = 'N-Test_cumulative.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file ------------------------------------------------
         reference_file = 'rTest_N-Test_wiemer-schorlemmer.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)

         # Input arguments for summary file object
         args = [cum_file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2007, 6, 25)
         doc = self.__update(args, 
                             test_date_1,
                             reference_file)
         

         ### Validate results ---------------------------------------------------

         # Check that cumulative true result value has been set to the 
         # one from result file:
         element_name = 'eventCount'
         expected_values = "2"         
         self.__validate(element_name, expected_values, doc)
         
         # Check that cumulative simulation values have been set to the 
         # simulation values from result file:
         element_name = 'eventCountForecast'
         expected_values = "2.5"         
         self.__validate(element_name, expected_values, doc)

         # Check delta values of cumulative 
         element_name = 'delta1'
         expected_values = "0.71270250481635422"
         self.__validate(element_name, expected_values, doc)         

         element_name = 'delta2'
         expected_values = "0.54381311588332948"
         self.__validate(element_name, expected_values, doc)         
         

         ###---------------------------------------------------------------------
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2007, 6, 30)         
         doc = self.__update(args, 
                             test_date_2,
                             reference_file)

         ### Validate results----------------------------------------------------
         
         # Search for date values
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         doc,
                         CumulativeResultsTest.__useStringRep)
         
         # Validate cumulative values - should be original values * 2
         element_name = 'eventCount'
         expected_values = "4"         
         self.__validate(element_name, expected_values, doc)
         
         element_name = 'eventCountForecast'
         expected_values = "5.0"
         self.__validate(element_name, expected_values, doc)         

         # Check delta value of cumulative 
         element_name = 'delta1'
         expected_values = "0.71270250481635422 0.73497408470263836"
         self.__validate(element_name, expected_values, doc)         

         element_name = 'delta2'
         expected_values = "0.54381311588332948 0.44049328506521224"
         self.__validate(element_name, expected_values, doc)         


         ### Insert missing test date in the middle of processed dates ----------
         test_date_3 = datetime.date(2007, 6, 27)         
         reference_file = 'rTest_N-Test_wiemer-schorlemmer-missed.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)

         ### Validate results----------------------------------------------------
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be original*2 + new values from 
         # reference file
         element_name = 'eventCount'
         expected_values = "8"         
         self.__validate(element_name, expected_values, doc)
         
         element_name ='eventCountForecast'
         expected_values = '8'
         self.__validate(element_name, expected_values, doc)         

         # Validate delta's
         element_name = 'delta1'
         expected_values = "0.71270250481635422 0.47108131347413784 0.54703919051300631"
         self.__validate(element_name, expected_values, doc)         
         

         element_name = 'delta2'
         expected_values = "0.54381311588332948 0.68603598028230406 0.59254734143759302"
         self.__validate(element_name, expected_values, doc)         
         
         ### Replace test date results in the middle of processing --------------
         reference_file = 'rTest_N-Test_wiemer-schorlemmer-replaced.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be original simulation * 2 + replaced values
         # from reference file
         element_name = 'eventCount'
         expected_values = "6"         
         self.__validate(element_name, expected_values, doc)
         
         element_name = 'eventCountForecast'
         expected_values = '6'
         self.__validate(element_name, expected_values, doc)         

         # Validate delta's
         element_name = 'delta1'
         expected_values = "0.71270250481635422 0.4633673320992151 0.55432035863538842"
         self.__validate(element_name, expected_values, doc)         
         

         element_name = 'delta2'
         expected_values = "0.54381311588332948 0.72544495330960446 0.6063027824125915"
         self.__validate(element_name, expected_values, doc)         
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
        

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation L-test
   # are created and updated properly.
   #
   def testLEvaluationTest(self):
      """ Confirm that ResultsCumulativeSummary.py module generates and \
updates evaluation L-test cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      cum_file = 'L-Test_cumulative.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:
         
         ### Create summary file ------------------------------------------------
         reference_file = 'rTest_L-Test_wiemer-schorlemmer.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)
         
         # Input arguments for summary file object
         args = [cum_file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2007, 10, 1)
         doc = self.__update(args, 
                             test_date_1,
                             reference_file)
         
         ### Validate results----------------------------------------------------         
         
         ### Validate simulation values - the same as result file
         element_name = 'simulationData'
         expected_values = "-7.541801e+00 -7.369678e+00 \
                            -2.819391e+01 -8.746489e+00 \
                            -3.737373e+01 -2.968446e+01 \
                            -2.985046e+01 -2.298666e+00 \
                            9.796549e+00 3.191022e+00"
         self.__validate(element_name, expected_values, doc)

         # Validate gamma of cumulative result
         element_name = 'gamma'
         expected_values = "0.8"
         self.__validate(element_name, expected_values, doc)         
         
         
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2007, 10, 5)         
         doc = self.__update(args, 
                             test_date_2,
                             reference_file)
         
         ### Validate results----------------------------------------------------         
         
         # Validate test dates
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         doc,
                         CumulativeResultsTest.__useStringRep)
         
         # Validate simulation values - should be original simulation * 2
         element_name = 'simulationData'         
         expected_values = "-15.083602000000001 -14.739356000000001 \
                            -56.387819999999998 -17.492978000000001 \
                            -74.747460000000004 -59.368920000000003 \
                            -59.700920000000004 -4.5973319999999998 \
                            19.593098000000001 6.3820439999999996"
         self.__validate(element_name, expected_values, doc)         
         
         # Validate gamma -------------------------------------------------------
         element_name = 'gamma'
         expected_values = "0.8 0.8"
         self.__validate(element_name, expected_values, doc)         
         

         ### Update with missed date --------------------------------------------
         test_date_3 = datetime.date(2007, 10, 2)         
         reference_file = 'rTest_L-Test_wiemer-schorlemmer-missed.xml'
         doc = self.__update(args, 
                             test_date_3,
                             reference_file)

         ### Validate results----------------------------------------------------         
         
         # Validate processed test dates
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc,
                         CumulativeResultsTest.__useStringRep)
   
         # Validate simulation values
         element_name = 'simulationData'         
         expected_values = "-4.5836020000000008 -3.2393560000000008 \
                            -35.887819999999998 13.007021999999999 \
                            -34.247460000000004 -8.8689200000000028 \
                            0.79907999999999646 65.902668000000006 \
                            100.093098 96.882043999999993"
         self.__validate(element_name, expected_values, doc)                            

         # Validate gamma's
         element_name = 'gamma'
         expected_values = "0.8 0.4 0.7"
         self.__validate(element_name, expected_values, doc)          
         
                           
         ### Replace test date results in the middle of processing --------------
         reference_file = 'rTest_L-Test_wiemer-schorlemmer-replaced.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate simulation values - should be original simulation * 2 + values
         # from reference file
         element_name = 'simulationData'
         expected_values = "-15.083602000000001 -14.739356000000001 \
                            -56.387819999999998 -17.492978000000001 \
                            -74.747460000000004 -59.368920000000003 \
                            -59.700920000000004 -4.5973319999999998 \
                            19.593098000000001 6.3820439999999996"
         self.__validate(element_name, expected_values, doc)         

         # Validate delta's
         element_name = 'gamma'
         expected_values = "0.8 0.9 0.8"
         self.__validate(element_name, expected_values, doc)         
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         
         

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for RELM evaluation R-test
   # are created and updated properly.
   #
   def testREvaluationTest(self):
      """ Confirm that ResultsCumulativeSummary.py module generates and \
updates evaluation R-test cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      cum_file = 'R-Test_cumulative.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:
         
         ### Create summary file ------------------------------------------------
         reference_file = 'rTest_R-Test_ward.seismic81_wiemer-schorlemmer.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)

         # Input arguments for summary file object
         args = [cum_file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2007, 9, 15)
         doc = self.__update(args, 
                             test_date_1,
                             reference_file)
         
         ### Validate results----------------------------------------------------         
         
         ### Validate simulation values - the same as result file
         element_name = 'modelSimulationData1'
         expected_values = "1.0 1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9"
         self.__validate(element_name, expected_values, doc)

         element_name = 'modelSimulationData2'
         expected_values = "2.0 2.1 2.2 2.3 2.4 2.5 2.6 2.7 2.8 2.9"
         self.__validate(element_name, expected_values, doc)

         # Validate alpha and beta of cumulative result
         element_name = 'alpha'
         expected_values = "0.0"
         self.__validate(element_name, expected_values, doc)         
         
         element_name = 'beta'
         expected_values = "0.59999999999999998"
         self.__validate(element_name, expected_values, doc)         
         
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2007, 9, 17)         
         doc = self.__update(args, 
                             test_date_2,
                             reference_file)
         
         ### Validate results----------------------------------------------------         
         
         # Validate test dates
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)
         
         # Validate simulation values - should be original simulation * 2
         element_name = 'modelSimulationData1'         
         expected_values = "2.0 2.2 2.4 2.6 2.8 3.0 3.2 3.4 3.6 3.8"
         self.__validate(element_name, expected_values, doc)         

         element_name = 'modelSimulationData2'         
         expected_values = "4.0 4.2 4.4 4.6 4.8 5.0 5.2 5.4 5.6 5.8"
         self.__validate(element_name, expected_values, doc)         
         
         # Validate alpha and beta
         element_name = 'alpha'
         expected_values = "0.0 0.0"
         self.__validate(element_name, expected_values, doc)         
         
         element_name = 'beta'
         expected_values = "0.59999999999999998 0.59999999999999998"
         self.__validate(element_name, expected_values, doc)         

         
         ### Update with missed date --------------------------------------------
         test_date_3 = datetime.date(2007, 9, 16)         
         reference_file = 'rTest_R-Test_ward.seismic81_wiemer-schorlemmer-missed.xml'
         doc = self.__update(args, 
                             test_date_3,
                             reference_file)

         ### Validate results----------------------------------------------------         
         
         # Validate processed test dates
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)
   
         # Validate simulation values
         element_name = 'modelSimulationData1'         
         expected_values = "2.0 -0.8 2.4 -0.4 2.8 0.0 3.2 0.4 3.6 0.8"
         self.__validate(element_name, expected_values, doc)         

         element_name = 'modelSimulationData2'         
         expected_values = "3.0 4.2 3.4 4.6 3.8 5.0 4.2 5.4 4.6 5.8"
         self.__validate(element_name, expected_values, doc)         

         # Validate alpha and beta
         element_name = 'alpha'
         expected_values = "0.0 0.8 0.29999999999999999"
         self.__validate(element_name, expected_values, doc)         
         
         element_name = 'beta'
         expected_values = "0.59999999999999998 1.0 1.0"
         self.__validate(element_name, expected_values, doc)         
         
                           
         ### Replace test date results in the middle of processing --------------
         reference_file = 'rTest_R-Test_ward.seismic81_wiemer-schorlemmer-replaced.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate simulation values - should be original simulation * 2 + values
         # from reference file
         element_name = 'modelSimulationData1'         
         expected_values = "2.0 2.2 2.4 2.6 2.8 3.0 3.2 3.4 3.6 3.8"
         self.__validate(element_name, expected_values, doc)         

         element_name = 'modelSimulationData2'         
         expected_values = "4.0 4.2 4.4 4.6 4.8 5.0 5.2 5.4 5.6 5.8"
         self.__validate(element_name, expected_values, doc)         

         # Validate alpha and beta
         element_name = 'alpha'
         expected_values = "0.0 1.0 0.59999999999999998"
         self.__validate(element_name, expected_values, doc)         
         
         element_name = 'beta'
         expected_values = "0.59999999999999998 1.0 1.0"
         self.__validate(element_name, expected_values, doc)         
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         
         
         
   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for diagnostics evaluation 
   # PearsonResiduals test are created and updated properly.
   #
   def testPearsonResidualsDiagnosticsEvaluationTest(self):
      """ Confirm that DiagnosticsSummary.py module generates and \
updates evaluation RP cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      cum_file = 'RP-Test_cumulative.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file ------------------------------------------------
         reference_file = 'dTest_RP-Test_testModel-fromXML.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)

         # Input arguments for summary file object
         args = [cum_file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2013, 2, 7)
         doc = self.__update(args, 
                             test_date_1,
                             reference_file)
         

         ### Validate results ---------------------------------------------------

         # Check that cumulative true result value has been set to the 
         # one from result file:
         element_name = 'P.residual'
         expected_values = "-0.001 -0.002 -0.003 -0.004 -0.005"         
         self.__validate(element_name, expected_values, doc)
         
         ###---------------------------------------------------------------------
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2013, 3, 7)         
         doc = self.__update(args, 
                             test_date_2,
                             reference_file)

         ### Validate results----------------------------------------------------
         
         # Search for date values
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)
         
         # Validate cumulative values - should be original values * 2
         element_name = 'P.residual'
         expected_values = "-0.002 -0.004 -0.006 -0.008 -0.01"         
         self.__validate(element_name, expected_values, doc)
         

         ### Insert missing test date in the middle of processed dates ----------
         test_date_3 = datetime.date(2013, 2, 17)         
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)

         ### Validate results----------------------------------------------------
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be original values*3
         element_name = 'P.residual'
         expected_values = "-0.003 -0.006 -0.009 -0.012 -0.015"         
         self.__validate(element_name, expected_values, doc)

         
         ### Replace test date results in the middle of processing --------------
         reference_file = 'dTest_RP-Test_testModel-fromXML-replaced.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be original simulation * 2 + replaced values
         # from reference file
         element_name = 'P.residual'
         expected_values = "-0.004 -0.007 -0.01 -0.013 -0.016"         
         self.__validate(element_name, expected_values, doc)
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         


   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for diagnostics evaluation 
   # DevianceResiduals test are created and updated properly.
   #
   def testDevianceResidualsDiagnosticsEvaluationTest(self):
      """ Confirm that DiagnosticsSummary.py module generates and \
updates RD evaluation cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      cum_file = 'RD-Test_cumulative.xml'               
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         ### Create summary file ------------------------------------------------
         reference_file = 'dTest_RD-Test_testModel-fromXML.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)

         # Input arguments for summary file object
         args = [cum_file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2013, 2, 7)
         doc = self.__update(args, 
                             test_date_1,
                             reference_file)
         

         ### Validate results ---------------------------------------------------

         # Check that cumulative true result value has been set to the 
         # one from result file:
         element_name = 'deviance'
         expected_values = "0.1 0.2 0.3 0.4 0.5"         
         self.__validate(element_name, expected_values, doc)
         
         ###---------------------------------------------------------------------
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2013, 3, 7)         
         doc = self.__update(args, 
                             test_date_2,
                             reference_file)

         ### Validate results----------------------------------------------------
         
         # Search for date values
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         doc,
                         CumulativeResultsTest.__useStringRep)
         
         # Validate cumulative values - should be original values * 2
         element_name = 'deviance'
         expected_values = "0.2 0.4 0.6 0.8 1.0"         
         self.__validate(element_name, expected_values, doc)
         

         ### Insert missing test date in the middle of processed dates ----------
         test_date_3 = datetime.date(2013, 2, 17)         
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)

         ### Validate results----------------------------------------------------
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be original values*3
         element_name = 'deviance'
         expected_values = "0.3 0.6 0.9 1.2 1.5"         
         self.__validate(element_name, expected_values, doc)

         
         ### Replace test date results in the middle of processing --------------
         reference_file = 'dTest_RD-Test_testModel-fromXML-replaced.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values, 
                         doc,
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be original simulation * 2 + replaced values
         # from reference file
         element_name = 'deviance'
         expected_values = "0.4 0.7 1.0 1.3 1.6"         
         self.__validate(element_name, expected_values, doc)
         
      finally:
         
         # Go back to the original directory
         os.chdir(cwd)         
         

   #-----------------------------------------------------------------------------
   #
   # This test verifies that cumulative test results for diagnostics evaluation 
   # SuperThinnedResiduals test are created and updated properly.
   #
   def testSuperThinnedResidualsDiagnosticsEvaluationTest(self):
      """ Confirm that DiagnosticsSummary.py module generates and \
updates RT evaluation cumulative results file properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      cum_file = 'RT-Test_cumulative.xml'
      cum_file_rtt = 'RTT-Test_cumulative.xml'
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      # Copy model file to the runtime directory of the test
      model_file = 'testModel_3_22_2013-fromXML.dat'
      shutil.copyfile(os.path.join(CumulativeResultsTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(CSEPTestCase.TestDirPath,
                                   model_file))  
      
      try:

         ### Create summary file ------------------------------------------------
         reference_file = 'dTest_RT-Test_testModel-fromXML.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file)
         test_class_ref = EvaluationTestFactory().classReference(test_type)

         # Input arguments for summary file object
         args = [cum_file, 
                 test_class_ref]

         ### Initialize summary file with results:
         test_date_1 = datetime.date(2013, 2, 7)
         doc = self.__update(args, 
                             test_date_1,
                             reference_file)
         

         reference_file_rtt = 'dTest_RTT-Test_testModel-fromXML.xml'
         test_type = EvaluationTest.typeFromFilename(reference_file_rtt)
         test_class_ref_rtt = EvaluationTestFactory().classReference(test_type)

         # Input arguments for summary file object
         args_rtt = [cum_file_rtt, 
                     test_class_ref_rtt]

         ### Create RTT summary file with results:
         doc_rtt = self.__update(args_rtt, 
                                 test_date_1,
                                 reference_file_rtt)
         
         ### Validate RTT results ----------------------------------------------
         element_name = 'kValue'
         expected_values = "100.0"         
         self.__validate(element_name, expected_values, doc_rtt)

         ### Validate RT results -----------------------------------------------

         # Check that cumulative true result value has been set to the 
         # one from result file:
         element_name = 'lon'
         expected_values = "-124.8245 -119.9289 -123.49683 -116.41883 -125.223556397"         
         self.__validate(element_name, expected_values, doc)
         
         element_name = 'lat'
         expected_values = "41.1155 39.5253 40.83583 34.81333 40.8681199674"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'mag'
         expected_values = "5.0 5.0 5.4 5.06 8.56488843968"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'tag'
         expected_values = "1.0 1.0 1.0 1.0 2.0"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'kValue'
         expected_values = "100.0"         
         self.__validate(element_name, expected_values, doc)


         ###---------------------------------------------------------------------
         ### Update cumulative file with the same result info, but with new date
         test_date_2 = datetime.date(2013, 3, 7)         
         doc = self.__update(args, 
                             test_date_2,
                             reference_file)

         ### Validate results----------------------------------------------------
         
         # Search for date values
         element_name = 'testDate'
         expected_values = "%s %s" %(test_date_1, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)
         
         # Validate cumulative values - should be original values listed twice
         element_name = 'lon'
         expected_values = "-124.8245 -119.9289 -123.49683 -116.41883 -125.223556397 -124.8245 -119.9289 -123.49683 -116.41883 -125.223556397"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'lat'
         expected_values = "41.1155 39.5253 40.83583 34.81333 40.8681199674 41.1155 39.5253 40.83583 34.81333 40.8681199674"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'mag'
         expected_values = "5.0 5.0 5.4 5.06 8.56488843968 5.0 5.0 5.4 5.06 8.56488843968"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'tag'
         expected_values = "1.0 1.0 1.0 1.0 2.0 1.0 1.0 1.0 1.0 2.0"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'kValue'
         expected_values = "200.0"         
         self.__validate(element_name, expected_values, doc)

         ### Create RTT summary file with results ------------------------------
         doc_rtt = self.__update(args_rtt, 
                                 test_date_2,
                                 reference_file_rtt)
         
         ### Validate RTT results ----------------------------------------------
         element_name = 'kValue'
         expected_values = "200.0"         
         self.__validate(element_name, expected_values, doc_rtt)
         

         ### Insert missing test date in the middle of processed dates ---------
         test_date_3 = datetime.date(2013, 2, 17)         
         reference_file = 'dTest_RT-Test_testModel-fromXML-missed.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)

         ### Validate results---------------------------------------------------
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be [original, missed, original] values
         element_name = 'lon'
         expected_values = "-124.8245 -119.9289 -123.49683 -116.41883 -125.223556397 -124.0 -119.0 -124.8245 -119.9289 -123.49683 -116.41883 -125.223556397"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'lat'
         expected_values = "41.1155 39.5253 40.83583 34.81333 40.8681199674 41.0 39.0 41.1155 39.5253 40.83583 34.81333 40.8681199674"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'mag'
         expected_values = "5.0 5.0 5.4 5.06 8.56488843968 6.0 7.0 5.0 5.0 5.4 5.06 8.56488843968"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'tag'
         expected_values = "1.0 1.0 1.0 1.0 2.0 1.0 1.0 1.0 1.0 1.0 1.0 2.0"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'kValue'
         expected_values = "205.0"         
         self.__validate(element_name, expected_values, doc)
         

         ### Create RTT summary file with results ------------------------------
         doc_rtt = self.__update(args_rtt, 
                                 test_date_3,
                                 reference_file_rtt)
         
         ### Validate RTT results ----------------------------------------------
         element_name = 'kValue'
         expected_values = "205.0"         
         self.__validate(element_name, expected_values, doc_rtt)
          
         
         ### Replace test date results in the middle of processing --------------
         reference_file = 'dTest_RT-Test_testModel-fromXML-replaced.xml'
         doc = self.__update(args, 
                             test_date_3, 
                             reference_file)
         
         # Validate test dates in the file
         element_name = 'testDate'
         expected_values = "%s %s %s" %(test_date_1, test_date_3, test_date_2)
         self.__validate(element_name, 
                         expected_values,
                         doc, 
                         CumulativeResultsTest.__useStringRep)

         # Validate cumulative values - should be [original, replaced, original] values
         # from reference file
         element_name = 'lon'
         expected_values = "-124.8245 -119.9289 -123.49683 -116.41883 -125.223556397 -126.0 -120.0 -124.8245 -119.9289 -123.49683 -116.41883 -125.223556397"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'lat'
         expected_values = "41.1155 39.5253 40.83583 34.81333 40.8681199674 42.0 40.0 41.1155 39.5253 40.83583 34.81333 40.8681199674"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'mag'
         expected_values = "5.0 5.0 5.4 5.06 8.56488843968 7.5 7.6 5.0 5.0 5.4 5.06 8.56488843968"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'tag'
         expected_values = "1.0 1.0 1.0 1.0 2.0 2.0 2.0 1.0 1.0 1.0 1.0 2.0"         
         self.__validate(element_name, expected_values, doc)

         element_name = 'kValue'
         expected_values = "215.0"         
         self.__validate(element_name, expected_values, doc)
         
         ### Create RTT summary file with results ------------------------------
         doc_rtt = self.__update(args_rtt, 
                                 test_date_3,
                                 reference_file_rtt)
         
         ### Validate RTT results ----------------------------------------------
         element_name = 'kValue'
         expected_values = "215.0"         
         self.__validate(element_name, expected_values, doc_rtt)
         
         
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
      """ Create/update cumulative file with given test results."""

      cumulative_file = args[0]
      class_ref = args[1]
      summary = ResultsSummaryFactory().object(class_ref.resultsSummaryType(),
                                               args)

      ### Initialize/update summary file with results:
      reference_path = os.path.join(CumulativeResultsTest.__referenceDataDir,
                                    result_file)
      
      forecast_group = ForecastGroup(CSEPTestCase.TestDirPath,
                                     RELMAftershockPostProcess.Type,
                                     class_ref.Type)
      
      forecast_group.tests[0].testDir = CSEPTestCase.TestDirPath
      forecast_group.tests[0].scaleFactor = 1.0
      summary.evaluationTest(forecast_group.tests[0])
      
      summary.update(reference_path, 
                     test_date)
      
      ### Validate results ------------------------------------------------------
      error_message = "CumulativeResultsTest: expected cumulative file %s." \
                      %cumulative_file
      
      ### Check that summary file is generated
      self.failIf(os.path.exists(cumulative_file) == False, 
                  error_message)

      return CSEPInitFile(cumulative_file)


   #-----------------------------------------------------------------------------
   #
   # This is a helper method to validate content of cumulative file based on given
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
                  doc, 
                  use_string_rep = False):
      """ Validate content of cumulative file."""

      nodes = doc.elements(element_name)
      simulation_results = nodes[0].text

      error_message = "'%s' element in '%s' file: expected %s values, got %s." \
                      %(element_name, 
                        doc.name, 
                        expected_values, 
                        simulation_results)
      if use_string_rep is False:                
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
