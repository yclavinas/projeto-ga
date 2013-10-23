"""
   ForecastHandler module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import numpy as np
import os, re, datetime, string, time

import CSEP, CSEPLogging, CSEPXML, CSEPFile, CSEPGeneric
from CSEPInitFile import CSEPInitFile
from CSEPPropertyFile import CSEPPropertyFile



#-------------------------------------------------------------------------------
#
# ForecastHandler.
#
# This abstract class is designed to represent a handler for the forecast file.
# It handles forecast data to be used by evaluation tests, and was introduced
# to the testing framework to support polygon-based and rate-based forecasts by
# the same evaluation tests.
#
class ForecastHandler (object):

    # ASCII representation of the forecast
    class ASCII (object):
        IssueDate = 'issue_date'
        StartDate = 'forecast_start_date'
        Duration = 'forecast_duration'
                

    # XML representation of the forecast
    class XML (CSEPInitFile, list):
        
        # Static data of the class
        __logger = None


        ModelName = 'modelName'
        Version = 'version'
        Author = 'author'
   
        # Dictionary of ASCII to XML metadata elements: there is one-to-one transition
        # of data for these fields
        Metadata = {'modelname' : ModelName,
                    'version' : Version,
                    'author' : Author}

        # Element names and attributes for XML format data
        CellMaskAttribute = 'mask'
        BinMaskAttribute = 'mk'
    
        IssueDate = 'issueDate'
        VerifiedBy = 'verifiedBy'
        VerifiedOn = 'verifiedOn'
        StartDate = 'forecastStartDate'
        EndDate = 'forecastEndDate'
       
        LastMagBinOpen = 'lastMagBinOpen'
        CellDimension = 'defaultCellDimension'
        BinDimension = 'defaultMagBinDimension'
        DepthLayer = 'depthLayer'
        LatRange = 'latRange'
        LonRange = 'lonRange'
        Lon = 'lon'
        Lat = 'lat'
        Bin = 'bin'
        Cell = 'cell'
        Magn = 'm'
   
   
        #=======================================================================
        # Initialization of XML object
        # 
        # Input:
        #        file_path - Optional path to the file that stores Polygon info.
        #                    Default is None.
        #        parent_tag - Tag of Polygon's parent element. Default is None.
        #        sibling_tag - Tag of sibling element if sibling information
        #                      should be considered for any format conversions.   
        #=======================================================================
        def __init__ (self, 
                      file_path,
                      elem_namespace=CSEPXML.FORECAST_NAMESPACE):
            """ Initialization for XML class."""
            
            CSEPInitFile.__init__(self,
                                  file_path,
                                  namespace = elem_namespace)

            list.__init__(self, [])
            
            if ForecastHandler.XML.__logger is None:
                ForecastHandler.XML.__logger = CSEPLogging.CSEPLogging.getLogger(ForecastHandler.XML.__name__)
         

        #--------------------------------------------------------------------------------
        #
        # Utility to convert forecast rates from (EQ per forecast period per km^2) to 
        # (EQ per forecast period per degree^2) units. It expects input forecast
        # in XML format and generates new XML format forecast file with rates 
        # new units rate and to populate XML master template with
        # converted to new units.
        #
        def kmToDegreeXMLRates(self, 
                               new_forecast_file): 
          """ Convert forecast rates from (EQ per forecast period per km^2) to 
              (EQ per forecast period per degree^2) units."""
       
          cell_dims = self.elements(ForecastHandler.XML.CellDimension)[0]
          lat_half_range = float(cell_dims.attrib[ForecastHandler.XML.LatRange]) * 0.5
          lon_half_range = float(cell_dims.attrib[ForecastHandler.XML.LonRange]) * 0.5
    
    
          # Step through all cell elements in the template
          for cell in self.elements(ForecastHandler.XML.Cell):
             
             lon = float(cell.attrib[ForecastHandler.XML.Lon])
             lat = float(cell.attrib[ForecastHandler.XML.Lat])
    
             nw_lon = lon - lon_half_range
             nw_lat = lat + lat_half_range
             se_lon = lon + lon_half_range
             se_lat = lat - lat_half_range
    
             # There is only one bin element per cell, populate it with model rate
             for bin in self.children(cell, ForecastHandler.XML.Bin):
             
                # Populate bin values with model's bin rate
                rate = float(bin.text.strip()) * CSEPGeneric.GeoUtils.areaOfRectangularRegion(nw_lat, nw_lon,
                                                                                              se_lat, se_lon)
                bin.text = str(rate)
          
          
          # Save model with updated rates to the file
          fhandle = CSEPFile.openFile(new_forecast_file, 
                                      CSEPFile.Mode.WRITE)
          self.write(fhandle)
          fhandle.close()
          
          return


        #-----------------------------------------------------------------------------
        #
        # Trim provided template to the magnitude threshold (required by Canterbury
        # special study)
        #
        def trimTemplate (self, 
                          output_filename,
                          magn_upper = 8.0):
            """ Read template file in and trim bins with values above provided threshold.""" 
            
            
            # Step through all "cell" elements
            for each_cell in self.elements(Forecast.XMLCell):
                
                # Step through bins:
                for each_bin in self.children(each_cell, Forecast.XMLBin):
                    
                    # Extract magnitude value for the bin:
                    magn = float(each_bin.attrib[Forecast.XMLMagn])
                    if magn > magn_upper:
                        each_cell.remove(each_bin)
                        
            # Write trimmed template to new file
            fhandle = CSEPFile.openFile(output_filename, 
                                        CSEPFile.Mode.WRITE)
            self.write(fhandle)
            fhandle.close()


        #-----------------------------------------------------------------------
        #
        # Converts forecast data from ASCII to the XML format. It uses master 
        # forecast template in XML format.
        # 
        def _toXML (self,
                    model_file, 
                    start_date, 
                    end_date, 
                    name):
          """ Converts forecast data from ASCII to the XML format. It uses master 
              forecast template in XML format."""
              
          pass
          

        #-----------------------------------------------------------------------
        #
        # Converts forecast data from ASCII to the XML format. It uses master 
        # forecast template in XML format.
        # 
        def toXML (self,
                   model_file, 
                   start_date = None, 
                   end_date = None, 
                   name = None):
            """ Converts forecast data from ASCII to the XML format. It uses master 
                 forecast template in XML format."""

         
            return self._toXML(model_file, 
                               start_date, 
                               end_date, 
                               name)
         

        #=======================================================================
        # Validate XML object (implemented by derived classes)
        #=======================================================================
        def _toASCII (self, 
                      fhandle):
            """ Convert XML forecast data into ASCII format."""
            
            pass

            
        #-----------------------------------------------------------------------------
        #
        # toASCII
        # 
        def toASCII (self,
                     result_file = None):
            """ Convert XML forecast data into ASCII format, and save it to the file.
                The function uses the same filename but with 
                '-fromXML.dat' extension to indicate origin of the data."""
            
            # Open ASCII file for writing
            ascii_filename = result_file
            if result_file is None:
                ascii_filename = CSEP.Forecast.fromXMLTemplateFilename(self.name,
                                                                       CSEPFile.Extension.ASCII)
              
            fhandle = CSEPFile.openFile(ascii_filename,
                                        CSEPFile.Mode.WRITE)
          
            self._toASCII(fhandle)
              
            # Close the file
            fhandle.close()
          
            return ascii_filename



        #-----------------------------------------------------------------------
        #
        # Convert forecast data from XML to the ASCII format in preparation for
        # map generation.
        # 
        def toASCIIMap (self, 
                        dir_path, 
                        test_name = None, 
                        scale_rate = 1.0):
          """ Convert XML forecast data into ASCII format ready for map generation,
              and save it to the file. The function uses the same filename but with 
              Forecast.FromXMLExtension.ASCII extension to indicate origin of the 
              data."""
          
          
          # Create result directory if it doesn't exist (when maps are generated
          # in stand-alone mode)
          if os.path.exists(dir_path) is False:
              os.makedirs(dir_path)
              
              
          # Open map ASCII file for writing
          map_filename = CSEPGeneric.Forecast.mapFilename(self.name,
                                                          dir_path,
                                                          test_name)
          # Check if file already exists
          if os.path.exists(map_filename) is True:
          
             return map_filename
    
    
          # Open map file for writing
          fhandle = CSEPFile.openFile(map_filename,
                                      CSEPFile.Mode.WRITE)

          self._toASCIIMap(fhandle,
                           scale_rate)
          # Close the file
          fhandle.close()
          
          return map_filename


        #========================================================================
        #
        # verifyInfo
        #
        # Returns string containing information how file was validated
        #
        #========================================================================
        @staticmethod
        def verifyInfo():
            """Return string containing information how file was validated"""
           
            return '%s using CSEP V%s' %(os.uname()[1],
                                         CSEP.Version)


        #=======================================================================
        # Validate XML object (implemented by derived classes)
        #=======================================================================
        def _validate (self, 
                       master_xml):
            """ Validate XML representation of the forecast."""
            
            pass
        

        #-----------------------------------------------------------------------
        #
        # validate
        # 
        # This method validates XML format forecast according to the master 
        # template defined for the experiment.
        #
        def validate (self,
                      post_process_obj, 
                      model_archive_dir = None):
            """ Validate XML format of the 'raw' (generated by the model) forecast
                by populating master XML template, and automatically adjust model
                provided latitude and longitude values to be in [-90;90] and [-180;180] 
                corresponding ranges."""


            # Validation is disabled
            if CSEP.Forecast.ApplyXMLMasterValidation is False:
                return self.name

            from Forecast import Forecast as ForecastBaseClass
            
            # Make sure it's generated by the CSEP Testing Framework
            issue_element = self.elements(ForecastHandler.XML.IssueDate)[0]
            verify_str = self.verifyInfo()
              
            if ForecastHandler.XML.VerifiedBy in issue_element.attrib:
                # Make sure it's verified by the CSEP of any version 
                # 'user at hostname'
                if not ('using CSEP V' in issue_element.attrib[ForecastHandler.XML.VerifiedBy]):
                     msg = "%s: %s forecast file is verified by '%s', need to be verified by '%s'" \
                           %(CSEPLogging.CSEPLogging.frame(ForecastHandler.XML),
                             self.name,
                             issue_element.attrib[ForecastHandler.XML.VerifiedBy],
                             verify_str)
                     ForecastHandler.XML.__logger.warning(msg)
    
                else:
                    # Forecast is already verified, exit the routine
                    msg = "%s: %s forecast file is already verified by '%s'" \
                            %(CSEPLogging.CSEPLogging.frame(ForecastHandler.XML),
                              self.name,
                              issue_element.attrib[ForecastHandler.XML.VerifiedBy])
                    ForecastHandler.XML.__logger.warning(msg)
              
                    return self.name
               
            else:
                # Report that file needs to be validated by the CSEP testing framework
                msg = "%s: %s forecast file needs to be verified by '%s'" \
                         %(CSEPLogging.CSEPLogging.frame(ForecastHandler.XML),
                           self.name,
                           verify_str)
                ForecastHandler.XML.__logger.info(msg)

              
            # Read XML template in, and get handler to the root element:
            master_xml = CSEPInitFile(post_process_obj.template, 
                                      namespace = self.namespace)
    
            # Extract depth element
            depth_elem = master_xml.elements(ForecastHandler.XML.DepthLayer)[0]
          
            # Extract top and bottom depth values
            master_depth_range_top = CSEPXML.FloatFormatStr %float(depth_elem.attrib['min'])
            master_depth_range_bottom = CSEPXML.FloatFormatStr %float(depth_elem.attrib['max'])
              
            # Extract depth element
            depth_elem = self.elements(ForecastHandler.XML.DepthLayer)[0]
          
            # Extract top and bottom depth values
            if master_depth_range_top != CSEPXML.FloatFormatStr %float(depth_elem.attrib['min']):
                error_msg = "Inconsistent value for minimum value of depth range: '%s' value provided by '%s' vs. \
'%s' value provided by '%s'" %(master_depth_range_top,
                               master_xml.name,
                               depth_elem.attrib['min'],
                               self.name)
    
                ForecastHandler.XML.__logger.error(error_msg)
                raise RuntimeError, error_msg
              
          
            if master_depth_range_bottom != CSEPXML.FloatFormatStr %float(depth_elem.attrib['max']):
                error_msg = "Inconsistent value for maximum value of depth range: '%s' value provided by '%s' vs. \
'%s' value provided by '%s'" %(master_depth_range_bottom,
                               master_xml.name,
                               depth_elem.attrib['max'],
                               self.name)
    
                ForecastHandler.XML.__logger.error(error_msg)
                raise RuntimeError, error_msg
              
        
            # Set template metadata elements about the model
            master_xml.elements(ForecastHandler.XML.ModelName)[0].text = self.elements(ForecastHandler.XML.ModelName)[0].text
            master_xml.elements(ForecastHandler.XML.Version)[0].text = self.elements(ForecastHandler.XML.Version)[0].text
            master_xml.elements(ForecastHandler.XML.Author)[0].text = self.elements(ForecastHandler.XML.Author)[0].text
            master_xml.elements(ForecastHandler.XML.IssueDate)[0].text = self.elements(ForecastHandler.XML.IssueDate)[0].text
            master_xml.elements(ForecastHandler.XML.IssueDate)[0].attrib[ForecastHandler.XML.VerifiedBy] = verify_str
            master_xml.elements(ForecastHandler.XML.IssueDate)[0].attrib[ForecastHandler.XML.VerifiedOn] = '%s' %datetime.datetime.now()
        
            # Validate start and end dates of the forecast as provided by the model
            # vs. runtime defined dates for the model
            if post_process_obj is not None and \
               post_process_obj.start_date is not None:
                for each_date_str, each_date_elem in zip([ForecastHandler.XML.StartDate,
                                                          ForecastHandler.XML.EndDate],
                                                          [post_process_obj.start_date,
                                                           post_process_obj.end_date]):
                      
                      # Dates for the forecast as defined by the CSEP
                      date_str = "%sT%s" %(each_date_elem.date(), 
                                           each_date_elem.time())
                      model_date_str = self.elements(each_date_str)[0].text
                       
                      if model_date_str.startswith(date_str) is False:
                          ForecastHandler.XML.__logger.warning("%s: Replacing provided '%s' element value %s' with '%s'" 
                                                               %(self.name,
                                                                 each_date_str,
                                                                 model_date_str,
                                                                 date_str))
                      else:
                          # Use date as provided by the model
                          date_str = model_date_str
                          
                      master_xml.elements(each_date_str)[0].text = date_str

            # PostProcess is not provided: XML forecast from some other test date
            # in archive directory is being scanned
            else:
                for each_date_str in [ForecastHandler.XML.StartDate,
                                      ForecastHandler.XML.EndDate]:
                      
                     # Use date as provided by the model
                      master_xml.elements(each_date_str)[0].text = self.elements(each_date_str)[0].text
        
                  
            # Do verification specific to the forecast type
            model_warnings = self._validate(master_xml)
              
            # Report all warnings if any:
            for each_msg, cells in model_warnings.iteritems():
        
                msg = "%s: %s for cells (lon, lat) = '%s'" \
                      %(CSEPLogging.CSEPLogging.frame(ForecastHandler.XML),
                        each_msg,
                        cells)
                       
                ForecastHandler.XML.__logger.warning(msg)
                 
        
            # Re-name original XML format of the forecast as generated by the model and 
            # corresponding metadata file
            original_model_file = self.name
        
            if model_archive_dir is None:
                  # If archive directory is not provided, store original XML format
                  # of the forecast and metadata in current directory
                  model_archive_dir, tmp_file = os.path.split(self.name)
        
            # Archive directory doesn't exist, create one
            if len(model_archive_dir) != 0  and \
                 os.path.exists(model_archive_dir) is False:
                  os.makedirs(model_archive_dir)
                  
            ### If file is a soft link:
            # 1. Move original file link points to
            # 2. Create XML format of the forecast based on master template 
            #    under the same directory where original file resides
            if os.path.islink(self.name) is True:
                 original_model_file = os.path.realpath(self.name)
        
            xml_path, xml_file = os.path.split(original_model_file)
              
            ### Rename metadata file         
            archive_dir = model_archive_dir
            meta_path = os.path.join(archive_dir, 
                                     CSEPPropertyFile.metaFilename(xml_file))
        
            if os.path.exists(meta_path) is False:
        
                ForecastHandler.XML.__logger.info("%s metadata file does not exist" %meta_path)
                # Check one level up in archive directory
                archive_dir, date_dir = os.path.split(model_archive_dir)
                meta_path = os.path.join(archive_dir,
                                         CSEPPropertyFile.metaFilename(xml_file))
        
            ForecastHandler.XML.__logger.info("Checking for %s metadata file" %meta_path)
            if os.path.exists(meta_path) is True:
                  
                new_meta_path = os.path.join(model_archive_dir,
                                             CSEPPropertyFile.metaFilename(xml_file.replace(CSEPFile.Extension.XML,
                                                                                            CSEPFile.Extension.XML + CSEPFile.Extension.ORIGINAL)))
                ForecastHandler.XML.__logger.info("Copying %s metadata file to %s" %(meta_path,
                                                                                     new_meta_path))
                CSEPPropertyFile.copyMetafile(meta_path,
                                              new_meta_path,
                                              {CSEPPropertyFile.Metadata.DataFileKeyword : CSEPFile.Extension.ORIGINAL,
                                               CSEPPropertyFile.Metadata.FileDescriptionKeyword : ' (as generated by the model)'},
                                               CSEPFile.Extension.ORIGINAL)
        
                # Create metadata file for the forecast 
                comment = "Forecast file in %s format that is based on XML master template %s" \
                          %(CSEPFile.Format.XML, 
                            post_process_obj.template)
                 
                ForecastBaseClass.metadata(original_model_file,
                                           comment,
                                           archive_dir)
        
            # rename the hard copy of the file link points to 
            # create XML format forecast file based on master template under the
            # same directory the original forecast files resides in
            original_xml_file = os.path.join(model_archive_dir, 
                                             xml_file + CSEPFile.Extension.ORIGINAL)
            ForecastHandler.XML.__logger.info('Re-naming %s to %s' %(original_model_file,
                                                                     original_xml_file))
            os.rename(original_model_file,
                      original_xml_file)
                 
                 
            # Save populated template with model to the file
            ForecastHandler.XML.__logger.info('Over-writing %s' %original_model_file)
            fhandle = CSEPFile.openFile(CSEPFile.Name.xml(original_model_file), 
                                        CSEPFile.Mode.WRITE)
            master_xml.write(fhandle)
            fhandle.close()
              
              
            return CSEPFile.Name.xml(self.name)

      
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    # 
    def __init__ (self):
        """ Initialization for ForecastHandler class"""
        
        pass
    

    #----------------------------------------------------------------------------
    #
    # Load forecast data from ASCII or Matlab format file 
    #
    # Input: 
    #        forecast_file - Path to the forecast file in Matlab format
    #
    # Output:
    #          NumPy.array with forecast data
    #
    def load (self, forecast_file):
        """ Load forecast data from the file."""
        
        pass
    

    #===========================================================================
    # numberEvents
    #
    # This method computes the number of events in provided vector    
    #
    # Input:
    #         binned_catalog - numpy.array(:,1) object which represents "catalog"
    #                          of events
    #         
    # Output: Number of events in catalog
    #
    #===========================================================================
    @staticmethod
    def numberEvents(binned_catalog):
        """ Computes the number of events."""

        # Get the number of events
        return np.nansum(binned_catalog.astype(np.float))
    

    #--------------------------------------------------------------------
    #
    # Invoke forecast model.
    # This method is implemented by children classes.
    #
    # Input: None.
    #
    # Output: None.
    #
    def addObservations (self,
                         forecast,
                         catalog,
                         compute_likelihood = True,
                         true_likelihood = None):
        """ Computes vector containing realization of the forecast 
            ('catalog' of events)."""
        
        pass

