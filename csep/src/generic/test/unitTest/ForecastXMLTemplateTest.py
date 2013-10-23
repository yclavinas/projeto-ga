"""
Module ForecastXMLTemplateTest
"""

__version__ = "$Revision: 4149 $"
__revision__ = "$Id: ForecastXMLTemplateTest.py 4149 2012-12-19 03:06:30Z liukis $"


import sys, os, unittest, shutil, datetime, filecmp

import CSEPFile, CSEPGeneric, CSEP, CSEPXML
from Environment import *
from CSEPTestCase import CSEPTestCase
from ForecastGroup import ForecastGroup
from OneDayModelPostProcess import OneDayModelPostProcess
from CSEPInitFile import CSEPInitFile
from ForecastHandlerFactory import ForecastHandlerFactory
from ForecastHandler import ForecastHandler
from PolygonForecastHandler import PolygonForecastHandler


 #--------------------------------------------------------------------
 #
 # Validate that forecast conversion to the XML forecast template is 
 # working properly.
 #
class ForecastXMLTemplateTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'xmlForecastTemplate')

   
   #--------------------------------------------------------------------
   #
   # This test verifies that forecast conversion routine to Matlab format
   # through the XML format forecast template is working properly.
   #
   def testTemplate(self):
      """ Confirm that XML format forecast template is \
working properly."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Enable XML format forecast template
      CSEP.Forecast.UseXMLMasterTemplate = True
      
      # Copy forecast files to the test directory
      model_file = 'test_model.mat'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(CSEPTestCase.TestDirPath, model_file))    
      

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)

      
      try:
         # Use test directory as forecast group directory
         ascii_file = CSEPGeneric.Forecast.toASCII(model_file)
       
         template_file = 'test_template.xml'
         
         # Some fake dates for testing purposes only
         start_date = CSEPTestCase.Date
         end_date = start_date + datetime.timedelta(days=10)
         
         template = ForecastHandlerFactory().CurrentHandler.XML(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                                                         template_file))
         xml_file = template.toXML(ascii_file, 
                                   start_date,
                                   end_date,
                                   ascii_file)
                      
         # Convert XML format forecast to Matlab
         model = ForecastHandlerFactory().CurrentHandler.XML(xml_file)
         ascii_from_xml_file = model.toASCII()
          
         # Convert ASCII to Matlab
         matlab_file = CSEPGeneric.Forecast.toMatlab(ascii_from_xml_file)
      

         ### Validate results
         # Matlab format file generated from XML forecast template is returned
         expected_file = 'test_model-fromXML.mat'
         error_message = "XMLForecastTemplate: failed to get expected '%s' \
filename." %expected_file
         self.failIf(matlab_file != expected_file, error_message)
         
         
         # Compare result Matlab file to the reference file: save result file
         # into ASCII format file
         ascii_file = CSEPGeneric.Forecast.toASCII(matlab_file)
         
         reference_file = os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                       ascii_file)
         self.failIf(CSEPFile.compare(reference_file, ascii_file) == False, 
                     "XMLForecastTemplate failed to compare ASCII format results.")
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


   #-----------------------------------------------------------------------------
   #
   # This test verifies that forecast conversion routine to Matlab format
   # through the XML format forecast template with open magnitude bins is 
   # working properly (uses value of 10 for last bin magnitude)
   #
   def testOpenMagBin(self):
      """ Confirm that XML format forecast template with open magnitude bin is \
