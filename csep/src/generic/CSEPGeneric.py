"""
Module CSEPGeneric
"""

__version__ = "$Revision: 4150 $"
__revision__ = "$Id: CSEPGeneric.py 4150 2012-12-19 03:08:43Z liukis $"


import os, math, datetime, scipy.io, operator, re
import numpy as np

import MatlabLogical, CSEPFile, CSEP, Environment, CSEPLogging, CSEPUtils
from cseprandom import CSEPRandom


#--------------------------------------------------------------------------------
#
# CSEPGeneric.
#
# This module contains generic routines that serve as interface to the Matlab 
# code to process catalog, forecast, and test results data.
#

# Filename for matlab script to invoke
__MATLAB_SCRIPT = "invoke.m"    

# Filename for the Matlab output
__MATLAB_OUTPUT_FILE = "invoke_output.txt"


# Logger object for the module
__logger = None


#-------------------------------------------------------------------------------
# Function to access logger object for the module.
#-------------------------------------------------------------------------------
def _moduleLogger():
    """ Get logger object for the module, initialize one if it does not exist"""
    
    global __logger
    if __logger is None:
        __logger = CSEPLogging.CSEPLogging.getLogger(__name__)
    
    return __logger


#--------------------------------------------------------------------------------
#
# addPath
# 
# This method writes Matlab path to open file.
#
# Input: 
#          path_list - Optional list of paths to add to the Matlab script.
#                      Default is None.
#
# Output: Handle to the open file.
# 
def openScript (path_list = None):
   """ Open Matlab script file for writing and write path instructions 
       required by the CSEP software to the open file."""

   # Open the file
   fhandle = file(__MATLAB_SCRIPT, CSEPFile.Mode.WRITE)
   

   # Path to the top level source directory
   src_path = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV], 
                           'src')
   
   # Add common paths
   dir_path = os.path.join(src_path, 'generic', 'matlab')
   line = "addpath('%s');\n" %(dir_path)
   fhandle.write(line)
   
   dir_path = os.path.join(src_path, 'get_Catalog')
   line = "addpath('%s');\n" %(dir_path)
   fhandle.write(line) 
   
   if path_list is not None:
      for each_dir in path_list:
         line = "addpath('%s');\n" %(each_dir)
         fhandle.write(line) 

   return fhandle


#--------------------------------------------------------------------------------
#
# initialize
# 
# This method initializes Matlab environment according to user's specifications 
# (through Python command line options).
#
# Input:
#          path_list - Optional list of paths to add to the Matlab script. 
#                      Default is None.
#
# Output: Handle to the open file.
# 
def initializeScript (path_list = None):
   """  Write lines to the file that initialize Matlab environment. 
        These lines include setting up Matlab path and calling Matlab 
        initialization routine."""

   fhandle = openScript(path_list)
   
   line = "initialize(%s, %s);\n" \
           %(MatlabLogical.Boolean[CSEPRandom.ReadSeedFromFile],
             CSEP.Catalog.NumDeclusterSimulations)
   fhandle.write(line)   
   
   return fhandle


#--------------------------------------------------------------------------------
#
# finalizeScript
# 
# This method finalizes Matlab script according to user's specifications.
#
# Input: 
#          fhandle - Handle to the open file
#
# Output: None
# 
def finalizeScript (fhandle): 
   """  Write final lines to the Matlab script file."""

   # Exit Matlab
   fhandle.write("quit;\n")        
        
   # Close the file
   fhandle.close()  


#--------------------------------------------------------------------------------
#
# invokeScript
# 
# This method invokes Matlab script.
#
# Input:
#          options - Optional command-line arguments to invoke Matlab script.
#                    Default is an empty string.
#
# Output: None.
# 
def invokeScript (options = ''):
   """ Invoke Matlab script file."""

   command  = "cat %s" %(__MATLAB_SCRIPT)

   # show content of the script   
   _moduleLogger().info("Invoking Matlab script: %s" \
                        %Environment.commandOutput(command))                 

   command = "matlab %s" %options
        
   command = command + " -nodisplay -nosplash < " + \
             __MATLAB_SCRIPT + " > "  + __MATLAB_OUTPUT_FILE
            
   Environment.invokeCommand(command)
      

   cleanup_files = []

   # View output of matlab that is redirected to the file
   command = "cat %s\n" %(__MATLAB_OUTPUT_FILE)
   Environment.invokeCommand(command)
  
   # Cleanup
   cleanup_files.append(__MATLAB_OUTPUT_FILE)

   # Cleanup 
   cleanup_files.append(__MATLAB_SCRIPT)
   command = "rm -f %s" %(' '.join(cleanup_files))
   Environment.invokeCommand(command);                


#--------------------------------------------------------------------------------
#
# saveASCII
# 
# This method writes Matlab variable to the file in ASCII format.
#
# Input: 
#         fhandle - Handle to the open script file
#         result_variable - Name of Matlab variable to store results to
#         result_file - Filename for result data in Matlab format 
#                       (with '.mat' extension)
#
# Output: None.
#    
def saveASCII (fhandle, result_variable, result_file):
   """ Save Matlab variable in ASCII format file."""
   
   ### Remove file extension
   ascii_filename = CSEPFile.Name.ascii(result_file)
   line = "save('%s', '%s', '-ascii', '-double', '-tabs');\n" \
          %(ascii_filename, result_variable)
   fhandle.write(line)
   
   return fhandle    


#============================================================================
# Class to represent variable range for the simulations
#============================================================================
class Range (object):

   #========================================================================
   #
   # Initialize Range object
   #
   def __init__ (self, min_val, max_val):
       """ Initialize Range object"""
   
       self.min = min_val
       self.max = max_val
       self.diff = max_val - min_val
       
    
   #========================================================================
   #
   # Place random angle error within [0; 2*PI] range
   #
   # Inputs:
   #         error - numpy array object of random values
   #  
   # Output: random value within the range
   #========================================================================
   def applyError(self, error):
       """Place random error within the range"""
       
       return (self.min + error*self.diff) 
   

