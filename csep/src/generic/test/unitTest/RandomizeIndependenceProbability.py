"""
Module RandomizeIndependenceProbability
"""

__version__ = "$Revision: 3318 $"
__revision__ = "$Id: RandomizeIndependenceProbability.py 3318 2011-05-23 22:04:06Z  $"


import os, unittest, shutil, datetime
import numpy as np

import CSEPGeneric, CSEPFile, CSEP, GeographicalRegions
from CSEPTestCase import CSEPTestCase
from RELMMainshockPostProcess import RELMMainshockPostProcess
from PostProcess import PostProcess
from CSEPLogging import CSEPLogging


#--------------------------------------------------------------------
#
# Validate that Independence Probability column of the catalog is
# randomized according to the rules:
# 1. Get rid of 'zero' values
# 2. Don't use random numbers for events with ''IndependenceProbability'' = '1'
# 3. Leave events with RandomNumber <= IndependenceProbability
#
class RandomizeIndependenceProbability (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 
                                     'randomizeIndependenceProbability')

   
   #--------------------------------------------------------------------
   #
   # Overwrite CSEPTestCase initialization routine for Matlab.
   #
   def initialize(self):
       """ Initialize CSEP environment for the test."""

       CSEPTestCase.initialize(self)
       CSEP.Catalog.NumUncertainties = 1
       
   
   #--------------------------------------------------------------------
   #
   # This test verifies a fix for ticket #19: randomize Independence Probability according
   # to the specified rules.
   # It verifies result data based on ASCII files.
   #
   def test(self):
      """ Confirm that independence probability is randomized according to the rules."""

      # Setup test name
      CSEPTestCase.setTestName(self, "RandomizeIndependenceProbability")

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)

      
      try:
         random_filename = "uncertainty.1-randomSeed.txt"
         
         # Copy random numbers file used by evaluation test to the test directory
         shutil.copyfile(os.path.join(self.__referenceDataDir, random_filename),
                         os.path.join(CSEPTestCase.TestDirPath, random_filename))    

         ### Apply uncertainties to catalog
         np_catalog = CSEPGeneric.Catalog.importZMAP(os.path.join(self.__referenceDataDir, 
                                                                  "catalog.dat"))
                  
         
         filters = PostProcess.Threshold(RELMMainshockPostProcess.MinMagnitude,
                                         RELMMainshockPostProcess.MaxDepth,
                                         datetime.datetime(2006, 1, 1))
         
         # Kludgy way of specifying column index into the data - nothing to
         # do about it while still using Matlab code. 
         independence_probability_column = 15
         result_files = PostProcess.Uncertainties(dir = CSEPTestCase.TestDirPath)
         result_dir = CSEPGeneric.Catalog.modifications(np_catalog, 
                                                        GeographicalRegions.Region.info().testArea,
                                                        filters,
                                                        result_files,
                                                        independence_probability_column)
         
         ### Validate results
         result_catalog = "catalog.uncert.1.dat"
         
         reference_file = os.path.join(self.__referenceDataDir, 
                                       result_catalog)
         test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                  result_catalog)
         
         CSEPLogging.getLogger(RandomizeIndependenceProbability.__name__).info("Comparing reference catalog \
with randomized independence probability file %s with generated catalog file %s" \
                 %(reference_file, test_file))
         
         error_msg = "CSEPGeneric.Catalog.modifications() failed."
         self.failIf(CSEPFile.compare(reference_file, 
                                      test_file,
                                      precision = 1E-10) is False, 
                     error_msg)
        
      finally:
         # Go back to the original directory
         os.chdir(cwd)         
      

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
