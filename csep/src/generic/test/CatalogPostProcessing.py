"""
Module CatalogPostProcessing
"""

__version__ = "$Revision: 3425 $"
__revision__ = "$Id: CatalogPostProcessing.py 3425 2011-08-04 22:58:54Z liukis $"


import sys, os, unittest, shutil, datetime, filecmp

import CSEPFile, CSEP, ANSSDataSource, CMTDataSource, \
       GeographicalRegions

from CSEPTestCase import CSEPTestCase
from RELMCatalog import RELMCatalog
from CatalogDataSource import CatalogDataSource
from DataSourceFactory import DataSourceFactory
from RELMAftershockPostProcess import RELMAftershockPostProcess
from RELMMainshockPostProcess import RELMMainshockPostProcess
from OneDayModelPostProcess import OneDayModelPostProcess
from OneDayModelInputPostProcess import OneDayModelInputPostProcess
from ThreeMonthsModelPostProcess import ThreeMonthsModelPostProcess
from OneYearModelPostProcess import OneYearModelPostProcess
from PostProcessFactory import PostProcessFactory
from CSEPLogging import CSEPLogging


 #-------------------------------------------------------------------------------
 #
 # Test post-processing of the undeclustered catalog data used for the forecast 
 # evaluation tests. These tests validate generated catalog uncertainties as well.
 #