#--------------------------------------------------------------------------------
#
# Catalog.
#
# This module contains generic routines for catalog data.
#
class Catalog:
    
   # ZMAP column-oriented format of the catalog 
   class ZMAPFormat (object):
        
      Longitude = 0
      Latitude = 1
      DecimalYear = 2
      Month = 3
      Day = 4
      Magnitude = 5
      Depth = 6
      Hour = 7
      Minute = 8
      Second = 9
        
      # Error columns
      HorizontalError = 10
      DepthError = 11
      MagnitudeError = 12
        
      NetworkName = 13
      NumColumns = 14
   
   
   # Indices to access random matrix to generate catalog uncertainties
   class Uncertainty (object):
       
       # Column-oriented format for array of random numbers
       class Format (object):
           Distance = 0     # To apply to horizontal error
           Angle = 1
           Depth = 2
           Magnitude = 3
           Probability = 4  # To apply to independence probability if declustered 
                            # catalog
                  
           # Number of columns in array of random numbers for applying 
           # uncertainties (will be incremented by 1 if IndependenceProbability is present)
           NumColumns = 4
       
       FilePrefix = 'uncertainty'
       FilePostfix = '-randomSeed.txt'

       __angleRange = Range(0.0, 2.0 * np.pi)

       __deg2Rad = np.pi/180.0
       __rad2Deg = 180.0/np.pi
       
       __EarthRadius = 6374
       __EarthCircumference = 2*np.pi*__EarthRadius


       #========================================================================
       #
       # Shift catalog events according to the horizontal error. Array values
       # replacement is "in place" meaning that passed by reference array gets
       # modified by this method. 
       #
       # Inputs:
       #         catalog - numpy object with catalog data
       #         random_distance - Vector of random numbers used to generate a 
       #                           total distance for the shift.
       #         random_angle - Vector of random numbers used to generate an 
       #                        angle for the shift.
       #  
       # Output: None
       #========================================================================
       @staticmethod
       def applyHorizontalError (catalog,
                                 random_distance,
                                 random_angle):
           """ Apply horizontal error to the event. Use random distance and random
               angle to rotate by. """
               

           ### Apply horizontal error to longitude and latitude: 
            
           # Randomize horizontal error - total distance to shift the event,
           # and take absolute value
           catalog[:, Catalog.ZMAPFormat.HorizontalError] = np.abs(CSEPUtils.normalRandom(catalog[:, Catalog.ZMAPFormat.HorizontalError], 
                                                                                          random_distance))
           
           # Generate random angle (in radians) - to move event by computed distance
           # in the direction of this angle.
           alpha = Catalog.Uncertainty.__angleRange.applyError(random_angle)
           
           # Do the shift (use spherical geometry)
           bSide = (90.0 - catalog[:, Catalog.ZMAPFormat.Latitude])*Catalog.Uncertainty.__deg2Rad
           cSide = catalog[:, Catalog.ZMAPFormat.HorizontalError]*360.0*Catalog.Uncertainty.__deg2Rad/Catalog.Uncertainty.__EarthCircumference
            
           # Use the cosine rule
           aSide = np.arccos(np.cos(bSide)*np.cos(cSide) + np.sin(bSide)*np.sin(cSide)*np.cos(alpha))
            
           # New latitude
           catalog[:, Catalog.ZMAPFormat.Latitude] = 90.0 - aSide*Catalog.Uncertainty.__rad2Deg
            
           # Use the sine rule
           # vGamma is the difference of longitudes for two points
           vGamma = np.arcsin(np.sin(cSide)*np.sin(alpha)/np.sin(aSide))
            
           # New longitude
           catalog[:, Catalog.ZMAPFormat.Longitude] += vGamma*Catalog.Uncertainty.__rad2Deg
           

   
   #-----------------------------------------------------------------------------
   #
   # toASCII
   # 
   # This method converts forecast data from ASCII to the Matlab format.
   #
   # Input: 
   #         catalog_file - Filename for catalog in Matlab format.
   #         result_variable - Matlab variable name for the result data. 
   #                                  Default is 'mModel'.   
   #         expected_matlab_var - Optional argument to specify Matlab variable
   #                               for the data stored in the Matlab file. Default
   #                               is None.
   #         result_file - Optional filename for ASCII format of catalog. Default
   #                       is None meaning to use original 'catalog_file' name  
   #                       with ASCII extension.
   #
   # Output: Filename for ASCII data.
   # 
   @staticmethod
   def toASCII (catalog_file, 
                result_variable = 'mCatalogNoDecl',
                expected_matlab_var = None,
                result_file = None):
      """ Convert Matlab catalog data into ASCII format, and save it to the file.
          The function uses the same filename but with ASCII extension to 
          store ASCII formatted data."""
        
      catalog = None
      
      # Get rid of warning by setting 'struct_as_record' argument
      catalog_fh = scipy.io.loadmat(catalog_file,
                                    struct_as_record=True)
      
      expected_vars = [MatlabLogical.CatalogVar.Declustered,
                       MatlabLogical.CatalogVar.Undeclustered,
                       'mCatalog']
      # Allow caller to specify which variable should be read from the Matlab
      # file
      if expected_matlab_var is not None:
          expected_vars.append(expected_matlab_var)
        
      for each_var in expected_vars:
          if each_var in catalog_fh:
              catalog = catalog_fh[each_var]
              break
             
      if catalog is None:
            error_msg = "Unexpected variable is specified by '%s' catalog file. \
Expected one of %s (got %s)" %(catalog_file,
                               expected_vars,
                               catalog_fh.keys())
            _moduleLogger().error(error_msg)
            raise RuntimeError, error_msg
        
      
      # Save data to ASCII file
      __ascii_filename = result_file
      if result_file is None:
          __ascii_filename = CSEPFile.Name.ascii(catalog_file)
      
      # NOTE(fab): numpy.set_printoptions() does not work
      # np.set_printoptions(nanstr='NaN')
      _write_catalog(__ascii_filename,
                     catalog)
      
      return __ascii_filename
   
   
   #-----------------------------------------------------------------------------
   #
   # toMatlab.
   # 
   # This method converts raw data to the Matlab ZMAP format.
   #
   # Input: 
   #         raw_file - Filename for catalog raw data.
   #         result_file - Filename for result catalog data.
   #         result_variable - Matlab variable name for the result data. 
   #                           Default is 'mCatalog'.   
   #
   # Output: None.
   # 
   @staticmethod
   def toMatlab (raw_file, 
                 result_file, 
                 result_variable = 'mCatalog'):
      """ Import raw catalog data into ZMAP Matlab format."""

      # Load ASCII data from the file
      np_array = np.fromfile(raw_file)
      if np_array.size == 0:
          np.array.shape = 0, 0
          
      else:
         np_array = np.loadtxt(raw_file)
         
      scipy.io.savemat(result_file,
                       {result_variable : np_array})


   #----------------------------------------------------------------------------
   #
   # ZMAPtoMatlab.
   #
   # This method converts ASCII ZMAP data to a Matlab matrix.
   #
   # Input:
   #         raw_file - Filename for ASCII ZMAP catalog data (as created by 
   #                    preProcess() in data source)
   #         horizontal_error - Horizontal error value to use if it's not 
   #                            provided by catalog. Default is 1.0.
   #         depth_error - Depth error value to use if it's not provided by
   #                       catalog. Default is 3.0. 
   #         magnitude_error - Magnitude error value to use if it's not provided by
   #                       catalog. Default is 0.1 
   #         result_file - Filename for result catalog data. Default is None 
   #                       meaning don't save result catalog to the file.
   #
   # Output: numpy.array object with catalog data
   #
   @staticmethod
   def importZMAP (raw_file, 
                   horizontal_error = 1.0,
                   depth_error = 3.0,
                   magnitude_error = 0.1,
                   result_file = None,
                   seismic_network = None):
      """ Read ASCII ZMAP catalog data into CSEP numpy.array object."""


      # ATTN! Check for an empty file: np.loadtxt() raises an exception 
      # if an empty file
      np_catalog = np.fromfile(raw_file)
      
      if np_catalog.size == 0:
          
            # CSEP is relying on 2-dim arrays
            np_catalog.shape = 0, 0

      else:

          np_catalog = CSEPFile.read(raw_file)
          
          # ZMAP format is expected to have CSEPGeneric.Catalog.ZMAPFormat.NumColumns columns
          nrows, ncols = np_catalog.shape
          
          if ncols < Catalog.ZMAPFormat.NumColumns:
              
              # Append empty columns to have expected number of columns in ZMAP format
              # of the catalog
              missing_cols = Catalog.ZMAPFormat.NumColumns - ncols
              
              np_catalog = np.append(np_catalog, np.zeros((nrows, missing_cols)),
                                     axis = 1)
              
          ### Check for missing errors
          selection = (np_catalog[:, Catalog.ZMAPFormat.HorizontalError] == 0.0) | \
                      np.isnan(np_catalog[:, Catalog.ZMAPFormat.HorizontalError])
          # Default horizontal error
          np_catalog[selection, Catalog.ZMAPFormat.HorizontalError] = horizontal_error
          
          selection = (np_catalog[:, Catalog.ZMAPFormat.DepthError] == 0.0) | \
                      np.isnan(np_catalog[:, Catalog.ZMAPFormat.DepthError])
          # Default depth error
          np_catalog[selection, Catalog.ZMAPFormat.DepthError] = depth_error
    
          # Check for NaN values for magnitude error, or not provided values
          selection = (np_catalog[:, Catalog.ZMAPFormat.MagnitudeError] == 0.0) | \
                      np.isnan(np_catalog[:, Catalog.ZMAPFormat.MagnitudeError])
          np_catalog[selection, Catalog.ZMAPFormat.MagnitudeError] = magnitude_error
      
          if seismic_network is not None:
              np_catalog[:, Catalog.ZMAPFormat.NetworkName] = seismic_network

      if result_file is not None:
          _write_catalog(result_file,
                         np_catalog)
          
      return np_catalog


   #-----------------------------------------------------------------------------
   #
   # cutToArea.
   # 
   # This method cuts catalog data according to the area of interest.
   #
   # Input: 
   #         np_catalog - Numpy object with catalog data.
   #         area_file - Filename for geographical area.
   #         result_file - Filename for result catalog data.
   #         cell_half_dim - Half of cell's dimension. Default is 0.05 degrees.
   #
   # Output: None.
   #
   @staticmethod
   def cutToArea (np_catalog, 
                  area_file, 
                  result_file = None, 
                  cell_half_dim = 0.05):
      """ Cut catalog to the geographical area of interest."""
        

      catalog_array = np_catalog

      if area_file is not None and catalog_array.size != 0:
          # No need to filter empty array
          test_area_file = CSEPFile.Name.ascii(area_file)
          region_array = np.loadtxt(test_area_file)
        
          # Add new column (backward compatibility with Matlab implementation of
          # cutting to the area - to make acceptance tests pass) 
          within_area_flag = np.zeros((catalog_array.shape[0], 1))
        
          # Fix for Trac ticket #114 (inherited from Matlab codes):
          # floating point representation of area coordinates plus 
          # inclusive/exclusive boundary check was voiding valid events
          __threshold = 0.0001
          __area_lon_index = 0
          __area_lat_index = 1
        
          for index, coords in enumerate(zip(catalog_array[:, Catalog.ZMAPFormat.Longitude],
                                             catalog_array[:, Catalog.ZMAPFormat.Latitude])):
            
              __x, __y = coords
              selection = ((region_array[:, __area_lon_index] - __x - cell_half_dim <= __threshold) & \
                           (region_array[:, __area_lon_index] - __x + cell_half_dim > __threshold) & \
                           (region_array[:, __area_lat_index] - __y - cell_half_dim <= __threshold) & \
                           (region_array[:, __area_lat_index] - __y + cell_half_dim > __threshold))

