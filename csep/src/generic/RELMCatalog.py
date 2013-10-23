"""
Module RELMCatalog
"""

__version__ = "$Revision: 3563 $"
__revision__ = "$Id: RELMCatalog.py 3563 2011-12-06 19:39:38Z liukis $"

import sys, os, datetime, logging, glob, scipy.io
import numpy as np

import CSEPFile, CSEPLogging, CSEPPropertyFile, CSEP, MatlabLogical, CSEPGeneric
from PostProcess import PostProcess
from PostProcessFactory import PostProcessFactory
from DataSourceFactory import DataSourceFactory
from CSEPStorage import CSEPStorage
from CSEPEventHandler import CSEPEventHandler


#--------------------------------------------------------------------------------
#
# RELMCatalog.
#
# This class is designed to extract catalog data and pre-process it for
# the use by a forecast.
# It is relying on environment variable CENTERPATH to 
# construct a script to be executed in the Matlab for the pre-processing.
#
class RELMCatalog (CSEPStorage, CSEPEventHandler):

    # Static data of the class
    
    # Keyword identifying type of the class.
    Type = "Catalog"

    # Sub-directory used to archive existing "map-ready" files
    __archiveDir = 'archive'
    
      
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        test_dir - A directory path where to write output data to. Default is a 
    #                      current directory.
    #        data_source - A source object for catalog data. Default is ANSS 
    #                      catalog data with start date of 1/1/1985.
    #        post_process - An object to represent post-processing for the
    #                       catalog. Default is None.
    # 
    def __init__ (self, test_dir = os.getcwd(), 
                        data_source = DataSourceFactory().object(),
                        post_process = None):
        """ Initialization for RELMCatalog class."""

        # Instantiate base classes
        CSEPStorage.__init__(self, test_dir)
        
        # Copy event handler of provided data source
        CSEPEventHandler.__init__(self, data_source)
        
        # Data source to use for catalog data
        self.__dataSource = data_source
                
        self.testDir = test_dir
        
        # Post-processing object
        self.postProcess = post_process


    #--------------------------------------------------------------------
    #
    # Create data for the test.
    #
    # Input: 
    #        test_date - datetime object that represents testing date.
    #        data_dir - directory with raw data file if download_raw_data 
    #                   is set to False. Default is None.
    #
    # Output:
    #        List of newly created catalog files. Returned list of files will be
    #        empty if catalog was already present in the self.testDir directory,
    #        or PostProcessing is None (no requirement to generate catalog)
    #  
    def create (self, test_date,  
                      data_dir = None):
        """ Download catalog data as specified by the input test date.
            This method invokes bash script to download the catalog, and 
            issues a set of 'awk' and 'sed' commands to pre-process downloaded
            data. Post-processing of the catalog data will be invoked if it was
            specified during RELMCatalog object instantiation with PostProcess
            object."""

        result_files = []
        
        # Check if required catalog already exists:
        if self.postProcess is not None and \
           (os.path.exists(os.path.join(self.testDir, 
                                        self.postProcess.files.catalog))):
           return result_files
        
        
        # cd to the test directory, remember current directory 
        cwd = os.getcwd()
        
        if cwd != self.testDir:
           os.chdir(self.testDir)
        
        try:
   
            
            CSEPLogging.CSEPLogging.getLogger(RELMCatalog.__name__).info("create(): Before __dataSource.extract: %s" %self.__dataSource)
            
            # Set search criteria in case download of the raw catalog data is 
            # disabled
            if self.postProcess is not None:
                self.__dataSource.dirSearchCriteria(os.path.join(self.testDir, 
                                                                 self.postProcess.files.catalog),
                                                    self.testDir)
            
            preprocessed_data_file = self.__dataSource.extract(test_date,
                                                               data_dir)
                
   
            # Invoke post-processing script that is specific to the forecast type or
            # model
            if self.postProcess is not None:
               
               # Stage already archived catalog files if any
               required_files, optional_files = self.postProcess.reproducibility
               
               if CSEPStorage.stage(self, 
                                    required_files.keys()) is False:

                  # Create catalog file if it could not be staged based on 
                  # archived files
                  self.postProcess.apply(test_date, preprocessed_data_file)
                  
                  # Move any map-ready catalog files if any (generated from
                  # already existing catalogs)
                  map_filenames = glob.glob("%s/%s*" %(self.testDir, 
                                                       CSEP.Forecast.MapReadyPrefix))
                  if len(map_filenames) != 0:

                      for each_map in map_filenames:
                          filenames = CSEPPropertyFile.CSEPPropertyFile.filenamePair(CSEP.Forecast.MapReadyPrefix, 
                                                                                     CSEPFile.Name.ascii(self.postProcess.files.catalog))
              
                          # Unpack the sequence
                          datafile, metafile = filenames
              
                          datafile_path = os.path.join(self.testDir,
                                                       RELMCatalog.__archiveDir,
                                                       datafile)
                           
                          os.renames(each_map, datafile_path)
                      
                          # Create metadata file
                          description = "Map-ready catalog file %s" %each_map
                          CSEPPropertyFile.CSEPPropertyFile.createMetafile(os.path.join(self.testDir,
                                                                                        RELMCatalog.__archiveDir,
                                                                                        metafile), 
                                                                           each_map,
                                                                           CSEPFile.Format.ASCII,
                                                                           description)

                  
               else:
                  
                  # Stage optional files if they exist
                  CSEPStorage.stage(self, optional_files.keys())  

               # If all requested files have been staged, return flag as if 
               # files have been generated - that way unique copies of staged data
               # files will be created for future reproducibility
               
               # Create a copy of post-processed catalog file with unique filename 
               # and generate corresponding metadata file. New files are generated
               # under the same directory as original catalog file.

               # Step through all registered files for reproducibility, and create
               # a copy with unique filename
               description = "-".join([self.postProcess.type(),
                                       self.postProcess.files.catalog])
                
               CSEPLogging.CSEPLogging.getLogger(RELMCatalog.__name__).debug("Reproducibility data: %s" \
                                                                             %[registry for registry in self.postProcess.reproducibility])

               # TODO: rename catalog uncertainties and random numbers used by them -
               #       for now the whole directory is given a unique name     
                
               # Report existing entries for reproducibility (some are optional)
               # Don't remove original entries - original post-processed catalog might
               # still be in use
               result_files = self.postProcess.copyAndCleanup(self.Type,
                                                              self.testDir,
                                                              description,
                                                              cleanup=False)
               
               CSEPEventHandler.fire(self,
                                     [[os.path.join(self.testDir, entry) for entry in result_files]])     
        
        finally:
           # Go back to the original directory
           if cwd != self.testDir:
              os.chdir(cwd)        
           
        return result_files 
     

    #===========================================================================
    #
    # load
    # 
    # Load catalog data from provided Matlab file. This method can load a single
    # or multiple catalogs (with applied uncertainties) from the file. 
    # 
    # Input:
    #        catalog_file - Path to the Matlab format catalog file
    #
    # Output:
    #        numpy.array object with catalog data
    #
    #===========================================================================
    @staticmethod
    def load(catalog_file):
        """Load catalog data from provided Matlab file."""

        catalog = None
        
        # Load declustered catalog ('mCatalogDecl' variable) or 
        # undeclustered catalog ('mCatalog' variable) or
        # catalogs with applied uncertainties
        if os.path.exists(catalog_file):
            
            # Support loading of the catalog file in ASCII format (used by miniCSEP)
            if CSEPFile.Extension.toFormat(catalog_file) == CSEPFile.Format.ASCII:
                # ATTN! Check for an empty file: np.loadtxt() raises an exception 
                # if an empty file
                catalog = np.fromfile(catalog_file)
                if catalog.size == 0:
                    # CSEP is relying on 2-dim arrays
                    catalog.shape = 0, 0
                    
                else:
                    catalog = CSEPFile.read(catalog_file)
                    
            else:
                # Get rid of warning by setting 'struct_as_record' argument
                catalog_fh = scipy.io.loadmat(catalog_file,
                                              struct_as_record=True)
                    
                expected_vars = [MatlabLogical.CatalogVar.Declustered,
                                 MatlabLogical.CatalogVar.Undeclustered,
                                 MatlabLogical.CatalogVar.Uncertainties] 
                
                for each_var in expected_vars:
                    if each_var in catalog_fh:
                        catalog = catalog_fh[each_var]
                        break
                     
                if catalog is None:
                    error_msg = "Unexpected variable is specified by '%s' catalog file. \
        Expected one of %s (got %s)" %(catalog_file,
                                       expected_vars,
                                       catalog_fh.keys())
            
                    CSEPLogging.CSEPLogging.getLogger(RELMCatalog.__name__).error(error_msg)
                    raise RuntimeError, error_msg

        else:
            log_msg = "Catalog file '%s' does not exist, skipping loading of the file" \
                      %catalog_file
            CSEPLogging.CSEPLogging.getLogger(RELMCatalog.__name__).info(log_msg)

        return catalog
    
    
    #===========================================================================
    #
    # cutToTime
    # 
    # Filter catalog by time   
    # 
    # Input:
    #        catalog - numpy.array object that represents catalog data
    #        time_threshold - datetime object to filter by
    #        compare_sign - String representation of the comparison operator.
    #                       Default is '>='. 
    #
    # Output:
    #        numpy.array object that represents filtered catalog data
    #
    #===========================================================================
    @staticmethod
    def cutToTime(catalog,
                  time_threshold,
                  compare_sign = '>='):
        """Cut catalog to provided datetime threshold."""

        # Filter catalog if it's non-empty
        # Fix for Trac ticket #232: Empty catalog passed to
        # CSEPGeneric.Catalog.modifications() to generate catalog uncertainties
        # raises 'IndexError: index out of bounds' exception
        # ATTN: catalog uncertainties will be initialized to one-element of '0'
        # if empty catalog is passed to CSEPGeneric.Catalog.modifications()
        if catalog.size > 1:
            
            CSEPLogging.CSEPLogging.getLogger(RELMCatalog.__name__).info("RELMCatalog.cutToTime(): %s %s"
                                                                         %(compare_sign,
                                                                           time_threshold))
            
            catalog_dates = np.array([datetime.datetime(int(each[CSEPGeneric.Catalog.ZMAPFormat.DecimalYear]),
                                                        int(each[CSEPGeneric.Catalog.ZMAPFormat.Month]),
                                                        int(each[CSEPGeneric.Catalog.ZMAPFormat.Day]),
                                                        int(each[CSEPGeneric.Catalog.ZMAPFormat.Hour]),
                                                        int(each[CSEPGeneric.Catalog.ZMAPFormat.Minute]),
                                                        int(each[CSEPGeneric.Catalog.ZMAPFormat.Second]),
                                                        CSEP.Time.microseconds(each[CSEPGeneric.Catalog.ZMAPFormat.Second])) for each in catalog])
            
            
            selection, = np.where(CSEP.Operator[compare_sign](catalog_dates, time_threshold))
            
            cut_to_time_catalog = catalog[selection, :] 

            return cut_to_time_catalog
        
        else:
            # Return original empty catalog: 
            # Cutting empty catalog to np.zeros((0,1), dtype=bool) strips off
            # second array dimension
            # OR
            # cutting catalog to np.zeros((0,), dtype=bool) causes invalid index 
            # when applied to catalog
            return catalog


