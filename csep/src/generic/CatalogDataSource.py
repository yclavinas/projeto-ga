"""
Module CatalogDataSource
"""

__version__ = "$Revision: 3811 $"
__revision__ = "$Id: CatalogDataSource.py 3811 2012-08-17 03:51:11Z liukis $"

import os, operator, glob, datetime

import CSEPLogging, CSEPFile, CSEPGeneric, CSEP
from CSEPStorage import CSEPStorage
from CSEPEventHandler import CSEPEventHandler
from SVNRepository import SVNRepository
from CSEPPropertyFile import CSEPPropertyFile


#--------------------------------------------------------------------------------
#
# CatalogSource.
#
# This class provides an interface to extract catalog data from a given source.
#
class CatalogDataSource (CSEPStorage, CSEPEventHandler):

    # Static data of the class

    # Filename to store raw catalog data as retrieved from authorized data source
    _RawFile = "import_raw.dat"
    
    # Filename to store pre-processed catalog data
    PreProcessedFile = "import_processed.dat"
    
    # ATTN: Attributes specific to the data being retrieved from the data source:
    # made static on the assumption that forecast group(s) share catalog data
    # source within testing region.
    
    # Log file to capture command output
    __logFile = "download.out"

    # Logger object for the class
    __logger = None

    # Keyword used for filename identifier
    FileType = "DataSource"
    
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    #        start_date - Start date for the catalog data as 'datetime.date'
    #                     object. Default is None.
    #        download_data - Flag if raw data should be downloaded. Default is
    #                        False.
    #        pre_process_data - Flag if raw data should be pre-processed.
    #                           Default is False.
    #        min_magnitude - Minimum magnitude for raw data. Default is 3.0 
    # 
    def __init__ (self, start_date = None, 
                        download_data = False, 
                        pre_process_data = False,
                        min_magnitude = None,
                        svn_working_dir = None):
        """ Initialization for CatalogSource class."""

        CSEPStorage.__init__(self)
        CSEPEventHandler.__init__(self)
        
        if CatalogDataSource.__logger is None:
           CatalogDataSource.__logger = CSEPLogging.CSEPLogging.getLogger(CatalogDataSource.__name__)
           
        # Re-set class start data attribute if it's provided
        # Start date for downloaded catalog data
        self._startDate = start_date
        
        if self._startDate is not None and \
           isinstance(self._startDate, str):
            self._starDate = datetime.datetime.strptime(self._startDate, 
                                                        CSEP.Time.DateFormat)
            
        # Minimum magnitude for downloaded catalog data
        self._minMagnitude = min_magnitude
        
        self.__preProcess = pre_process_data
     
        # Flag if raw data has been downloaded:
        # set to True if requested 'download_data' is set to False,
        # set to False if requested 'download_data' is set to True
        self.__isDownloaded = not download_data
        
        # If SVN repository should be used to archive downloaded raw catalog data
        CatalogDataSource.__logger.info("SVN working copy is provided: %s" %svn_working_dir)
        self.__svn = SVNRepository(svn_working_dir,
                                  start_date)

        self.__setRawDataPath()


    #---------------------------------------------------------------------------
    def type (self):
        """ Return string representation of the source."""

        # If base class is instantiated, None type is specified
        return None


    #--------------------------------------------------------------------------- 
    def __setRawDataPath (self, data_path=None):
        """Set full path to the file to store raw data as downloaded from
           authorized data source. """
           
        # If "staged" directory for the data is provided (to use already 
        # existing raw data)
        if data_path is not None:
            self.__rawFilepath = os.path.join(data_path,
                                              CatalogDataSource._RawFile)
        
        # If SVN archive is used, include path to SVN working copy    
        elif self.__svn.isWorkingCopy is True:
            self.__rawFilepath = os.path.join(self.__svn.workingCopyDir(),
                                              CatalogDataSource._RawFile)
        
        else:
            # Use current directory
            self.__rawFilepath = os.path.join(os.getcwd(),
                                              CatalogDataSource._RawFile)
        
        CatalogDataSource.__logger.info("Setting raw data filepath to %s (given data_path=%s)"
                                        %(self.__rawFilepath,
                                          data_path))
        return self.__rawFilepath


    #--------------------------------------------------------------------------- 
    def __getRawDataPath (self):
        """Get full path to the file to store raw data as downloaded from
           authorized data source. """
           
        return self.__rawFilepath
    
    
    RawFile = property(__getRawDataPath,
                       __setRawDataPath,
                       doc = 'Full path to the file to store raw data as downloaded from authorized data source')
    

    #--------------------------------------------------------------------------- 
    def __getSVN (self):
        """Get SVNRepository object for the data source."""
           
        return self.__svn
    
    
    SVN = property(__getSVN,
                   doc = 'SVNRepository object for the data source.')

    
    #---------------------------------------------------------------------------
    #
    # Return start date for raw catalog data retrieved from data source
    #
    # Input: None.
    #
    # Output: start data of catalog data
    #
    def __getStartDate (self):
        """ Return start date for raw catalog data retrieved from data source."""

        return self._startDate
    
    StartDate = property(__getStartDate, 
                         doc = "Start date for raw catalog data retrieved from data source")


    #---------------------------------------------------------------------------
    #
    # Return minimum magnitude for raw catalog data retrieved from data source
    #
    # Input: None.
    #
    # Output: start data of catalog data
    #
    def __getMinMagnitude (self):
        """ Return minimum magnitude for raw catalog data retrieved from data source."""

        return self._minMagnitude
    
    MinMagnitude = property(__getMinMagnitude, 
                            doc = "Minimum magnitude for raw catalog data retrieved from data source")


    #---------------------------------------------------------------------------
    #
    # Return file format of pre-processed catalog data. Implemented by derived
    # classes.
    #
    # Input: None.
    #
    # Output: String representing the file format of pre-processed catalog data.
    #
    def fileFormat (self):
        """ String representing the file format of pre-processed catalog data."""

        raise RuntimeError, "fileFormat() is called on an abstract class." 
     

    #----------------------------------------------------------------------------
    #
    # Return log file used to capture download command output
    #
    # Input: None.
    #
    # Output: log file used to capture download command output
    #
    def logFile (self):
        """ Return log file used to capture download command output."""

        return '_'.join([self.type(), 
                         CatalogDataSource.__logFile])
     

    #----------------------------------------------------------------------------
    #
    # Extract catalog data from specified source.
    #
    # Input:
    #        test_date - Date for raw catalog data.
    #        data_dir - Directory with raw data file if download_raw_data 
    #                   is set to False. Default is None.
    #
    # Output: Filename for pre-processed catalog data.
    #
    def extract (self, test_date, data_dir = None):
       """ Extract raw data from the source, and pre-process into catalog
           ZMAP format. Method arguments allow optional data_dir to specify 
           location of already existing data."""


       # If directory with existing raw data is provided, use it
       self.__setRawDataPath(data_dir)

       # SVN will re-use the same 'import_raw.dat' file (GPSDataSource) to 
       # download raw catalog data to, then 'import_raw.dat' will always exist,
       # so need to check if SVN archive is used
       if os.path.exists(self.RawFile) is False or \
          self.__svn.isWorkingCopy is True:
           
           data_in_svn = False
           use_svn_tag = None
           got_file = False

           if self.__isDownloaded is False:
               CatalogDataSource.__logger.info("Downloading catalog data for %s..." \
                                               %test_date.date())
    
               # If data_dir is provided and raw data does not exist there,
               # use SVN working copy directory to download the data to, 
               # then create link to downloaded file
               raw_data_in_svn = False
               if self.__svn.isWorkingCopy is True and \
                  data_dir is not None:
                   
                   raw_data_in_svn = True
                   self.__setRawDataPath()
                  
                 
               # Lock directory with raw data file
               self.__svn.lock()
               try:
                   self.download(test_date)
                
               except:
                   self.__svn.unlock()
                   raise
                   
               self.__svn.unlock()
               
               # Create link to original raw data file as used by download,
               # and restore path to raw data file as it was originally set up
               if raw_data_in_svn is True:
                   original_file = self.RawFile
                   link_file = self.__setRawDataPath(data_dir)

                   # Each forecast group will attempt to create a link to SVN 
                   # working copy of the file, check if it exists already
                   if os.path.exists(link_file) is False:
                       CatalogDataSource.__logger.info("Creating %s link to catalog data %s..." \
                                                       %(link_file,
                                                         original_file))
                       os.symlink(original_file,
                                  link_file)
               
               
               got_file = True
               self.__isDownloaded = True
               
           else:             
               # Check if raw catalog data can be staged based on
               # search criteria if any
               # TODO: implement checkout from SVN based on metadata for existing
               # data files
               got_file = CSEPStorage.stage(self, 
                                            [self.RawFile])

               # Catalog from SVN would be exported to runtime directory if data
               # was stored in SVN repository, or None if not
               use_svn_tag = self.SVNTag
                   
               ### TODO: make sure to use SVN tag as it was used to check out 
               # raw data from SVN to record it in metadata
               # raw_data_dir = os.getcwd()?

           # If raw data file is stored in SVN, report SVN tag for it 
           if SVNRepository.workingCopy(self.RawFile) is True:
               data_in_svn = True

           # raw file or link to it is a working copy of SVN 
           if SVNRepository.workingCopy(os.path.realpath(self.RawFile)) is True: 
               # Capture SVN tag used for raw data by this run
               use_svn_tag = self.__svn.tagURL()
               

           if got_file is True:
               if data_in_svn is False:
                   # Fire registered events for raw data file: cleanup of original
                   # data file
                   args = [self.RawFile]
                   CSEPEventHandler.fire(self, [args])
               
               # Create copy with unique filename and corresponding metadata file
               # it one already does not exist
               meta_files = glob.glob(os.path.join(os.path.dirname(self.RawFile),
                                                   '*%s' %CSEPPropertyFile.Metadata.Extension))
               has_meta = False
               for each_meta in meta_files:
                   meta_obj = CSEPPropertyFile.Metadata(each_meta)
                   if os.path.basename(self.RawFile) in meta_obj.originalDataFilename:
                       has_meta = True
                       break
                   
               if has_meta is False: 
                   comment = "Raw catalog data downloaded from %s data source." \
                             %self.type()
                   self.__copyData(self.RawFile, 
                                   comment,
                                   data_in_svn,
                                   use_svn_tag)             
              
   
       # Pre-process raw catalog data
       preprocessed_data_file = CatalogDataSource.PreProcessedFile
   
       if data_dir != None:
           preprocessed_data_file = os.path.join(data_dir, 
                                                 CatalogDataSource.PreProcessedFile)
     
       # Pre-processing - expects raw catalog data
       if self.__preProcess is True:
         
          # If data source implements SVNRepository, then raw_data_file may 
          # not be generated if original files are archived and used to 
          # generate pre-processed catalog 
          if os.path.exists(self.RawFile) is False and \
             self.__svn.isWorkingCopy is False :
              error_msg = "Expected raw catalog file %s does not exist." \
                          %self.RawFile
              CatalogDataSource.__logger.error(error_msg)
               
              raise RuntimeError, error_msg          
          
          # Issue pre-processing specific to the data source if file doesn't exist,
          # OR 
          # re-process the file if data source is implemented as SVNRepository
          if os.path.exists(preprocessed_data_file) is False:
              
              # Lock directory with raw data file: if other processes download the
              # data, raw catalog might get reset to empty file - observed during 
              # multiple processings in parallel on csep-cert
              self.__svn.lock()
              
              try:
                  CatalogDataSource.__logger.info("Pre-processing %s" %self.RawFile)
                  self.preProcess(self.RawFile, 
                                  preprocessed_data_file)
                  
              except:
                  self.__svn.unlock()
                  raise
              
              self.__svn.unlock()
              
              # Fire registered events for pre-processed data file
              # NOTE: if data source implements SVNRepository, then pre-processed
              # catalog may not exist (GPSDataSource generates stationlist.txt instead
              # within SVN working copy directory) 
              if os.path.exists(preprocessed_data_file) is True:
                  if os.path.isabs(preprocessed_data_file) is False:
                      cwd = os.getcwd()
                      preprocessed_data_file = os.path.join(cwd, 
                                                            preprocessed_data_file)

                  meta_files = glob.glob(os.path.join(os.path.dirname(preprocessed_data_file),
                                                      '*%s' %CSEPPropertyFile.Metadata.Extension))
                  has_meta = False
                  for each_meta in meta_files:
                      meta_obj = CSEPPropertyFile.Metadata(each_meta)
                      if os.path.basename(preprocessed_data_file) in meta_obj.originalDataFilename:
                          has_meta = True
                          break
                   
                  if has_meta is False:    
                      args = [preprocessed_data_file]
                      CSEPEventHandler.fire(self, [args])
                       
                      # Create copy with unique filename and corresponding metadata file
                      comment = "Downloaded %s catalog data, pre-processed into %s format." \
                                %(self.type(), self.fileFormat())
                      self.__copyData(preprocessed_data_file, 
                                      comment)             

       return preprocessed_data_file


    #----------------------------------------------------------------------------
    #
    # Download raw catalog data. This method should be implemented by 
    # derived classes.
    #
    # Input:
    #        test_date - Date for raw catalog data.    
    #
    # Output: string representing the type of the source.
    #
    def download (self, test_date):
        """ Download raw catalog from specified data source."""

        pass


    #----------------------------------------------------------------------------
    #
    # Return flag that indicates if raw catalog data was dowloaded from 
    # the data source.
    #
    def __getIsDownloaded (self):
        """ Return flag that indicates if raw catalog data was dowloaded from 
            the data source."""

        return self._isDownloaded
 

    #----------------------------------------------------------------------------
    #
    # Download raw catalog data. This method should be implemented by 
    # derived classes.
    #
    def __setIsDownloaded (self, value):
        """ Set flag that indicates if raw catalog data was dowloaded from 
            the data source:

            value - Value to set flag with."""

        self._isDownloaded = value
        return


    isDownloaded = property(__getIsDownloaded, 
                            __setIsDownloaded,
                             doc = "Flag to indicate if raw catalog data was dowloaded from \
the data source")
    

    #---------------------------------------------------------------------------
    #
    # Pre-process raw catalog data. This method should be implemented by 
    # derived classes.
    #
    # Input:
    #        raw_data_file - Raw catalog data file.
    #        preprocessed_data_file - Filename for output pre-processed data.
    #
    # Output: string representing the type of the source.
    #
    def preProcess (self, raw_data_file, preprocessed_data_file):
        """ Download raw catalog from specified data source."""

        pass


    #---------------------------------------------------------------------------
    #
    # Create a copy of catalog file with unique filename and generate 
    # corresponding metadata file.
    #
    # Input:
    #          filename - Name of the data file.
    #          comment - Comment about data file to be inserted into metadata file.
    #          in_svn - Flag if data resides in SVN repository. Default is False.
    #          svn_tag - SVN repository tag url if data exists in repository. 
    #                    Default is None.
    #
    # Output: None
    #
    def __copyData (self, 
                    filename, 
                    comment, 
                    in_svn = False, 
                    svn_tag = None):
        """ Generate copy of specified catalog file with unique filename, and generate
            corresponding metadata file."""

        filenames = CSEPPropertyFile.filenamePair(self.type(),
                                                  CatalogDataSource.FileType) 

        # Unpack the sequence
        datafile, metafile = filenames
       
        # Extract directory path for original file and create unique copy
        # under the same directory
        data_path, data_file = os.path.split(filename)
        if len(data_path) != 0:
            datafile = os.path.join(data_path, datafile)
            
            if in_svn is True:
                # Data file is in SVN, create metadata file in current location
                data_path = os.getcwd()
                 
            metafile = os.path.join(data_path, metafile)
            
        # No need to deep copy original file if data file has been staged,
        # it's sufficient to store metadata about created link to original file
        if os.path.islink(filename) is False and \
           in_svn is False and svn_tag is None:
            CSEPFile.copy(filename, datafile)
       
        # Create metadata file
        CatalogDataSource.__logger.info("Creating metadata file %s for %s (SVN tag=%s)" \
                                        %(metafile,
                                          filename,
                                          svn_tag))
        CSEPPropertyFile.createMetafile(metafile, 
                                        filename,
                                        CSEPFile.Format.ASCII,
                                        comment,
                                        filename,
                                        in_svn = in_svn,
                                        svn_tag = svn_tag)
        
        return


    #----------------------------------------------------------------------------
    #
    # Cut catalog data to geographical area.
    #
    # Input: 
    #         np_catalog - Numpy.array object with catalog data
    #         area_file - Filename for geographical area.
    #         result_file - Filename for result catalog data.
    #
    # Output: result_file
    #
    @classmethod
    def cutToArea (cls,
                   catalog_file, 
                   area_file, 
                   result_file = None):
        """ Cut catalog data to geographical area."""

        return CSEPGeneric.Catalog.cutToArea(catalog_file,
                                             area_file, 
                                             result_file)
    

    #----------------------------------------------------------------------------
    #
    # Cut catalog data to geographical area.
    #
    # Input: 
    #         np_catalog - Numpy.array object with catalog data
    #         start_time - datetime object that represents start date for 
    #                      the period.
    #         stop_time - datetime object that represents end date for the period.
    #         result_file - Filename for result catalog data.      
    #         start_time_sign - Sign operator for start_time boundary. 
    #                           Default is greater or equal sign (>=).
    #         stop_time_sign - Sign operator for start_time boundary. 
    #                           Default is less or equal sign (<=).
    #
    # Output: result_file
    #
    @classmethod
    def cutToTimePeriod (cls,
                         catalog_file, 
                         start_time, 
                         stop_time,
                         result_file = None,
                         start_time_sign = operator.ge,
                         stop_time_sign = operator.le):
        """ Cut catalog data to time period."""

        return CSEPGeneric.Catalog.cutToTimePeriod(catalog_file,
                                                   start_time, 
                                                   stop_time,
                                                   result_file,
                                                   start_time_sign,
                                                   stop_time_sign)

        
    #-----------------------------------------------------------------------------
    #
    # modifications
    # 
    # This method applies uncertainties to the catalog data. The filtering of the 
    # result catalogs is kind of hidden from the caller (using Matlab...). 
    # It applies the same filtering as for original catalog defined by 
    # CSEPGeneric.Catalog.filter() method.
    #
    # Input: 
    #         np_catalog - Numpy.array object with catalog data
    #         area_file - Area file for catalog filtering
    #         threshold - PostProcess.Threshold object with filters values
    #         result_files - PostProcess.Files.Uncertainties object with names
    #                        of files and directories for catalog uncertainties
    #         probability_column - Column index for independence probability. This
    #                              column is available for declustered catalog only. 
    #                              Default is 0.
    #
    # Output: Directory that stores intermediate data products (random seed values)
    #         required for reproducibility of results 
    # 
    @classmethod    
    def modifications (cls,
                       catalog_file, 
                       area_file, 
                       threshold,
                       result_files,
                       probability_column = 0):
        """ Create catalog modifications by applying randomized uncertainties 
            to the original catalog"""

        return CSEPGeneric.Catalog.modifications(catalog_file, 
                                                 area_file,
                                                 threshold,
                                                 result_files,
                                                 probability_column)
        

    #----------------------------------------------------------------------------
    #
    # Filter catalog data based on specified geographical location, 
    # minimum magnitude, maximum depth, and starting date for the forecast 
    # model.
    #
    # Input: 
    #         np_catalog - Numpy.array object with catalog data
    #         area_file - Area file for catalog filtering
    #         threshold - PostProcess.Threshold object with filters values
    #         result_file - Filename for result data. Default is None.
    #
    # Output: result_file
    #
    @classmethod    
    def filter (cls,
                catalog_file, 
                area_file,
                threshold, 
                result_file = None):
        """ Filter catalog data based on specified geographical location, 
            minimum magnitude, maximum depth, and starting date for the forecast 
            model. Filter values are provided by 'threshold' object."""

        return CSEPGeneric.Catalog.filter(catalog_file,
                                          area_file, 
                                          threshold,
                                          result_file)
    
    
    #----------------------------------------------------------------------------
    #
    # decluster
    # 
    # This method declusters catalog data according to the Reasenberg declustering
    # algorithm.
    #
    # Input: 
    #         catalog_file - Filename for catalog data
    #         result_file - Filename for result data.
    #         supplemental_result_file - Filename for catalog with supplemental
    #                                    independence probability column.
    #
    # Output: Tuple of numpy.array objects with declustered catalog,
    #         catalog with independence probability, and filenames for both 
    #         catalogs as stored by Matlab
    #
    @classmethod    
    def declusterReasenberg (cls,
                             catalog_file):
        """ Decluster catalog and generate supplemental catalog with independence
            probability information to be used for catalog uncertainties."""

        return CSEPGeneric.Catalog.declusterReasenberg(catalog_file)
    
