"""
Module ForecastMapTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os, unittest, shutil, datetime

import CSEP, CSEPFile, CSEPGeneric, GeographicalRegions
from ForecastGroup import ForecastGroup
from CSEPTestCase import CSEPTestCase
from RELMAftershockPostProcess import RELMAftershockPostProcess
from OneYearModelPostProcess import OneYearModelPostProcess
from OneDayModelPostProcess import OneDayModelPostProcess
from ForecastHandlerFactory import ForecastHandlerFactory
from ForecastHandler import ForecastHandler
from PolygonForecastHandler import PolygonForecastHandler


#-------------------------------------------------------------------------------
#
# Validate that map file of the forecast is generated according to the rules:
# 1. Map-ready forecast file has 3 columns: 
#    * longitude
#    * latitude
#    * sum of forecast cell bins rates (scaled by factor in step 1) or 'nan'
#      if all bins within the cell have masking bit set to '0' 
# 
class ForecastMapTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'forecastMap')

   # File : longitude, latitude, sum of rates
   __referenceData = { 'test.model.dat' : ["-125.35 40.15 6.7 1",
                                           "-125.35 40.25 3.0 0",
                                           "-125.35 40.35 2.5 1"]}
   
   # Catalog data: longitude, latitude, magnitude
   __catalogData = ["-1.1522783000000000e+02 3.2306669999999997e+01 5.3700000000000001e+00",
                    "-1.2443350000000000e+02 4.0280670000000001e+01 5.0000000000000000e+00"]
   
   # Catalog data: longitude, latitude, magnitude
   __catalogDataLaterDate = ["-1.2443350000000000e+02 4.0280670000000001e+01 5.0000000000000000e+00"]
   
   
   #--------------------------------------------------------------------
   #
   # Overwrite CSEPTestCase initialization routine for Matlab.
   #
   def initialize(self):
       """ Initialize Matlab related variables for the test."""

       CSEPTestCase.initialize(self)
       CSEP.Forecast.initialize(forecast_map = True)
   
   
   #-----------------------------------------------------------------------------
   #
   # This test verifies that map-ready forecast data is created properly.
   #
   def testCaliforniaMap(self):
      """ Confirm that map-ready forecast data is generated according to the \
rules."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy forecast group directory to the test directory
      local_forecast_dir = os.path.join(CSEPTestCase.TestDirPath,
                                        'models')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir, 'models'),
                      local_forecast_dir)

      # Copy observation catalog to the test directory
      local_event_dir = os.path.join(CSEPTestCase.TestDirPath,
                                     'observations')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir,
                                   'observations'),
                      local_event_dir)
      local_event_file = os.path.join(local_event_dir,
                                      'catalog.nodecl.dat')
      
      group = ForecastGroup(local_forecast_dir,
                            RELMAftershockPostProcess.Type)
      CSEP.Forecast.GenerateMap = True

      # Create map - use test directory as results directory
      for each_model in group.files():
         
         png_map_filename = group.createMap(each_model,
                                            CSEPTestCase.TestDirPath,
                                            local_event_file,
                                            scale_factor = 0.5)
         
         # Check that map file in PNG format was generated
         error = "Failed to generate map file for the model: %s" %png_map_filename
         self.failIf(os.path.exists(png_map_filename) is False, error)
         
         ### Validate results - make sure file got generated
         map_filename = CSEPGeneric.Forecast.mapFilename(each_model,
                                                            CSEPTestCase.TestDirPath)
         
         error = "Expected forecast map file '%s' does not exist." %(map_filename)
         self.failIf(os.path.exists(map_filename) is False, error)
            
         # Read file in and compare against reference data
         fhandle = CSEPFile.openFile(map_filename)
         lines = fhandle.readlines()
         fhandle.close()
         
         # Reference data is 3 events that are repeated throughout the model
         for i, result_line in enumerate(lines): 
                                                #ForecastMapTest.__referenceData[each_model]):

            error_msg = "Failed to compare forecast map file lines: test line '%s' vs. \
reference line '%s'" %(result_line, ForecastMapTest.__referenceData[each_model][i%3])
            self.failIf(CSEPFile.compareLines(result_line, 
                                              ForecastMapTest.__referenceData[each_model][i%3]) is not True,
                        error_msg)
      
      
      ### Check that map-ready catalog data is in proper format:
      fhandle = CSEPFile.openFile(CSEPGeneric.Catalog.mapFilename(local_event_file,
                                                                  group.postProcess().start_date))
      lines = fhandle.readlines()
      fhandle.close()
      
      for event_line, reference_line in zip(lines, 
                                            ForecastMapTest.__catalogData):
         
         error_msg = "Failed to compare event map file lines: test line '%s' vs. \
reference line '%s'" %(event_line, reference_line)
         self.failIf(CSEPFile.compareLines(event_line, reference_line) is not True,
                     error_msg)
      
      
   #-----------------------------------------------------------------------------
   #
   # This test verifies that map-ready forecast data is created properly for 
   # the group with a later entry date into the testing center.
   #
   def testLaterEntryDateForecastsCaliforniaMap(self):
      """Create maps for forecasts with later entry date into the testing center."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy forecast group directory to the test directory
      local_forecast_dir = os.path.join(CSEPTestCase.TestDirPath,
                                        'models')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir, 'models'),
                      local_forecast_dir)

      # Copy observation catalog to the test directory
      local_event_dir = os.path.join(CSEPTestCase.TestDirPath,
                                     'observations')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir,
                                   'observations'),
                      local_event_dir)
      local_event_file = os.path.join(local_event_dir,
                                      'catalog.nodecl.dat')
      
      group = ForecastGroup(local_forecast_dir,
                            RELMAftershockPostProcess.Type,
                            post_process_inputs=[datetime.datetime(2006, 6, 1),
                                                 datetime.datetime(2011, 6, 1)])
      CSEP.Forecast.GenerateMap = True

      # Create map - use test directory as results directory
      for each_model in group.files():
         
         png_map_filename = group.createMap(each_model,
                                            CSEPTestCase.TestDirPath,
                                            local_event_file, 
                                            scale_factor = 0.5)
         
         # Check that map file in PNG format was generated
         error = "Failed to generate map file for the model: %s" %png_map_filename
         self.failIf(os.path.exists(png_map_filename) is False, error)
         
         ### Validate results - make sure file got generated
         map_filename = CSEPGeneric.Forecast.mapFilename(each_model,
                                                            CSEPTestCase.TestDirPath)
         
         error = "Expected forecast map file '%s' does not exist." %(map_filename)
         self.failIf(os.path.exists(map_filename) is False, error)
            
            
      ### Check that map-ready catalog data is in proper format:
      fhandle = CSEPFile.openFile(CSEPGeneric.Catalog.mapFilename(local_event_file,
                                                                  group.postProcess().start_date))
      lines = fhandle.readlines()
      fhandle.close()
      
      for event_line, reference_line in zip(lines, 
                                            ForecastMapTest.__catalogDataLaterDate):
         
         error_msg = "Failed to compare event map file lines: test line '%s' vs. \
reference line '%s'" %(event_line, reference_line)
         self.failIf(CSEPFile.compareLines(event_line, reference_line) is not True,
                     error_msg)
      

   #-----------------------------------------------------------------------------
   #
   # This test verifies that forecasts maps are generated for the NW Pacific 
   # testing region.
   #
   def testNWPacificMap(self):
      """ Confirm that forecast maps are generated for the NW Pacific testing \
