"""
Module HybridForecastTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, unittest, shutil, datetime
import numpy as np

import Environment, CSEPFile, CSEPGeneric

from CSEPTestCase import CSEPTestCase
from ForecastGroup import ForecastGroup
from ForecastGroupInitFile import ForecastGroupInitFile
from OneDayModelPostProcess import OneDayModelPostProcess
from BogusForecastModel1 import BogusForecastModel1
from BogusForecastModel2 import BogusForecastModel2
from HybridForecast import HybridForecast
from ForecastHandlerFactory import ForecastHandlerFactory


 #------------------------------------------------------------------------------
 #
 # Validate that HybridForecast class is working properly.
 #
class HybridForecastTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 
                                     'hybridForecast')

   __bogusDataFile = 'CA_one_day_forecast.dat'
   
   
   #--------------------------------------------------------------------
   #
   # Set up testing scenario.
   #
   # Input: 
   #        None.
   # 
   def setUp (self):
        """ Set up routine for the class."""
        
        CSEPTestCase.setUp(self)
        
        # Don't require input catalog when constructing HybridForecast's
        BogusForecastModel1.RequireInputCatalog = False
        BogusForecastModel2.RequireInputCatalog = False


   #--------------------------------------------------------------------
   #
   # Clean up test case scenario by storing testing scenario results.
   #
   # Input: 
   #        None.
   # 
   def tearDown (self):
       """ Cleanup routine for the class."""

       BogusForecastModel1.RequireInputCatalog = True
       BogusForecastModel2.RequireInputCatalog = True

       CSEPTestCase.tearDown(self)

   
   #----------------------------------------------------------------------------
   #
   # This test verifies that HybridForecast file is properly created based
   # on dynamic forecasts models installed within testing framework. 
   #
   def testHybridForecastBasedOnModels(self):
      """ Confirm that HybridForecast generates forecast according to \
provided configuration in ForecastGroup's configuration file. HybridForecast is \
based on dynamic forecasts models installed within testing framework."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      init_file = "forecast_based_on_models.init.xml"
      shutil.copyfile(os.path.join(self.__referenceDataDir, 
                                   init_file),
                      os.path.join(CSEPTestCase.TestDirPath, 
                                   "forecast.init.xml"))    

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)
      
      for each_model in group.models:
            if each_model.type() in [BogusForecastModel1.Type, BogusForecastModel2.Type]:
                
                # Set forecast data for the model
                np_forecast = ForecastHandlerFactory().CurrentHandler.load(os.path.join(HybridForecastTest.__referenceDataDir,
                                                         HybridForecastTest.__bogusDataFile))
                
                if each_model.type() == BogusForecastModel1.Type:
                    np_forecast[:, CSEPGeneric.Forecast.Format.Rate] = 0.1
                else:
                    np_forecast[:, CSEPGeneric.Forecast.Format.Rate] = 0.2
                    
                each_model.data(np_forecast)

      # Create forecasts
      group.create(datetime.datetime(2012, 6, 28),
                   CSEPTestCase.TestDirPath)
      
      ### Validate results 
      
      # Models within the group should include HybridForecast
      result_forecast = os.path.join(group.dir(),
                                     "ModelHybrid_6_28_2012.dat")
                                     
      hybrid_forecast = ForecastHandlerFactory().CurrentHandler.load(result_forecast)
      self.assertFalse(np.any(np.abs(hybrid_forecast[:, CSEPGeneric.Forecast.Format.Rate] - 0.13) >= 1E-10), 
                       "Expected rate of 0.13 for %s" %result_forecast)


   #----------------------------------------------------------------------------
   #
   # This test verifies that HybridForecast file is properly created based
   # on static file-based forecasts within testing framework. 
   #
   def testHybridForecastBasedOnFiles(self):
      """ Confirm that HybridForecast generates forecast according to \
provided configuration in ForecastGroup's configuration file. HybridForecast is \
based on static forecasts within testing framework."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      xmldoc = ForecastGroupInitFile(self.__referenceDataDir, 
                                     "forecast_based_on_files.init.xml")
      
      # Modify path to the forecasts files directory to be relative to the
      # CENTERCODE
      for each_index in xrange(0, 2):
          attrs = xmldoc.elementAttribs(HybridForecast.XML.GroupElement,
                                        index=each_index)
          attrs[HybridForecast.XML.DirAttribute] = os.path.join(self.__referenceDataDir,
                                                                attrs[HybridForecast.XML.DirAttribute])
      
      
      # Write modified file to the test directory
      init_file = os.path.join(CSEPTestCase.TestDirPath, 
                               "forecast.init.xml")
      fhandle = CSEPFile.openFile(init_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)
      
      # Create forecasts
      group.create(datetime.datetime(2012, 6, 28),
                   CSEPTestCase.TestDirPath)
      
      ### Validate results 
      
      # Models within the group should include HybridForecast
      result_forecast = os.path.join(group.dir(),
                                     "FileHybrid_6_28_2012.dat")
                                     
      hybrid_forecast = ForecastHandlerFactory().CurrentHandler.load(result_forecast)
      self.assertFalse(np.any(np.abs(hybrid_forecast[:, CSEPGeneric.Forecast.Format.Rate] - 0.38) >= 1E-10), 
                       "Expected rate of 0.38 for %s" %result_forecast)
      

   #----------------------------------------------------------------------------
   #
   # This test verifies that HybridForecast file is properly created based
   # on tokens to existing forecasts within testing framework. 
   #
   def testHybridForecastBasedOnTokens(self):
      """ Confirm that HybridForecast generates forecast according to \
