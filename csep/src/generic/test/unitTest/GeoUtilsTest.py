"""
Module GeoUtilsTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import unittest, os, math

import CSEPGeneric, CSEPFile
from CSEPTestCase import CSEPTestCase


 #-------------------------------------------------------------------------------
 #
 # Validate that GeoUtils functionality is working properly.
 #
class GeoUtilsTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'geoUtils')

   
   #--------------------------------------------------------------------
   #
   # This test verifies a fix for ticket #1: catalog data is cut to the geographical area.
   # It verifies result data based on ASCII files.
   #
   def test(self):
      """ Confirm that GeoUtils.areaOfRectangularRegion works properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, "AreaOfRectangularRegion")

      # Lon/Lat indices for cell centers 
      lat_index = 0
      lon_index = 1
      area_index = 2
      cell_half_dim = 0.25

      # Each reference file for the test contains data in the following format:
      # latitude longitude area(square km)
      # where the latitude and longitude refer to the center of the cell and 
      # each cell is 0.5 degree x 0.5 degree
      # Jeremy provided reference data that he generated with original Java code
      for each_file in ['nwPacificArea.txt', 'swPacificArea.txt']:
         
         reference_file = os.path.join(self.__referenceDataDir, each_file)

         for each_line in CSEPFile.openFile(reference_file):

            tokens = [float(i) for i in each_line.split()]
            
            nw_lon = tokens[lon_index] - cell_half_dim
            nw_lat = tokens[lat_index] + cell_half_dim
            se_lon = tokens[lon_index] + cell_half_dim
            se_lat = tokens[lat_index] - cell_half_dim
            
            #print "Lat=", tokens[lat_index], "Lon=", tokens[lon_index], \
            #      nw_lon, nw_lat, se_lon, se_lat
            
            # Compute cell area, and multiply it's rate by area in km^2
            cell_area = CSEPGeneric.GeoUtils.areaOfRectangularRegion(nw_lat, nw_lon,
                                                                     se_lat, se_lon)
      
   
            ### Validate results
            percent_diff = 2*math.fabs(cell_area - tokens[area_index])/(cell_area + tokens[area_index])
            self.failIf(percent_diff > 1, 
                        "Percent difference exceeds 1 percent (%s) computing '%s' area for lat=%s lon=%s: got %s, expected %s"
                        %(percent_diff, each_file, 
                          tokens[lat_index], tokens[lon_index],
                          cell_area, tokens[area_index]))
      

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