class CatalogPostProcessing (CSEPTestCase):

    
    #----------------------------------------------------------------------------
    #
    # Test post-processing of ANSS catalog data used for one-day forecast 
    # evaluation tests, and evaluate generated catalog uncertainties.
    #
    def testOneDayModelPostProcessing(self):
        """ Test post-processing of undeclustered ANSS catalog for one-day \
forecast evaluation as well as catalog uncertainties, and succeed. """

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())

        uncertainties_reference_dir = "shortterm_uncertainties"
          
        # Invoke post-processing test for one day forecast evaluation
        self.__postProcessing(OneDayModelPostProcess.Type,
                              uncertainties_reference_dir,
                              args = [CSEPTestCase.CumulativeStartDate])
        

    #----------------------------------------------------------------------------
    #
    # Test post-processing of CMT catalog data used for one-day forecast 
    # evaluation tests.
    #
    def testCMTOneDayModelPostProcessing(self):
        """ Test post-processing of CMT catalog for one-day \
forecast evaluation and succeed. """

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        GeographicalRegions.Region().set(GeographicalRegions.NWPacific)

        # Set post-processing specific data 
        one_day_min_magn = OneDayModelPostProcess.MinMagnitude
        one_day_max_depth = OneDayModelPostProcess.MaxDepth
        
        OneDayModelPostProcess.MinMagnitude = 5.8
        OneDayModelPostProcess.MaxDepth = 70.0

        try:
           
           CSEPTestCase.setDataSource(CMTDataSource.CMTDataSource.Type)
           
           # Invoke post-processing test for one day forecast evaluation
           self.__postProcessing(OneDayModelPostProcess.Type,
                                 pre_processed_file = 'cmt_import_processed.dat',
                                 args = [CSEPTestCase.CumulativeStartDate],
                                 data_source = DataSourceFactory().object(CMTDataSource.CMTDataSource.Type,
                                                                          input_variables = CSEPTestCase.DataSourceArgs))

        finally:
           
           GeographicalRegions.Region().set(GeographicalRegions.California)

           OneDayModelPostProcess.MinMagnitude = one_day_min_magn
           OneDayModelPostProcess.MaxDepth = one_day_max_depth
           

    #----------------------------------------------------------------------------
    #
    # Test post-processing of CMT catalog data used for one-day forecast 
    # evaluation tests.
    #
    def testCMTOneDayModelPostProcessingTrac188(self):
        """ Test Trac #188 fix for post-processing of CMT catalog for one-day \
forecast evaluation and succeed. """

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        GeographicalRegions.Region().set(GeographicalRegions.Global)

        # Set post-processing specific data 
        one_day_min_magn = OneDayModelPostProcess.MinMagnitude
        one_day_max_depth = OneDayModelPostProcess.MaxDepth
        
        OneDayModelPostProcess.MinMagnitude = 5.95
        OneDayModelPostProcess.MaxDepth = 30.0

        try:
            
           CSEPTestCase.setDataSource(CMTDataSource.CMTDataSource.Type)
                      
           # Invoke post-processing test for one day forecast evaluation
           self.__postProcessing(OneDayModelPostProcess.Type,
                                 pre_processed_file = 'cmt_import_processed_Trac188.dat',
                                 args = [CSEPTestCase.CumulativeStartDate],
                                 data_source = DataSourceFactory().object(CMTDataSource.CMTDataSource.Type,
                                                                          input_variables = CSEPTestCase.DataSourceArgs),
                                 test_date = datetime.datetime(2009, 9, 17),
                                 reference_catalog = 'CMT.Trac188.OneDayModel.catalog.nodecl.dat')

        finally:
           
           GeographicalRegions.Region().set(GeographicalRegions.California)

           OneDayModelPostProcess.MinMagnitude = one_day_min_magn
           OneDayModelPostProcess.MaxDepth = one_day_max_depth


    #----------------------------------------------------------------------------
    #
    # Test post-processing of CMT catalog data used for one-year forecast 
    # evaluation tests.
    #
    def testCMTOneYearModelPostProcessing(self):
        """ Test post-processing of CMT catalog for one-year \
forecast evaluation and succeed. """

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())

        GeographicalRegions.Region().set(GeographicalRegions.NWPacific)

        # Set post-processing specific data 
        one_year_min_magn = OneYearModelPostProcess.MinMagnitude
        one_year_max_depth = OneYearModelPostProcess.MaxDepth
        
        OneYearModelPostProcess.MinMagnitude = 5.8
        OneYearModelPostProcess.MaxDepth = 70.0

        try:

           CSEPTestCase.setDataSource(CMTDataSource.CMTDataSource.Type)
                      
           # Invoke post-processing test for one day forecast evaluation
           self.__postProcessing(OneYearModelPostProcess.Type,
                                 pre_processed_file = 'cmt_import_processed.dat',
                                 data_source = DataSourceFactory().object(CMTDataSource.CMTDataSource.Type,
                                                                          input_variables = CSEPTestCase.DataSourceArgs),
                                 args = [datetime.datetime(2006, 9, 2), 
                                         datetime.datetime(2007, 9, 2),
                                         datetime.datetime(2006, 1, 1)])

        finally:
           
           GeographicalRegions.Region().set(GeographicalRegions.California)

           OneYearModelPostProcess.MinMagnitude = one_year_min_magn
           OneYearModelPostProcess.MaxDepth = one_year_max_depth


    #----------------------------------------------------------------------------
    #
    # Test post-processing of CMT catalog data used as an input for one-day and
    # and one-year forecast generation.
    #
    def testCMTOneDayModelInputPostProcessing(self):
        """ Test post-processing of CMT catalog that is used to generate one-day  \
and one-year forecasts. """

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
        GeographicalRegions.Region().set(GeographicalRegions.NWPacific)

        # Set post-processing specific data 
        one_day_min_magn = OneDayModelPostProcess.MinMagnitude
        one_day_max_depth = OneDayModelPostProcess.MaxDepth
        
        OneDayModelPostProcess.MinMagnitude = 5.8
        OneDayModelPostProcess.MaxDepth = 70.0

        try:

           CSEPTestCase.setDataSource(CMTDataSource.CMTDataSource.Type)
           
           # Invoke post-processing test for one day forecast input:
           # Skip time column from comparison (can't convert HH:MM::SS to float)
           self.__postProcessing(OneDayModelInputPostProcess.Type,
                                 pre_processed_file = 'cmt_import_processed.dat',
                                 data_source = DataSourceFactory().object(CMTDataSource.CMTDataSource.Type,
                                                                          input_variables = CSEPTestCase.DataSourceArgs),
                                 skip_columns = [4])

        finally:
           
           GeographicalRegions.Region().set(GeographicalRegions.California)

           OneDayModelPostProcess.MinMagnitude = one_day_min_magn
           OneDayModelPostProcess.MaxDepth = one_day_max_depth
           

    #--------------------------------------------------------------------------------------
    #
    # Test post-processing of the catalog data used for the longterm forecast 
    # evaluation tests, and evaluate generated catalog uncertainties.
    #
    def testRELMAftershockPostProcessing (self):
        """ Test post-processing of undeclustered catalog for longterm forecast evaluation
            as well as catalog uncertainties, and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
  
        uncertainties_reference_dir = "longterm_uncertainties"
        
        # Invoke post-processing test for RELM aftershock forecast model evaluation    
        self.__postProcessing(RELMAftershockPostProcess.Type,
                              uncertainties_reference_dir)
        

    #--------------------------------------------------------------------------------------
    #
    # Test post-processing of the catalog data used by shortterm forecasts generation.
    # Generated catalog is being used as an input data by the shortterm forecast
    # model code (STEP, ETAS models).
    #
    def testOneDayModelInputPostProcessing (self):
        """ Test post-processing of undeclustered catalog for shortterm \