region."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # Setup testing region
      GeographicalRegions.Region().set(GeographicalRegions.NWPacific)
      
      # Copy forecast group directory to the test directory
      forecasts = 'modelsNWPacific'
      local_forecast_dir = os.path.join(CSEPTestCase.TestDirPath,
                                        forecasts)
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir, 
                                   forecasts),
                      local_forecast_dir)

      # Copy observation catalog to the test directory
      local_event_dir = os.path.join(CSEPTestCase.TestDirPath,
                                     'nwObservations')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir,
                                   'nwObservations'),
                      local_event_dir)
      local_event_file = os.path.join(local_event_dir,
                                      'catalog.nodecl.dat')
      
      group = ForecastGroup(local_forecast_dir,
                            OneYearModelPostProcess.Type,
                            post_process_inputs=[datetime.datetime(2008, 5, 9),
                                                 datetime.datetime(2009, 5, 9)])
      
      CSEP.Forecast.GenerateMap = True

      # Create map - use test directory as results directory
      for each_model in group.files():
         
         png_map_filename = group.createMap(each_model,
                                            CSEPTestCase.TestDirPath,
                                            local_event_file)
         
         # Check that map file in PNG format was generated
         error = "Failed to generate map file for the model: %s" %png_map_filename
         self.failIf(os.path.exists(png_map_filename) is False, 
                     error)
         
         ### Validate results - make sure file got generated
         map_filename = CSEPGeneric.Forecast.mapFilename(each_model,
                                                            CSEPTestCase.TestDirPath)
         
         error = "Expected forecast map file '%s' does not exist." %(map_filename)
         self.failIf(os.path.exists(map_filename) is False, error)

      GeographicalRegions.Region().set(GeographicalRegions.California)
      

   #-----------------------------------------------------------------------------
   #
   # This test verifies that forecasts maps are generated for the SW Pacific 
   # testing region.
   #
   def testSWPacificMap(self):
      """ Confirm that forecast maps are generated for the SW Pacific testing \
region."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # Setup testing region
      GeographicalRegions.Region().set(GeographicalRegions.SWPacific)
      
      # Copy forecast group directory to the test directory
      forecasts = 'modelsSWPacific'
      local_forecast_dir = os.path.join(CSEPTestCase.TestDirPath,
                                        forecasts)
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir, 
                                   forecasts),
                      local_forecast_dir)

      # Copy observation catalog to the test directory
      local_event_dir = os.path.join(CSEPTestCase.TestDirPath,
                                     'swObservations')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir,
                                   'swObservations'),
                      local_event_dir)
      local_event_file = os.path.join(local_event_dir,
                                      'catalog.nodecl.dat')

      group = ForecastGroup(local_forecast_dir,
                            OneYearModelPostProcess.Type,
                            post_process_inputs=[datetime.datetime(2008, 5, 9),
                                                 datetime.datetime(2009, 5, 9)])
      
      CSEP.Forecast.GenerateMap = True

      # Create map - use test directory as results directory
      for each_model in group.files():
         
         png_map_filename = group.createMap(each_model,
                                            CSEPTestCase.TestDirPath,
                                            local_event_file)
         
         # Check that map file in PNG format was generated
         error = "Failed to generate map file for the model: %s" %png_map_filename
         self.failIf(os.path.exists(png_map_filename) is False, 
                     error)
         
         ### Validate results - make sure file got generated
         map_filename = CSEPGeneric.Forecast.mapFilename(each_model,
                                                            CSEPTestCase.TestDirPath)
         
         error = "Expected forecast map file '%s' does not exist." %(map_filename)
         self.failIf(os.path.exists(map_filename) is False, error)

      GeographicalRegions.Region().set(GeographicalRegions.California)


   #-----------------------------------------------------------------------------
   #
   # This test verifies that forecasts maps are generated for the Global 
   # testing region.
   #
   def testGlobalMap(self):
      """ Confirm that forecast maps are generated for the Global testing \
