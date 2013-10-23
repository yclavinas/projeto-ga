"""
Module GenericDistributionTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, glob, datetime

from Environment import *
from Forecast import Forecast
from CSEPOptions import CommandLineOptions
from ForecastHandlerFactory import ForecastHandlerFactory

import CSEPFile, BatchInitFile, BatchProcessing, CSEP, CSEPTestCase


 #-------------------------------------------------------------------------------
 #
 # Validate that BatchProcessing class is working properly.
 #
class GenericDistributionTest (CSEPTestCase.CSEPTestCase):

   class DataInfo (object):
       
       #========================================================================
       # Initialize object
       # 
       # Inputs:
       #         result_dir - Result directory for the test
       #         result_file_token - List of tokens for result file to search for     
       #========================================================================
       def __init__(self, 
                    result_dir,
                    result_file_token):
           
           self.dir = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                   result_dir)
           
           self.tokens = result_file_token
           
            
   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.CSEPTestCase.ReferenceDataDir, 
                                     'genericDistribution')

   
   #-----------------------------------------------------------------------------
   #
   # This test verifies that EvalutionTest.py module can be invoked in
   # stand-alone mode. 
   #
   def testEvalutionTestModuleWithMatlabForecast(self):
      """ Confirm that EvaluationTest.py module can be invoked in stand-alone \
mode to evaluate forecasts provided in Matlab format."""

      # Setup test name
      CSEPTestCase.CSEPTestCase.setTestName(self, 
                                            self.id())
      

      # Create forecast group directory under runtime test directory
      group_dir = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                               "testForecasts")
      os.makedirs(group_dir)

      # Copy 2 (R-Test requires 2 forecasts) forecasts into test runtime directory
      forecast_file = 'ebel.aftershock.mat'
      shutil.copyfile(os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                   'data',
                                   'forecasts',
                                   'RELMMainshockAftershock',
                                   forecast_file),
                      os.path.join(group_dir, 
                                   forecast_file))

      forecast_file = 'bird_liu.neokinema.mat'
      shutil.copyfile(os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                   'data',
                                   'forecasts',
                                   'RELMMainshockAftershock',
                                   forecast_file),
                      os.path.join(group_dir, 
                                   forecast_file))
      
      # Create observation catalog directory under runtime test directory
      catalog_dir = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                 "testResults")
      shutil.copytree(os.path.join(GenericDistributionTest.__referenceDataDir,
                                   'catalogs',
                                   'RELMAftershock'),
                      catalog_dir) 
      
      
      # Copy configuration file for batch processing and set runtime directories
      xmldoc = BatchInitFile.BatchInitFile(os.path.join(GenericDistributionTest.__referenceDataDir,
                                                        "batch_matlab.init.xml"))
      
      for each_process in xmldoc.elements(BatchInitFile.BatchInitFile.ProcessInfo.XMLElement):
          process_attribs = each_process.attrib
          process_attribs['testDir'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['testDir'])

          process_attribs['forecasts'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                      process_attribs['forecasts'])

          process_attribs['logFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['logFile'])

          ### Create observation catalog directory under runtime test results directory
          shutil.copytree(os.path.join(GenericDistributionTest.__referenceDataDir,
                                       'catalogs',
                                       'RELMAftershock'),
                          process_attribs['testDir']) 
      
      # Write modified file to the test directory
      batch_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                "batch.init.xml")
      
      fhandle = CSEPFile.openFile(batch_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      
      
      cwd = os.getcwd() 
      os.chdir(CSEPTestCase.CSEPTestCase.TestDirPath)
      
      try:
         
         # Clear exceptions generated by other unit tests
         sys.exc_clear()
         del sys.argv[1:]
         
         # Simulate command-line arguments
         option = "%s=%s" %(CommandLineOptions.CONFIG_FILE, 
                            batch_file)
         sys.argv.append(option)
                  
         batch_obj = BatchProcessing.BatchProcessing()
         batch_obj.run()
         
      finally:
            os.chdir(cwd)
            

      # Test date is used as test identifier - unique per each test
      __resultData = {datetime.datetime(2009, 7, 1) : GenericDistributionTest.DataInfo('NTestForecast',
                                                                                       ['rTest_N-Test_ebel.aftershock',
                                                                                        'rTest_N-Test_bird_liu.neokinema']),
                      datetime.datetime(2009, 7, 2) : GenericDistributionTest.DataInfo('LTestForecast',
                                                                                       ['rTest_L-Test_ebel.aftershock',
                                                                                        'rTest_L-Test_bird_liu.neokinema']),
                      datetime.datetime(2009, 7, 3) : GenericDistributionTest.DataInfo('RTestForecast',
                                                                                       ['rTest_R-Test_bird_liu.neokinema_ebel.aftershock']),
                      datetime.datetime(2009, 7, 4) : GenericDistributionTest.DataInfo('MTestForecast',
                                                                                       ['rTest_M-Test_ebel.aftershock',
                                                                                        'rTest_M-Test_bird_liu.neokinema']),
                      datetime.datetime(2009, 7, 5) : GenericDistributionTest.DataInfo('STestForecast',
                                                                                       ['rTest_S-Test_ebel.aftershock',
                                                                                        'rTest_S-Test_bird_liu.neokinema'])}
            
      # Verify that test results and corresponding plot files are generated
      for test_date, result_data in __resultData.items(): 
         
         for each_token in result_data.tokens:
             
             command = "%s/*%s.xml*" %(result_data.dir, 
                                       each_token)
             xml_files = glob.glob(command)
             
    
             error_msg = "Failed to generate test results %s" \
                         %command 
             self.failIf(len(xml_files) == 0, 
                         error_msg)
             
             command = "%s/*%s.svg*" %(result_data.dir, 
                                       each_token)
             svg_files = glob.glob(command)
             
             error_msg = "Failed to generate SVG plots %s" \
                         %command
             self.failIf(len(svg_files) == 0, error_msg)
   

   #-----------------------------------------------------------------------------
   #
   # This test verifies that EvalutionTest.py module can be invoked in
   # stand-alone mode. 
   #
   def testEvalutionTestModuleWithXMLForecast(self):
      """ Confirm that EvaluationTest.py module can be invoked in stand-alone \
