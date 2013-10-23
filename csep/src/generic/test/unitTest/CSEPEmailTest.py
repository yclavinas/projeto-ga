"""
Module CSEPEmailTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest

from CSEPTestCase import CSEPTestCase
from CSEPInitFile import CSEPInitFile
from CSEPEmail import CSEPEmail


 #-------------------------------------------------------------------------------
 #
 # Validate that CSEPEmail class is working properly.
 #
class CSEPEmailTest (CSEPTestCase):

   # Static data of the class

   # Unit tests use sub-directory of global reference data directory
   __referenceDataFile = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'email',
                                     'config.init.xml')

   
   #-----------------------------------------------------------------------------
   #
   # This test verifies that DispatcherInitFile class identifies CSEPEmail class 
   # element values properly.
   #
   def testElementsValues(self):
      """ Confirm that configuration file identifies CSEPEmail class\
elements values properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, "CSEPEmailValues")
   
      init_file = CSEPInitFile(CSEPEmailTest.__referenceDataFile)

      ### Validate results
      email_info = init_file.elements(CSEPEmail.Element)[0]    
      
      hostname = email_info.attrib[CSEPEmail.HostAttribute]
      reference_value = 'host.domain'
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, hostname)
      self.failIf(hostname != reference_value, error_message)        

      fromaddr = email_info.attrib[CSEPEmail.FromAttribute]
      reference_value = 'foo@domain'
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, fromaddr)
      self.failIf(fromaddr != reference_value, error_message)        
      
      user = email_info.attrib[CSEPEmail.UserAttribute]
      reference_value = 'foouser'
      error_message = "Expected '%s' value, got '%s'." %(reference_value, user)
      self.failIf(user != reference_value, error_message)        
      
      password = email_info.attrib[CSEPEmail.PasswordAttribute]
      reference_value = 'foo'
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, password)
      self.failIf(password != reference_value, error_message)        
      
      email_addrs = init_file.elementValue(CSEPEmail.Element).split()
      
      reference_value = ['user1@domain', 'user2@domain']
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, email_addrs)
      self.failIf(email_addrs != reference_value, error_message)        

      subject = email_info.attrib[CSEPEmail.SubjectPrefixAttribute]
      reference_value = 'Some foo tests'
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, subject)
      self.failIf(subject != reference_value, error_message)        
   
      subject_from = email_info.attrib[CSEPEmail.SubjectFromAttribute]
      reference_value = 'FromFooProcess'
      error_message = "Expected '%s' value, got '%s'." \
                      %(reference_value, subject_from)
      self.failIf(subject_from != reference_value, error_message)        


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