#===============================================================================
#              selection = (abs(__x - region_array[:, __area_lon_index]) <= __cell_dim) & \
#                          (abs(__y - region_array[:, __area_lat_index]) <= __cell_dim)
#===============================================================================
              within_area_flag[index] = selection.sum()              
            
          # Matlab backward compatibility: preserve number of geographical region 
          # cells event falls into
          catalog_array = np.append(catalog_array, 
                                    within_area_flag, 
                                    axis=1)
        
          # Leave events that fall into specified geographical area
          selection, ignore_col_selection = np.where(within_area_flag > 0)
          catalog_array = catalog_array[selection, :] 
            
      if result_file is not None:
          _write_catalog(result_file,
                         catalog_array)
    
      return catalog_array

   
   #-----------------------------------------------------------------------------
   #
   # cutToTimePeriod
   # 
   # This method cuts catalog data according to the time period. The method 
   # includes time period boundaries when cutting catalog.
   #
   # Input: 
   #         catalog_file - Filename for catalog data.
   #         start_time - datetime object that represents start date for 
   #                      the period.
   #         stop_time - datetime object that represents end date for the period.
   #         result_file - Filename for result catalog data. Default is None.      
   #         start_time_sign - Sign operator for start_time boundary. 
   #                           Default is greater or equal sign (>=).
   #         start_time_sign - Sign operator for stop_time boundary. 
   #                           Default is less or equal sign (<=).
   #
   # Output: None.
   # 
   @staticmethod
   def cutToTimePeriod (np_catalog, 
                        start_date, 
                        stop_date, 
                        result_file = None,
                        start_time_sign = operator.ge, 
                        stop_time_sign = operator.le):
      """ Cut catalog to the time period of interest."""
        
      catalog_array = np_catalog
      
      if catalog_array is not None and \
         catalog_array.size != 0:
          # No need to filter empty array
          catalog_dates = np.array([datetime.datetime(int(each[Catalog.ZMAPFormat.DecimalYear]),
                                                      int(each[Catalog.ZMAPFormat.Month]),
                                                      int(each[Catalog.ZMAPFormat.Day]),
                                                      int(each[Catalog.ZMAPFormat.Hour]),
                                                      int(each[Catalog.ZMAPFormat.Minute]),
                                                      int(each[Catalog.ZMAPFormat.Second]),
                                                      CSEP.Time.microseconds(each[Catalog.ZMAPFormat.Second])) for each in catalog_array])
            
          selection, = np.where((start_time_sign(catalog_dates, start_date)) & \
                                (stop_time_sign(catalog_dates, stop_date))) 
            
          catalog_array = catalog_array[selection, :] 
    
      if result_file is not None:
          _write_catalog(result_file,
                     catalog_array)
        
      return catalog_array
      
   
   #----------------------------------------------------------------------------
   # 
   # Class to represent parameters for Reasenberg declustering algorithm
   #
   class ReasenbergDeclusterAlgorithm (object):

       # Static data attributes
       __daysToMins = 24*60 # days-to-minutes scale factor
       
       __dfTauminRange = Range(0.5, 2.5)
       __dfTaumaxRange = Range(3.0, 15.0)
       __dfPRange      = Range(0.9, 0.999)
       __dfXkRange     = Range(0.0, 1.0)
       __dfXmeffRange  = Range(3.0, 3.0)
       __dfRfactRange  = Range(5.0, 20.0)
       __dfErrRange    = Range(2.0, 2.0)
       __dfDerrRange   = Range(5.0, 5.0)
       
       
       __executableFile = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                      'src',
                                      'ReasenbergDecluster',
                                      'cluster2000x')
       
       # Filename for catalog in HYPO71 format
       __HYPO71CatalogFilename = 'hypo71Catalog.dat'

       # Parameter file for the algorithm
       __parameterFile = 'ReasenbergParameters.dat'
       
       # Output file with cluster information as generated by the algorithm 
       __clusterFile = 'cluster.ano'
       
       # The data format as used by Fortran code
       # 1=HYPOINV, 2=HYPOINV-2000, 3=HYPO71, 4=HYPO71-2000, 5=FREE
       __dataFormat = 4


       #========================================================================
       #
       # Initialize
       #
       # Inputs:
       #         np_catalog - numpy.array object with catalog data to decluster
       #         
       def __init__ (self,
                     np_catalog):
           """ Initialize ReasenbergDeclusterAlgorithm """
           
           
           # Catalog to decluster
           self.__catalog = np_catalog
           
           # Year parameters (adjusted by min year value encountered in input
           # catalog): set by ReasenbergDeclusterAlgorithm.toHYPO71Format() method
           self.__minYear = None
           self.__maxYear = None
           

       #========================================================================
       #
       # Invoke Reasenberg declustering algorithm with
       # default parameters (as used by Matlab mc_Decluster.m implementation
       # of the algorithm)
       #
       # Inputs: Default algorithm parameters (as used by Matlab implementation
       #         of the algorigthm)
       #
       #         
       # Output: vector of "is-mainshock" flags for the catalog
       #
       def run (self,
                dfTaumin = 1,
                dfTaumax = 10,
                dfP = 0.95,
                dfXk = 0.5,
                dfXmeff = 1.5,
                dfRfact = 10.0,
                dfErr = 1.5,
                dfDerr = 2.0,
                random_v = None):
           """ Invoke Reasenberg decluster algorithm."""
           
           
           # Convert catalog to HYPO71-2000 format expected by Fortran code
           self.toHYPO71Format(self.__catalog)
           
           if random_v is not None:
                dfTaumin = Catalog.ReasenbergDeclusterAlgorithm.__dfTauminRange.applyError(random_v[0])
                dfTaumax = Catalog.ReasenbergDeclusterAlgorithm.__dfTaumaxRange.applyError(random_v[1])
                dfP = Catalog.ReasenbergDeclusterAlgorithm.__dfPRange.applyError(random_v[2])
                dfXk = Catalog.ReasenbergDeclusterAlgorithm.__dfXkRange.applyError(random_v[3])
                dfXmeff = Catalog.ReasenbergDeclusterAlgorithm.__dfXmeffRange.applyError(random_v[4])
                dfRfact = Catalog.ReasenbergDeclusterAlgorithm.__dfRfactRange.applyError(random_v[5])
                dfErr = Catalog.ReasenbergDeclusterAlgorithm.__dfErrRange.applyError(random_v[6])
                dfDerr = Catalog.ReasenbergDeclusterAlgorithm.__dfDerrRange.applyError(random_v[7])

           # Write parameter file for the algorithm
           self.writeParameterFile(dfTaumin*Catalog.ReasenbergDeclusterAlgorithm.__daysToMins,
                                   dfTaumax*Catalog.ReasenbergDeclusterAlgorithm.__daysToMins,
                                   dfP,
                                   dfXk,
                                   dfXmeff,
                                   dfRfact,
                                   dfErr,
                                   dfDerr)
           Environment.invokeCommand('cat %s' %Catalog.ReasenbergDeclusterAlgorithm.__parameterFile)
              
           Environment.invokeCommand('%s %s' %(Catalog.ReasenbergDeclusterAlgorithm.__executableFile,
                                               Catalog.ReasenbergDeclusterAlgorithm.__parameterFile))
              
           # Extract cluster information from one of the data files generated by
           # the algorigthm
           __cluster_vector = np.loadtxt(Catalog.ReasenbergDeclusterAlgorithm.__clusterFile, 
                                         dtype=np.int, 
                                         usecols=[-2])

           __mainshock_selection = np.zeros(__cluster_vector.shape,
                                            np.bool)
           __select, = np.where(__cluster_vector == 0)
           __mainshock_selection[__select] = True

           for index in xrange(1, __cluster_vector.max() + 1):
               
               # Find all events for the cluster
               __select, = np.where(__cluster_vector[:] == index)
               
               # ATTN: validation to 'is True' fails
               if __select.any() == True:
                   
                   __cluster_max_magnitude = self.__catalog[__select, Catalog.ZMAPFormat.Magnitude].max() 
                   __select_max, = np.where(self.__catalog[__select, Catalog.ZMAPFormat.Magnitude] == \
                                            __cluster_max_magnitude)
                   # print "__select_max for cluster=", index, ': ', __select_max
                   
                   # Determine mainshock event from the cluster
                   __select_mainshock = None
                   if __select_max.size == 1:
                       __select_mainshock = __select[__select_max]
                       
                   else:
#===============================================================================
#                       _moduleLogger().info("Multiple events of %s cluster correspond \
# to maximum magnitude=%s, choosing very first event with index=%s"
#                                            %(index, 
#                                              __cluster_max_magnitude,
#                                              __select[0]))
#===============================================================================
                       
                       __select_mainshock = __select[__select_max[0]]
                    
                   #print '__select_mainshock=', __select_mainshock
                    
                   __mainshock_selection[__select_mainshock] = True


           # Clean up after algorithm
           command = 'rm -rf cluster.* %s' %Catalog.ReasenbergDeclusterAlgorithm.__parameterFile
           Environment.invokeCommand(command)
              
                    
           # Return mainshock vector
           return __mainshock_selection
           
           
       #========================================================================
       #
       # Write parameter file for declustering algorithm written in Fortran
       #
       # Inputs: Algorithm parameters
       #
       def writeParameterFile(self,
                              dfTaumin,
                              dfTaumax,
                              dfP,
                              dfXk,
                              dfXmeff,
                              dfRfact,
                              dfErr,
                              dfDerr):
           """ Convert ZMAP format of the catalog to HYPO71-2000 format as 
               expected by original Fortran code for Reasenberg algorithm"""
           
           # Write input file for Fortran declustering algorithm
           __params_fhandle = CSEPFile.openFile(Catalog.ReasenbergDeclusterAlgorithm.__parameterFile,
                                                CSEPFile.Mode.WRITE)
                                                       
           __params_fhandle.write('%s\n' %Catalog.ReasenbergDeclusterAlgorithm.__HYPO71CatalogFilename)
           __params_fhandle.write('%s\n' %Catalog.ReasenbergDeclusterAlgorithm.__dataFormat)
           __params_fhandle.write('%2d\n' %self.__minYear)
           __params_fhandle.write('%2d\n' %self.__maxYear)
           __params_fhandle.write('%.10f\n' %dfXmeff)
           __params_fhandle.write('%.10f\n' %dfRfact)
           __params_fhandle.write('%.10f\n' %dfTaumin)
           __params_fhandle.write('%.10f\n' %dfTaumin)
           __params_fhandle.write('%.10f\n' %dfTaumax)
           __params_fhandle.write('%.10f\n' %dfP)
           __params_fhandle.write('%.10f\n' %dfXk)

           __params_fhandle.close()
       
       
       #========================================================================
       # Convert ZMAP format of the catalog to the HYPO71 format as expected
       # by Fortran declustering code:
       # HYPO71 FORMAT YEAR 2000
       #
       # C--HYPO71-2000 FORMAT
       #   104 read (3, 2010, err= 900, END=35) icent,itime,lat1,ins,xlat1,
       #      1                     lon1,iew,xlon1,dep1,xmag1,erh1,erz1,q1
       #  2010 format (4i2,1x,2i2,6x,i3,a1,f5.2,i4,a1,f5.2,
       #      1        f7.2,2x,f5.2,17x,2f5.1,1x,a1)
       #
       # Inputs:
       #         np_catalog - numpy.array object with catalog data
       #
       # Output: Value for minimum year in provided input catalog
       #========================================================================
       def toHYPO71Format(self, np_catalog):
           """ Convert ZMAP format of the catalog to HYPO71-2000 format as 
               expected by original Fortran code for Reasenberg algorithm"""
           

           # Catalog in HYPO71 format already exists (from previous run)
           if os.path.exists(Catalog.ReasenbergDeclusterAlgorithm.__HYPO71CatalogFilename) is True:
               return
           
           # Fortran declustering code is not Y2000 compliant, use workaround 
           # suggested by Thomas van Stiphout: subtract minimum year as appears in 
           # input catalog from all catalog events
           __min_year = np.floor(np_catalog[:, Catalog.ZMAPFormat.DecimalYear].min())
           
           # Create deep copy of year column: to be offset by minimum year value 
           # within catalog
           __year_column = np_catalog[:, Catalog.ZMAPFormat.DecimalYear].copy()
           __year_column -= __min_year
           
           self.__minYear = np.floor(__year_column.min())
           self.__maxYear = np.ceil(__year_column.max())
           
           
           num_events, num_colums = np_catalog.shape
           
           # Prepare longitude with E/W sign
           __lon_str =  np.array(['E'] * num_events)
           selection, = np.where(np_catalog[:, Catalog.ZMAPFormat.Longitude] < 0.0)
           __lon_str[selection] = 'W'

           # Prepare latitude with S/N sign
           __lat_str =  np.array(['N'] * num_events)
           selection, = np.where(np_catalog[:, Catalog.ZMAPFormat.Latitude] < 0.0)
           __lat_str[selection] = 'S'

           __abs_lon_degrees = np.abs(np_catalog[:, Catalog.ZMAPFormat.Longitude])
           __abs_lat_degrees = np.abs(np_catalog[:, Catalog.ZMAPFormat.Latitude])
           
           __lon_degrees = np.floor(__abs_lon_degrees)
           __lat_degrees = np.floor(__abs_lat_degrees) 

           __lon_min = (__abs_lon_degrees - __lon_degrees)*60.0
           __lat_min=(__abs_lat_degrees - __lat_degrees)*60.0
           
           output_fhandler = CSEPFile.openFile(Catalog.ReasenbergDeclusterAlgorithm.__HYPO71CatalogFilename, 
                                               CSEPFile.Mode.WRITE)

           #__empty_long_str = ''.rjust(22)
           # Thomas used numeric representation of ' ' to populate one before last
           # entry in HYPO71 format of the catalog. Use the same value to fill
           # the entry
           __blank_float_val = 32.0
           for index in xrange(0, num_events):
               
                output_fhandler.write("%4.0f%02.0f%02.0f %02.0f%02.0f%6.2f%3d%1s%05.2f%4d%s%05.2f%7.2f  %5.2f%22.1f%5.1f   \n"
                                      %(np.floor(__year_column[index]), 
                                        np_catalog[index, Catalog.ZMAPFormat.Month],
                                        np_catalog[index, Catalog.ZMAPFormat.Day],
                                        np_catalog[index, Catalog.ZMAPFormat.Hour],
                                        np_catalog[index, Catalog.ZMAPFormat.Minute],
                                        np_catalog[index, Catalog.ZMAPFormat.Second],
                                        __lat_degrees[index], __lat_str[index], __lat_min[index],
                                        __lon_degrees[index], __lon_str[index], __lon_min[index],
                                        np_catalog[index, Catalog.ZMAPFormat.Depth],
                                        np_catalog[index, Catalog.ZMAPFormat.Magnitude],
                                        #__empty_long_str,
                                        __blank_float_val,
                                        np_catalog[index, Catalog.ZMAPFormat.DepthError]))
                
           return
                                 

   #----------------------------------------------------------------------------
   #
   # declusterReasenberg
   # 
   # This method declusters catalog data according to the Reasenberg declustering
   # algorithm. It uses original Fortran code as posted on USGS web site:
   # ftp://ehzftp.wr.usgs.gov/cluster2000/cluster2000x.f
   #
   # Input: 
   #         np_catalog - numpy.array object with atalog data
   #         result_file - Filename for declustered catalog. Default is None
   #                       that means not to store result catalog to the file.
   #         supplemental_result_file - Filename for catalog with supplemental
   #                                    independence probability column. Default
   #                                    is None that means not to store result
   #
   # Output: Tuple of numpy.array objects that represent declustered catalog
   #         and original catalog with supplemental independence probability 
   #         column
   # 
   @staticmethod
   def declusterReasenberg (np_catalog,
                            supplemental_result_file = "decluster_indep_probability.dat"):
      """ Decluster catalog using original Fortran code for Reasenberg algorigthm
          as distributed by USGS."""
        
      
      __algorithm = Catalog.ReasenbergDeclusterAlgorithm(np_catalog)
      __mainshock = __algorithm.run()
      
      declustered_catalog = np_catalog[__mainshock, :]

      generator = CSEPRandom(CSEP.Catalog.Filename.DeclusterParameter)
          
      # For backward compatibility with Matlab, specify Fortran 
      # (column-order) of the array with random numbers
      __num_columns = 8
      np_random = np.array(generator.createNumbers(CSEP.Catalog.NumDeclusterSimulations * __num_columns)).reshape(CSEP.Catalog.NumDeclusterSimulations,
                                                                                                                  __num_columns,
                                                                                                                  order='F')
      
      __indep_probability = np.zeros((np_catalog.shape[0], 1),
                                     dtype = np.float)

      #=========================================================================
      # Run simulations for the algorithm to get independence probability       
      #=========================================================================
      for i in xrange(0, CSEP.Catalog.NumDeclusterSimulations):
          
          __mainshock = __algorithm.run(random_v = np_random[i, :])                
          __indep_probability[__mainshock, 0] += 1
          
      __indep_probability /= CSEP.Catalog.NumDeclusterSimulations
      
      # Attach independence probability to the original catalog
      catalog_with_indep_probability = np.append(np_catalog,
                                                 __indep_probability,
                                                 axis = 1)
      
      _write_catalog(supplemental_result_file, 
                     catalog_with_indep_probability) 
      
      return (declustered_catalog,
              catalog_with_indep_probability, 
              supplemental_result_file)
      
  
   
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
   #         result_dir - Directory to store intermediate results to (random seed
   #                      files). Default is 'uncertainties'.
   #         result_file - Filename for result data
   #         threshold - PostProcess.Threshold object with filters values
   #         probability_column - Column index for independence probability. This
   #                              column is available for declustered catalog only. 
   #                              Default is 0.
   #         result_files - PostProcess.Files.Uncertainties object with files and 
   #                        directory information for catalog uncertainties.
   #
   # Output: Directory that stores intermediate data products (random seed values)
   #         required for reproducibility of results.
   # 
   @staticmethod
   def modifications (np_catalog, 
                      area_file,
                      threshold,
                      result_files,
                      probability_column = 0):
      """ Create catalog modifications by applying randomized uncertainties to the
          original catalog."""


      _moduleLogger().info('Applying uncertainties to the catalog...')

      # Result cell array of catalog modifications
      __catalog_modifications = np.zeros((CSEP.Catalog.NumUncertainties,),
                                         dtype=np.object)
      
      __uncert_dir = None
        
      # No need to apply uncertainties to an empty catalog
      if np_catalog.size != 0:
      
          if os.path.exists(result_files.dir) is False:
              os.makedirs(result_files.dir) 

          __uncert_dir = result_files.dir  

          # Get dimensions for random matrix
          random_rows, random_cols = np_catalog.shape
          random_cols = Catalog.Uncertainty.Format.NumColumns
         
          if probability_column != 0:
              random_cols += 1

          # ATTN: For backward compatibility with Matlab codes, start indexing
          #       from 1 as in Matlab
          for index in xrange(1, CSEP.Catalog.NumUncertainties + 1):
            
              _moduleLogger().info('Generating uncertainty catalog %s...' %index)
                
              # Catalog with uncertainties:
              __uncertainty = np_catalog.copy()
                
              # Format seed filename for the simulation random numbers
              simulation_random_file = os.path.join(result_files.dir,
                                                    '%s.%s%s' %(Catalog.Uncertainty.FilePrefix,
                                                                index, 
                                                                Catalog.Uncertainty.FilePostfix))
        
              random_generator = CSEPRandom(simulation_random_file)
                
              # For backward compatibility with Matlab, specify Fortran 
              # (column-order) of the array with random numbers
              random_array = np.array(random_generator.createNumbers(random_rows * random_cols)).reshape(random_rows,
                                                                                                         random_cols,
                                                                                                         order='F')

              __random_dist = random_array[:, Catalog.Uncertainty.Format.Distance]
              __random_angle = random_array[:, Catalog.Uncertainty.Format.Angle]
              __random_depth = random_array[:, Catalog.Uncertainty.Format.Depth]
              __random_magn = random_array[:, Catalog.Uncertainty.Format.Magnitude]
                
              __random_prob = None
                   
              # The column exists only for declustered catalog
              if probability_column != 0:
                  __random_prob = random_array[:, Catalog.Uncertainty.Format.Probability]
               
              # Apply horizontal error if enabled    
              if CSEP.Catalog.UseHorizontalError is True:
                    
                  # Apply horizontal error to longitude and latitude: 
                  Catalog.Uncertainty.applyHorizontalError(__uncertainty, 
                                                           __random_dist, 
                                                           __random_angle)
               
              # Apply depth error if enabled
              if CSEP.Catalog.UseDepthError is True:
                    
                  # Randomize depth error
                  __uncertainty[:, Catalog.ZMAPFormat.DepthError] = \
                      CSEPUtils.normalRandom(__uncertainty[:, Catalog.ZMAPFormat.DepthError],
                                             __random_depth)
                   
                  # Apply depth error
                  __uncertainty[:, Catalog.ZMAPFormat.Depth] += \
                      __uncertainty[:, Catalog.ZMAPFormat.DepthError]          
               
                
              # Apply magnitude error if enabled    
              if CSEP.Catalog.UseMagnitudeError is True:
                  # Randomize magnitude error
                  __uncertainty[:, Catalog.ZMAPFormat.MagnitudeError] = \
                      CSEPUtils.normalRandom(__uncertainty[:, Catalog.ZMAPFormat.MagnitudeError],
                                             __random_magn)
                  
                  # Apply magnitude error   
                  __uncertainty[:, Catalog.ZMAPFormat.Magnitude] += \
                      __uncertainty[:, Catalog.ZMAPFormat.MagnitudeError]       
               
              # Randomize independence probability if such column is defined
              if probability_column != 0:
                   
                  # Get rid of events that have '0' independence probability, and
                  # remove corresponding random numbers for those events
                  selection, = np.where(__uncertainty[:, probability_column] != 0)
                  __uncertainty = __uncertainty[selection, :]
                  __random_prob = __random_prob[selection, :]
                  
                  # Don't use random number if original independence probability is '1'
                  selection, = np.where(__uncertainty[:, probability_column] == 1)
                   
                  # Reset random numbers for such probabilities to original value of '1'
                  __random_prob[selection, :] = __uncertainty[selection, 
                                                              probability_column]
                   
                  # Remove events that have random numbers larger than original independence 
                  # probability
                  selection = (__random_prob <= __uncertainty[:, probability_column])
                   
                  # Reduce catalog
                  __uncertainty = __uncertainty[selection, :]
                   
            
              if CSEP.DebugMode is True:
                  # Save catalog data in Matlab format 
                  file_name = os.path.join(result_files.dir,
                                           'catalog.uncert.%d.dat' %index)
                  _write_catalog(file_name, 
                                 __uncertainty)
                
              # Store new catalog
              # ATTN: For backward compatibility with Matlab codes, indexing
              #       starts from 1 as in Matlab
              __catalog_modifications[index - 1] = Catalog.filter(__uncertainty,
                                                                  area_file,
                                                                  threshold)
              
              if CSEP.DebugMode is True:
                  # Save catalog data in Matlab format 
                  file_name = os.path.join(result_files.dir,
                                           'catalog.uncert-filtered.%d.dat' %index)
                  _write_catalog(file_name, 
                                 __catalog_modifications[index - 1])
              
           # all simulations
       # Save all catalog uncertainties to the file