working properly."""

      # Setup test name
      CSEPTestCase.setTestName(self,
                               self.id())

      # Enable XML format forecast template
      CSEP.Forecast.UseXMLMasterTemplate = True
      
      # Copy forecast files to the test directory
      model_file = 'test_model.mat'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(CSEPTestCase.TestDirPath, model_file))    
      

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)

      
      try:
         # Use test directory as forecast group directory
         ascii_file = CSEPGeneric.Forecast.toASCII(model_file)
       
         template_file = 'test_template_open_mag_bin.xml'
         
         # Some fake dates for testing purposes only
         start_date = CSEPTestCase.Date
         end_date = start_date + datetime.timedelta(days=10)
         
         template = ForecastHandlerFactory().CurrentHandler.XML(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                                                             template_file))
         xml_file = template.toXML(ascii_file, 
                                   start_date,
                                   end_date,
                                   ascii_file)
                      
         # Convert XML format forecast to Matlab
         model = ForecastHandlerFactory().CurrentHandler.XML(xml_file)
         ascii_from_xml_file = model.toASCII()
          
         # Convert ASCII to Matlab
         matlab_file = CSEPGeneric.Forecast.toMatlab(ascii_from_xml_file)
      

         ### Validate results
         # Matlab format file generated from XML forecast template is returned
         expected_file = 'test_model-fromXML.mat'
         error_message = "XMLForecastTemplate: failed to get expected '%s' \
filename." %expected_file
         self.failIf(matlab_file != expected_file, error_message)
         
         
         # Compare result Matlab file to the reference file: save result file
         # into ASCII format file
         ascii_file = CSEPGeneric.Forecast.toASCII(matlab_file)
         
         reference_file = os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                       'test_model_open_mag_bin-fromXML.dat')
         self.failIf(CSEPFile.compare(reference_file, ascii_file) is False, 
                     "XMLForecastTemplate failed to compare ASCII format results.")
         
      finally:
         # Go back to the original directory
         os.chdir(cwd)         


   #----------------------------------------------------------------------------
   #
   # This test verifies that ForecastHandler.XML.validate() is working according
   # to Trac ticket #177 description:
   # 1. Validates template settings: XML elements such as defaultCellDimension,
   #    defaultMagBinDimension, depthLayer
   # 2. Automatically adjusts model provided longitude values to be in 
   #    [-180;180] range
   # 3. Does not validate XML format if it's already verified by the process
   #    on current machine by current CSEP Version
   #
   def testTracTicket177(self):
      """ Confirm that validation by master XML forecast template is \
