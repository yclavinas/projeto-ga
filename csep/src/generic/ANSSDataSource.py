"""
Module ANSSDataSource
"""

__version__ = "$Revision: 3682 $"
__revision__ = "$Id: ANSSDataSource.py 3682 2012-03-16 22:01:07Z liukis $"

import os, datetime, ftplib
import numpy as np

import Environment, CSEPFile, CSEPLogging, CSEPGeneric, CSEPUtils, CSEP
from CatalogDataSource import CatalogDataSource


# Environment variable to define directory path for working copy of SVN
# repository to store ANSS raw data downloads
ARCHIVE_ENV = 'ANSS_ARCHIVE_DIR'


#--------------------------------------------------------------------------------
#
# ANSSDataSource
#
# This class provides an interface to extract ANSS catalog data.
#
class ANSSDataSource (CatalogDataSource):

    # Static data of the class
    Type = "ANSS"
    
    # FTP command to use for download
    __downloadSite = 'www.ncedc.org'
    __downloadDir = 'pub/catalogs/anss'

    # Working copy of SVN repository if it's used by the data source
    __archiveDir = None
    
    __logger = None
    
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    #        start_date - Optional start date for the catalog data. Default is a
    #                     datetime.datetime() object for 1/1/1985.
    #        download_data - Flag if raw data should be downloaded. Default is
    #                        True.
    #        pre_process_data - Flag if raw data should be pre-processed.
    #                           Default is True.
    # 
    def __init__ (self, 
                  start_date = datetime.datetime(1985, 1, 1), 
                  download_data = True,
                  pre_process_data = True,
                  min_magnitude = 3.0):
        """ Initialization for ANSSDataSource class."""
    
        if ANSSDataSource.__logger is None:
           ANSSDataSource.__logger = CSEPLogging.CSEPLogging.getLogger(ANSSDataSource.__name__)

        # If SVN repository should be used to archive downloaded raw catalog data
        if ARCHIVE_ENV in os.environ:
            ANSSDataSource.__archiveDir = os.environ[ARCHIVE_ENV]

        CatalogDataSource.__init__(self, start_date, 
                                         download_data, 
                                         pre_process_data,
                                         min_magnitude,
                                         ANSSDataSource.__archiveDir)
        

    #--------------------------------------------------------------------
    #
    # Return source type as defined by the class.
    #
    # Input: None.
    #
    # Output: string representing the type of the source.
    #
    def type (self):
        """ Return string representation of the source."""

        return ANSSDataSource.Type


    #---------------------------------------------------------------------------
    #
    # Return file format of pre-processed catalog data.
    #
    # Input: None.
    #
    # Output: String representing the file format of pre-processed catalog data.
    #
    def fileFormat (self):
        """ String representing the file format of pre-processed catalog data."""

        return 'ZMAP'


    #--------------------------------------------------------------------
    #
    # Download catalog data from specified source.
    #
    # Input:
    #        test_date - Date for raw catalog data.
    #
    # Output: None.
    #
    def download (self, test_date):
       """ Extract raw ANSS catalog for specified test date."""


       # Download raw data, append command output to the log file
       year = self.StartDate.year
       month = self.StartDate.month
       
       # Log in to the data server
       ftp = ftplib.FTP(ANSSDataSource.__downloadSite)
       ftp.login()

       # Collect raw ANSS data into a single file
       raw_fhandle = CSEPFile.openFile(self.RawFile, 
                                       CSEPFile.Mode.WRITE + CSEPFile.Mode.BINARY)
       
       while year < test_date.year:
          
          if year != self.StartDate.year:
              month = 1

          # Go to the last month of the year
          while month <= 12:
             year_dir = os.path.join(ANSSDataSource.__downloadDir,
                                      str(year))
             month_catalog = "%s.%02d.cnss" %(year, month)
             
             ANSSDataSource.__logger.info("Downloading %s from %s"
                                          %(month_catalog, year_dir))

             # Use binary mode for retrieval - otherwise new lines are not
             # preserved in downloaded data
             ftp.retrbinary('RETR %s' %os.path.join(year_dir,
                                                    month_catalog),
                           raw_fhandle.write)

             month += 1
              
          year += 1
          
       else:
          
          # Download up to (including) the test month data for the final year,
          # append command output to the log file
          month = 1
          year_dir = os.path.join(ANSSDataSource.__downloadDir,
                                  str(test_date.year))
          
          while month <= test_date.month:
              
             month_catalog = "%s.%02d.cnss" %(test_date.year, month)
             
             ANSSDataSource.__logger.info("Downloading %s from %s"
                                          %(month_catalog, year_dir))

             # Use binary mode for retrieval - otherwise new lines are not
             # preserved in downloaded data
             ftp.retrbinary('RETR %s' %os.path.join(year_dir,
                                                   month_catalog),
                           raw_fhandle.write)
             #raw_fhandle.write('\n')
              
             month += 1

       raw_fhandle.close()
       ftp.quit()
       
       ### 1) Check for data change if any and commit updates to SVN if there is a change,
       ### 2) Tag main trunk in repository
       self.SVN.commit("%s data to process %s test date, committed on %s" 
                       %(ANSSDataSource.Type,
                         test_date.date(),
                         datetime.datetime.now()))
       

    #--------------------------------------------------------------------
    #
    # Pre-process catalog data into ZMAP-format.
    #
    # Input:
    #        raw_data_file - Raw catalog data file.
    #        preprocessed_data_file - Filename for output pre-processed data.
    #
    # Output: None.
    #
    def preProcess (self, 
                    raw_data_file, 
                    preprocessed_data_file):
       """ Pre-process raw ANSS data into catalog ZMAP format."""


       # Fix for ticket #53:
       # Get rid of events other than earthquakes in the catalog
       filtered_raw_data_file = 'filtered_raw_data.txt'
       fhandler = CSEPFile.openFile(raw_data_file)
       raw_data_fhandler = CSEPFile.openFile(filtered_raw_data_file, 
                                             CSEPFile.Mode.WRITE)
       try:
          # Read all lines in
          all_lines = fhandler.readlines()
          
          # See http://www.ncedc.org/ftp/pub/doc/cat5/cnss.catalog.5 for the
          # field description of the ANSS catalog
          # Actual position of the event is 102, but indexing begins with '0'
          event_position = 101
          
          for line in all_lines:
             # Extract event classifier from the line:  starting with column 101
             # NOTE: if more digits of precision are provided for the fields 
             #       preceeding the event type, ANSS '102' position gets shifted  
             # Exclude B, N, Q and H types of events, include all others (including
             # ones with missing type)
             pos = event_position
             line_len = len(line)
             #print "line: %s (line_len=%s, substr_131_4=%s)" \
             #      %(line, line_len, line[130:134])
             event_type_found = False
             
             while pos < line_len and event_type_found is False:
                if line[pos].isalpha() or \
                   line[pos].isspace():
                   event_type_found = True                   

                   if line[pos] != 'B' and \
                      line[pos] != 'N' and \
                      line[pos] != 'Q' and \
                      line[pos] != 'H':
                
                      #logger.info("Writing event: %s with event id[pos=%s]='%s' mag=%s" \
                      #            %(line.strip(), pos, line[pos], line[129:134]))
                      raw_data_fhandler.write(line)
                      
                   else:
                      ANSSDataSource.__logger.info("Skipping non-event line with event id='%s': %s" \
                                                   %(line[pos], line.strip()))

                   break
                      
                else:
                   pos += 1      
             
             # Log message if end of line has been reached without       
             if event_type_found is False:
                ANSSDataSource.__logger.warning("Could not identify event type for the line: '%s'. Skipping the event." \
                                                %line)
                      
       finally:
          fhandler.close() 
          raw_data_fhandler.close()
          

       self.filterRawCatalog(filtered_raw_data_file,
                             preprocessed_data_file)
          
         
      
    #----------------------------------------------------------------------------
    #
    # Prepare pre-processed catalog by filtering raw event data 
    #
    # Input: 
    #        raw_file - Raw, filtered by event type, catalog data file
    #        preprocessed_file - Filename for result pre-processed catalog
    #
    def filterRawCatalog(self,
                         raw_file, 
                         preprocessed_file):
       """ Prepare pre-processed catalog by filtering raw event data"""
        
        
       center_code_env = Environment.Environment.Variable[Environment.CENTER_CODE_ENV]
         
       script_path = os.path.join(center_code_env,
                                  'src', 
                                  'get_Catalog', 
                                  'getCatalog_PreProcess.Mag.awk')      
       command = "awk -v minMagnitude=%s -f %s %s > temp1.dat" \
                 %(self.MinMagnitude,
                   script_path, 
                   raw_file)
       Environment.invokeCommand(command)

       script_path = os.path.join(center_code_env,
                                  'src', 
                                  'get_Catalog', 
                                  'getCatalog_PreProcess.Loc.awk')      
       command = "awk -f %s temp1.dat > temp2.dat" %(script_path)
       Environment.invokeCommand(command)

       script_path = os.path.join(center_code_env, 
                                  'src', 
                                  'get_Catalog', 
                                  'getCatalog_PreProcess.sed')      
       command = "sed -f %s temp2.dat > %s" %(script_path, 
                                              preprocessed_file)
       Environment.invokeCommand(command)
        
       # Cleanup temporary files
       Environment.invokeCommand('rm -rf temp1.dat temp2.dat %s' %raw_file)

      
    #---------------------------------------------------------------------------
    #
    # Import utility for pre-processed catalog data into internal 
    # CSEP ZMAP format
    #
    # Input: 
    #        raw_file - Pre-processed catalog data file
    #        catalog_file - Optional file to save imported catalog to. Default
    #                       is None.
    #
    # Output: Numpy.array object with catalog data
    #
    @classmethod    
    def importToCSEP (cls,
                      raw_file,
                      catalog_file = None):
        """ Import utility for pre-processed catalog data into ZMAP format"""
        
        
        # Pre-allocate numpy array to hold catalog array
        output_str = Environment.invokeCommand('wc -l %s' %raw_file)
        num_lines = int(output_str.split()[0])
        
        catalog_array = np.zeros((num_lines,
                                  CSEPGeneric.Catalog.ZMAPFormat.NumColumns))

        catalog_array[:, CSEPGeneric.Catalog.ZMAPFormat.HorizontalError] = 2.0
        catalog_array[:, CSEPGeneric.Catalog.ZMAPFormat.DepthError] = 5.0
        catalog_array[:, CSEPGeneric.Catalog.ZMAPFormat.MagnitudeError] = 0.1

        for index, each_line in enumerate(CSEPFile.openFile(raw_file)):

            event = catalog_array[index, :]
            __adjust_date_by_day_flag = False
            
            # Have to read by characters since some of the fields might be missing
            event[CSEPGeneric.Catalog.ZMAPFormat.Longitude] = float(each_line[0:10])
            event[CSEPGeneric.Catalog.ZMAPFormat.Latitude] = float(each_line[11:20])
            event[CSEPGeneric.Catalog.ZMAPFormat.DecimalYear] = float(each_line[21:25])
            event[CSEPGeneric.Catalog.ZMAPFormat.Month] = float(each_line[26:28])
            event[CSEPGeneric.Catalog.ZMAPFormat.Day] = float(each_line[29:31])
            event[CSEPGeneric.Catalog.ZMAPFormat.Magnitude] = float(each_line[32:37])
            event[CSEPGeneric.Catalog.ZMAPFormat.Depth] = float(each_line[38:46])
            event[CSEPGeneric.Catalog.ZMAPFormat.Hour] = float(each_line[47:49])
            event[CSEPGeneric.Catalog.ZMAPFormat.Minute] = float(each_line[50:52])
            event[CSEPGeneric.Catalog.ZMAPFormat.Second] = float(each_line[53:60])

            # ANSS catalog provides seconds=60.0 for some events starting with 1962/4/13
            while event[CSEPGeneric.Catalog.ZMAPFormat.Second] >= 60.0:
                event[CSEPGeneric.Catalog.ZMAPFormat.Second] -= 60.0
                event[CSEPGeneric.Catalog.ZMAPFormat.Minute] += 1.0
                    
            while event[CSEPGeneric.Catalog.ZMAPFormat.Minute] >= 60.0:
                event[CSEPGeneric.Catalog.ZMAPFormat.Minute] -= 60.0
                event[CSEPGeneric.Catalog.ZMAPFormat.Hour] += 1.0

            if event[CSEPGeneric.Catalog.ZMAPFormat.Hour] >= 24.0:
                event[CSEPGeneric.Catalog.ZMAPFormat.Hour] -= 24.0
                __adjust_date_by_day_flag = True 
            
            event_date = datetime.datetime(int(event[CSEPGeneric.Catalog.ZMAPFormat.DecimalYear]),
                                           int(event[CSEPGeneric.Catalog.ZMAPFormat.Month]),
                                           int(event[CSEPGeneric.Catalog.ZMAPFormat.Day]),
                                           int(event[CSEPGeneric.Catalog.ZMAPFormat.Hour]),
                                           int(event[CSEPGeneric.Catalog.ZMAPFormat.Minute]),
                                           int(event[CSEPGeneric.Catalog.ZMAPFormat.Second]),
                                           CSEP.Time.microseconds(event[CSEPGeneric.Catalog.ZMAPFormat.Second]))
                
            if __adjust_date_by_day_flag is True:
                event_date = event_date + datetime.timedelta(hours=24)

            event[CSEPGeneric.Catalog.ZMAPFormat.DecimalYear] = CSEPUtils.decimalYear(event_date)
             
            # Check if horizontal error is provided
            value = each_line[61:68].strip()
            if len(value):
                value = float(value)
                
                if value == 0.0:
                    # For backward compatibility with Matlab codes, set to 1.0 if 
                    # value of zero is provided 
                    catalog_array[index, CSEPGeneric.Catalog.ZMAPFormat.HorizontalError] = 1.0
                else:
                    catalog_array[index, CSEPGeneric.Catalog.ZMAPFormat.HorizontalError] = value

            # Check if depth error is provided
            value = each_line[69:76].strip()
            if len(value):
                value = float(value)
                
                if value == 0.0:
                    # For backward compatibility with Matlab codes, set to 1.0 if 
                    # value of zero is provided
                    catalog_array[index, CSEPGeneric.Catalog.ZMAPFormat.DepthError] = 3.0
                else:
                    catalog_array[index, CSEPGeneric.Catalog.ZMAPFormat.DepthError] = value
                
            # Check if seismic network code can be converted to number
            try:
                event[CSEPGeneric.Catalog.ZMAPFormat.NetworkName] = int(each_line[77:80])
                
            except ValueError:
                # Do nothing, leave network at default value of "0"
                pass

        ### Filter for events with M >= 0.0
        selection, = np.where(catalog_array[:, CSEPGeneric.Catalog.ZMAPFormat.Magnitude] >= 0.0)
        catalog_array = catalog_array[selection, :]
        
        # Save catalog to the file if required
        if catalog_file is not None:
            np.savetxt(catalog_file, 
                       catalog_array) 

        return catalog_array
    
    

if __name__ == '__main__':
    
    import CSEPOptionParser
    from CSEPOptions import CommandLineOptions

    
    parser = CSEPOptionParser.CSEPOptionParser()
        
    # List of requred options
    required_options = [CommandLineOptions.YEAR,
                        CommandLineOptions.MONTH,
                        CommandLineOptions.DAY]
    options = parser.options(required_options)
    
    
    source = ANSSDataSource()
    source.download(datetime.datetime(options.year,
                                      options.month,
                                      options.day))
    
     