#===============================================================================
# TODO: Should use NPZ binary format
#        >>> np.savez('obj_array.npz', modifications=obj_arr)
#        >>> b = np.load('obj_array.npz')
#        >>> b.files
#        ['modifications']
#        >>> b['modifications']
#        array([[[1 2 3]
#         [4 5 6]
#         [7 8 9]], [[10 11]
#         [12 13]]], dtype=object)
#        >>>
#===============================================================================
      scipy.io.savemat(result_files.catalog,
                       {result_files.matlabVar : __catalog_modifications})
        
      # non-empty catalog
      _moduleLogger().info('Done with catalog uncertainties.')
        
      return __uncert_dir


   #-----------------------------------------------------------------------------
   #
   # filter
   # 
   # This method filters catalog data based on the specified area, minimum 
   # magnitude, maximum depth and starting date for the forecast model.
   #
   # Input: 
   #         catalog_file - Filename for catalog data.
   #         area_file - Area file for catalog filtering
   #         threshold - PostProcess.Threshold object with filters values
   #         result_file - Filename for result data. Default is None.
   #         
   #         result_variable - Name of Matlab variable to store results to. 
   #                           Default is 'mCatalog'.
   #
   # Output: None.
   #
   @staticmethod 
   def filter (np_catalog, 
               area_file, 
               threshold,
               result_file = None):
      """  Filter catalog data based on specified geographical location, 
           minimum magnitude, maximum depth, and starting date for the forecast 
           model."""
        
      # Filter out events that are:
      #  Outside of test area
      #  Before year ForecastDecYearThreshold
      #  Depth > ForecastDepthThreshold 
      #  Magnitude < ForecastMagnitudeThreshold
      catalog_array = Catalog.cutToArea(np_catalog, 
                                        area_file)  
    
      # Prepare catalog
      if catalog_array.size != 0:
          
          selection, = np.where(catalog_array[:, Catalog.ZMAPFormat.DecimalYear] >= threshold.DecimalStartDate)
          catalog_array = catalog_array[selection,:]

          if catalog_array.size != 0:
              selection, = np.where(catalog_array[:, Catalog.ZMAPFormat.Magnitude] >= threshold.MinMagnitude)
              catalog_array = catalog_array[selection, :]

          if catalog_array.size != 0:
              selection, = np.where(catalog_array[:, Catalog.ZMAPFormat.Depth] <= threshold.MaxDepth)
              catalog_array = catalog_array[selection, :]
        
          # Ignore events above Earth surface
          if catalog_array.size != 0:
              selection, = np.where(catalog_array[:, Catalog.ZMAPFormat.Depth] >= 0)
              catalog_array = catalog_array[selection, :]

      if result_file is not None:
          _write_catalog(result_file, 
                         catalog_array)
      
      return catalog_array
   
   
   #-----------------------------------------------------------------------------
   #
   # Returns filename of map-ready catalog ASCII data.
   #
   # Input: 
   #        file_path - Path to the file.
   #        start_date - Start date for the catalog.
   #        result_dir - Optional directory to store map file to. Default is None.
   #
   # Output:
   #        Full path to the map file.
   #
   @staticmethod
   def mapFilename (file_path, 
                    start_date, 
                    result_dir = None):
      """ Returns full path to the filename for the map-ready catalog data."""

        
      data_path, data_name = os.path.split(file_path)
      
      # Use other than original catalog directory to store map-ready file to
      # if such directory is specified.
      if result_dir is not None:
         data_path = result_dir
         
      date_str = ''
      if start_date is not None:
         date_str = start_date.strftime("%Y_%m_%d_")
         
      return os.path.join(data_path, "%s%s%s" %(CSEP.Forecast.MapReadyPrefix, 
                                                date_str,
                                                CSEPFile.Name.ascii(data_name)))
   

   #-----------------------------------------------------------------------------
   #
   # toASCIIMap
   # 
   # This method creates map-ready catalog data, and writes it to the following 
   # ASCII format file:
   # 1. Longitude
   # 2. Latitude
   # 3. Magnitude
   #
   # Input: 
   #         catalog_file - Path to the catalog file.
   #         start_date - Start date for the catalog. In a case if catalog file
   #                      is shared by "original" and "corrected" forecasts groups,
   #                      it would need to filter catalog events by the start date
   #                      of the forecast testing period. Default is None.
   #         dir_path - Optional directory to store map-ready catalog file.
   #                    Default is None.
   #
   # Output:
   #         Filepath to the map-ready catalog data.
   #
   @staticmethod 
   def toASCIIMap (catalog_path, 
                   start_date = None,
                   dir_path = None):
      """  Create map-ready catalog data, and write it to the ASCII \
format file."""
      
      
      map_filename = Catalog.mapFilename(catalog_path, 
                                         start_date, 
                                         dir_path)
      
      # Check if file already exists
      if os.path.exists(map_filename) is True:
      
         return map_filename
      

      # Create file
      fhandle = CSEPFile.openFile(catalog_path)
      
      out_fhandle = CSEPFile.openFile(map_filename, 
                                      CSEPFile.Mode.WRITE)

      for event_line in fhandle.readlines():
         
         event_values = event_line.split()
         
         record_event = True
         
         # Check event date
         if start_date is not None:
            # Can't convert string representation of float directly to int:
            event_date = datetime.datetime(int(float(event_values[Catalog.ZMAPFormat.DecimalYear])),
                                           int(float(event_values[Catalog.ZMAPFormat.Month])),
                                           int(float(event_values[Catalog.ZMAPFormat.Day])),
                                           int(float(event_values[Catalog.ZMAPFormat.Hour])),
                                           int(float(event_values[Catalog.ZMAPFormat.Minute])),
                                           int(float(event_values[Catalog.ZMAPFormat.Second])),
                                           CSEP.Time.microseconds(float(event_values[Catalog.ZMAPFormat.Second])))
         
            if event_date < start_date:
               record_event = False

         if record_event is True:
             out_fhandle.write("%s\t%s\t%s\n" %(event_values[Catalog.ZMAPFormat.Longitude], 
                                                event_values[Catalog.ZMAPFormat.Latitude],
                                                event_values[Catalog.ZMAPFormat.Magnitude]))
      
      out_fhandle.close()
      fhandle.close()
      
      _moduleLogger().info("Map-ready ASCII format of observation catalog file '%s': '%s'" 
                           %(catalog_path, 
                             map_filename))
      
      return map_filename
    