working properly (see Trac ticket #177 for description)."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Enable XML format forecast template
      CSEP.Forecast.UseXMLMasterTemplate = True
      CSEP.Forecast.ApplyXMLMasterValidation = True
      one_day_template = OneDayModelPostProcess.ForecastTemplate
      OneDayModelPostProcess.ForecastTemplate = os.path.join(ForecastXMLTemplateTest.__referenceDataDir,
                                                             'templateTrac177.xml')

      start_date = datetime.datetime(2009, 12, 1)
      end_date = datetime.datetime(2009, 12, 2)
      post_process_obj = OneDayModelPostProcess()
      post_process_obj.startDate(start_date)
      post_process_obj.endDate(end_date)
              
      
      #=========================================================================
      ### Validate settings
      #=========================================================================
      # Copy forecast files to the test directory
      model_file = 'model_Trac177_magnitude_settings.xml'
      test_dir = os.path.join(CSEPTestCase.TestDirPath,
                              'model_settings')
      os.makedirs(test_dir)
      
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    
      

      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(test_dir)

      ### Magnitude range            
      try:
         sys.exc_clear()
         del sys.argv[1:]         
 
         _mod_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
         xml_file = _mod_file.validate(post_process_obj)
 
      except RuntimeError, error:
          # Validate raised exception message
         self.failIf("Inconsistent value for magnitude range" not in error.args[0], 
                     "Failed to raise exception of expected content for wrong magnitude range, got exception '%s'"
                     %error.args[0])

      except:
         os.chdir(cwd)           
         OneDayModelPostProcess.ForecastTemplate = one_day_template
          
         # Unexpected exception is raised:
         error_message = "Unexpected exception is raised: '%s'." \
                         %sys.exc_info()[0]
         self.fail(error_message)
          

      model_file = 'model_Trac177_latitude_settings.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    

      ### Latitude range
      try:
         sys.exc_clear()
         del sys.argv[1:]         
 
         _val_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
         xml_file = _val_file.validate(post_process_obj)
 
      except RuntimeError, error:
          # Validate raised exception message
         self.failIf("Inconsistent value for latitude range" not in error.args[0], 
                     "Failed to raise exception of expected content for wrong latitude range, got exception '%s'"
                     %error.args[0])
          
      except:
         os.chdir(cwd)           
         OneDayModelPostProcess.ForecastTemplate = one_day_template

         # Unexpected exception is raised:
         error_message = "Unexpected exception is raised: '%s'." \
                         %sys.exc_info()[0]
         self.fail(error_message)


      model_file = 'model_Trac177_longitude_settings.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    

      ### Longitude range
      try:
         sys.exc_clear()
         del sys.argv[1:]         
 
         _mod_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
         xml_file = _mod_file.validate(post_process_obj)
 
      except RuntimeError, error:
          # Validate raised exception message
          self.failIf("Inconsistent value for longitude range" not in error.args[0], 
                      "Failed to raise exception of expected content for wrong longitude range, got exception '%s'"
                      %error.args[0])
          
      except:
         os.chdir(cwd)           
         OneDayModelPostProcess.ForecastTemplate = one_day_template

         # Unexpected exception is raised:
         error_message = "Unexpected exception is raised: '%s'." \
                         %sys.exc_info()[0]
         self.fail(error_message)


      model_file = 'model_Trac177_minDepth_settings.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    

      ### Min depth
      try:
         sys.exc_clear()
         del sys.argv[1:]         
 
         _mod_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
         xml_file = _mod_file.validate(post_process_obj)
 
      except RuntimeError, error:
          # Validate raised exception message
          self.failIf("Inconsistent value for minimum value of depth range" not in error.args[0], 
                      "Failed to raise exception of expected content for wrong minimum value of depth range, got exception '%s'"
                      %error.args[0])
          
      except:
          os.chdir(cwd)           
          OneDayModelPostProcess.ForecastTemplate = one_day_template

          # Unexpected exception is raised:
          error_message = "Unexpected exception is raised: '%s'." \
                          %sys.exc_info()[0]
          self.fail(error_message)


      model_file = 'model_Trac177_maxDepth_settings.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    

      ### Max depth
      try:
         sys.exc_clear()
         del sys.argv[1:]         
 
         _mod_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
         xml_file = _mod_file.validate(post_process_obj)
 
      except RuntimeError, error:
          # Validate raised exception message
          self.failIf("Inconsistent value for maximum value of depth range" not in error.args[0], 
                      "Failed to raise exception of expected content for wrong maximum value of depth range, got exception '%s'"
                      %error.args[0])
          
      except:
          os.chdir(cwd)           
          OneDayModelPostProcess.ForecastTemplate = one_day_template

          # Unexpected exception is raised:
          error_message = "Unexpected exception is raised: '%s'." \
                          %sys.exc_info()[0]
          self.fail(error_message)


      os.chdir(cwd)
      test_dir = os.path.join(CSEPTestCase.TestDirPath,
                              'model_conversions')
      os.makedirs(test_dir)
      os.chdir(test_dir)
      
      model_file = 'model_Trac177.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    

      sys.exc_clear()
      del sys.argv[1:]         
 
      _mod_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      _mod_file.validate(post_process_obj)
          
      xml_doc = CSEPInitFile(model_file,
                             namespace = CSEPXML.FORECAST_NAMESPACE)
 
      ### Start and end dates of the forecast
      
      # Expected start date string
      start_date_str = '%sT%s' %(start_date.date(), start_date.time())
      self.failIf(xml_doc.elements(ForecastHandler.XML.StartDate)[0].text.startswith(start_date_str) is False,
                  "%s: Expected %s value for %s element, got %s" %(xml_doc.name,
                                                                   start_date_str,
                                                                   ForecastHandler.XML.StartDate,
                                                                   xml_doc.elements(ForecastHandler.XML.StartDate)[0].text))

      # Expected end date string
      end_date_str = '%sT%s' %(end_date.date(), end_date.time())
      self.failIf(xml_doc.elements(ForecastHandler.XML.EndDate)[0].text.startswith(end_date_str) is False,
                  "%s: Expected %s value for %s element, got %s" %(xml_doc.name,
                                                                   end_date_str,
                                                                   ForecastHandler.XML.EndDate,
                                                                   xml_doc.elements(ForecastHandler.XML.EndDate)[0].text))
      
      ### Longitude conversion
      model = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      ascii_file = model.toASCII()
      reference_file = os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                    ascii_file)
      self.failIf(CSEPFile.compare(reference_file, ascii_file) is False, 
                  "%s: failed to compare ASCII format results." %ascii_file)
      

      ### Less bins provided by the model with lastMagBinOpen=True
      model_file = 'model_Trac177_less_bins.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    

      _val_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      _val_file.validate(post_process_obj)
          

      model = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      ascii_file = model.toASCII()
      reference_file = os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                    ascii_file)
      self.failIf(CSEPFile.compare(reference_file, ascii_file) is False, 
                  "%s: failed to compare ASCII format results." %ascii_file)


      ### Model has not provided rates for some of the bins with lastMagBinOpen=True
      model_file = 'model_Trac177_missing_bins.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(test_dir, 
                                   model_file))    

      _val_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      _val_file.validate(post_process_obj)
      
      model = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      ascii_file = model.toASCII()
      reference_file = os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                    ascii_file)
      self.failIf(CSEPFile.compare(reference_file, ascii_file) is False, 
                  "%s: failed to compare ASCII format results." %ascii_file)
         
         
      # Go back to the original directory
      os.chdir(cwd)         
      OneDayModelPostProcess.ForecastTemplate = one_day_template


   #----------------------------------------------------------------------------
   #
   # This test verifies that ForecastHandler.XML.validate() is working according
   # to Trac ticket #255 description: reports only a warning and skips cells 
   # outside of defined template if such cells are provided by the model
   #
   def testTracTicket255(self):
      """ Confirm that validation by master XML forecast template is \
working properly on extra cells provided by the model (see Trac ticket #255: \
Error condition caused by forecast's extra cells should be downgraded to a \
warning condition)."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Enable XML format forecast template
      CSEP.Forecast.UseXMLMasterTemplate = True
      CSEP.Forecast.ApplyXMLMasterValidation = True
      one_day_template = OneDayModelPostProcess.ForecastTemplate
      OneDayModelPostProcess.ForecastTemplate = os.path.join(ForecastXMLTemplateTest.__referenceDataDir,
                                                             'templateTrac177.xml')

      start_date = datetime.datetime(2009, 12, 1)
      end_date = datetime.datetime(2009, 12, 2)
      post_process_obj = OneDayModelPostProcess()
      post_process_obj.startDate(start_date)
      post_process_obj.endDate(end_date)
              
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)

              
      model_file = 'model_Trac255_extra_cell.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(CSEPTestCase.TestDirPath, 
                                   model_file))    

      _val_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      xml_file = _val_file.validate(post_process_obj)
 
      OneDayModelPostProcess.ForecastTemplate = one_day_template

      model = ForecastHandlerFactory().CurrentHandler.XML(xml_file)
      ascii_file = model.toASCII()
      reference_file = os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                    ascii_file)
      self.failIf(CSEPFile.compare(reference_file, ascii_file) is False, 
                  "%s: failed to compare ASCII format results." %ascii_file)

      os.chdir(cwd)


   #----------------------------------------------------------------------------
   #
   # This test verifies that ForecastHandler.validate() is working 
   # properly for XML files that contain CSEPPolygon information
   #
   def testValidateXMLForPolygon(self):
      """ Confirm that validation by master XML forecast template is \
