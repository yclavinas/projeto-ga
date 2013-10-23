"""
Module BatchInitFileTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, datetime

import CSEP
from Environment import *
from CSEPTestCase import CSEPTestCase
from BatchInitFile import BatchInitFile
from DispatcherOptionParser import *
from CSEPOptions import CommandLineOptions


 #--------------------------------------------------------------------
 #
 # Validate that BatchInitFile class is working properly.
 #
class BatchInitFileTest (CSEPTestCase):

   # Static data of the class

   # Unit tests use sub-directory of global reference data directory
   __referenceDataFile = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'batchInitFile',
                                     'batch.init.xml')

   __referenceData = {'/data/forecasts/foo/dispatcher.init.xml': 
                      {CommandLineOptions.LOG_FILE : '/foo/reprocess_dispatcher', 
                       'schedule' : [datetime.datetime(2007, 8, 1),
                                     datetime.datetime(2007, 12, 31),
                                     datetime.datetime(2008, 1, 1),
                                     datetime.datetime(2008, 2, 29)]},
                       '/data/forecasts/foo/another_dispatcher.init.xml' :
                      {CommandLineOptions.LOG_FILE : '/foo/reprocess_another_dispatcher', 
                       'schedule' : [datetime.datetime(2008, 1, 1),
                                     datetime.datetime(2008, 2, 1),
                                     datetime.datetime(2008, 3, 1)]}}
   
   
   #--------------------------------------------------------------------
   #
   # This test verifies that BatchInitFile class identifies  
   # element values properly.
   #
   def testElementsValues(self):
      """ Confirm that BatchInitFile identifies elements values properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, "BatchInitFileValues")
   
      init_file = BatchInitFile(BatchInitFileTest.__referenceDataFile)

      ### Validate results
      reference_value = '/batch/top/level/directory'

      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, 
                        init_file.directory)
      self.failIf(init_file.directory != reference_value, 
                  error_message)        
      
      options = init_file.optionsInfo
      reference_value = "publish_user@localhost"  
      
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, 
                        options[CommandLineOptions.PUBLISH_SERVER])
      self.failIf(options[CommandLineOptions.PUBLISH_SERVER] != reference_value, 
                  error_message)        
      
      reference_value = "/publish/dir"  
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, 
                        options[CommandLineOptions.PUBLISH_DIR])
      self.failIf(options[CommandLineOptions.PUBLISH_DIR] != reference_value, 
                  error_message)        

      ### Parse Dispatcher configuration elements
      all_processes = init_file.processInfo


      expected_exec = os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                   'src', 'generic', 'Dispatcher.py')
      for each_entry in all_processes:
                         
         if each_entry.executable != expected_exec:
            error_msg = "Expected '%s' executable, got '%s'" \
                        %each_entry.executable
            self.fail(error_msg)
            
         if each_entry[CommandLineOptions.CONFIG_FILE] not in BatchInitFileTest.__referenceData.keys():
            error_message = "Expected 'process' element with one of '%s' config files" \
                            %BatchInitFileTest.__referenceData.keys()

            self.fail(error_message)
            
         else:
            
            config_file = each_entry[CommandLineOptions.CONFIG_FILE]
            reference_data = BatchInitFileTest.__referenceData[config_file]
            
            # Validate logFile
            error_message = "Expected logFile value of '%s', got '%s'"\
                            %(reference_data[CommandLineOptions.LOG_FILE], 
                              each_entry[CommandLineOptions.LOG_FILE])
            self.failIf(reference_data[CommandLineOptions.LOG_FILE] != 
                        each_entry[CommandLineOptions.LOG_FILE], error_message)

            # Validate schedule
            for each_date in reference_data['schedule']:
               error_message = "Expected %s date within process with %s configuration" \
                               %(each_date, 
                                 each_entry[CommandLineOptions.CONFIG_FILE])
               self.failIf(each_entry.schedule.has(each_date) is False,
                           error_message) 
         

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
