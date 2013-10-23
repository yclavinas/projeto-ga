
"""
Module PlotXMLResultsTest
"""

__version__ = "$Revision: 4246 $"
__revision__ = "$Id: PlotXMLResultsTest.py 4246 2013-03-27 18:31:04Z liukis $"


import sys, os, unittest, shutil, copy, re

import GeographicalRegions
from CSEPTestCase import CSEPTestCase
from EvaluationTest import EvaluationTest
from EvaluationTestFactory import EvaluationTestFactory


 #--------------------------------------------------------------------
 #
 # Validate that plotting routines based on XML format result data are
 # generating files.
 #
class PlotXMLResultsTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'plotXMLResults')


   #-----------------------------------------------------------------------------
   #
   # This test verifies that plot is generated for all-models summary of
   # RELM evaluation N-test. The rest of RELM tests don't plot summary results,
   # there are only tables with result variables that can be created based
   # on these files. 
   #
   def testAllModelSummaryPlot(self):
      """ Confirm that plotting routines based on XML format summary result data \
for all models participating in the forecast group are generating svg files"""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:

         # Copy test results files to the test directory
         result_files = ['rTest_N-Test_RELMMainshockModels.xml',
                         'rTest_N-Test_OneDayModels.xml',
                         'rTest_N-Test_NWPacific_one_year_models.xml',
                         'rTest_L-Test_RELMMainshockModels.xml',
                         'rTest_M-Test_RELMMainshockModels.xml',
                         'rTest_S-Test_RELMMainshockModels.xml',
                         'rTest_L-Test_OneDayModels.xml',
                         'rTest_M-Test_OneDayModels.xml',
                         'rTest_S-Test_OneDayModels.xml']
         
         for each_file in result_files:
            shutil.copyfile(os.path.join(self.__referenceDataDir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)
            
            plot_files = test_class_ref.plotAllModelsSummary(each_file)

            ### Validate results - make sure file got generated
            for each_plot in plot_files:
                error = "Expected plot file '%s' does not exist." %(each_plot)
                self.failIf(os.path.exists(each_plot) == False, error)
            
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         
   

   #-----------------------------------------------------------------------------
   #
   # This test verifies that plot is generated for all-models summary of
   # RELM evaluation N-test and placed in proved output directory.
   # The rest of RELM tests don't plot summary results,
   # there are only tables with result variables that can be created based
   # on these files. 
   #
   def testAllModelSummaryPlotWithOutputDir(self):
      """ Confirm that plotting routines based on XML format summary result data \
for all models participating in the forecast group are generating svg files and \
placing them in provided output directory"""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      # Specify output directory to put plot files to - to support Trac ticket
      # #211 (Add support for new web application to view CSEP results)
      output_dir = 'plotOutputDir'
      os.makedirs(output_dir)
      
      try:

         # Copy test results files to the test directory
         result_files = ['rTest_N-Test_RELMMainshockModels.xml',
                         'rTest_N-Test_OneDayModels.xml',
                         'rTest_N-Test_NWPacific_one_year_models.xml',
                         'rTest_L-Test_RELMMainshockModels.xml',
                         'rTest_M-Test_RELMMainshockModels.xml',
                         'rTest_S-Test_RELMMainshockModels.xml',
                         'rTest_L-Test_OneDayModels.xml',
                         'rTest_M-Test_OneDayModels.xml',
                         'rTest_S-Test_OneDayModels.xml']
         
         for each_file in result_files:
            shutil.copyfile(os.path.join(self.__referenceDataDir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)
            
            plot_files = test_class_ref.plotAllModelsSummary(each_file,
                                                             output_dir)

            ### Validate results - make sure file got generated
            for each_plot in plot_files:
                error = "Expected plot file '%s' does not exist." %(each_plot)
                self.failIf(os.path.exists(each_plot) == False, error)
            
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


   #----------------------------------------------------------------------------
   #
   # This test verifies that plotting routines based on XML format 
   # result data are working properly for diagnostics tests results that
   # were generated using empty observation catalog.
   #
   def testDiagnosticsTestsResultsWithEmptyCatalog(self):
      """ Confirm that plotting routines based on XML format result data \
are generating svg files."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      ref_dir = os.path.join(self.__referenceDataDir,
                             'diagnostic_tests_with_empty_catalog')
      try:
         # Copy test results files to the test directory
         result_files = ['dTest_LW-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RD-Test_helmstetter_et_al.hkj.aftershock-fromXML_shen_et_al.geodetic.aftershock-fromXML.xml',
                         'dTest_RP-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RT-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RTT-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml']

         for each_file in result_files:
            shutil.copyfile(os.path.join(ref_dir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)
            
            plot_files = test_class_ref.plot(each_file)

            ### Validate results - make sure file got generated
            for each_plot in plot_files:
                error = "Expected plot file '%s' does not exist." %(each_plot)
                self.failIf(os.path.exists(each_plot) == False, error)
            
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


   #-----------------------------------------------------------------------------
   #
   # This test verifies that forecasts maps are generated for the Global 
   # testing region.
   #
   def testDiagnosticsTestsSummaryForGlobalRegion(self):
      """ Confirm that Diagnostics Tests evaluation results plots are generated for the Global testing \
region."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # Setup testing region
      GeographicalRegions.Region().set(GeographicalRegions.Global)
      
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      ref_dir = os.path.join(self.__referenceDataDir,
                             'diagnostic_tests_global_region')
      try:
         # Copy test results files to the test directory
         result_files = ['diagnosticsSummary.dTest_RP-Test_KJSSGlobalOneDay-fromXML.xml']

         for each_file in result_files:
            shutil.copyfile(os.path.join(ref_dir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)
            
            plot_files = test_class_ref.plotSummary(each_file)

            ### Validate results - make sure file got generated
            for each_plot in plot_files:
                error = "Expected plot file '%s' does not exist." %(each_plot)
                self.failIf(os.path.exists(each_plot) == False, error)
            

         # Copy test results files to the test directory
         result_files = ['dTest_RT-Test_Triple_SOneYearGlobal_RateBased_1_1_2013-fromXML.xml']

         for each_file in result_files:
            shutil.copyfile(os.path.join(ref_dir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)
            
            plot_files = test_class_ref.plot(each_file)

            ### Validate results - make sure file got generated
            for each_plot in plot_files:
                error = "Expected plot file '%s' does not exist." %(each_plot)
                self.failIf(os.path.exists(each_plot) == False, error)

         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         

         GeographicalRegions.Region().set(GeographicalRegions.California)
      




   #--------------------------------------------------------------------
   #
   # This test verifies that plotting routines based on XML format 
   # result data are working properly.
   #
   def testDailyTestResults(self):
      """ Confirm that plotting routines based on XML format result data \
are generating svg files."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:
         # Copy test results files to the test directory
         result_files = ['rTest_L-Test_ebel.mainshock.corrected.5points.xml',
                         'rTest_L-Test_ebel.mainshock.corrected.xml',
                         'rTest_N-Test_ebel.mainshock.xml',
                         'rTest_R-Test_ebel.mainshock.corrected_ebel.mainshock.xml',
                         'rTest_N-Test_STEP-6-16-2007.xml',
                         'rTest_N-Test_EEPAS-0F-2-16-2008-fromXML.xml',
                         'aTest_MASS-Test_ebel.aftershock.xml',
                         'aTest_ROC-Test_ebel.aftershock.xml',
                         'aTest_ROC-Test_EASTThreeMonthCalifornia_AlarmBased_4_27_2009-fromXML_result.xml',
                         'rTest_S-Test_kagan_et_al.aftershock-fromXML.xml',
                         'rTest_M-Test_shen_et_al.geodetic.aftershock-fromXML.xml',
                         'dTest_LW-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RTT-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RT-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RP-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RD-Test_helmstetter_et_al.hkj.aftershock-fromXML_shen_et_al.geodetic.aftershock-fromXML.xml',
                         'dTest_RP-Test_shen_et_al.geodetic.aftershock-fromXML.xml',
                         'sTest_T-Test.xml',
                         'sTest_W-Test.xml']
         
         
         for each_file in result_files:
            shutil.copyfile(os.path.join(self.__referenceDataDir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)
            
            plot_files = test_class_ref.plot(each_file)

            ### Validate results - make sure file got generated
            for each_plot in plot_files:
                error = "Expected plot file '%s' does not exist." %(each_plot)
                self.failIf(os.path.exists(each_plot) == False, error)
            
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


   #----------------------------------------------------------------------------
   #
   # This test verifies that plotting routines based on XML format 
   # result data with specified output directory are working properly.
   #
   def testDailyTestResultsWithOutputDir(self):
      """ Confirm that plotting routines based on XML format result data \
are generating svg files and placing them in specified output directory."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      # Specify output directory to put plot files to - to support Trac ticket
      # #211 (Add support for new web application to view CSEP results)
      output_dir = 'plotOutputDir'
      os.makedirs(output_dir)
      
      try:
         # Copy test results files to the test directory
         result_files = ['rTest_L-Test_ebel.mainshock.corrected.5points.xml',
                         'rTest_L-Test_ebel.mainshock.corrected.xml',
                         'rTest_N-Test_ebel.mainshock.xml',
                         'rTest_R-Test_ebel.mainshock.corrected_ebel.mainshock.xml',
                         'rTest_N-Test_STEP-6-16-2007.xml',
                         'rTest_N-Test_EEPAS-0F-2-16-2008-fromXML.xml',
                         'aTest_MASS-Test_ebel.aftershock.xml',
                         'aTest_ROC-Test_ebel.aftershock.xml',
                         'aTest_ROC-Test_EASTThreeMonthCalifornia_AlarmBased_4_27_2009-fromXML_result.xml',
                         'rTest_S-Test_kagan_et_al.aftershock-fromXML.xml',
                         'rTest_M-Test_shen_et_al.geodetic.aftershock-fromXML.xml',
                         'dTest_LW-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RTT-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RT-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RP-Test_helmstetter_et_al.hkj.aftershock-fromXML.xml',
                         'dTest_RD-Test_helmstetter_et_al.hkj.aftershock-fromXML_shen_et_al.geodetic.aftershock-fromXML.xml',
                         'dTest_RP-Test_shen_et_al.geodetic.aftershock-fromXML.xml',
                         'sTest_T-Test.xml',
                         'sTest_W-Test.xml']
         
         
         for each_file in result_files:
            shutil.copyfile(os.path.join(self.__referenceDataDir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)
            
            plot_files = test_class_ref.plot(each_file,
                                             output_dir)

            ### Validate results - make sure file got generated
            for each_plot in plot_files:
                error = "Expected plot file '%s' does not exist." %(each_plot)
                self.failIf(os.path.exists(each_plot) == False, error)
            
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


   #--------------------------------------------------------------------
   #
   # This test verifies that plotting routines based on XML format 
   # summary result data are working properly.
   #
   def testSummaryTestResults(self):
      """ Confirm that plotting routines based on XML format summary result data \
are generating svg files. There are intermediate and cumulative summary results."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      try:
         # Copy test results files to the test directory
         result_files = ['cumulative.rTest_L-Test_STEP-fromXML.xml',
                         'cumulative.rTest_N-Test_STEP-fromXML.xml',
                         'cumulative.rTest_R-Test_STEP-fromXML_ETAS-fromXML.xml',
                         'cumulative.rTest_M-Test_ETAS-fromXML.xml',
                         'cumulative.rTest_S-Test_ETAS-fromXML.xml',
                         'intermediate.rTest_L-Test_ebel.aftershock.corrected-fromXML.xml',
                         'intermediate.rTest_N-Test_shen-et-al.geodetic.aftershock-fromXML.xml',
                         'intermediate.rTest_M-Test_wiemer_schorlemmer.alm-fromXML.xml',
                         'intermediate.rTest_S-Test_wiemer_schorlemmer.alm-fromXML.xml',
                         'intermediate.rTest_R-Test_helmstetter-et-al.hkj.aftershock-fromXML_ebel.aftershock-fromXML.xml']
         
         
         for each_file in result_files:
            shutil.copyfile(os.path.join(self.__referenceDataDir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)

            plot_file = test_class_ref.plotSummary(each_file)

            ### Validate results - make sure file got generated
            error = "Expected summary plot file '%s' does not exist." %(plot_file)
            self.failIf(os.path.exists(plot_file) == False, error)
            
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


   #----------------------------------------------------------------------------
   #
   # This test verifies that plotting routines based on XML format 
   # summary result data are working properly and plots are placed in provided
   # output directory.
   #
   def testSummaryTestResultsWithOutputDir(self):
      """ Confirm that plotting routines based on XML format summary result data \
are generating svg files and placing them in specified output directory. \
There are intermediate and cumulative summary results."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      # Specify output directory to put plot files to - to support Trac ticket
      # #211 (Add support for new web application to view CSEP results)
      output_dir = 'plotOutputDir'
      os.makedirs(output_dir)
      
      try:
         # Copy test results files to the test directory
         result_files = ['cumulative.rTest_L-Test_STEP-fromXML.xml',
                         'cumulative.rTest_N-Test_STEP-fromXML.xml',
                         'cumulative.rTest_R-Test_STEP-fromXML_ETAS-fromXML.xml',
                         'cumulative.rTest_M-Test_ETAS-fromXML.xml',
                         'cumulative.rTest_S-Test_ETAS-fromXML.xml',
                         'intermediate.rTest_L-Test_ebel.aftershock.corrected-fromXML.xml',
                         'intermediate.rTest_N-Test_shen-et-al.geodetic.aftershock-fromXML.xml',
                         'intermediate.rTest_M-Test_wiemer_schorlemmer.alm-fromXML.xml',
                         'intermediate.rTest_S-Test_wiemer_schorlemmer.alm-fromXML.xml',
                         'intermediate.rTest_R-Test_helmstetter-et-al.hkj.aftershock-fromXML_ebel.aftershock-fromXML.xml']
         
         
         for each_file in result_files:
            shutil.copyfile(os.path.join(self.__referenceDataDir, each_file),
                            os.path.join(CSEPTestCase.TestDirPath, each_file))    

            # Extract test type from filename:
            test_type = EvaluationTest.typeFromFilename(each_file)
            
            # Create plot file for the results using classmethod of corresponding
            # EvaluationTest class
            test_class_ref = EvaluationTestFactory().classReference(test_type)

            plot_file = test_class_ref.plotSummary(each_file,
                                                   output_dir)

            ### Validate results - make sure file got generated
            error = "Expected summary plot file '%s' does not exist." %(plot_file)
            self.failIf(os.path.exists(plot_file) == False, error)
            
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