provided configuration in ForecastGroup's configuration file. HybridForecast is \
based on forecasts filenames tokens within testing framework."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      xmldoc = ForecastGroupInitFile(self.__referenceDataDir, 
                                     "forecast_based_on_tokens.init.xml")
      
      # Modify path to the forecasts files directory to be relative to the
      # CENTERCODE
      for each_index in xrange(0, 2):
          attrs = xmldoc.elementAttribs(HybridForecast.XML.GroupElement,
                                        index=each_index)
          attrs[HybridForecast.XML.DirAttribute] = os.path.join(self.__referenceDataDir,
                                                                attrs[HybridForecast.XML.DirAttribute])
      
      
      # Write modified file to the test directory
      init_file = os.path.join(CSEPTestCase.TestDirPath, 
                               "forecast.init.xml")
      fhandle = CSEPFile.openFile(init_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)
      
      # Create forecasts
      group.create(datetime.datetime(2012, 6, 28),
                   CSEPTestCase.TestDirPath)
      
      ### Validate results 
      
      # Models within the group should include HybridForecast
      result_forecast = os.path.join(group.dir(),
                                     "TokenHybrid_6_28_2012.dat")
                                     
      hybrid_forecast = ForecastHandlerFactory().CurrentHandler.load(result_forecast)
      self.assertFalse(np.any(np.abs(hybrid_forecast[:, CSEPGeneric.Forecast.Format.Rate] - 0.38) >= 1E-10), 
                       "Expected rate of 0.38 for %s" %result_forecast)
      


   #----------------------------------------------------------------------------
   #
   # This test verifies that HybridForecast file is properly created based
   # on static file-based forecasts and dynamicly installed models
   # within testing framework. 
   #
   def testHybridForecastBasedOnFilesAndModels(self):
      """ Confirm that HybridForecast generates forecast according to \
provided configuration in ForecastGroup's configuration file. HybridForecast is \
based on static and dynamic forecasts within testing framework."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      xmldoc = ForecastGroupInitFile(self.__referenceDataDir, 
                                     "forecast_based_on_files_models.init.xml")
      
      # Modify path to the forecasts files directory to be relative to the
      # CENTERCODE
      for each_index in xrange(0, 3):
          attrs = xmldoc.elementAttribs(HybridForecast.XML.GroupElement,
                                        index=each_index)
          if HybridForecast.XML.DirAttribute in attrs:
              attrs[HybridForecast.XML.DirAttribute] = os.path.join(self.__referenceDataDir,
                                                                    attrs[HybridForecast.XML.DirAttribute])
      
      
      # Write modified file to the test directory
      init_file = os.path.join(CSEPTestCase.TestDirPath, 
                               "forecast.init.xml")
      fhandle = CSEPFile.openFile(init_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)

      # Set data for BogusForecastModel's to be compatible with file-based forecast
      for each_model in group.models:
            if each_model.type() in [BogusForecastModel1.Type, BogusForecastModel2.Type]:
                
                # Set forecast data for the model
                np_forecast = ForecastHandlerFactory().CurrentHandler.load(os.path.join(HybridForecastTest.__referenceDataDir,
                                                         HybridForecastTest.__bogusDataFile))
                
                if each_model.type() == BogusForecastModel1.Type:
                    np_forecast[:, CSEPGeneric.Forecast.Format.Rate] = 0.1
                else:
                    np_forecast[:, CSEPGeneric.Forecast.Format.Rate] = 0.2
                    
                each_model.data(np_forecast)

      
      # Create forecasts
      group.create(datetime.datetime(2012, 6, 28),
                   CSEPTestCase.TestDirPath)
      
      ### Validate results 
      
      # Models within the group should include HybridForecast
      result_forecast = os.path.join(group.dir(),
                                     "FileAndModelHybrid_6_28_2012.dat")
                                     
      hybrid_forecast = ForecastHandlerFactory().CurrentHandler.load(result_forecast)
      self.assertFalse(np.any(np.abs(hybrid_forecast[:, CSEPGeneric.Forecast.Format.Rate] - 0.4) >= 1E-10), 
                       "Expected rate of 0.4 for %s" %result_forecast)


   #----------------------------------------------------------------------------
   #
   # This test verifies that HybridForecast file is properly created based
   # on static file-based forecasts and dynamicly installed models
   # within testing framework. 
   #
   def testHybridForecastBasedOnFilesAndModelsWithNVariable(self):
      """ Confirm that HybridForecast generates forecast according to \
