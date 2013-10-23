"""
Module CatalogPreProcessing
"""

__version__ = "$Revision: 3643 $"
__revision__ = "$Id: CatalogPreProcessing.py 3643 2012-02-24 19:37:07Z liukis $"


import os, unittest, shutil, filecmp, datetime
import numpy as np

import CSEPGeneric
from CSEPTestCase import CSEPTestCase
from RELMCatalog import RELMCatalog
from CatalogDataSource import CatalogDataSource
from CMTDataSource import CMTDataSource
from ANSSDataSource import ANSSDataSource
from CSEPLogging import CSEPLogging


 #--------------------------------------------------------------------
 #
 # Test pre-processing of the catalog data.
 #
class CatalogPreProcessing (CSEPTestCase):
    
    # Test uses sub-directory of global reference data directory
    __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                       'preProcess')

    # Filename to store raw CMT catalog data
    RawFileCMT = "import_raw_cmt.dat"
	
    # Filename to store pre-processed catalog data
    PreProcessedFileCMT = "import_processed_cmt.dat"

    # Flag if raw catalog data should be downloaded
    __downloadRawData = False
    

    #----------------------------------------------------------------------------
    #
    # Test pre-processing of raw ANSS catalog data and evaluate generated filtered 
    # catalog.
    #
    def testANSSDataSource(self):
        """ Test pre-processing of raw catalog data and succeed. \
(the result catalog is in so-called ZMAP-format)."""
   
        # Setup test name
        CSEPTestCase.setTestName(self, self.id())
   
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        data_start_date = datetime.datetime(1985, 1, 1)
        data_source = ANSSDataSource(data_start_date, 
                                     CatalogPreProcessing.__downloadRawData)
        data_source.RawFile = os.path.join(CSEPTestCase.TestDirPath,
                                           CatalogDataSource._RawFile)
        
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        # Copy reference raw data file to the test directory
        shutil.copyfile(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     CatalogDataSource._RawFile),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     CatalogDataSource._RawFile))

        # Pass test directory with already existing raw data to be used by the 
        # test   
        catalog.create(CSEPTestCase.Date,
                       CSEPTestCase.TestDirPath)
        
        test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                 CatalogDataSource.PreProcessedFile)
        
        result_file = os.path.join(CatalogPreProcessing.__referenceDataDir,
                                   CatalogDataSource.PreProcessedFile)
        
        CSEPLogging.getLogger(CatalogPreProcessing.__name__).info(
           "Comparing reference catalog file %s to generated ANSS catalog file %s..." \
           %(result_file, test_file))

        self.failIf(filecmp.cmp(result_file, test_file) == False, 
                    'Catalog pre-processing failed.')


    #----------------------------------------------------------------------------
    #
    # Test fix for Trac ticket #114: pre-processing of raw ANSS catalog events
    # that have missing depth values sets:
    # depth value to 7.5 km
    # parses time of the event correctly (before would be set to 00:00:00) 
    #
    def testANSSDataSourceMissingDepth(self):
        """ Test pre-processing of raw catalog events with missing depth values and succeed. \
Missing depth value should be set to 7.5km, and time of the event should be parsed correctly."""
   
        # Setup test name
        CSEPTestCase.setTestName(self, self.id())
   
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        data_start_date = datetime.datetime(1932, 1, 1)
        data_source = ANSSDataSource(data_start_date, 
                                     CatalogPreProcessing.__downloadRawData)
        data_source.RawFile = os.path.join(CSEPTestCase.TestDirPath,
                                           CatalogDataSource._RawFile)
        
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        # Copy reference raw data file to the test directory
        shutil.copyfile(os.path.join(CatalogPreProcessing.__referenceDataDir, 
                                     'import_raw.1932.dat'),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     CatalogDataSource._RawFile))

        # Pass test directory with already existing raw data to be used by the 
        # test   
        catalog.create(CSEPTestCase.Date,
                       CSEPTestCase.TestDirPath)
        
        test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                 CatalogDataSource.PreProcessedFile)
        
        result_file = os.path.join(CatalogPreProcessing.__referenceDataDir,
                                   'import_processed.1932.dat')
        
        CSEPLogging.getLogger(CatalogPreProcessing.__name__).info(
           "Comparing reference catalog file %s to generated ANSS catalog file %s..." \
           %(result_file, test_file))

        self.failIf(filecmp.cmp(result_file, test_file) == False, 
                    'Catalog pre-processing of missing depth values failed.')



    #----------------------------------------------------------------------------
    #
    # Test pre-processing of raw CMT catalog data and evaluate generated filtered 
    # catalog.
    #
    def testCMTDataSource(self):
        """ Test pre-processing of raw  cmt catalog data and succeed \
(the result catalog is in 1 line format)."""
        
        # Setup test name
        CSEPTestCase.setTestName(self, self.id())
        
        data_start_date = datetime.datetime(1977, 1, 1)
        input_args = 'includePreliminary=True'

        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        data_source = CMTDataSource(data_start_date,
                                    CatalogPreProcessing.__downloadRawData,
                                    args=input_args)
        data_source.RawFile = os.path.join(CSEPTestCase.TestDirPath,
                                           CatalogDataSource._RawFile)

        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        # Copy reference raw data file to the test directory
        shutil.copyfile(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     CatalogPreProcessing.RawFileCMT),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     CatalogDataSource._RawFile))
   
        catalog.create(CSEPTestCase.Date,
                       CSEPTestCase.TestDirPath)
        
        test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                 CatalogDataSource.PreProcessedFile)
        
        result_file = os.path.join(CatalogPreProcessing.__referenceDataDir,
                                   self.PreProcessedFileCMT)
        
        CSEPLogging.getLogger(CatalogPreProcessing.__name__).info(
           "Comparing reference catalog file %s to generated CMT catalog file %s..." \
           %(result_file, test_file))

        self.failIf(filecmp.cmp(result_file, test_file) == False, 
                    'Catalog pre-processing failed.')


    #----------------------------------------------------------------------------
    #
    # Test a fix for Trac ticket #140: CMT scalar magnitude moment is
    # pre-processed to the value with 2 significant digits while it's provided 
    # with 3 significant digits in raw catalog
    #
    def testCMTDataSourceTracTicket140(self):
        """ Test a fix for Trac ticket #140: CMT scalar moment magnitude should \
be provided with 3 significant digits in pre-processed catalog."""
        
        # Setup test name
        CSEPTestCase.setTestName(self, self.id())
        
        data_start_date = datetime.datetime(1977, 1, 1)
        input_args = 'includePreliminary=True'

        data_source = CMTDataSource(data_start_date,
                                    CatalogPreProcessing.__downloadRawData,
                                    args=input_args)
        data_source.RawFile = os.path.join(CSEPTestCase.TestDirPath,
                                           CatalogDataSource._RawFile)

        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        # Copy reference raw data file to the test directory
        shutil.copyfile(os.path.join(CatalogPreProcessing.__referenceDataDir, 
                                     'import_raw_CMT_Trac140.dat'),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     CatalogDataSource._RawFile))
   
        catalog.create(CSEPTestCase.Date,
                       CSEPTestCase.TestDirPath)
        
        test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                 CatalogDataSource.PreProcessedFile)
        
        result_file = os.path.join(CatalogPreProcessing.__referenceDataDir,
                                   'import_processed_CMT_Trac140.dat')
        
        CSEPLogging.getLogger(CatalogPreProcessing.__name__).info(
           "Comparing reference catalog file %s to generated CMT catalog file %s..." \
           %(result_file, test_file))

        self.failIf(filecmp.cmp(result_file, test_file) == False, 
                    'Catalog pre-processing failed.')
	

    #----------------------------------------------------------------------------
    #
    # Test a fix for Trac ticket #187: Negative centroid time offset 
    # relative to 00:00 seconds in CMT raw catalog results in invalid time
    #
    def testCMTDataSourceTracTicket187(self):
        """ Test a fix for Trac ticket #187: Negative centroid time offset \
relative to 00:00 seconds in CMT raw catalog results in invalid time."""
        
        # Setup test name
        CSEPTestCase.setTestName(self, self.id())
        
        data_start_date = datetime.datetime(1977, 1, 1)
        input_args = 'includePreliminary=True'

        data_source = CMTDataSource(data_start_date,
                                    CatalogPreProcessing.__downloadRawData,
                                    args=input_args)
        data_source.RawFile = os.path.join(CSEPTestCase.TestDirPath,
                                           CatalogDataSource._RawFile)

        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        # Copy reference raw data file to the test directory
        shutil.copyfile(os.path.join(CatalogPreProcessing.__referenceDataDir, 
                                     'import_raw_CMT_Trac187.dat'),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     CatalogDataSource._RawFile))
   
        catalog.create(CSEPTestCase.Date,
                       CSEPTestCase.TestDirPath)
        
        test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                 CatalogDataSource.PreProcessedFile)
        
        result_file = os.path.join(CatalogPreProcessing.__referenceDataDir,
                                   'import_processed_CMT_Trac187.dat')
        
        CSEPLogging.getLogger(CatalogPreProcessing.__name__).info(
           "Comparing reference catalog file %s to generated CMT catalog file %s..." \
           %(result_file, test_file))

        self.failIf(filecmp.cmp(result_file, test_file) == False, 
                    'Catalog pre-processing failed.')
	
    
    #----------------------------------------------------------------------------
    #
    # Test import of filtered raw catalog data of over one million events into
    # Matlab format, and check for existence of imported catalog file.
    #
    def testImportOfMillionEvents(self):
        """ Test import of over one million events into Matlab format \
(the result catalog is in so-called ZMAP-format)."""
   
        # Setup test name
        CSEPTestCase.setTestName(self, self.id())

        # Import catalog data into Matlab format
        result_file = os.path.join(CSEPTestCase.TestDirPath, 
                                   'import.mat')
        
        ANSSDataSource.importToCSEP(os.path.join(CatalogPreProcessing.__referenceDataDir, 
                                                  "import_processed_1million.dat"), 
                                     result_file)
                
        self.failIf(os.path.exists(result_file) == False, 
                    'Import of catalog with one million events failed.')
        

# Invoke the module
if __name__ == '__main__':

   # Invoke all tests - must have testXXX method in the class defined
   unittest.main()
   
   #runner = unittest.TextTestRunner()
   #runner.run(TestSuite())   
        
# end of main