working properly for polygon-based forecasts."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Set current forecast handler to polygon-based:
      ForecastHandlerFactory().object(PolygonForecastHandler.Type)
      
      # Enable XML format forecast template
      CSEP.Forecast.UseXMLMasterTemplate = True
      CSEP.Forecast.ApplyXMLMasterValidation = True      
    
      one_day_template = OneDayModelPostProcess.ForecastTemplate
      OneDayModelPostProcess.ForecastTemplate = os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                             'data',
                                                             'templates',
                                                             'oceanic_transform_faults.forecast.xml')

      start_date = datetime.datetime(2011, 12, 1)
      end_date = datetime.datetime(2011, 12, 2)
      post_process_obj = OneDayModelPostProcess()
      post_process_obj.startDate(start_date)
      post_process_obj.endDate(end_date)
              
      # cd to the test directory, remember current directory 
      cwd = os.getcwd()
      os.chdir(CSEPTestCase.TestDirPath)
      
      os.makedirs('archive')

              
      model_file = 'PolygonForecast.xml'
      shutil.copyfile(os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                   model_file),
                      os.path.join(CSEPTestCase.TestDirPath, 
                                   model_file))    

      _val_file = ForecastHandlerFactory().CurrentHandler.XML(model_file)
      xml_file = _val_file.validate(post_process_obj,
                                    'archive')
 
      OneDayModelPostProcess.ForecastTemplate = one_day_template

      model = ForecastHandlerFactory().CurrentHandler.XML(xml_file)
      ascii_file = model.toASCII()
      reference_file = os.path.join(ForecastXMLTemplateTest.__referenceDataDir, 
                                    ascii_file)
      # Don't want to convert Polygon vertex coordinates to float
      self.failIf(filecmp.cmp(reference_file, ascii_file) is False, 
                  "%s vs %s: failed to compare ASCII format results." %(reference_file,
                                                                        ascii_file))

      os.chdir(cwd)

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