#--------------------------------------------------------------------------------
#
# Forecast.
#
# This module contains generic routines for forecast data.
#
class Forecast:
   
   # Static data of the class
   # Class to represent forecast format
   class Format (object):

       MatlabVar = 'mModel'
        
       MinLongitude = 0
       MaxLongitude = 1
       MinLatitude = 2
       MaxLatitude = 3
       DepthTop = 4
       DepthBottom = 5
       MinMagnitude = 6
       MaxMagnitude = 7
       Rate = 8
       MaskBit = 9
       Observations = 10
       PrecomputedZeroLikelihood = 11

   
   #-----------------------------------------------------------------------------
   #
   # Returns filename for the the model map ASCII data.
   #
   @staticmethod
   def mapFilename (file_path, dir_name, test_name = None):
      """ Returns full path to the filename for the forecast map."""

        
      model_path, model_name = os.path.split(file_path)

      # Get rid of FromXMLPostfix (if any) from filename
      model_name = re.sub(CSEP.Forecast.FromXMLPostfix,
                          '',
                          model_name)
      
      prefix = CSEP.Forecast.MapReadyPrefix
      if test_name is not None:
         prefix += test_name
         prefix += "_"
      
      return os.path.join(dir_name, "%s%s" %(prefix, 
                                             CSEPFile.Name.ascii(model_name)))

   
   #--------------------------------------------------------------------
   #
   # toMatlab.
   # 
   # This method converts forecast data from ASCII to the Matlab format.
   #
   # Input: 
   #         model_file - Filename for forecast in ASCII format.
   #         result_variable - Matlab variable name for the result data. 
   #                           Default is 'mModel'.   
   #
   # Output: 
   #         Filename for Matlab format data.
   #
   @staticmethod 
   def toMatlab (model_file, 
                 result_variable = None,
                 result_file = None):
      """ Convert ASCII forecast data into Matlab format, and save it to the file."""
      
      # Python had  problems using Forecast.Format.MatlabVar as 
      # default value for input arguments to the function, so have to do it
      # within the function (most likely because function is defined within
      # "Forecast" namespace too)
      if result_variable is None:
          result_variable = Forecast.Format.MatlabVar
      
      # Load ASCII data from the file
      np_array = np.fromfile(model_file)
      if np_array.size == 0:
          np_array.shape = 0, 0
          
      else:
         np_array = CSEPFile.read(model_file)
         
      __matlab_filename = result_file
      if __matlab_filename is None:
          __matlab_filename = CSEPFile.Name.matlab(model_file)
          
      scipy.io.savemat(__matlab_filename,
                       {result_variable : np_array})
        
      
      return __matlab_filename


   #-----------------------------------------------------------------------------
   #
   # toASCII
   # 
   # This method converts forecast data from Matlab to ASCII format.
   #
   # Input: 
   #         model_file - Filename for forecast in Matlab format.
   #         result_variable - Matlab variable name for the result data. 
   #                           Default is 'mModel'.
   #         result_file - Optional filename for result data in ASCII format.
   #                       Default is None, meaning that original model_file
   #                       with replaced extension to ASCII will be used to store
   #                       result data.   
   #
   # Output: Filename for ASCII data.
   # 
   @staticmethod
   def toASCII (model_file, 
                result_variable = None,
                result_file = None):
      """ Convert Matlab forecast data into ASCII format, and save it to the file.
          The function uses the same filename but with ASCII extension to 
          store ASCII formatted data."""

      # Python had  problems using Forecast.Format.MatlabVar as 
      # default value for input arguments to the function, so have to do it
      # within the function (most likely because function is defined within
      # "Forecast" namespace too)
      if result_variable is None:
          result_variable = Forecast.Format.MatlabVar

      forecast = None
      
      # Get rid of warning by setting 'struct_as_record' argument
      forecast_fh = scipy.io.loadmat(model_file,
                                     struct_as_record=True)
        
      if result_variable in forecast_fh:
          forecast = forecast_fh[result_variable]
      else:
            error_msg = "Unexpected variable is specified by '%s' forecast file. \
Expected one of %s (got %s)" %(model_file,
                               result_variable,
                               forecast_fh.keys())
            _moduleLogger().error(error_msg)
            raise RuntimeError, error_msg
        
      
      # Save data to ASCII file
      __ascii_filename = result_file
      if result_file is None:
          __ascii_filename = CSEPFile.Name.ascii(model_file)
      
      _write_catalog(__ascii_filename,
                     forecast)
      
      return __ascii_filename


