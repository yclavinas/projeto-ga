"""
Module GeographicalRegionsInitFileTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, datetime

import CSEP, GeographicalRegions, RegionInfo
from Environment import *
from CSEPTestCase import CSEPTestCase


 #--------------------------------------------------------------------
 #
 # Validate that GeographicalRegionsInitFile class is working properly.
 #
class GeographicalRegionInitFileTest (CSEPTestCase):

   # Static data of the class

   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'geographicalRegionsInitFile')

   __referenceDataFile = os.path.join(__referenceDataDir,
                                     'TestGeographicalRegions.init.xml')

   __referenceRegions = {'testRegion1' : RegionInfo.RegionInfo(os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                                            'testDir1',
                                                                            'testCollectionArea1.txt'),
                                                               'testDir1/testArea1.txt',
                                                               'test1_script.foo --option1',
                                                               'src/GMTScripts'),
                                                                        
                         'testRegion2' : RegionInfo.RegionInfo(None,
                                                               os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                                            'testDir2',
                                                                            'testArea2.txt'),
                                                               'test2_script.foo --option1 --option2',
                                                               os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                                            'src', 
                                                                            'GMTScripts'))} 
   
   
   #--------------------------------------------------------------------
   #
   # This test verifies that DispatcherInitFile class identifies  
   # element values properly.
   #
   def testElementsValues(self):
      """ Confirm that GeographicalRegionsInitFile identifies \
elements values properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())
   
      # Remember currently set region
      save_region = GeographicalRegions.Region.Selected
      
      try:   
         init_file = GeographicalRegions.Region(self.__referenceDataDir)
   
         ### Validate results
         
         ### Check that default geographical regions are still available
         expected_regions_names = [GeographicalRegions.California,
                                   GeographicalRegions.NWPacific,
                                   GeographicalRegions.SWPacific,
                                   GeographicalRegions.Global]
         expected_regions_names.extend(GeographicalRegionInitFileTest.__referenceRegions.keys()) 
          
         all_regions_names = GeographicalRegions.Region.all()
         for each_region in expected_regions_names:
             
             self.failIf(each_region not in all_regions_names,
                         '%s region is not available region of %s' %(each_region,
                                                                     all_regions_names))

         ### Check values of newly introduced regions
         for name, region_info in GeographicalRegionInitFileTest.__referenceRegions.iteritems():
             
             # Set current region to one of the test regions
             GeographicalRegions.Region().set(name)
             selected_region = GeographicalRegions.Region.info()
             
             # Verify information about the region
             self.failIf(region_info.collectionArea != selected_region.collectionArea,
                         'Collection area file %s does not match expected %s' %(selected_region.collectionArea,
                                                                                region_info.collectionArea))

             self.failIf(region_info.testArea != selected_region.testArea,
                         'Test area file %s does not match expected %s' %(selected_region.testArea,
                                                                          region_info.testArea))
         
             self.failIf(region_info.mapScript != selected_region.mapScript,
                         "Map script '%s' does not match expected '%s'" %(selected_region.mapScript,
                                                                          region_info.mapScript))

             self.failIf(region_info.mapScriptLocation != selected_region.mapScriptLocation,
                         'Script location %s does not match expected %s' %(selected_region.mapScriptLocation,
                                                                          region_info.mapScriptLocation))
         
         
         ### Test custom class for testRegion1 as provided through configuration file
         GeographicalRegions.Region().set('testRegion1')
         selected_region = GeographicalRegions.Region.info()
         
         min_lat, max_lat, min_lon, max_lon = selected_region.areaCoordinates()
         expected_value = 33
         self.failIf(min_lat[0] != expected_value,
                     'Failed to compare min_lat value as provided by custom class for testRegion1: got %s, expected %s' 
                     %(min_lat[0], expected_value))

         expected_value = 34
         self.failIf(max_lat[0] != expected_value,
                     'Failed to compare max_lat value as provided by custom class for testRegion1: got %s, expected %s' 
                     %(max_lat[0], expected_value))
         
         expected_value = -110
         self.failIf(min_lon[0] != expected_value,
                     'Failed to compare min_lon value as provided by custom class for testRegion1: got %s, expected %s' 
                     %(min_lon[0], expected_value))

         expected_value = -105
         self.failIf(max_lon[0] != expected_value,
                     'Failed to compare max_lon value as provided by custom class for testRegion1: got %s, expected %s' 
                     %(max_lon[0], expected_value))
         
         self.failIf(selected_region.testExtraMethod() != 'foo',
                     'Failed to call extra method as provided by BogusRegionClass at runtime')
      finally:
         
         # Go back to the original directory
         GeographicalRegions.Region().set(save_region) 


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