mode to evaluate forecasts provided in XML format."""

      # Setup test name
      CSEPTestCase.CSEPTestCase.setTestName(self, 
                                            self.id())
      

      # Create forecast group directory under runtime test directory
      group_dir = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                               "testForecasts")
      os.makedirs(group_dir)

      # Copy 2 (R-Test requires 2 forecasts) forecasts into test runtime directory
      for forecast_file in ('ebel.aftershock.xml', 'bird_liu.neokinema.xml'):
          shutil.copyfile(os.path.join(GenericDistributionTest.__referenceDataDir,
                                       forecast_file),
                          os.path.join(group_dir, 
                                       forecast_file))

      # Create observation catalog directory under runtime test directory
      catalog_dir = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                 "testResults")
      shutil.copytree(os.path.join(GenericDistributionTest.__referenceDataDir,
                                   'catalogs',
                                   'RELMAftershock'),
                      catalog_dir) 
      
      
      # Copy configuration file for batch processing and set runtime directories
      xmldoc = BatchInitFile.BatchInitFile(os.path.join(GenericDistributionTest.__referenceDataDir,
                                                        "batch_xml.init.xml"))
      
      for each_process in xmldoc.elements(BatchInitFile.BatchInitFile.ProcessInfo.XMLElement):
          process_attribs = each_process.attrib
          process_attribs['testDir'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['testDir'])

          process_attribs['forecasts'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                      process_attribs['forecasts'])

          process_attribs['logFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['logFile'])

          if 'catalog' in process_attribs:
              process_attribs['catalog'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                        process_attribs['catalog'])

          ### Create observation catalog directory under runtime test results directory
          shutil.copytree(os.path.join(GenericDistributionTest.__referenceDataDir,
                                       'catalogs',
                                       'RELMAftershock'),
                          process_attribs['testDir']) 
      
      # Write modified file to the test directory
      batch_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                "batch.init.xml")
      
      fhandle = CSEPFile.openFile(batch_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      
      
      cwd = os.getcwd() 
      os.chdir(CSEPTestCase.CSEPTestCase.TestDirPath)
      
      try:
         
         # Clear exceptions generated by other unit tests
         sys.exc_clear()
         del sys.argv[1:]
         
         # Simulate command-line arguments
         option = "%s=%s" %(CommandLineOptions.CONFIG_FILE, 
                            batch_file)
         sys.argv.append(option)
                  
         batch_obj = BatchProcessing.BatchProcessing()
         batch_obj.run()
         
      finally:
            os.chdir(cwd)
            

      # Test date is used as test identifier - unique per each test
      __resultData = {datetime.datetime(2009, 7, 1) : GenericDistributionTest.DataInfo('NTestForecast',
                                                                                       ['rTest_N-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_N-Test_bird_liu.neokinema-fromXML']),
                      datetime.datetime(2009, 7, 2) : GenericDistributionTest.DataInfo('LTestForecast',
                                                                                       ['rTest_L-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_L-Test_bird_liu.neokinema-fromXML']),
                      datetime.datetime(2009, 7, 3) : GenericDistributionTest.DataInfo('RTestForecast',
                                                                                       ['rTest_R-Test_bird_liu.neokinema-fromXML_ebel.aftershock-fromXML']),
                      datetime.datetime(2009, 7, 4) : GenericDistributionTest.DataInfo('MTestForecast',
                                                                                       ['rTest_M-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_M-Test_bird_liu.neokinema-fromXML']),
                      datetime.datetime(2009, 7, 5) : GenericDistributionTest.DataInfo('STestForecast',
                                                                                       ['rTest_S-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_S-Test_bird_liu.neokinema-fromXML']),
                      datetime.datetime(2009, 7, 1) : GenericDistributionTest.DataInfo('NTestForecastManualSettings',
                                                                                       ['rTest_N-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_N-Test_bird_liu.neokinema-fromXML']),
                      datetime.datetime(2009, 7, 2) : GenericDistributionTest.DataInfo('LTestForecastManualSettings',
                                                                                       ['rTest_L-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_L-Test_bird_liu.neokinema-fromXML']),
                      datetime.datetime(2009, 7, 3) : GenericDistributionTest.DataInfo('RTestForecastManualSettings',
                                                                                       ['rTest_R-Test_bird_liu.neokinema-fromXML_ebel.aftershock-fromXML']),
                      datetime.datetime(2009, 7, 4) : GenericDistributionTest.DataInfo('MTestForecastManualSettings',
                                                                                       ['rTest_M-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_M-Test_bird_liu.neokinema-fromXML']),
                      datetime.datetime(2009, 7, 5) : GenericDistributionTest.DataInfo('STestForecastManualSettings',
                                                                                       ['rTest_S-Test_ebel.aftershock-fromXML',
                                                                                        'rTest_S-Test_bird_liu.neokinema-fromXML'])}
            
      # Verify that test results and corresponding plot files are generated
      for test_date, result_data in __resultData.items(): 
         
         for each_token in result_data.tokens:
             
             command = "%s/*%s.xml*" %(result_data.dir, 
                                       each_token)
             xml_files = glob.glob(command)
             
    
             error_msg = "Failed to generate test results %s" \
                         %command 
             self.failIf(len(xml_files) == 0, 
                         error_msg)
             
             command = "%s/*%s.svg*" %(result_data.dir, 
                                       each_token)
             svg_files = glob.glob(command)
             
             error_msg = "Failed to generate SVG plots %s" \
                         %command
             self.failIf(len(svg_files) == 0, error_msg)


   #-----------------------------------------------------------------------------
   #
   # This test verifies that ForecastGroup.py module can be invoked in
   # stand-alone mode to generate forecast map
   #
   def testGeographicalRegionsMapGeneration(self):
      """ Confirm that GeographicalRegions.py module can be invoked in \