region."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # Setup testing region
      GeographicalRegions.Region().set(GeographicalRegions.Global)
      
      # Copy forecast group directory to the test directory
      forecasts = 'modelsGlobal'
      local_forecast_dir = os.path.join(CSEPTestCase.TestDirPath,
                                        forecasts)
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir, 
                                   forecasts),
                      local_forecast_dir)

      # Copy observation catalog to the test directory
      local_event_dir = os.path.join(CSEPTestCase.TestDirPath,
                                     'globalObservations')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir,
                                   'globalObservations'),
                      local_event_dir)
      local_event_file = os.path.join(local_event_dir,
                                      'catalog.nodecl.dat')

      group = ForecastGroup(local_forecast_dir,
                            OneYearModelPostProcess.Type,
                            post_process_inputs=[datetime.datetime(2008, 11, 9),
                                                 datetime.datetime(2009, 11, 9)])
      
      CSEP.Forecast.GenerateMap = True

      # Create map - use test directory as results directory
      for each_model in group.files():
         
         png_map_filename = group.createMap(each_model,
                                            CSEPTestCase.TestDirPath,
                                            local_event_file)
         
         # Check that map file in PNG format was generated
         error = "Failed to generate map file for the model: %s" %png_map_filename
         self.failIf(os.path.exists(png_map_filename) is False, 
                     error)
         
         ### Validate results - make sure file got generated
         map_filename = CSEPGeneric.Forecast.mapFilename(each_model,
                                                            CSEPTestCase.TestDirPath)
         
         error = "Expected forecast map file '%s' does not exist." %(map_filename)
         self.failIf(os.path.exists(map_filename) is False, error)

      GeographicalRegions.Region().set(GeographicalRegions.California)
      

   #-----------------------------------------------------------------------------
   #
   # This test verifies that forecasts maps are generated for the Global 
   # testing region.
   #
   def testOceanicTransformFaultsMap(self):
      """ Confirm that forecast maps are generated for the OceanicTransformFaults \
testing region."""

      # Setup test name
      CSEPTestCase.setTestName(self, self.id())

      # Setup testing region
      GeographicalRegions.Region().set(GeographicalRegions.OceanicTransformFaults)

      # Set current forecast handler to polygon-based:
      ForecastHandlerFactory().object(PolygonForecastHandler.Type)
      
      # Copy forecast group directory to the test directory
      forecasts = 'modelsOceanicTransformFaults'
      local_forecast_dir = os.path.join(CSEPTestCase.TestDirPath,
                                        forecasts)
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir, 
                                   forecasts),
                      local_forecast_dir)

      # Copy observation catalog to the test directory
      local_event_dir = os.path.join(CSEPTestCase.TestDirPath,
                                     'globalObservations')
      shutil.copytree(os.path.join(ForecastMapTest.__referenceDataDir,
                                   'globalObservations'),
                      local_event_dir)
      local_event_file = os.path.join(local_event_dir,
                                      'catalog.nodecl.dat')

      group = ForecastGroup(local_forecast_dir,
                            OneDayModelPostProcess.Type)
      
      CSEP.Forecast.GenerateMap = True

      # Create map - use test directory as results directory
      for each_model in group.files():
         
         png_map_filename = group.createMap(each_model,
                                            CSEPTestCase.TestDirPath,
                                            local_event_file)
         
         # Check that map file in PNG format was generated
         error = "Failed to generate map file for the model: %s" %png_map_filename
         self.failIf(os.path.exists(png_map_filename) is False, 
                     error)
         
         ### Validate results - make sure file got generated
         map_filename = CSEPGeneric.Forecast.mapFilename(each_model,
                                                            CSEPTestCase.TestDirPath)
         
         error = "Expected forecast map file '%s' does not exist." %(map_filename)
         self.failIf(os.path.exists(map_filename) is False, error)

      GeographicalRegions.Region().set(GeographicalRegions.California)


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
