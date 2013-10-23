"""
Module CutToAreaCatalog
"""

__version__ = "$Revision: 2947 $"
__revision__ = "$Id: CutToAreaCatalog.py 2947 2010-05-27 02:25:41Z liukis $"


import sys, os, unittest, shutil
import numpy as np

import CSEPGeneric, CSEPFile
from Environment import *
from CSEPTestCase import CSEPTestCase


 #--------------------------------------------------------------------
 #
 # Validate that catalog data is cut to the area of interest properly.
 #
class CutToAreaCatalog (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'cutToAreaCatalog')

   
   #--------------------------------------------------------------------
   #
   # This test verifies a fix for ticket #1: catalog data is cut to the geographical area.
   # It verifies result data based on ASCII files.
   #
   def test(self):
      """ Confirm that catalog data is cut to the geographical area."""

      # Setup test name
      CSEPTestCase.setTestName(self, "CutToAreaCatalog")

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)

      
      try:
         # Reference catalog data file for the test
         reference_catalog = os.path.join(self.__referenceDataDir, "catalog.dat")
         area_file = os.path.join(self.__referenceDataDir, "test_area.dat")
         result_catalog = "cut_catalog.dat"

         ### Cut catalog to the area
         np_catalog = CSEPGeneric.Catalog.importZMAP(reference_catalog)
         CSEPGeneric.Catalog.cutToArea(np_catalog, area_file, result_catalog)
   
         ### Validate results
         reference_file = os.path.join(self.__referenceDataDir, 
                                       result_catalog)
         test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                  result_catalog)
         
         error_msg = "CSEPGeneric.Catalog.cutToArea failed."
         self.failIf(CSEPFile.compare(reference_file, test_file) == False, 
                     error_msg)
        
      finally:
         # Go back to the original directory
         os.chdir(cwd)         
      

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