stand-alone mode to generate forecast map."""

      # Setup test name
      CSEPTestCase.CSEPTestCase.setTestName(self, 
                                            self.id())
      

      # Copy configuration file for batch processing and set runtime directories
      xmldoc = BatchInitFile.BatchInitFile(os.path.join(GenericDistributionTest.__referenceDataDir,
                                                        "batch_region_maps.init.xml"))
      
      for each_process in xmldoc.elements(BatchInitFile.BatchInitFile.ProcessInfo.XMLElement):
          process_attribs = each_process.attrib
          
          process_attribs['testDir'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['testDir'])
          
          process_attribs['logFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['logFile'])
          

      # Write modified file to the test directory
      batch_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                "batch.init.xml")
      
      fhandle = CSEPFile.openFile(batch_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      
      
      cwd = os.getcwd() 
      os.chdir(CSEPTestCase.CSEPTestCase.TestDirPath)
      
      try:
         
         # Clear exceptions generated by other unit tests
         sys.exc_clear()
         del sys.argv[1:]
         
         # Simulate command-line arguments
         option = "%s=%s" %(CommandLineOptions.CONFIG_FILE, 
                            batch_file)
         sys.argv.append(option)
                  
         batch_obj = BatchProcessing.BatchProcessing()
         batch_obj.run()
         
      finally:
            os.chdir(cwd)
            
            
      # Test date is used as test identifier - unique per each test
      __resultMapDirs = ['CaliforniaMap',
                         'CaliforniaMapWithCatalog',
                         'NWPacificMap',
                         'SWPacificMap']
            
            
      # Verify that test results and corresponding plot files are generated
      for each_dir in __resultMapDirs: 
         
         command = "%s/*.png*" %os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                             each_dir) 
         plot_files = glob.glob(command)
         

         error_msg = "Failed to generate PNG map %s" \
                     %command 
         self.failIf(len(plot_files) == 0, 
                     error_msg)


   #-----------------------------------------------------------------------------
   #
   # This test verifies that ForecastGroup.py module can be invoked in
   # stand-alone mode to magnitude distribution plots of the forecasts
   #
   def testMagnitudeDistributionPlots(self):
      """ Confirm that ForecastGroup.py module can be invoked in stand-alone \
