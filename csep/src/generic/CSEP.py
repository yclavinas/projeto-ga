"""
CSEP module
"""

from __future__ import with_statement

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, operator, urllib2, datetime, re
from dateutil import tz
import CSEPLogging, CSEPFile


# CSEP Namespace
NAMESPACE = "scec.csep"


# Dictionary that maps string representation of the operator to actual operator
Operator = {'>=' : operator.ge,
            '>' : operator.gt,
            '<=' : operator.le,
            '<' : operator.lt}

# $CENTERCODE sub-directory with configuration files specific to the 
# testing center
TestingCenterConfigDir = "TestingCenterConfiguration" 

Version = '13.4.0'

# Flag used by unit and acceptance tests (stores intermediate data products to 
# files for further evaluation)
DebugMode = False


#-------------------------------------------------------------------------------
#
# This module stores variables specific to the CSEP environment.
#

# Catalog related variables
class Catalog (object):
    
    
    # Variable name for catalogs with applied uncertainties
    UncertaintiesVar = "mModifications"     

    class Filename (object):
        
        # Two different filenames for catalog come from legacy Matlab codes
        # where different Matlab variable was used to store catalog
        # Name of undeclustered catalog
        Undeclustered = "catalog.nodecl.dat"
        
        # Name of declustered catalog
        Declustered = "catalog.decl.dat"

        # Filename to store catalog uncertainties to 
        Uncertainties = "catalog.modifications.mat"
        
        # Parameter file used by declustering algorithm 
        DeclusterParameter = "DeclusterParameter-randomSeed.txt"
        

    # Number of simulations for declustering algorithm
    NumDeclusterSimulations = 1000
    
    # Number of catalogs with applied uncertainties
    NumUncertainties = 1000

    # Flag to apply depth error for catalog uncertainties
    UseHorizontalError = True
    
    # Flag to apply horizontal error for catalog uncertainties
    UseDepthError = True
    
    # Flag to apply magnitude error for catalog uncertainties
    UseMagnitudeError = True
    
    # Initialize variables (as specified on a command-line)
    @staticmethod
    def initialize (num_decluster_simulations,
                    num_catalog_variations,
                    horizontal_error = True,
                    depth_error = True,
                    magnitude_error = True):
        """ Initialize Catalog settings"""

        Catalog.NumDeclusterSimulations = num_decluster_simulations
        Catalog.NumUncertainties = num_catalog_variations
        Catalog.UseHorizontalError = horizontal_error
        Catalog.UseDepthError = depth_error
        Catalog.UseMagnitudeError = magnitude_error


# Forecast related variables
class Forecast (object):

   # Flag if forecast weights should be enabled during evaluation 
   UseWeights = True

   # Flag if master XML template should be used by forecast models for 
   # evaluation tests - to guarantee the same dimensions and bin order for 
   # all models
   UseXMLMasterTemplate = False
 
   # Flag to disable validation of the forecast in XML format as generated
   # by the model code 
   # (please see Trac ticket #177: XML format of forecast should still be 
   # passed through master XML template)
   ApplyXMLMasterValidation = True
      
   # Flag if forecast map should be generated - default is False
   GenerateMap = False
   
   # File postfix used by forecast files that are based on XML master template
   FromXMLPostfix = '-fromXML'

   # File prefix to use for forecast and observation data that are inputs
   # to the map generating routines
   MapReadyPrefix = 'MapReady_'
   
   # File prefix to use for map images
   MapPrefix = 'Map_'

   # Option to specify type of the forecast
   Type = 'type'
   AlarmBasedType = 'AlarmBased'
   RateBasedType = 'RateBased'

   # Initialize variables (as specified on a command-line)
   @staticmethod
   def initialize (forecast_weights = True,
                   forecast_xml_template = False,
                   validate_xml_forecast = True,
                   forecast_map = False):
       """ Initialize Forecast settings"""

       Forecast.UseWeights = forecast_weights
       Forecast.UseXMLMasterTemplate = forecast_xml_template
       Forecast.ApplyXMLMasterValidation = validate_xml_forecast
       Forecast.GenerateMap = forecast_map


   #--------------------------------------------------------------------
   #
   # Returns expected filename for the the model data that is
   # based on XML template.
   #
   # Input: 
   #        file_path - Path to the file.
   #        extension - File extension of interest. Default is Matlab file
   #                    extension.
   #
   # Output:
   #         Expected filename
   #
   @staticmethod
   def fromXMLTemplateFilename (file_path, 
                                extension = CSEPFile.Extension.ASCII):
      """ Returns filename that is based on XML template"""

        
      # Get rid of FromXMLPostfix (if any) from filename
      filename = re.sub(Forecast.FromXMLPostfix,
                        '',
                        file_path)
        
      # Replace extension with 'fromXML.extension'
      file_from_xml = re.sub('([.][^.]+$)', 
                             Forecast.FromXMLPostfix + 
                             extension,
                             filename)
      return file_from_xml
    

