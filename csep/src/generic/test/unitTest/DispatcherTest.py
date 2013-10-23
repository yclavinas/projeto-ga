"""
Module DispatcherTest
"""

__version__ = "$Revision: 2912 $"
__revision__ = "$Id: DispatcherTest.py 2912 2010-04-16 06:03:45Z liukis $"


import sys, os, unittest, shutil

from Environment import *
from CSEPTestCase import CSEPTestCase
from Dispatcher import Dispatcher
from DispatcherInitFile import DispatcherInitFile
from CSEPOptions import CommandLineOptions


 #--------------------------------------------------------------------
 #
 # Validate that Dispatcher class is working properly.
 #
class DispatcherTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 
                                     'dispatcher')

   
   #--------------------------------------------------------------------
   #
   # This test verifies that Dispatcher raises an exception if
   # configuration file does not exist.
   #
   def testConfigFileExistence(self):
      """ Confirm that exception is raised if configuration \
file does not exist."""

      # Setup test name
      CSEPTestCase.setTestName(self, "DispatcherInitFileExistence")

      ### Validate results
      # Could use self.assertRaises() but will not be able to check 
      # the content of the exception ---> just use try-except block
      try:

         sys.exc_clear()
         del sys.argv[1:]         

         # Simulate command-line arguments
         option = "%s=%s" %(CommandLineOptions.YEAR, CSEPTestCase.Date.year)
         sys.argv.append(option)
         option = "%s=%s" %(CommandLineOptions.MONTH, CSEPTestCase.Date.month)  
         sys.argv.append(option)         
         option = "%s=%s" %(CommandLineOptions.DAY, CSEPTestCase.Date.day)        
         sys.argv.append(option)         
                  
         object = Dispatcher()
         
      except RuntimeError, error:
         self.failIf("Elements of 'forecastFactoryConfigFile' tag are requested \
for non-existent 'dispatcher.init.xml' file" not in error.args[0], 
            "Failed to raise exception of expected content for non-existent file, got exception '%s'"
            %error.args[0])

      except:
         # Unexpected exception is raised:
         error_message = "Unexpected exception is raised: '%s'." \
                         %sys.exc_info()[0]
         self.fail(error_message)


   #--------------------------------------------------------------------
   #
   # This test verifies that Dispatcher raises an exception if
   # top level directory is not specified by configuration file.
   #
   def testRootDirPresence(self):
      """ Confirm that exception is raised if configuration \
file does not specify top level directory."""

      # Setup test name
      CSEPTestCase.setTestName(self, "DispatcherRootDir")

      ### Validate results
      # Could use self.assertRaises() but will not be able to check 
      # the content of the exception ---> just use try-except block
      try:
                 
         sys.exc_clear()
         del sys.argv[1:]         
                  
         # Simulate command-line arguments
         option = "%s=%s" %(CommandLineOptions.YEAR, CSEPTestCase.Date.year)
         sys.argv.append(option)
         option = "%s=%s" %(CommandLineOptions.MONTH, CSEPTestCase.Date.month)  
         sys.argv.append(option)         
         option = "%s=%s" %(CommandLineOptions.DAY, CSEPTestCase.Date.day)        
         sys.argv.append(option)         

         option = "%s=%s" %(CommandLineOptions.CONFIG_FILE, 
                            os.path.join(DispatcherTest.__referenceDataDir,
                                         "dispatcher_no_root_dir.init.xml"))        
         sys.argv.append(option)         
                  
         object = Dispatcher()
         
      except RuntimeError, error:
         expected_string = "'%s' element is missing" \
                           %(DispatcherInitFile.RootDirectoryElement)
         self.failIf(error.args[0].find(expected_string) == -1, 
            "Failed to raise exception of expected content for missing \
root directory element.")

      except:
         # Unexpected exception is raised:
         error_message = "Unexpected exception is raised: '%s'." \
                         %sys.exc_info()[0]

         self.fail(error_message)


   #--------------------------------------------------------------------
   #
   # This test verifies that Dispatcher raises an exception if
   # none of the forecast group directories are specified by
   # configuration file.
   #
   def testForecastGroupPresence(self):
      """ Confirm that exception is raised if configuration \
file does not specify any forecast group directories."""

      # Setup test name
      CSEPTestCase.setTestName(self, "DispatcherForecastGroup")

      ### Validate results
      # Could use self.assertRaises() but will not be able to check 
      # the content of the exception ---> just use try-except block
      try:

         sys.exc_clear()
         del sys.argv[1:]         
         
         # Simulate command-line arguments
         option = "%s=%s" %(CommandLineOptions.YEAR, CSEPTestCase.Date.year)
         sys.argv.append(option)
         option = "%s=%s" %(CommandLineOptions.MONTH, CSEPTestCase.Date.month)  
         sys.argv.append(option)         
         option = "%s=%s" %(CommandLineOptions.DAY, CSEPTestCase.Date.day)        
         sys.argv.append(option)         

         option = "%s=%s" %(CommandLineOptions.CONFIG_FILE, 
                            os.path.join(DispatcherTest.__referenceDataDir,
                                         "dispatcher_no_group.init.xml"))        
         sys.argv.append(option)         
                  
         object = Dispatcher()
         
      except RuntimeError, error:
         expected_string = "At least one '%s' element must be provided" \
                           %(DispatcherInitFile.ForecastGroupElement)
         self.failIf(error.args[0].find(expected_string) == -1, 
            "Failed to raise exception of expected content for missing \
forecast group directory element.")

      except:
         # Unexpected exception is raised:
         error_message = "Unexpected exception is raised: '%s'." \
                         %sys.exc_info()[0]
         self.fail(error_message)


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
