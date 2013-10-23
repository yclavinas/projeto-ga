"""
Module BatchProcessingTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, glob, datetime

import CSEPFile, BatchInitFile, BatchProcessing, CSEPTestCase, DispatcherInitFile
from CSEPOptions import CommandLineOptions


 #-------------------------------------------------------------------------------
 #
 # Validate that BatchProcessing class is working properly.
 #
class BatchProcessingTest (CSEPTestCase.CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'batchProcessing')

   
   #-----------------------------------------------------------------------------
   #
   # This test verifies that BatchProcessing class spawns multiple processes in
   # sequence. Configuration parameters for child processes are specified 
   # through 
   #
   def testMultipleProcesses(self):
      """ Confirm that BatchProcessing class spawns multiple processes in a \
sequence."""

      # Setup test name
      CSEPTestCase.CSEPTestCase.setTestName(self, self.id())
      

      # Directory on remote machine to push results plots to
      publish_dir = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                 "publish_results")
      if os.path.exists(publish_dir) is False:
         os.mkdir(publish_dir)
         
      # Copy forecast group directory to the runtime test directory
      group_dir = "forecasts"
      shutil.copytree(os.path.join(BatchProcessingTest.__referenceDataDir, group_dir),
                      os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                   group_dir))
      
      # Copy dispatcher initialization file and replace forecast group 
      # directory with runtime path - it can't be a relative
      # path to the dispatcher's directory
      xmldoc = DispatcherInitFile.DispatcherInitFile(os.path.join(BatchProcessingTest.__referenceDataDir,
                                                                  "dispatcher.init.xml"))
      groups = xmldoc.elements(DispatcherInitFile.DispatcherInitFile.ForecastGroupElement)
      groups[0].text = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                    group_dir)
      
      # Prepend runtime directory path to the dispatcher top-level directory
      dir_path = xmldoc.elements(DispatcherInitFile.DispatcherInitFile.RootDirectoryElement)[0]
      dir_path.text = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                   dir_path.text)
      dir_path.attrib[DispatcherInitFile.DispatcherInitFile.PreProcessedDataDirAttribute] = CSEPTestCase.CSEPTestCase.ReferenceDataDir
      dir_path.attrib[DispatcherInitFile.DispatcherInitFile.RawDataDirAttribute] = CSEPTestCase.CSEPTestCase.ReferenceDataDir
      
      # Write modified file to the test directory
      init_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                               "dispatcher.init.xml")
      
      fhandle = CSEPFile.openFile(init_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      
      # Copy configuration file for batch processing and set publish directory
      # to local to the test sub-directory
      xmldoc = BatchInitFile.BatchInitFile(os.path.join(BatchProcessingTest.__referenceDataDir,
                                                        "batch.init.xml"))
      options_elems = xmldoc.elements(BatchInitFile.BatchInitFile.OptionsInfo.XMLElement)
      
      attribs = options_elems[0].attrib
      attribs['publishDirectory'] = publish_dir
      
      # Specify location of raw catalog data - don't download the file
      attribs['testDir'] = CSEPTestCase.CSEPTestCase.TestDirPath
      options_elems[0].attrib = attribs
      
      # Set log file to the full path of test directory
      config_options = xmldoc.elements(BatchInitFile.BatchInitFile.ProcessInfo.XMLElement)
      
      log_file = config_options[0].attrib['logFile']
      config_options[0].attrib['logFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                         'dispatcher_runs', 'logs', log_file)

      # Prepend test directory as full path to the dispatcher configuration file
      config_file = config_options[0].attrib['configFile']
      config_options[0].attrib['configFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                            config_file)
      
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
            
            
      # Verify that plot files were published to the server
      for test_date in [datetime.datetime(2006, 6, 15), 
                        datetime.datetime(2006, 10, 15)]:
         
         reference_dir = os.path.join(publish_dir, "forecasts", "results",
                                      "%s" %test_date.date())      
         error_msg = "Failed to publish test results to the %s directory" \
                     %reference_dir
         self.failIf(os.path.exists(reference_dir) is False, 
                     error_msg)
         
         command = "%s/*svg*" %reference_dir
         svg_files = glob.glob(command)
         
         error_msg = "No SVG files found for daily test results under %s directory" \
                     %reference_dir
         self.failIf(len(svg_files) == 0, error_msg)
   

   #-----------------------------------------------------------------------------
   #
   # This test verifies a fix for Trac ticket #159: Add ability to re-process
   # file-based forecasts over various time periods in batch mode
   #
   def testFileBasedForecasts(self):
      """ Confirm that file-based forecasts can be processed over various time
      periods in batch mode."""

      # Setup test name
      CSEPTestCase.CSEPTestCase.setTestName(self, self.id())
      

      # Directory on remote machine to push results plots to
      publish_dir = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                 "publish_results")
      if os.path.exists(publish_dir) is False:
         os.mkdir(publish_dir)
         
      # Copy forecast group directory to the runtime test directory
      group_dir = "forecasts"
      shutil.copytree(os.path.join(BatchProcessingTest.__referenceDataDir, group_dir),
                      os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                   group_dir))
      
      # Copy dispatcher initialization file and replace forecast group 
      # directory with runtime path - it can't be a relative
      # path to the dispatcher's directory
      xmldoc = DispatcherInitFile.DispatcherInitFile(os.path.join(BatchProcessingTest.__referenceDataDir,
                                                                  "dispatcher.init.xml"))
      groups = xmldoc.elements(DispatcherInitFile.DispatcherInitFile.ForecastGroupElement)
      groups[0].text = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                                    group_dir)
      
      # Prepend runtime directory path to the dispatcher top-level directory
      dir_path = xmldoc.elements(DispatcherInitFile.DispatcherInitFile.RootDirectoryElement)[0]
      dir_path.text = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                   dir_path.text)
      dir_path.attrib[DispatcherInitFile.DispatcherInitFile.PreProcessedDataDirAttribute] = CSEPTestCase.CSEPTestCase.ReferenceDataDir
      dir_path.attrib[DispatcherInitFile.DispatcherInitFile.RawDataDirAttribute] = CSEPTestCase.CSEPTestCase.ReferenceDataDir
      
      # Write modified file to the test directory
      init_file = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath, 
                               "dispatcher.init.xml")
      
      fhandle = CSEPFile.openFile(init_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      
      # Copy configuration file for batch processing and set publish directory
      # to local to the test sub-directory
      xmldoc = BatchInitFile.BatchInitFile(os.path.join(BatchProcessingTest.__referenceDataDir,
                                                        "batch_file_based.init.xml"))
      options_elems = xmldoc.elements(BatchInitFile.BatchInitFile.OptionsInfo.XMLElement)
      
      attribs = options_elems[0].attrib
      attribs['publishDirectory'] = publish_dir
      
      # Specify location of raw catalog data - don't download the file
      attribs['testDir'] = CSEPTestCase.CSEPTestCase.TestDirPath
      options_elems[0].attrib = attribs
      
      # Set log file to the full path of test directory
      config_options = xmldoc.elements(BatchInitFile.BatchInitFile.ProcessInfo.XMLElement)
      
      for each_config in config_options:
          log_file = each_config.attrib['logFile']
          each_config.attrib['logFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                       'dispatcher_runs', 'logs', log_file)

          # Prepend test directory as full path to the dispatcher configuration file
          config_file = each_config.attrib['configFile']
          each_config.attrib['configFile'] = os.path.join(CSEPTestCase.CSEPTestCase.TestDirPath,
                                                          config_file)
      
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
            
            
      # Verify that plot files were published to the server
      for test_date in [datetime.datetime(2005, 12, 31), 
                        datetime.datetime(2009, 1, 1)]:
         
         reference_dir = os.path.join(publish_dir, "forecasts", "results",
                                      "%s" %test_date.date())      
         error_msg = "Failed to publish test results to the %s directory" \
                     %reference_dir
         self.failIf(os.path.exists(reference_dir) is False, 
                     error_msg)
         
         command = "%s/*svg*" %reference_dir
         svg_files = glob.glob(command)
         
         error_msg = "No SVG files found for daily test results under %s directory" \
                     %reference_dir
         self.failIf(len(svg_files) == 0, error_msg)

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