forecast generation, and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
  
        # Invoke post-processing test for catalog that is used as input for one day forecast
        # generation

        # There are no uncertainties applied to the catalog
        self.__postProcessing(OneDayModelInputPostProcess.Type)


    #--------------------------------------------------------------------------------------
    #
    # Test post-processing of declustered catalog data used for the longterm forecast 
    # evaluation tests, and validate generated catalog uncertainties as well.
    #
    def testRELMMainshockPostProcessing (self):
        """ Test declustered catalog post-processing for longterm forecast \
evaluation, as well as catalog uncertainties, and succeed."""

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())

        # Invoke post-processing test for RELM mainshock forecast model evaluation  
        uncertainties_reference_dir = "longterm_decluster_uncertainties"          
        params_file = "DeclusterParameter-randomSeed.txt"
        
        self.__postProcessing(RELMMainshockPostProcess.Type,
                              uncertainties_reference_dir, 
                              params_file,
                              uncertainty_catalog='catalog.uncert-filtered')


    #--------------------------------------------------------------------------------------
    #
    # Invoke post-processing of the catalog data used for the forecast 
    # evaluation tests, and evaluate generated catalog uncertainties if any
    #
    # Inputs: 
    #            post_process_type - Keyword identifying PostProcessing to be
    #                                          applied to the catalog data.
    #            uncertainties_dir - Directory with reference catalogs with 
    #                                       uncertainties (used for evaluation of result data). 
    #                                       Default is None.
    #            parameter_file - Parameter file used by the post-process. 
    #                                    Default is None.
    #            pre_processed_file - Pre-processed data file for the test. 
    #                                 Default is CatalogDataSource.PreProcessedFile.
    #            args - Optioinal input arguments for post-processing object.
    #                   Default is None.
    #            data_source - Catalog data source. Default is ANSSDataSource.
    #            skip_columns - Columns to skip during result validation. Default
    #                           is an empty list.
    #            test_date - Test date for the catalog. Default is CSEPTestCase.Date.
    #
    def __postProcessing(self,
                         post_process_type,  
                         uncertainties_dir = None,
                         parameter_file = None,
                         pre_processed_file = CatalogDataSource.PreProcessedFile,
                         args = None,
                         data_source = DataSourceFactory().object(input_variables = CSEPTestCase.DataSourceArgs),
                         skip_columns = [],
                         test_date = CSEPTestCase.Date,
                         reference_catalog = None,
                         uncertainty_catalog = None):
        """ Invoke catalog post-processing that is specific to the forecast class."""

  
        # Create post-processing object for the catalog data
        post_process = PostProcessFactory().object(post_process_type,
                                                   args)
        
        # Instantiating a catalog object will take care
        # of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath, 
                              data_source, 
                              post_process)
        
        
        # Copy reference raw catalog data file to the test directory
        shutil.copyfile(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     pre_processed_file),
                        os.path.join(CSEPTestCase.TestDirPath, 
                                     CatalogDataSource.PreProcessedFile))    


        if parameter_file != None:
              # Copy parameters file to the test directory (decluster parameters)
              shutil.copyfile(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                           parameter_file),
                              os.path.join(CSEPTestCase.TestDirPath, 
                                           parameter_file))    
        
        
        # Copy original random numbers files to the test directory (used for generating
        # catalog uncertainties)
        if uncertainties_dir != None:
              random_dir = "%s/random" %(uncertainties_dir)
              shutil.copytree(os.path.join(CSEPTestCase.ReferenceDataDir, 
                                           random_dir),
                              os.path.join(CSEPTestCase.TestDirPath, 
                                           "uncertainties"))
        
        
        # Create catalog and apply uncertainties to it. 
        catalog.create(test_date)
        
        ### Compare newly created catalog to the reference in ascii format

        # Define filenames and paths for reference and test data

        # Catalog filename used by post-processing
        ascii_catalog_file = post_process.files.catalog

        reference_catalog_file = reference_catalog
        if reference_catalog_file is None:
            
            # Reference catalog is not provided, figure out the filename for it 
            reference_catalog_file = ''
            if data_source.type() != ANSSDataSource.ANSSDataSource.Type:
               reference_catalog_file = "%s." %data_source.type()
            
            reference_catalog_file += "%s.%s" %(post_process_type, ascii_catalog_file)
        
        reference_file = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                      reference_catalog_file)
        test_file = os.path.join(CSEPTestCase.TestDirPath, ascii_catalog_file)

        
        CSEPLogging.getLogger(CatalogPostProcessing.__name__).info(
           "Comparing reference catalog file %s with generated catalog file %s..." \
           %(reference_file, test_file))

        error_msg = "Catalog %s post-processing failed." %(post_process_type)
        
        self.failIf(CSEPFile.compare(reference_file, test_file,
                                     precision = 1E-11,
                                     skip_column_index = skip_columns) is False, 
                    error_msg)
        

        ### Compare all generated catalogs with uncertainties if any
        if uncertainties_dir is not None:
              error = "Uncertainty catalog %s post-processing failed "  \
                      %(post_process_type)
             
              num_catalogs = CSEP.Catalog.NumUncertainties + 1
              
              for index in xrange(1, num_catalogs):
                  # Compare generated catalog with uncertainty to the original data
                  filename = "catalog.uncert.%s.dat" %(index)
                  if uncertainty_catalog is not None:
                      filename = "%s.%s.dat" %(uncertainty_catalog,
                                               index)
                  reference_file = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                                uncertainties_dir, 
                                                filename)
                  test_file = os.path.join(CSEPTestCase.TestDirPath, 
                                           "uncertainties", 
                                           filename)
                 
              
                  CSEPLogging.getLogger(CatalogPostProcessing.__name__).info(
                     "Comparing reference catalog file %s with generated catalog \
file %s..." %(reference_file, test_file))          
                 
                  error_msg = "%s (file index %s)" %(error, index)
                  
                  # Due to the re-implementation of Matlab codes in Python,
                  # generated (by Python) random numbers are not written to the 
                  # file anymore (to be read by Matlab codes). As a result, had
                  # to increase threshold used by file compare due to the  
                  # floating point format used by Matlab to store random numbers
                  # to the file
                  self.failIf(CSEPFile.compare(reference_file, 
                                               test_file,
                                               precision=1E-6) is False, 
                              error_msg)    
                  
                  
# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