mode to generate forecast magnitude distribution plots."""

      # Setup test name
      CSEPTestCase.CSEPTestCase.setTestName(self, 
                                            self.id())
      

      # Copy configuration file for batch processing and set runtime directories
      xmldoc = BatchInitFile.BatchInitFile(os.path.join(GenericDistributionTest.__referenceDataDir,
                                                        "batch_magnitude_plots.init.xml"))
      
      for each_process in xmldoc.elements(BatchInitFile.BatchInitFile.ProcessInfo.XMLElement):
          
          process_attribs = each_process.attrib

          process_attribs['testDir'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['testDir'])
          
          process_attribs['logFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                    process_attribs['logFile'])


      # Write modified file to the test directory
      batch_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                "batch.init.xml")
      
      fhandle = CSEPFile.openFile(batch_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      
      
      cwd = os.getcwd() 
      os.chdir(CSEPTestCase.CSEPTestCase.TestDirPath)
      
      try:
         
         # Create directory for  
         
         # Clear exceptions generated by other unit tests
         sys.exc_clear()
         del sys.argv[1:]
         
         # Simulate command-line arguments
         option = "%s=%s" %(CommandLineOptions.CONFIG_FILE, 
                            batch_file)
         sys.argv.append(option)
                  
         batch_obj = BatchProcessing.BatchProcessing()
         batch_obj.run()
         
      finally:
            os.chdir(cwd)
            
            
      # Verify that requested plot for the forecast was generated
      forecast_file = 'ebel.aftershock.dat'
      result_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                 'magnitudeDistributionPlot',
                                 "%s%s%s" %(Forecast.MagnitudeDistributionPrefix,
                                            CSEPFile.Name.extension(forecast_file),
                                            CSEPFile.Extension.SVG))

      error_msg = "Failed to generate expected forecast format %s" \
                  %result_file 
      self.failIf(os.path.exists(result_file) is False, 
                  error_msg)


   #----------------------------------------------------------------------------
   #
   # This test verifies that ForecastHandlerFactory.py module can be invoked in
   # stand-alone mode to convert forecasts: ASCII to XML, XML to ASCII format
   #
   def testASCIIXMLConversions(self):
      """ Confirm that ForecastHandlerFactory.py module can be invoked in stand-alone \
mode to apply forecasts conversions: ASCII to XML, XML to ASCII format."""

      # Setup test name
      CSEPTestCase.CSEPTestCase.setTestName(self, 
                                            self.id())
      
      # Create forecast group directory under runtime test directory
      __group_dirs = {os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                   "testASCIIToXML") : (os.path.join(GenericDistributionTest.__referenceDataDir,
                                                                     'ebel.aftershock.dat'),
                                                        'ebel.aftershock.xml'),
                                                        
                      os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                   "testXMLToASCII") : (os.path.join(GenericDistributionTest.__referenceDataDir,
                                                                     'ebel.aftershock.xml'),
                                                        'ebel.aftershock-fromXML.dat')}
      
      for group_dir, forecast_file in __group_dirs.iteritems():
          os.makedirs(group_dir)
    
          # Copy forecast into test runtime directory
          shutil.copyfile(forecast_file[0],
                          os.path.join(group_dir, 
                                       os.path.basename(forecast_file[0])))
      
      cwd = os.getcwd() 
      os.chdir(CSEPTestCase.CSEPTestCase.TestDirPath)
      
      try:

         ### Invoke ASCII to XML conversion
         test_dir = 'testXMLToASCII'
         forecast_file = 'ebel.aftershock.xml'
         dest_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                  test_dir, 
                                  forecast_file) 
         
         model = ForecastHandlerFactory().CurrentHandler.XML(dest_file)
         result_file = model.toASCII() 

         self.failIf(os.path.exists(result_file) is False,
                     'testASCIIToXML: failed to generate expected %s file' %result_file)

         
         ### Invoke XML to ASCII conversion
         test_dir = 'testASCIIToXML'
         forecast_file = 'ebel.aftershock.dat'
         dest_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                  test_dir, 
                                  forecast_file) 
         
         xml_template = os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                     'data/templates/csep-forecast-template-M5.xml')
         start_date = datetime.datetime(2006, 1, 1)
         end_date = datetime.datetime(2011, 1, 1)
         
         template = ForecastHandlerFactory().CurrentHandler.XML(xml_template)
         result_file = template.toXML(dest_file, 
                                      start_date, 
                                      end_date,
                                      forecast_file)
         
         self.failIf(os.path.exists(result_file) is False,
                     'testXMLToASCII: failed to generate expected %s file' %result_file)
         
      finally:
            os.chdir(cwd)
            

# Invoke the module
if __name__ == '__main__':

   import logging
   
   
   # Invoke all tests
   unittest.main()
        
   # Shutdown logging
   logging.shutdown()

# end of main
