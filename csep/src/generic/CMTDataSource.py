"""
Module CMTDataSource
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, datetime, time, operator, shutil
import numpy as np

import CSEPFile, MatlabLogical, CSEPLogging, Environment, CSEP, CSEPGeneric, \
       CSEPUtils
from CatalogDataSource import CatalogDataSource
from CSEPInputParams import CSEPInputParams


# Environment variable to define directory path for working copy of SVN
# repository to store CMT raw data downloads
ARCHIVE_ENV = 'CMT_ARCHIVE_DIR'


#--------------------------------------------------------------------------------
#
# CMTCatalogSource
#
# This class provides an interface to extract Centroid-Moment-Tensor (CMT) 
# catalog data. The web-based data source provides catalog in "final" format 
# that has 6-months latency, and preliminary (or Quick CMT) data that contains 
# events for the last 6 months. This class acquires both data, and combines them
# in one file.
#
class CMTDataSource (CatalogDataSource):

    # Static data of the class
    Type = "CMT"
    
    # Number of 'ndk' format file lines per event
    LinesPerEvent = 5
    
    # Event date index into 'ndk' format line of tokens
    DateIndex = 1
    
    
    # Class to represent one-line per event of CMT format used internally by 
    # the CSEP
    class OneLinePerEventFormat (object):
        #=======================================================================
        # One-line-per-event format of CMT catalog:
        # column description
        # ===================
        # 1      eventid
        # 2      2-digit year
        # 3      month
        # 4      day
        # 5      time
        # 6      centroid time offset
        # 7      latitude
        # 8      longitude
        # 9      depth
        # 10     scalar moment exponent
        # 11     scalar moment base
        # 12     eigenvector plunge
        # 13     eigenvector azimuth
        # 14     eigenvector plunge
        # 15     eigenvector azimuth
        # 16     nodal plane %1 strike
        # 17     nodal plane %1 dip
        # 18     nodal plane %1 rake
        # 19     nodal plane %2 strike
        # 20     nodal plane %2 dip
        # 21     nodal plane %2 rake
        EventId = 0
        Year = 1
        Month = 2
        Day = 3
        Time = 4
        Latitude = 6
        Longitude = 7
        Depth = 8        
        ScalarMomentExponent = 9
        ScalarMomentBase = 10

    
    # FTP command to use for download
    __downloadSite = 'http://www.ldeo.columbia.edu/~gcmt/projects/CMT/catalog'
    
    # Directory for SVN working copy if used to archive raw data
    __archiveDir = None
    
    # Filename of final catalog
    __finalCatalogFilename = 'jan76_dec05.ndk'
    
    # Start date for final catalogs that posted by month on the CMT server
    __finalCatalogByMonthStartDate = datetime.date(2006, 1, 1)
    
    # Subdirectory of download location that contains latest final catalog data by
    # YEAR/month.ndk
    __finalCatalogByMonthDirectory = "NEW_MONTHLY"
    
    # Directory and filename of preliminary (Quick CMT) catalog
    __quickCatalogDir = "NEW_QUICK"
    __quickCatalogFilename = 'qcmt.ndk'
    
     # Parameter to specify if preliminary catalog data (QuickCMT for the last 6
    # months) should be included into the catalog
    __includePreliminaryOption = 'includePreliminary'
    
    # Dictionary of data source parameters and their default values
    __defaultOptions = {__includePreliminaryOption : False}
    
    # File extensions to store in SVN repository
    __dataTypes = ['.ndk']

    __logger = None
    
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    #        start_date - Start date for the catalog data. Default is 1/1/1977.
    #        download_data - Flag if raw data should be downloaded. Default is
    #                        True.
    #        pre_process_data - Flag if raw data should be pre-processed.
    #                           Default is True.
    #        args - Optional list of arguments that is specific to the
    #               data source. For example, flag if preliminary data
    #               should be downloaded from the CMT data source. Default
    #               is None.
    # 
    def __init__ (self, 
                  start_date = datetime.datetime(1977, 1, 1), 
                  download_data = True,
                  pre_process_data = True,
                  args = None):
        """ Initialization for CMTDataSource class."""

        if CMTDataSource.__logger is None:
           CMTDataSource.__logger = CSEPLogging.CSEPLogging.getLogger(CMTDataSource.__name__)
        
        # If SVN repository should be used to archive downloaded raw catalog data
        if ARCHIVE_ENV in os.environ:
            CMTDataSource.__archiveDir = os.environ[ARCHIVE_ENV]
        
        CatalogDataSource.__init__(self, start_date, 
                                         download_data, 
                                         pre_process_data,
                                         svn_working_dir = CMTDataSource.__archiveDir)
        
        self.__args = CSEPInputParams.parse(CMTDataSource.__defaultOptions,
                                            args)


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

        return CMTDataSource.Type
     

    #---------------------------------------------------------------------------
    #
    # Return start date for raw catalog data retrieved from data source
    #
    # Input: None.
    #
    # Output: start data of catalog data
    #
    def __getOptions (self):
        """ Return additional options used to retrieve raw catalog data from data source."""

        return self.__args
    
    Options = property(__getOptions, 
                         doc = "Additional options used to retrieve raw catalog data from data source")
     

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

        return 'one-line-per-event (please refer to https://intensity.usc.edu/trac/csep/wiki/Catalogs)'


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
       """ Extract raw CMT catalog for specified test date."""


       # Extract directory path to download data to:
       data_path, data_file = os.path.split(self.RawFile)
       
       local_final_catalog = os.path.join(data_path,
                                          CMTDataSource.__finalCatalogFilename) 
        
       # Download final data, append command output to the log file
       if CSEP.URL.retrieve(CMTDataSource.__downloadSite, 
                            local_final_catalog) is True:
          # Copy content of final catalog into expected filename
          shutil.copyfile(local_final_catalog, 
                          self.RawFile)

       else:
          # Raise an exception
          error_msg = "Failed to retrieve %s from %s" \
                      %(local_final_catalog,
                        CMTDataSource.__downloadSite)
          
          CMTDataSource.__logger.error(error_msg)            
          raise RuntimeError, error_msg
       
       
       # List of raw files to be removed at the end of download
       files_to_remove = [] # ['*.ndk'] store all raw files
          
       # Download final catalog that is provided individually (by month) 
       # starting with 1-1-2006, append command output to the log file
       curr_date = CMTDataSource.__finalCatalogByMonthStartDate
       
       # Keep track of last downloaded month for final catalog - to know the
       # beginning of the preliminary catalog
       download_month = curr_date
       url = os.path.join(CMTDataSource.__downloadSite,
                          CMTDataSource.__finalCatalogByMonthDirectory)
       
       # Keep track of last downloaded month for final catalog
       last_downloaded_month = None
       
       while curr_date.year <= test_date.year:
          
          # Download all available months for the year
          end_month = test_date.month
          
          # Get all months if it's not the testing year
          if curr_date.year != test_date.year:
             end_month = 12
          
          for month_index in xrange(1, end_month+1):
             
             download_month = curr_date.replace(month=month_index)
             
             # Format filename for the current month of the year to download
             filename = "%s%s.ndk" %(download_month.strftime('%b').lower(),
                                     download_month.strftime('%y'))
             filename = os.path.join(data_path,
                                     filename)
                                     
             if CSEP.URL.retrieve(os.path.join(url,
                                               "%s" %download_month.year),
                                  filename) is False:
             
                # Detect the last month downloaded for the final catalog -
                # it's going to be the start date for the preliminary catalog

                # Check if new data is posted in the file that has a year as a name
                filename = "%s" %download_month.year
                filename = os.path.join(data_path,
                                        filename)
                
                if CSEP.URL.retrieve(url, 
                                     filename) is True:

                    # Concatenate downloaded file to the cumulative file
                    command = 'cat %s >> %s' %(filename, 
                                               self.RawFile)
                    Environment.invokeCommand(command)
                     
                    # Extract last available month in the file from last event
                    # (last 5 lines)
                    fhandle = CSEPFile.openFile(filename)
                    all_lines = fhandle.readlines()
                    
                    tokens = all_lines[-CMTDataSource.LinesPerEvent].split()
                    last_date = datetime.date(*time.strptime(tokens[CMTDataSource.DateIndex],
                                                '%Y/%m/%d')[:3])

                    last_year = last_date.year
                    last_month = last_date.month + 1
                    if last_month > 12:
                       last_year += 1
                       last_month = last_month % 12
                    
                    # Re-set download date to the next month   
                    download_month = datetime.date(last_year, 
                                                   last_month,
                                                   download_month.day)

                files_to_remove.append(filename)
                
                # Log start date of preliminary data
                CMTDataSource.__logger.info('Quick CMT catalog start date is %s' %download_month)
                
                # To break outter most loop - set year to last year
                curr_date = curr_date.replace(year=test_date.year)                    
                break
             
             
             # Concatenate downloaded file to the cumulative file
             command = 'cat %s >> %s' %(filename, 
                                        self.RawFile)
             Environment.invokeCommand(command)
             
             last_downloaded_month = download_month
          
             
          # Increment year for download
          curr_date = curr_date.replace(year=curr_date.year + 1)    
          

       # Download preliminary CMT catalog data if such option was specified and
       # if final catalog ends before test date (to avoid events for the same month
       # to be included from final and preliminary catalogs)
       test_month_in_final_catalog = (last_downloaded_month.year == test_date.year and
                                      last_downloaded_month.month == test_date.month)
       
       if MatlabLogical.Boolean[self.__args[CMTDataSource.__includePreliminaryOption]] == \
          MatlabLogical.Boolean[True] and (test_month_in_final_catalog is False):

          local_quick_catalog = os.path.join(data_path,
                                             CMTDataSource.__quickCatalogFilename) 

          if CSEP.URL.retrieve(os.path.join(CMTDataSource.__downloadSite,
                                            CMTDataSource.__quickCatalogDir),
                               local_quick_catalog) is True:

             # Extract only events that begin after the end of final catalog:
             # extract every 5 lines of catalog data and parse out the date
             fhandle = CSEPFile.openFile(self.RawFile,
                                         CSEPFile.Mode.APPEND)
   
             append_lines = False
             
             for count, line in enumerate(open(local_quick_catalog,
                                               'rU')):
                
                if append_lines is False and count % CMTDataSource.LinesPerEvent == 0:
                   # This is first line for the event
                   tokens = line.split()
                   
                   # Second token is event date
                   if datetime.date(*time.strptime(tokens[CMTDataSource.DateIndex],
                                                   '%Y/%m/%d')[:3]) >= download_month:
                      
                      # Start appending data to the raw file with final data
                      # ATTN: Based on the assumption that all events are chronologically
                      #       sorted in the original file as downloaded from the
                      #       web-site.
                      CMTDataSource.__logger.info("Appending quick events beginning with %s" 
                                                  %tokens[CMTDataSource.DateIndex])
                      append_lines = True
                      
                
                if append_lines is True:
                   fhandle.write(line)
   
             # Explicitly close the file handle to guarantee write buffer being
             # flushed before SVN commit takes place
             fhandle.close()
                
          else:
          
             # Raise an exception
             error_msg = "Failed to retrieve %s from %s" \
                         %(local_quick_catalog,
                           CMTDataSource.__downloadSite)
             
             CMTDataSource.__logger.error(error_msg)            
             raise RuntimeError, error_msg
      

       ### 1) Check for data change if any and commit updates to SVN if there is a change,
       ### 2) Tag main trunk in repository
       self.SVN.commit("%s data to process %s test date, committed on %s" 
                       %(CMTDataSource.Type,
                         test_date.date(),
                         datetime.datetime.now()),
                        CMTDataSource.__dataTypes)
      
      
       # Cleanup temporary files
       if len(files_to_remove):
           Environment.invokeCommand('rm -rf ' + ' '.join(files_to_remove))
          

    #----------------------------------------------------------------------------
    #
    # Pre-process catalog data into 'short'-format. It reduces catalog data from
    # original 5 lines per event to 1 line per event 'short' format.
    #The .ndk format is written in following fixed format (please see
    # http://jumpy.igpp.ucla.edu/~kagan/fpsh.txt for a detailed format explanation)
    #
    # CMT is using the following Format format to write catalog data:
    #line 1
    #        write(lu2,"(a4,1x,i4.4,'/',i2.2,'/',i2.2,1x,i2.2,':',i2.2,':',a4,1x,f6.2,f8.2,f6.1,f4.1,f4.1,1x,6a4)")
    #     1    isour,lyear,month,iday,ih,min,ch4,eplat,eplong,depth,xmb,xms, (ireg(i),i=1,6)
    #line 2
    #        write(lu2,"(a16,' B:',i3,i5,i4,' S:',i3,i5,i4,' M:',i3,i5,i4,' CMT:',i2,1x,a6,f5.1)")
    #     1     devent(1:16),isb,icb,icutb,iss,ics,icuts,ism,icm,icutm,itypcmt,ch6,durt
    #line 3
    #        write(lu2,"('CENTROID:',f9.1,f4.1,f7.2,f5.2,f8.2,f5.2,f6.1,f5.1,1x,a4,1x,a16)")
    #     1    TORG,ERRT,EPA,ERRA,EPO,ERRO,XD,ERRD,ch4,timestamp
    #line 4
    #        write(lu2,"(i2,6(f7.3,f6.3))") iexp,(xm(i),xerr(i),i=1,6)
    #line 5
    #        write(lu2,"('V',i2.2,3(f8.3,i3,i4),f8.3,2(i4,i3,i5))")
    #     1    iver, (ev(i),ipl(i),iaz(i),i=1,3),sc,(istr(i),idip(i), islp(i),i=1,2)
    #
    # Event example from raw CMT catalog
    #MLI  1976/01/01 01:29:39.6 -28.61 -177.64  59.0 6.2 0.0 KERMADEC ISLANDS REGION 
    #M010176A         B:  0    0   0 S:  0    0   0 M: 12   30 135 CMT: 1 BOXHD:  9.4
    #CENTROID:     13.8 0.2 -29.25 0.02 -176.96 0.01  47.8  0.6 FREE O-00000000000000
    #26  7.680 0.090  0.090 0.060 -7.770 0.070  1.390 0.160  4.520 0.160 -3.260 0.060
    #V10   8.940 75 283   1.260  2  19 -10.190 15 110   9.560 202 30   93  18 60   88    
    #
    #The explaination of each field in the short format is as follows,
    # 
    #1) Number  
    #2) Year 
    #3) Month
    #4) Date
    #5) Time 
    #6) Centroid-Time
    #7) Centroid-Latitude
    #8) Centroid-longitude
    #9) Centroid-depth
    #10) Exponent
    #11) Scalar moment, to be multiplied by 10**(exponent)
    #12) Plunge of 1st eigen vector
    #13) Azimuth of 1st eigen vector
    #14) Plunge of 2nd eigen vector
    #15) Azimuth of 2nd eigen vector
    #16) Strike for first nodal plane of the best-double-couple mechanism
    #17) Dip for first nodal plane of the best-double-couple mechanism
    #18) Rake for first nodal plane of the best-double-couple mechanism
    #19) Strike for second nodal plane of the best-double-couple mechanism 
    #20) Dip for second nodal plane of the best-double-couple mechanism
    #21) Rake for second nodal plane of the best-double-couple mechanism
    #
    # Input:
    #        raw_data_file - Raw catalog data file.
    #        preprocessed_data_file - Filename for output pre-processed data.
    #
    # Output: None.
    #
    def preProcess (self, raw_data_file, preprocessed_data_file):
        """ Pre-process raw CMT data into 'short' (one line instead of five lines
            per event) format."""
            
        fhandler = CSEPFile.openFile(raw_data_file)
        all_lines = fhandler.readlines()
        
        output_fhandler = CSEPFile.openFile(preprocessed_data_file, 
                                            CSEPFile.Mode.WRITE)
        try:
            count=0

            lines_per_event = 5
            num_events = len(all_lines)/lines_per_event
            
            while count < num_events:

                event_lines = all_lines[count*lines_per_event:(count+1)*lines_per_event]
                
#===============================================================================
#                Yan's formatting of one-line-per-event catalog:
#                5 READ (10, 7, END=20) eqh(15), IYE, IMO, IDA, IH, IMI, SEC,
#                        DT, ALA, ALO, DEPTH, MOM, AMOM, (EQH(LL), LL = 11, 14)
#                7 FORMAT (I6, 4I3, 1X, I2, 1X, F4.1, F7.1, 1X, F6.2, 1X,
#                          1 F7.2, 1X, F5.1, 1X, I2, 1X, F5.2, 2(1X, I2,1X, I3))
#===============================================================================

                # Event count
                count=count+1
                output_fhandler.write('%6d ' %count)

                # Date of the event
                line_index = 0
                start_index = 4
                end_index = 15
                date_obj = datetime.datetime.strptime(event_lines[line_index][start_index:end_index].strip(),
                                                      "%Y/%m/%d")
                    
                # Time of the event: copy string from raw CMT catalog (some 
                # events will have value of 60.0 for leap second)
                start_index = 15
                end_index = 26
                time_tokens = event_lines[line_index][start_index:end_index].strip().split(':')
                hour = int(time_tokens[0])
                mins = int(time_tokens[1])
                secs = float(time_tokens[2])
                
                # Read centroid time offset in respect to the relative time
                # CMT centroid format: 'CENTROID:',f9.1,f4.1,f7.2,f5.2,f8.2,f5.2,f6.1,f5.1
                line_index = 2
                event_lines[line_index] = event_lines[line_index].replace('CENTROID:', '')
                start_index = 0
                end_index = 9
                centroid_secs = float(event_lines[line_index][start_index:end_index])

                # Add centroid time to the relative time
                secs += centroid_secs
                
                # Fix for Trac ticket #187: Negative centroid time offset 
                # relative to 00:00 seconds in CMT raw catalog results in invalid time
                if secs < 0.0:
                    secs += 60.0
                    mins -= 1
                
                if mins < 0:
                    mins += 60
                    hour -= 1
                    
                if hour < 0:
                    hour += 24
                    date_obj = date_obj - datetime.timedelta(hours=24)
                
                while secs >= 60.0:
                    secs -= 60.0
                    mins += 1
                    
                while mins >= 60:
                    mins -= 60
                    hour += 1

                if hour >= 24:
                    hour -= 24
                    date_obj = date_obj + datetime.timedelta(hours=24)
                
                    
                output_fhandler.write(date_obj.strftime("%y %m %d "))

                # Write centroid time to one-line-per-event formatted file
                output_fhandler.write('%02d:%02d:%04.1f' %(hour,
                                                           mins,
                                                           secs))

                # Write centroid offset: Yan's "F7.1, 1X" format
                output_fhandler.write('%7.1f ' %centroid_secs)
                
                # Write centroid latitude: Yan's "F6.2, 1X" format
                start_index = 13
                end_index = 20
                centroid_lat = float(event_lines[line_index][start_index:end_index])
                
                output_fhandler.write('%6.2f ' %centroid_lat)
                
                # Write centroid longitude
                start_index = 25
                end_index = 33
                centroid_lon = float(event_lines[line_index][start_index:end_index])
                
                output_fhandler.write('%7.2f ' %centroid_lon)

                # Write centroid depth
                start_index = 38
                end_index = 44
                centroid_dep = float(event_lines[line_index][start_index:end_index])
                
                output_fhandler.write('%5.1f ' %centroid_dep)

                # Write exponent
                line_index = 3
                # Yan's format "I2, 1X, F5.2, 2(1X, I2,1X, I3)"
                
                output_fhandler.write('%s ' %event_lines[line_index][0:2])
                
                # Write scalar moment of magnitude (CMT is providing as f8.3 value)
                line_index = 4
                # Don't include trailing zero at the end of value - %5.3f formatting
                # string forces 3 spaces for digits after point, resulting in 6 digits
                # for values with two digits for integer part: '15.300' vs. expected
                # '15.30'
                precision_digits = 3
                if event_lines[line_index][55] == '0':
                    precision_digits = 2
                
                
                output_fhandler.write('%5.*f' %(precision_digits,
                                                float(event_lines[line_index][49:56].strip())))

                # CMT 5th line format: "('V',i2.2,3(f8.3,i3,i4),f8.3,2(i4,i3,i5))"
                start_index = 11
                end_index = 14
                output_fhandler.write(event_lines[line_index][start_index:end_index])

                start_index = 14
                end_index = 18
                output_fhandler.write(event_lines[line_index][start_index:end_index])

                start_index = 41
                end_index = 44
                output_fhandler.write(event_lines[line_index][start_index:end_index])

                start_index = 44
                end_index = 48
                output_fhandler.write(event_lines[line_index][start_index:end_index])
                output_fhandler.write(' ')
                
                # Write strike, dip and rake values for two planes (not read by Yan's code)
                start_index = 57
                end_index = 80
                output_fhandler.write(event_lines[line_index][start_index:end_index])

                output_fhandler.write('\n')
        
        finally:
                fhandler.close()
                output_fhandler.close()
      
        
    #----------------------------------------------------------------------------
    #
    # Import utility for pre-processed catalog data into internal CSEP ZMAP format
    #
    # Input: 
    #        raw_file - Pre-processed catalog data file
    #        catalog_file - Optional file to save imported catalog to. Default
    #                       is None.
    #
    # Output: catalog_file
    #
    @classmethod
    def importToCSEP (cls,
                      raw_file,
                      catalog_file = None):
        """ Import utility for pre-processed catalog data into ZMAP format"""


        # Check for an empty file: np.loadtxt() raises an exception if an empty file
        catalog_data = np.fromfile(raw_file)
        
        if catalog_data.size == 0:
            # CSEP is relying on 2-dim arrays
            catalog_data.shape = 0, 0
            
        else:
            # Have to use dtype=np.object since one-line format of CMT catalog
            # has mixed data types
            catalog_data = CSEPFile.read(raw_file,
                                         np.object)
        
        if catalog_file is not None:
            np.savetxt(catalog_file,
                       catalog_data,
                       fmt='%s')
            
        return catalog_data

    
    #----------------------------------------------------------------------------
    #
    # Cut catalog data to geographical area.
    #
    # Input: 
    #         catalog_data - Numpy.array object with catalog data stored in
    #                         np.object datatype.
    #         area_file - Filename for geographical area.
    #         result_file - Filename for result catalog data.
    #
    # Output: result_file
    #
    @classmethod
    def cutToArea (cls,
                   catalog_data, 
                   area_file, 
                   result_file = None):
        """ Cut catalog data to geographical area."""


        # There is no need to filter by geographical region if region file
        # is not provided, or catalog is empty
        result_data = catalog_data
        
        if area_file is not None and len(area_file) != 0 and catalog_data.size != 0:

           # Numeric representation of the area cells 
           area_boundaries = np.loadtxt(area_file,
                                        comments='# ') 

           if area_boundaries.size == 0:
              
              error_msg = "Empty area file '%s' is provided." %area_file
              raise RuntimeError, error_msg

           # if area file is only one-dimensional, reshape into 2-dim array
           if area_boundaries.ndim == 1:
               # Re-size inplace (reshape() returns new array object)
               area_boundaries.shape = (1,4) 
              
              
           __areaMinLatIndex = 0
           __areaMaxLatIndex = 1
           __areaMinLongIndex = 2
           __areaMaxLongIndex = 3
           
           catalog_coords = catalog_data[:, (CMTDataSource.OneLinePerEventFormat.Longitude,
                                             CMTDataSource.OneLinePerEventFormat.Latitude)].astype(np.float)
                                             
               
           selected_events = np.zeros((catalog_data.shape[0],),
                                      dtype = np.bool)
           for region_cell in area_boundaries: 

              selection, = np.where((catalog_coords[:, 0] >= region_cell[__areaMinLongIndex]) & \
                                    (catalog_coords[:, 0] <= region_cell[__areaMaxLongIndex]) & \
                                    (catalog_coords[:, 1] >= region_cell[__areaMinLatIndex]) & \
                                    (catalog_coords[:, 1] <= region_cell[__areaMaxLatIndex]))

              selected_events[selection] = True

     
#              print 'selection.shape=', selected_events.shape, \
#                    'catalog_data.shape=', catalog_data.shape 
           
           
           result_data = catalog_data[selected_events, :]

        # Save catalog if requested 
        if result_file is not None:
            np.savetxt(result_file,
                       result_data,
                       fmt='%s')
           
        return result_data
     

    #===========================================================================
    # Parse string representation of timestamp into datetime.time object
    #===========================================================================
    @staticmethod
    def __parseTimeString (timestamp):
        """Parses string of HH:MM:SS.MM into datetime.time object"""
        
        time_str, microsec_str = timestamp.split('.')

        microsec = int(microsec_str.ljust(6, '0')[:6])
        event_time = datetime.datetime.strptime(time_str,
                                                '%H:%M:%S')
        
        # Could be a bug in Python 2.5: replace does not seem to work,
        # printing event_time.microsecond still displays '0'
        # event_time.replace(microsecond = microsec)
        
        # Could be a bug in Python 2.5: datetime.time() returns time object 
        # without microsecods ===> as a workaround, have to explicitly construct
        # new time() object with hr, min, sec, microsec values 
        return datetime.time(event_time.hour,
                             event_time.minute,
                             event_time.second,
                             microsec)
        
            
    #----------------------------------------------------------------------------
    #
    # Cut catalog data by time period.
    #
    # Input: 
    #         catalog_data - Numpy.array object with catalog data stored in
    #                         np.object datatype.
    #         start_time - datetime object that represents start date for 
    #                      the period.
    #         stop_time - datetime object that represents end date for the period.
    #         result_file - Filename for result catalog data.      
    #         start_time_sign - Matlab sign for start_time boundary. 
    #                           Default is greater or equal sign (>=).
    #         stop_time_sign - Matlab sign for start_time boundary. 
    #                           Default is less or equal sign (<=).
    #
    # Output: result_file
    #
    @classmethod
    def cutToTimePeriod (cls,
                         catalog_data, 
                         start_time, 
                         stop_time,
                         result_file = None,
                         start_time_sign = operator.ge,
                         stop_time_sign = operator.le):
        """ Cut catalog data to time period."""


        cut_to_time_catalog = catalog_data
        
        # No need to cut empty catalog
        if catalog_data.size != 0:

            # Read data and time from catalog array
            catalog_date = np.array([datetime.datetime.combine(datetime.datetime.strptime('/'.join([event[CMTDataSource.OneLinePerEventFormat.Year],
                                                                                                    event[CMTDataSource.OneLinePerEventFormat.Month],
                                                                                                    event[CMTDataSource.OneLinePerEventFormat.Day]]),
                                                                                          '%y/%m/%d').date(),
                                                               CMTDataSource.__parseTimeString(event[CMTDataSource.OneLinePerEventFormat.Time])) for
                                     event in catalog_data])
    
            selection, = np.where((start_time_sign(catalog_date, start_time)) & \
                                  (stop_time_sign(catalog_date, stop_time)))
            cut_to_time_catalog = catalog_data[selection, :]
         
        # Save catalog to the file if required
        if result_file is not None:
            
            # This method is the final filtering step in preparation of the
            # input catalog to be passed to the models to generate forecast.
            # KJSS forecasts use internal binary format and expect ASCII input
            # catalog in specific format (6 digits for event id, etc.).
            # Have to specify explicit format in order for the KJSS models to
            # properly convert ASCII input catalog to their binary format. 
            np.savetxt(result_file, 
                       cut_to_time_catalog,
                       fmt=('%6s', '%s', '%s', '%s', '%s', # eventID, date, time 
                            '%6s', '%6s', '%7s', '%5s',    # centroid data
                            '%s', '%5s', '%2s', '%3s', '%2s', '%3s', # exponent, scalar moment of magnitude
                            '%3s', '%2s', '%4s', '%3s', '%2s', '%4s')) # not read by KJSS model 

        return cut_to_time_catalog
               
        
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
    #         catalog_file - Filename for catalog data
    #         area_file - Area file for catalog filtering
    #         result_file - Filename for result data
    #         probability_column - Column index for independence probability. This
    #                              column is available for declustered catalog only. 
    #                              Default is 0.
    #
    # Output: Directory that stores catalog modifications
    # 
    @classmethod
    def modifications (cls,
                       catalog_file, 
                       area_file, 
                       result_file, 
                       probability_column = 0):
        """ Create catalog modifications by applying randomized uncertainties 
            to the original catalog"""

        # Don't generate catalog uncertainties - information is not available in
        # one-line per event pre-processed catalog
        return None


    #===========================================================================
    # Compute moment magnitude 
    #===========================================================================
    @staticmethod
    def __momentMagnitude (mag_exponent,
                           mag_base):
        """Compute moment magnitude m_w using Eq'n 7 from Hanks & Kanamori (1979)"""
        
       
        # Filter by magnitude: formulas are provided by Jeremy on 2008/06/02:
        # Scalar moment
        M_0 = mag_base * np.power(10,  mag_exponent)

        # Compute moment magnitude m_w using Eq'n 7 from Hanks & Kanamori (1979):
        m_w = (2.0/3.0) * np.log10(M_0) - 10.7
           
        return m_w


    #----------------------------------------------------------------------------
    #
    # Filter catalog data based on specified geographical location, 
    # minimum magnitude, maximum depth, and starting date for the forecast 
    # model.
    #
    # Input: 
    #         catalog_data - Numpy.array object with catalog data stored in
    #                         np.object datatype.
    #         area_file - Area file for catalog filtering
    #         result_file - Filename for result data.
    #         result_variable - Name of Matlab variable to store results to. 
    #                           Default is 'mCatalog'.
    #
    # Output: result_file
    #
    @classmethod
    def filter (cls,
                catalog_data, 
                area_file, 
                threshold,
                result_file = None):
        """ Filter catalog data based on specified geographical location, 
            minimum magnitude, maximum depth, and starting date for the forecast 
            model as provided by 'threshold' object."""
        

        cut_to_area_catalog = CMTDataSource.cutToArea(catalog_data, 
                                                      area_file)

        filtered_catalog = cut_to_area_catalog
        
        # No need to filter empty catalog
        if cut_to_area_catalog.size != 0:
            filter_data = cut_to_area_catalog[:, (CMTDataSource.OneLinePerEventFormat.ScalarMomentExponent,
                                                  CMTDataSource.OneLinePerEventFormat.ScalarMomentBase,
                                                  CMTDataSource.OneLinePerEventFormat.Depth)].astype(np.float)
    
            cut_to_area_catalog[:, CMTDataSource.OneLinePerEventFormat.ScalarMomentBase] = \
               CMTDataSource.__momentMagnitude(filter_data[:, 0],
                                               filter_data[:, 1])
    
            selection, = np.where((cut_to_area_catalog[:, CMTDataSource.OneLinePerEventFormat.ScalarMomentBase] >= threshold.MinMagnitude) & \
                                  (filter_data[:, 2] <= threshold.MaxDepth))
    
            filtered_catalog = cut_to_area_catalog[selection, :]
        
        # Convert observation catalog to Matlab format for evaluation purposes
        CMTDataSource.__toZMAP(filtered_catalog, 
                               result_file)
        

    #===========================================================================
    # Convert CMT catalog in one-line-per-event format to ZMAP format
    #
    # Inputs:
    #         catalog_data - Numpy.array object with catalog data
    #
    # Outputs: Numpy.array object with array data in ZMAP format 
    #===========================================================================
    @staticmethod
    def __toZMAP (catalog_data,
                  result_file = None):
        """ Convert CMT catalog in one-line-per-event format to ZMAP format. """
        

        zmap_catalog = catalog_data
        
        if catalog_data.size != 0:
        
            # datatime of all catalog events
            catalog_date = np.array([datetime.datetime.combine(datetime.datetime.strptime('/'.join([event[CMTDataSource.OneLinePerEventFormat.Year],
                                                                                                    event[CMTDataSource.OneLinePerEventFormat.Month],
                                                                                                    event[CMTDataSource.OneLinePerEventFormat.Day]]),
                                                                                          '%y/%m/%d').date(),
                                                                                          CMTDataSource.__parseTimeString(event[CMTDataSource.OneLinePerEventFormat.Time])) \
                                     for event in catalog_data])
            
            # Array of hour, minute and seconds.miliseconds        
            events_time_tokens = np.array([each_time.split(':') for each_time in 
                                           catalog_data[:, CMTDataSource.OneLinePerEventFormat.Time]])
            
            ### Populate ZMAP format catalog with CMT data
            zmap_catalog = np.zeros((catalog_data.shape[0], 
                                     CSEPGeneric.Catalog.ZMAPFormat.NumColumns))
            
            # Longitude
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Longitude] = \
               catalog_data[:, CMTDataSource.OneLinePerEventFormat.Longitude]
                
            # Latitude
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Latitude] = \
               catalog_data[:, CMTDataSource.OneLinePerEventFormat.Latitude]
            
            # Decimal year   
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.DecimalYear] = \
               np.array([CSEPUtils.decimalYear(each_date) for each_date in catalog_date])
                          
            # Month
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Month] = np.array([each_date.month for each_date in catalog_date])
                
            # Day
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Day] = np.array([each_date.day for each_date in catalog_date])
    
            # Hour
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Hour] = np.array(events_time_tokens[:, 0])
            
            # Minutes
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Minute] = np.array(events_time_tokens[:, 1])
    
            # Seconds
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Second] = np.array(events_time_tokens[:, 2])
                
            # Magnitude (replaced by filter() method with moment magnitude)
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Magnitude] = \
               catalog_data[:, CMTDataSource.OneLinePerEventFormat.ScalarMomentBase]
                
            # Depth
            zmap_catalog[:, CSEPGeneric.Catalog.ZMAPFormat.Depth] = \
               catalog_data[:, CMTDataSource.OneLinePerEventFormat.Depth]
           
        if result_file is not None:
            np.savetxt(result_file,
                       zmap_catalog)
            
        ### ATTN: returned catalog is of mixed datatypes - force type conversion
        ###       if returned catalog is to be used in calculations
        return zmap_catalog
            
            
    #----------------------------------------------------------------------------
    #
    # decluster
    # 
    # This method declusters catalog data according to the Reasenberg declustering
    # algorithm.
    #
    # Input: 
    #         catalog_file - Filename for catalog data.
    #         result_file - Filename for result data.mCatalog = getCatalog_ImportCMT('src/generic/test/data/GlobalModels/oneLineCMTFromYan.dat')
    #
    # Output: result_file
    #
    @classmethod
    def declusterReasenberg (cls,
                             catalog_file, 
                             result_file):
        """ Decluster catalog."""

        raise RuntimeError, "declusterReasenberg() method is not implemented"

