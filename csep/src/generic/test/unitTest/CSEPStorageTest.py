"""
Module CSEPStorageTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, datetime

import CSEP
from CSEPStorage import CSEPStorage
from ForecastGroup import ForecastGroup
from CSEPTestCase import CSEPTestCase


#--------------------------------------------------------------------
#
# Validate that CSEPStorage class is working properly.
#
class CSEPStorageTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'storage')

   
   #-----------------------------------------------------------------------------
   #
   # This test verifies that CSEPStorage class identifies archived observation
   # catalog files properly, and stages it for the current processing using
   # their original filenames.
   #
   def testCatalogStorage(self):
      """ Confirm that CSEPStorage identifies archived observation catalog \
files properly, and stages them for current processing using their original \
filenames."""

      # Setup test name
      CSEPTestCase.setTestName(self, "CatalogStorage")

      # Copy reference files to the test directory
      catalog_dir = 'catalogs'
      shutil.copytree(os.path.join(self.__referenceDataDir, catalog_dir),
                      os.path.join(CSEPTestCase.TestDirPath, catalog_dir))

      cwd = os.getcwd() 
      os.chdir(os.path.join(CSEPTestCase.TestDirPath, catalog_dir))
      
      catalog_files = {'catalog.nodecl.mat': 'scec.csep.Catalog.OneDayModel-catalog.nodecl.mat.1199394557.702523.4',
                       'catalog.nodecl.dat': 'scec.csep.Catalog.OneDayModel-catalog.nodecl.mat.1199394557.686092.2', 
                       'catalog.modifications.mat': 'scec.csep.Catalog.OneDayModel-catalog.nodecl.mat.1199394557.694214.3'}
      
      try:
         
         storage = CSEPStorage('.')
         storage.stage(catalog_files.keys())
         
         ### Validate results
         for entry in catalog_files.keys():
            
            self.failIf(os.path.exists(entry) is False,
                        "Expected '%s' link does not exist." %entry)
            
            # Check that entry is a soft link to the expected data file
            result_path = os.path.join(CSEPTestCase.TestDirPath,
                                       catalog_dir,
                                       catalog_files[entry])
            
            self.failIf(result_path != os.path.realpath(entry),
                        "Expected '%s' link is not pointing to the expected '%s' file." \
                        %(result_path, os.path.realpath(entry)))
            
      finally:
         
         os.chdir(cwd)
      

   #-----------------------------------------------------------------------------
   #
   # This test verifies that CSEPStorage class identifies archived forecast
   # files properly, and stages it for the current processing using
   # their original filenames.
   #
   def testForecastStorage(self):
      """ Confirm that CSEPStorage identifies archived forecast \
files properly, and stages them for current processing using their original \
filenames."""

      # Setup test name
      CSEPTestCase.setTestName(self, "ForecastStorage")

      # Copy reference files to the test directory
      reference_dir = 'forecast_group'
      shutil.copytree(os.path.join(self.__referenceDataDir, reference_dir),
                      os.path.join(CSEPTestCase.TestDirPath, reference_dir))

      cwd = os.getcwd() 
      os.chdir(os.path.join(CSEPTestCase.TestDirPath))
      
      forecasts_files = ['BogusForecastModel1_2_5_2008.dat', 
                         'BogusForecastModel1_2_5_2008-fromXML.dat']
      
      save_enable_xml_template = CSEP.Forecast.UseXMLMasterTemplate
      
      try:

         CSEP.Forecast.UseXMLMasterTemplate = True
         
         # Catalog directory should not be used since files are staged 
         # and not created by model invokation
         catalog_dir = '.' 
         group = ForecastGroup(os.path.join(CSEPTestCase.TestDirPath,
                                            reference_dir))
         # Trigger file staging         
         group.create(datetime.datetime(2008, 2, 5),
                      catalog_dir)

         original_data_dir = os.path.join(reference_dir,
                                          'forecasts',
                                          'archive',
                                          '2008_2')
         
         ### Validate results
         for entry in forecasts_files:
            
            entry_path = os.path.join(CSEPTestCase.TestDirPath,
                                      reference_dir,
                                      'forecasts',
                                      entry)
            self.failIf(os.path.exists(entry_path) is False,
                        "Expected '%s' link does not exist." %entry_path)
            
            # Check that entry is a soft link to the expected data file
            result_path = os.path.join(CSEPTestCase.TestDirPath,
                                       original_data_dir,
                                       entry)
            
            self.failIf(result_path != os.path.realpath(entry_path),
                        "Expected '%s' link is not pointing to the expected '%s' file." \
                        %(entry_path, result_path))
            
      finally:
         
         os.chdir(cwd)
         CSEP.Forecast.UseXMLMasterTemplate = save_enable_xml_template
      

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
