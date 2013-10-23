"""
RegionInfo module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os
import numpy as np
import CSEPLogging, CSEPFile
from Environment import *


California = 'California'
SWPacific = 'SWPacific'
NWPacific = 'NWPacific'
Global = 'Global'

#--------------------------------------------------------------------------------
#
# Structure-like class to store variables specific to the CSEP testing region.
# 
class RegionInfo (object):
   
   # Indeces to access area file fields
   __areaMinLatIndex = 0
   __areaMaxLatIndex = 1
   __areaMinLongIndex = 2
   __areaMaxLongIndex = 3        
  
   # For file with grid cells coordinates
   __lonIndex = 0
   __latIndex = 1
   
   __defaultMapScriptLocation = os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                             'src', 
                                             'GMTScripts')
   
       ### Script name to invoke GMT map generation
   __GMTScriptFilename = 'invoke_gmt.sh'


   def __init__(self,
                collection_area, 
                testing_area,
                map_script, 
                map_script_location = __defaultMapScriptLocation): 
      
      self.collectionArea = collection_area
      self.testArea = testing_area

      # Script to invoke for map generation
      self.mapScript = map_script

      # Path to GMT scripts and related files used to generate forecast map
      self.mapScriptLocation = map_script_location
      
      if map_script_location is None:
          self.mapScriptLocation = RegionInfo.__defaultMapScriptLocation
      
   
   #-----------------------------------------------------------------------------
   #
   # areaCoordinates
   # 
   # Returns lists of minimum and maximum latitude/longitude coordinates that
   # define a testing geographical region.
   #
   # Inputs:
   #         area_file - Area file, default is None meaning that test area of
   #                     of the region should be used.
   #         is_for_map - Flag if area coordinates are requested for mapping 
   #                      purposes. Default is False.
   #    
   def areaCoordinates(self, 
                       area_file = None, 
                       is_for_map = False):  
      """Returns tuple of lists that represent minimum latitude, maximum
         latitude, minimum longitude, and maximum longitude of test area for the
         region."""
          
      min_lat = []
      max_lat = []
      min_lon = []
      max_lon = []

      __area = area_file
      
      # Use test area of the region by default
      if area_file is None and self.testArea is not None:
          __area = CSEPFile.Name.ascii(self.testArea)
          
      # Some regions have testing area set to None 
      if __area is not None:
            
          area_entries = CSEPFile.read(__area)        
        
          __rows, __cols = area_entries.shape
          
          # Grid coordinates are provided (like for California)
          if __cols == 2:
                 
              min_lat = area_entries[:, RegionInfo.__latIndex].min()
              max_lat = area_entries[:, RegionInfo.__latIndex].max()
              min_lon = area_entries[:, RegionInfo.__lonIndex].min()
              max_lon = area_entries[:, RegionInfo.__lonIndex].max()
          
          else: 
              # min/max values for lon/lat are provided (like for WesternPacific)       
           
              min_lat = area_entries[:, RegionInfo.__areaMinLatIndex].tolist()
              max_lat = area_entries[:, RegionInfo.__areaMaxLatIndex].tolist()
              min_lon = area_entries[:, RegionInfo.__areaMinLongIndex].tolist()
              max_lon = area_entries[:, RegionInfo.__areaMaxLongIndex].tolist()

          # Area coordinates should be returned as single values for the purpose
          # of map generation
          if (isinstance(min_lat, list) is True) and (is_for_map is True):
              min_lat = min(min_lat)
              max_lat = max(max_lat)
              min_lon = min(min_lon)
              max_lon = max(max_lon)
          
      return (min_lat, max_lat, min_lon, max_lon)  


   #-----------------------------------------------------------------------------
   #
   # testAreaBorder
   # 
   # Returns lists of x and y coordinates that define a border for the testing
   # area of the region.
   #
   # Inputs:
   #         area_file - File with area coordinates
   #
   @classmethod    
   def areaBorders(cls, area_file):  
      """Returns tuple of x and y coordinates that represent longitude and 
         latitude coordinates of the border of test area for the region."""

      border_x, border_y = [], []
      
      # Test area is defined for the region
      if area_file is not None:
          
        # Load area coordinates for the testing region
        area = CSEPFile.read(CSEPFile.Name.ascii(area_file))

        __rows, __cols = area.shape
        
        # Grid coordinates are provided (like for California)
        if __cols == 2:
                 
            area_x = area[:, RegionInfo.__lonIndex]
            area_y = area[:, RegionInfo.__latIndex]
            
            # Remove duplicate values
            unique_area_x = area_x.tolist()
    
            __s = set(unique_area_x)
            unique_area_x = list(__s)
            unique_area_x.sort()
            
            unique_area_y = area_y.tolist()
            __s = set(unique_area_y)
            unique_area_y = list(__s)
            unique_area_y.sort()
            
            __xnum = len(unique_area_x)
            __ynum = len(unique_area_y)
            
            __test_area = np.array([False] * __xnum*__ynum)
            __test_area.shape = (__ynum, __xnum)
    
            for each_lon, each_lat in zip(area_x, 
                                          area_y):
                
                __lon_index = unique_area_x.index(each_lon)
                __lat_index = unique_area_y.index(each_lat)
    
                __test_area[__lat_index, __lon_index] = True
            
            left_border = []
            right_border = []
            
            for __lat_index in xrange(0, __ynum):
                prev_cell_mask = False
                
                for __lon_index in xrange(0, __xnum):
                    # Coordinates of the cell
                    __x = __lon_index
                    __y = __lat_index
                    __mask = __test_area[__lat_index, __lon_index]
                    
                    if ((__mask == True) and (prev_cell_mask == False)) or \
                       ((__mask == False) and (prev_cell_mask == True)):
                        
                        
                        if prev_cell_mask == True:
                            # Use coordinates of previous cell for polygon point
                            __x -= 1
                        
                        if prev_cell_mask == False:
                            left_border.append([unique_area_x[__x],
                                                unique_area_y[__y]])
                        else:
                            right_border.append([unique_area_x[__x],
                                                 unique_area_y[__y]])
    
                    # Within the region
                    prev_cell_mask = __mask
            
            # To have continuous border, need to reverse left side of the border
            # before appending it to the right side
            left_border.reverse()        
            right_border.extend(left_border)
            
            # Make it a closed curve
            right_border.append(right_border[0])
            
            border_x = [i[0] for i in right_border]
            border_y = [i[1] for i in right_border]
            
        else:
            # min/max values for lon/lat are provided (like for WesternPacific)       
           
            min_lat = area[:, RegionInfo.__areaMinLatIndex].tolist()
            max_lat = area[:, RegionInfo.__areaMaxLatIndex].tolist()
            min_lon = area[:, RegionInfo.__areaMinLongIndex].tolist()
            max_lon = area[:, RegionInfo.__areaMaxLongIndex].tolist()
            
            for each_min_lat, each_max_lat, each_min_lon, each_max_lon in zip(min_lat,
                                                                              max_lat,
                                                                              min_lon,
                                                                              max_lon):
                
                # Add border points for rectangular area to the coordinates
                border_x.append(each_min_lon)
                border_y.append(each_min_lat)

                border_x.append(each_min_lon)
                border_y.append(each_max_lat)
                
                border_x.append(each_max_lon)
                border_y.append(each_max_lat)
                
                border_x.append(each_max_lon)
                border_y.append(each_min_lat)
            
                # Make border a closed curve
                border_x.append(each_min_lon)
                border_y.append(each_min_lat)


      return border_x, border_y
    

   #---------------------------------------------------------------------------
   #
   # Get testing region grid for the map display
   #
   # Input: None 
   #
   # Output: Tuple of meridians and parallels lists of the the testing grid
   #
   def grid (self, area_file = None, coords = None):
       """ Get testing region grid for the map display."""

       # Use test area of the region by default
       __area = area_file

       min_lat, max_lat, min_lon, max_lon = None, None, None, None
       
       if coords is not None:
           min_lat, max_lat, min_lon, max_lon = coords
       
       else: 
           
           if area_file is None and self.testArea is not None:
               __area = CSEPFile.Name.ascii(self.testArea)
                     
           # Extract region min/max longitude and latitude
           min_lat, max_lat, min_lon, max_lon = self.areaCoordinates(__area,
                                                                     is_for_map = True)


       grid_meridians = [val for val in xrange(int(np.floor(min_lon)), 
                                               int(np.ceil(max_lon)), 1) if val % 5 == 0]

       grid_parallels = [val for val in xrange(int(np.floor(min_lat)), 
                                               int(np.ceil(max_lat)), 1) if val % 2 == 0]

       return (grid_meridians, grid_parallels)
    

   #----------------------------------------------------------------------------
   #
   # Invoke GMT script specific to the testing region to generate the map of the
   # forecast. 
   # This method creates and invokes a bash script to generate the map.
   #
   # Input: 
   #        forecast_file - File path to the forecast in XML format
   #        results_dir - Directory to store result files to. Default is a
   #                      current directory.
   #        test_name - Name of the test for each forecast map is generated.
   #                    Default is None.
   #        catalog_file - Optional observation catalog file to display observed
   #                       events. Default is None.
   #        scale_factor - Scale factor to apply to the forecast. Default value
   #                       is 1.0 (don't scale)
   # Output: 
   #         Filename for the map file
   #
   @classmethod
   def createMap (cls,
                  region,
                  image_file,
                  forecast_data_file,
                  catalog_data_file): 
        """ Create a map of the forecast model based on selected geographical region."""


        # Create a wrapper script: have to set environment variables 
        # required to run the GMT script
        fhandle = CSEPFile.openFile(RegionInfo.__GMTScriptFilename,
                                    CSEPFile.Mode.WRITE)
        fhandle.write("#!" + BASH_SHELL + "\n")
       
        line = "export %s=%s;\n" %(NETCDF_HOME_ENV,
                                   os.environ[NETCDF_HOME_ENV])
        fhandle.write(line)        
       
        line = "export PATH=%s:%s:%s:$PATH;\n" \
                  %(region.mapScriptLocation,
                    os.environ[GMT_HOME_ENV],
                    os.environ[IMAGE_MAGICK_HOME_ENV])
        fhandle.write(line)
       
        fhandle.write("export LD_LIBRARY_PATH=%s;\n" \
                      %os.path.join(os.environ[NETCDF_HOME_ENV],
                                    'lib'))
   
        # To avoid GMT error when catalog file is not provided, don't ask
        # to plot observed events layer
        command = region.mapScript
        events_option = ''
        if catalog_data_file is not None:
           
           events_option = '-e %s' %catalog_data_file
           
           # Check if command already provides plot-layers option
           command_tokens = command.split(' -p ')
           if len(command_tokens) == 2:
               # Append events to the plot-layers option
               command += 'e'
           else:
               command += ' -p e' 
           
        line = '%s -f %s -d %s -o %s -l %s' \
               %(os.path.join(region.mapScriptLocation, 
                              command),
                 forecast_data_file,
                 region.mapScriptLocation,
                 image_file,
                 events_option)
       
        line += '\n' 
          
        fhandle.write(line)
        fhandle.close()
       
       
        # Set executable permissions on the file, and invoke the script
        os.chmod(RegionInfo.__GMTScriptFilename, 0755)
        # Some of the GMT commands generate warnings on stderr, ignore them
        ignore_stderr = True 
        invokeCommand(os.path.join(os.getcwd(), 
                                   RegionInfo.__GMTScriptFilename),
                      ignore_stderr)
        
                
        return image_file