# Invoke the module
if __name__ == '__main__':

     from CSEPOptions import CommandLineOptions
     import EvaluationTestOptionParser
     
     
     parser = EvaluationTestOptionParser.EvaluationTestOptionParser()

     parser.add_option('--rawDataDir',
                       type='string',
                       dest='raw_data_dir',
                       default=None,
                       help='Optional directory that stores raw catalog files. \
This option is used if pre-downloaded catalog is used by the module. Default is None.')

     
     # List of requred options for the test
     required_options = [CommandLineOptions.YEAR, 
                         CommandLineOptions.MONTH,
                         CommandLineOptions.DAY]

     options = parser.options(required_options)
     
     # Test date for the test
     test_date = datetime.datetime(options.year, 
                                   options.month,
                                   options.day)
     
     post_process = None
     
     if options.post_process is not None:
        
        args = []
        
        if options.post_process_args is not None:
            args = [datetime.datetime.strptime(each_date, 
                                               CSEP.Time.DateFormat) for each_date in
                    options.post_process_args.split()]
           
        post_process = PostProcessFactory().object(options.post_process,
                                                   args)
     
     
     # Create Catalog object and download the data if required
     ### (EvaluationTestOptionParser already took care of creating proper
     ###  CatalogDataSource based on provided properties)
     catalog = RELMCatalog(os.path.abspath(options.test_dir),
                           DataSourceFactory().object(options.data_source, 
                                                      isObjReference = True),
                           post_process)

     # Create catalog with specified post_processing
     catalog.create(test_date,
                    options.raw_data_dir)
        
     # Shutdown logging 
     logging.shutdown()
        
# end of main
      
        