provided configuration in ForecastGroup's configuration file. HybridForecast is \
based on static and dynamic forecasts within testing framework with N variable as
provided in configuration file."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      xmldoc = ForecastGroupInitFile(self.__referenceDataDir, 
                                     "forecast_based_on_files_models_withN.init.xml")
      
      # Modify path to the forecasts files directory to be relative to the
      # CENTERCODE
      for each_index in xrange(0, 2):
          attrs = xmldoc.elementAttribs(HybridForecast.XML.GroupElement,
                                        index=each_index)
          if HybridForecast.XML.DirAttribute in attrs:
              attrs[HybridForecast.XML.DirAttribute] = os.path.join(self.__referenceDataDir,
                                                                    attrs[HybridForecast.XML.DirAttribute])
      
      
      # Write modified file to the test directory
      init_file = os.path.join(CSEPTestCase.TestDirPath, 
                               "forecast.init.xml")
      fhandle = CSEPFile.openFile(init_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)

      # Set data for BogusForecastModel's to be compatible with file-based forecast
      for each_model in group.models:
            if each_model.type() in [BogusForecastModel1.Type, BogusForecastModel2.Type]:
                
                # Set forecast data for the model
                np_forecast = ForecastHandlerFactory().CurrentHandler.load(os.path.join(HybridForecastTest.__referenceDataDir,
                                                         HybridForecastTest.__bogusDataFile))
                
                if each_model.type() == BogusForecastModel1.Type:
                    np_forecast[:, CSEPGeneric.Forecast.Format.Rate] = 0.1
                else:
                    np_forecast[:, CSEPGeneric.Forecast.Format.Rate] = 0.2
                    
                each_model.data(np_forecast)

      
      # Create forecasts
      group.create(datetime.datetime(2012, 6, 28),
                   CSEPTestCase.TestDirPath)
      
      ### Validate results 
      
      # Models within the group should include HybridForecast
      result_forecast = os.path.join(group.dir(),
                                     "FileWithNAndModelHybrid_6_28_2012.dat")
                                     
      hybrid_forecast = ForecastHandlerFactory().CurrentHandler.load(result_forecast)
      self.assertFalse(np.any(np.abs(hybrid_forecast[:, CSEPGeneric.Forecast.Format.Rate] - 0.26) >= 1E-10), 
                       "Expected rate of 0.26 for %s" %result_forecast)



   #----------------------------------------------------------------------------
   #
   # This test verifies that HybridForecast file is properly created based
   # on static file-based forecasts within testing framework - there is no
   # operator (min or max) provided to apply to all components 
   #
   def testHybridForecastWithNoOperator(self):
      """ Confirm that HybridForecast generates forecast according to \
provided configuration in ForecastGroup's configuration file. HybridForecast is \
based on static forecasts within testing framework."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      xmldoc = ForecastGroupInitFile(self.__referenceDataDir, 
                                     "forecast_with_no_operator.init.xml")
      
      # Modify path to the forecasts files directory to be relative to the
      # CENTERCODE
      for each_index in xrange(0, 1):
          attrs = xmldoc.elementAttribs(HybridForecast.XML.GroupElement,
                                        index=each_index)
          attrs[HybridForecast.XML.DirAttribute] = os.path.join(self.__referenceDataDir,
                                                                attrs[HybridForecast.XML.DirAttribute])
      
      
      # Write modified file to the test directory
      init_file = os.path.join(CSEPTestCase.TestDirPath, 
                               "forecast.init.xml")
      fhandle = CSEPFile.openFile(init_file, 
                                  CSEPFile.Mode.WRITE)
      xmldoc.write(fhandle)
      fhandle.close()
      

      # Use test directory as forecast group directory
      group = ForecastGroup(CSEPTestCase.TestDirPath)
      
      # Create forecasts
      group.create(datetime.datetime(2012, 6, 28),
                   CSEPTestCase.TestDirPath)
      
      ### Validate results 
      
      # Models within the group should include HybridForecast
      result_forecast = os.path.join(group.dir(),
                                     "CumulativeHybrid_6_28_2012.dat")
                                     
      hybrid_forecast = ForecastHandlerFactory().CurrentHandler.load(result_forecast)
      self.assertFalse(np.any(np.abs(hybrid_forecast[:, CSEPGeneric.Forecast.Format.Rate] - 0.42) >= 1E-10), 
                       "Expected rate of 0.42 for %s" %result_forecast)


# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