# Date and time related variables
class Time (object):  

   # Format string to be used by ISO8601 format
   ### From Python docs: New in version 2.6: time and datetime  objects support
   ### a %f  format code which expands to the number of microseconds in the 
   ### object, zero-padded on the left to six places. 
   ISO8601Format = "%Y-%m-%dT%H:%M:%S"
   
   DateTimeFormat = "%Y/%m/%d %H:%M:%S"
   
   DateTimeSpaceFormat = "%Y %m %d %H:%M:%S"
   
   DateFormat = '%Y-%m-%d'
   
   # Seconds in one hour
   __secondsPerHour = 3600
   
   #----------------------------------------------------------------------------
   # Extract 'microseconds' value from given 'seconds' value
   #
   # Input:
   #        seconds - Floating point value that represents seconds of the
   #                  timestamp.
   #
   # Output: Integer value representing microseconds of the timestamp
   # 
   @staticmethod
   def microseconds(seconds):
       
       return int((seconds - int(seconds)) * 1e6)
   
   
   # Get offset in hours for local date and time from UTC
   #
   # Input:
   #        date_time - datatime object that represents local date and time
   #
   # Output:
   #        UTC offset in hours
   #   
   def UTCOffset (date_time):
      """ Get UTC offset in hours for local date and time."""
      
      local_date = datetime.datetime(date_time.year,
                                     date_time.month,
                                     date_time.day, 
                                     tzinfo=tz.tzlocal())        
      
      utc_date = datetime.datetime(date_time.year,
                                   date_time.month,
                                   date_time.day, 
                                   tzinfo=tz.tzutc())        
      diff = local_date - utc_date

      return diff.seconds/Time.__secondsPerHour
   
   UTCOffset = staticmethod(UTCOffset)
   

# Utility class to store generic data attributes to parse information about 
# downloaded from the web files.   
class URL (object):
   
   # Keywords used to parse information about downloaded data from the web
   __contentType = 'Content-Type'
   __notFoundError = '404 Not Found'
   
   WebPageType = 'text/html'
   DataPageType = 'text/plain'
   
   
   #-----------------------------------------------------------------------------
   # retrieve
   # 
   # Download specified file at url to the local file at url_file_path. 
   # It checks the type of downloaded file content, and raises an exception if
   # it's other than expected one.
   #
   # Inputs:
   #         url_address - URL address of the file
   #         url_file - Name of the file to download
   #         url_type - Expected content type of the file. Default is 
   #                    URL.__dataPageType.
   #
   # Output:
   #         True if file successfully was downloaded, False otherwise
   #
   @staticmethod
   def retrieve(url_address, 
                url_file_path, 
                url_type=DataPageType):
       """Download specified file at URL."""

       url_path, url_file = os.path.split(url_file_path)
       CSEPLogging.CSEPLogging.getLogger(__name__).info("Downloading %s from %s"
                                                        %(url_file, url_address))
       
       # Trac ticket #277: Failure to dowload one of existing CMT *ndk final 
       # calalogs results in earlier date used for preliminary catalog
       # Had to switch to use urllib2 to be able to parse out exception codes
       request = urllib2.Request(os.path.join(url_address, url_file))
       
       try:
           data = urllib2.urlopen(request)
           data_str = data.read()

           # Save data to local file
           with open(url_file_path, 'w') as fhandle:
               fhandle.write(data_str)
           
           # Fix for Trac ticket #173: Check for downloaded raw catalog file not 
           # being empty
           if len(data_str) == 0:
               error_msg = "%s: Downloaded data '%s' is empty" %(CSEPLogging.CSEPLogging.frame(URL),
                                                                 url_file_path)
               CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
               raise RuntimeError, error_msg
           
           # Acquire information about retrieved data and verify that content type
           # is as expected
           info = data.info()
           file_type = info.getheader(URL.__contentType)
    
           if file_type.find(url_type) < 0:
              # File content is not of expected type
              error_msg = "Downloaded '%s' file content has unexpected type: got '%s',\
expected '%s'" %(url_file_path, 
                 file_type, 
                 url_type)
        
              CSEPLogging.CSEPLogging.getLogger(__name__).info(error_msg)
              return False
       
       except urllib2.URLError, error:

           if hasattr(error, 'reason'):
               error_msg = "%s: Error reaching %s to extract '%s': %s" %(CSEPLogging.CSEPLogging.frame(URL),
                                                                         url_address,
                                                                         url_file,
                                                                         error.reason)
               CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
               raise RuntimeError, error_msg

           elif hasattr(error, 'code'):
               if error.code != 404:
                   error_msg = "%s: Error downloading '%s': %s" %(CSEPLogging.CSEPLogging.frame(URL),
                                                                  url_file_path,
                                                                  str(error))
                   CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
                   raise RuntimeError, error_msg
               
               else:
                   error_msg = "%s: file '%s' does not exist" %(CSEPLogging.CSEPLogging.frame(URL),
                                                                os.path.join(url_address,
                                                                             url_file))
                   CSEPLogging.CSEPLogging.getLogger(__name__).info(error_msg)
                   
                   # If file does not exist, return flag that file was not downloaded
                   return False
       
       return True
 

class OnError (object):
    
    @staticmethod
    def shutil (function, path, excinfo):
         """ Log error message as generated by "shutil" Python module """
         
         
         # If exception is raised, report it and print the backtrace
         exc_type, exc_value = excinfo[:2]
              
         if exc_type is not None and exc_value is not None:

           error_msg = "Exception occurred calling %s on %s file: %s = %s" \
                        %(function, 
                          path, 
                          exc_type, 
                          exc_value)
                  
           CSEPLogging.CSEPLogging.getLogger(__name__).warning(error_msg) 
         
         