#--------------------------------------------------------------------------------
#
# GeoUtils
#
# This class contains generic geodesic utilities.
#
class GeoUtils (object):   
   
   #--------------------------------------------------------------------------------
   #
   # Utility to compute the approximate area (in square km) of a rectangular 
   # lat-lon region specified by its NW and SE corners (decimal degrees lat and lon)
   #
   # Input:
   #        nwCornerLat - latitude of the NW corner of the rectangular region in 
   #                      which we're interested
   #        nwCornerLon - longitude of the NW corner of the rectangular region in 
   #                      which we're interested
   #        seCornerLat - latitude of the SE corner of the rectangular region in 
   #                      which we're interested
   #        seCornerLon - longitude of the SE corner of the rectangular region in 
   #                      which we're interested
   #
   # Output:
   #         approximate area in square km of the specified rectangular region
   #
   @staticmethod
   def areaOfRectangularRegion(nwCornerLat, nwCornerLon, 
                               seCornerLat, seCornerLon):
      """ Compute the approximate area (in square km) of a rectangular 
          lat-lon region specified by its NW and SE corners (decimal degrees lat and lon)
          
          Java implementation as provided by Jeremy Zechar:
              /**
              * Compute the approximate area (in square km) of a rectangular lat-lon region specified by its NW and SE corners (decimal degrees lat and lon).  We can think of this 
              * region as a trapezoid b/c the distance b/w the east and west sides of the "rectangle" will be smaller on the side of the rectangle further from the equator.  This 
              * implementation assumes that the rectangle does not cross the equator.  To picture this, consider a trapezoid with a top length of a, bottom length of c, and the side length 
              * of b.  Then we call e the height of the trapezoid and d the difference  b/w a and c.  Then the total area is the sum of three areas: the rectangle with height e and length 
              * which is the shorter of a and c; two equiareal triangles containing the leftovers, each of area de/2.  Thus the total area is min(a,c)*e + d*e.
              * 
              * @param nwCornerLat latitude of the NW corner of the rectangular region in which we're interested
              * @param nwCornerLon longitude of the NW corner of the rectangular region in which we're interested
              * @param seCornerLat latitude of the SE corner of the rectangular region in which we're interested
              * @param seCornerLon longitude of the SE corner of the rectangular region in which we're interested
              * @return approximate area in square km of the specified rectangular region
              */
             public static float areaOfRectangularRegion(float nwCornerLat, float nwCornerLon, float seCornerLat, float seCornerLon) {
                 float topWidth = GeoUtil.vincentyDistanceBetweenPoints(nwCornerLat, nwCornerLon, nwCornerLat, seCornerLon);
                 float bottomWidth = GeoUtil.vincentyDistanceBetweenPoints(seCornerLat, nwCornerLon, seCornerLat, seCornerLon);
                 float height = GeoUtil.vincentyDistanceBetweenPoints(nwCornerLat, nwCornerLon, seCornerLat, nwCornerLon);
         
                 float a = topWidth;
                 float b = height;
                 float c = bottomWidth;
                 float d = (float) Math.abs(0.5 * (a - c));
                 float e = (float) Math.sqrt(b * b - d * d);
         
                 float area = e * (Math.min(a, c) + d);
                 return area;
             }"""
   
      topWidth = GeoUtils.vincentyDistanceBetweenPoints(nwCornerLat, nwCornerLon, 
                                                        nwCornerLat, seCornerLon)
      bottomWidth = GeoUtils.vincentyDistanceBetweenPoints(seCornerLat, nwCornerLon, 
                                                           seCornerLat, seCornerLon)
      height = GeoUtils.vincentyDistanceBetweenPoints(nwCornerLat, nwCornerLon, 
                                                      seCornerLat, nwCornerLon)
   
      a = topWidth
      b = height
      c = bottomWidth
      d = math.fabs(0.5 * (a - c))
      e = math.sqrt(b * b - d * d)
   
      return e * (min(a, c) + d)
   
   
   #--------------------------------------------------------------------------------
   #
   # Utility to compute the approximate area (in square km) of a rectangular 
   # lat-lon region specified by its NW and SE corners (decimal degrees lat and lon)
   #
   # Input:
   #        latOrigin - first latitude point
   #        lonOrigin - first longitude point
   #        latDestination - second latitude point
   #        lonDestination - second longitude point
   #
   # Output:
   #         Vincenty distance b/w specified lat-lon points
   #
   @staticmethod
   def vincentyDistanceBetweenPoints(latOrigin, lonOrigin, 
                                     latDestination, lonDestination):
      """ Compute the Vincenty distance (in km) b/w two lat/lon points, 
          each of which is specified in decimal degrees.
          
          Java implementation as provided by Jeremy Zechar:

          /**
           * Compute the Vincenty distance (in km) b/w two lat/lon points, each of which is specified in decimal degrees.  We use the WGS-84 model for the Earth's ellipsoid.
           *
           * @param latOrigin first latitude point
           * @param lonOrigin first longitude point
           * @param latDestination second latitude point
           * @param lonDestination second longitude point
           * @return Vincenty distance b/w specified lat-lon points
           */
          public static float vincentyDistanceBetweenPoints(float latOrigin, float lonOrigin, float latDestination, float lonDestination) {
              double a = 6378.137;
              double b = 6356.7523142;
              double f = (a - b) / a;
      
              // The distance formula expects lat, lon in radians, so we need to convert them from degrees
              latOrigin = (float) Math.toRadians(latOrigin);
              lonOrigin = (float) Math.toRadians(lonOrigin);
              latDestination = (float) Math.toRadians(latDestination);
              lonDestination = (float) Math.toRadians(lonDestination);
      
              double L = lonOrigin - lonDestination;
              double U_1 = Math.atan((1 - f) * Math.tan(latOrigin));
              double U_2 = Math.atan((1 - f) * Math.tan(latDestination));
      
              double lambda = L;
              double lambdaPrime = 2 * Math.PI;
              double cosSquaredAlpha = 0;
              double sinSigma = 0;
              double cosSigma = 0;
              double cos2Sigma_m = 0;
              double sigma = 0;
              double epsilon = 1e-12;
              
              while (Math.abs(lambda - lambdaPrime) > epsilon) {
                  double temp1 = Math.cos(U_2) * Math.sin(lambda);
                  double temp2 = Math.cos(U_1) * Math.sin(U_2) - Math.sin(U_1) * Math.cos(U_2) * Math.cos(lambda);
                  sinSigma = Math.sqrt(temp1 * temp1 + temp2 * temp2);
                  cosSigma = Math.sin(U_1) * Math.sin(U_2) + Math.cos(U_1) * Math.cos(U_2) * Math.cos(lambda);
                  sigma = Math.atan2(sinSigma, cosSigma);
                  double sinAlpha = Math.cos(U_1) * Math.cos(U_2) * Math.sin(lambda) / (sinSigma + Double.MIN_VALUE);
                  cosSquaredAlpha = 1 - sinAlpha * sinAlpha;
                  cos2Sigma_m = Math.cos(sigma) - 2 * Math.sin(U_1) * Math.sin(U_2) / (cosSquaredAlpha + Double.MIN_VALUE);
                  double C = f / 16 * cosSquaredAlpha * (4 + f * (4 - 3 * cosSquaredAlpha));
                  lambdaPrime = lambda;
                  lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2Sigma_m + C * cosSigma * (-1 + 2 * cos2Sigma_m * cos2Sigma_m)));
              }
      
              double uSquared = cosSquaredAlpha * (a * a - b * b) / (b * b);
              double A = 1 + uSquared / 16384 * (4096 + uSquared * (-768 + uSquared * (320 - 175 * uSquared)));
              double B = uSquared / 1024 * (256 + uSquared * (74 - 47 * uSquared));
              double deltaSigma = B * sinSigma * (cos2Sigma_m + B / 4 * (cosSigma * (-1 + 2 * cos2Sigma_m * cos2Sigma_m - B / 6 *
                      cos2Sigma_m * (-3 + 4 * sinSigma * sinSigma * (-3 + 4 * cos2Sigma_m * cos2Sigma_m)))));
      
              float distance = (float) (b * A * (sigma - deltaSigma));
              return (distance);
          }        
        """      

      a = 6378.137
      b = 6356.7523142
      f = (a - b) / a

      # The distance formula expects lat, lon in radians, so we need to convert
      # them from degrees
      latOrigin = math.radians(latOrigin)
      lonOrigin = math.radians(lonOrigin)
      latDestination = math.radians(latDestination)
      lonDestination = math.radians(lonDestination)

      L = lonOrigin - lonDestination
      U_1 = math.atan((1 - f) * math.tan(latOrigin))
      U_2 = math.atan((1 - f) * math.tan(latDestination))

      lambda_var = L
      lambdaPrime = 2 * math.pi
      cosSquaredAlpha = 0
      sinSigma = 0
      cosSigma = 0
      cos2Sigma_m = 0
      sigma = 0
      epsilon = 1e-12
      
      # Python doesn't provide min_float constant (Double.MIN_VALUE in Java), 
      # compute it explicitly
      min_float = math.pow(2, -1074)
      if min_float == 0.0:
         error_msg = "Error initializing minimum positive floating point number."
         
         _moduleLogger().error(error_msg)
         raise RuntimeError, error_msg
        
        
      while math.fabs(lambda_var - lambdaPrime) > epsilon:
         
          temp1 = math.cos(U_2) * math.sin(lambda_var)
          temp2 = math.cos(U_1) * math.sin(U_2) - math.sin(U_1) * math.cos(U_2) * math.cos(lambda_var)
          sinSigma = math.sqrt(temp1 * temp1 + temp2 * temp2)
          cosSigma = math.sin(U_1) * math.sin(U_2) + math.cos(U_1) * math.cos(U_2) * math.cos(lambda_var)
          sigma = math.atan2(sinSigma, cosSigma)
          sinAlpha = math.cos(U_1) * math.cos(U_2) * math.sin(lambda_var) / (sinSigma + min_float)
          cosSquaredAlpha = 1 - sinAlpha * sinAlpha
          cos2Sigma_m = math.cos(sigma) - 2 * math.sin(U_1) * math.sin(U_2) / (cosSquaredAlpha + min_float)
          C = f / 16 * cosSquaredAlpha * (4 + f * (4 - 3 * cosSquaredAlpha))
          lambdaPrime = lambda_var
          lambda_var = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2Sigma_m + C * cosSigma * (-1 + 2 * cos2Sigma_m * cos2Sigma_m)))

      uSquared = cosSquaredAlpha * (a * a - b * b) / (b * b)
      A = 1 + uSquared / 16384 * (4096 + uSquared * (-768 + uSquared * (320 - 175 * uSquared)))
      B = uSquared / 1024 * (256 + uSquared * (74 - 47 * uSquared))
      deltaSigma = B * sinSigma * (cos2Sigma_m + B / 4 * (cosSigma * (-1 + 2 * cos2Sigma_m * cos2Sigma_m - B / 6 *
                   cos2Sigma_m * (-3 + 4 * sinSigma * sinSigma * (-3 + 4 * cos2Sigma_m * cos2Sigma_m)))))
      distance = b * A * (sigma - deltaSigma)
      return distance



# NOTE(fab): numpy.set_printoptions() does not work
# np.set_printoptions(nanstr='NaN')
# Fix by Fabian for Trac ticket #244: Replace 'nan' with 'NaN' when writing numpy array to the file
# TODO: Should use np.set_printoptions when it's working
#
def _write_catalog( filename, data ):
    """Write a numpy array to disk and replace 'nan' with 'NaN'"""
    np.savetxt( filename, data )
    sed_command = 'sed -i -e "s/nan/NaN/g" %s' % filename

    Environment.invokeCommand( sed_command )
    

