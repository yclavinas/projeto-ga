"""
   RateForecastHandler module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import scipy.io, datetime, time, string
import numpy as np

import CSEPFile, CSEPLogging, CSEPGeneric, CSEPUtils, CSEPXML, MatlabLogical
from ForecastHandler import ForecastHandler


#-------------------------------------------------------------------------------
#
# RateForecastHandler.
#
# This class is designed to represent a handler for the rate-based forecast file.
# It handles forecast data to be used by evaluation tests, and was introduced
# to the testing framework to support polygon-based and rate-based forecasts by
# the same evaluation tests.
#
class RateForecastHandler (ForecastHandler):

    # Static data of the class

    # Logger object for the class
    __logger = None
 
    Type = 'RateBased'


    #-----------------------------------------------------------------------------
    # This class is designed to represent a bin information: mask bit, rate, and
    # magnitude values.
    #
    # This class was introduced to avoid floating point representations problems 
    # used by Python. When instantiating tuples with already rounded 
    # floating point values to the second precision digit, it was still using
    # internal not "precise" representation. This class provides interface to
    # enforce rounding to the 2-nd precision digit.
    #
    class BinInfo (object):
      
      def __init__(self, magnitude, rate, mask = '1'):
         
         # String representation for magnitude
         self.magnitude = magnitude
         
         # String representation of rate
         self.rate = rate
         
         # String representation for mask bit
         self.mask = mask
    

    # Functionality specific to XML representation of rate-based forecasts 
    class XML (ForecastHandler.XML):

        # Longitude range for the forecast - used to reinterpret the values of
        # model provided cells if outside of the range
        MaxLongitude = 180.0
        MinLongitude = -180.0
        MaxReinterpretLon = 360.0        
        
        # Field separator for the metadata key and value
        __metaKeyValueSeparator = '='
        
                
        __logger = None
        
        #=======================================================================
        # Initialization of XML object
        #=======================================================================
        def __init__ (self, 
                      file_path):
            """ Initialization for XML class."""
            
            ForecastHandler.XML.__init__(self,
                                         file_path)
            
            if RateForecastHandler.XML.__logger is None:
                RateForecastHandler.XML.__logger = CSEPLogging.CSEPLogging.getLogger(RateForecastHandler.XML.__name__)


        #-----------------------------------------------------------------------------
        #
        # Parse forecast issue date as provided in ASCII format file into ISO8601 
        # format date and time.
        #
        @staticmethod
        def __parseIssueDate(date_string):
          """Parse issue date into ISO8601 format string. For now only
             entry string of default format (as in time.strptime()) 
             "Tue Aug 21 01:03:07 2007" is supported."""
          
          issue_time = datetime.datetime(*(time.strptime(date_string)[0:6]))
          return "%sT%s" %(issue_time.date(), issue_time.time())
       
    
        #-----------------------------------------------------------------------------
        #
        # Parse forecast start date as provided in ASCII format file in "%Y-%m-%d"
        # format into ISO8601 format date and time.
        #
        @staticmethod
        def __parseStartDate(date_string):
          """Parse forecast start date into ISO8601 format string.
             For now only entry string of "2007-07-22" format is supported."""
          
          start_date = datetime.datetime(*(time.strptime(date_string, "%Y-%m-%d")[0:6]))
          return ("%sT%s" %(start_date.date(), start_date.time()), start_date)
    
    
        #-----------------------------------------------------------------------------
        #
        # Parse forecast start date as provided in ASCII format file in "%Y-%m-%d"
        # format into ISO8601 format date and time.
        #
        @staticmethod
        def __parseDuration(duration_string, 
                            start_date):
          """Parse forecast duration in days and create ISO8601 format string 
             representation of the forecast end date. For now only entry string of 
             "1 day(s)" format is supported."""
          
          duration = string.replace(duration_string, 'day(s)', '')
          duration_value = int(duration.strip())
          
          date_diff = datetime.timedelta(duration_value)
          end_date = start_date + date_diff
          
          return "%sT%s" %(end_date.date(), end_date.time())


        #-----------------------------------------------------------------------------
        #
        # Parse forecast metadata as provided in ASCII format data.
        #
        @staticmethod
        def __parseMetadata(line, 
                            xmldoc,
                            start_date):
          """Parse forecast metadata as provided in ASCII format data."""
    
          # Flag to indicate if metadata is provided in the file
          meta_in_file = False
          
          # Set forecast metadata if any is available
          tokens = [token.strip() for token in \
                    line.split(RateForecastHandler.XML.__metaKeyValueSeparator)]
           
          if len(tokens) != 2:
             return (meta_in_file, start_date)
           
          meta_key, meta_value = tokens 
          
          # metadata has corresponding element in XML format
          if ForecastHandler.XML.Metadata.has_key(meta_key) is True:
             
             meta_in_file = True
             
             # Acquire corresponding XML element, and set it's text to the
             # metadata value
             xml_elements = xmldoc.elements(ForecastHandler.XML.Metadata[meta_key])
             xml_elements[0].text = meta_value
              
          elif meta_key == ForecastHandler.ASCII.IssueDate:
              
             meta_in_file = True
                       
             # Convert issue date into XML expected format element
             xml_elements = xmldoc.elements(ForecastHandler.XML.IssueDate)
             xml_elements[0].text = RateForecastHandler.XML.__parseIssueDate(meta_value)
              
          elif meta_key == ForecastHandler.ASCII.StartDate:
             
             meta_in_file = True
                       
             # Convert forecast start date into XML expected format element
             xml_elements = xmldoc.elements(ForecastHandler.XML.StartDate)
             xml_elements[0].text, start_date = RateForecastHandler.XML.__parseStartDate(meta_value)
              
          elif meta_key == ForecastHandler.ASCII.Duration:
             
             meta_in_file = True
                      
             # start date must be already known when parsing the duration 
             if start_date is None:
                
                error_msg = "RateForecastHandler.XML.__parseMetadata(): expected valid startDate \
object, received None"
                
                RateForecastHandler.XML.__logger.error(error_msg)
                raise RuntimeError, error_msg
             
             # Convert forecast start date and duration into end date XML 
             # format element
             xml_elements = xmldoc.elements(ForecastHandler.XML.EndDate)
             xml_elements[0].text = RateForecastHandler.XML.__parseDuration(meta_value, 
                                                                            start_date)
             
          return (meta_in_file, start_date)
      

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
    
          # Extract cell dimensions
          cell_dims = self.elements(ForecastHandler.XML.CellDimension)
          
          mask_on = CSEPXML.FloatFormatStrZeroDigit %(1.0)
          
          # Compute half of range to get to the center point
          lat_range = float(cell_dims[0].attrib[ForecastHandler.XML.LatRange]) * 0.5
          lon_range = float(cell_dims[0].attrib[ForecastHandler.XML.LonRange]) * 0.5
          
          # Extract bin dimensions
          bin_dims = self.elements(ForecastHandler.XML.BinDimension)
          # Compute half of range to get to the center point      
          mag_range = float(bin_dims[0].text) * 0.5
          
          # Extract depth element
          depth_elem = self.elements(ForecastHandler.XML.DepthLayer)
          
          # Extract top and bottom depth values
          depth_range_top = float(depth_elem[0].attrib['min'])
          depth_range_bottom = float(depth_elem[0].attrib['max'])
          
          # Read model_file into the dictionary that is adjusted to the cell/bin 
          # center point
          model_dict = {}
          fhandle = CSEPFile.openFile(model_file)
          counter = 0
          
          meta_in_file = False
          _start_date = None
          
          for line in fhandle.readlines():
             line  = line.strip()
             
             # Parse lines that begin with strings in case they contain metadata
             # about forecast
             if len(line) and line[0].isalpha() is True:
    
                _in_file, _file_start_date = RateForecastHandler.XML.__parseMetadata(line, 
                                                                                     self,
                                                                                     _start_date)
                if _in_file:
                    meta_in_file = True
                    
                if _file_start_date is not None:
                    _start_date = _file_start_date
                    
                # Done processing line that contains metadata
                continue
              
    
             line_tokens = line.split()
             if len(line_tokens) == 0:
                # Reached end of file
                break
             
             counter += 1
    
             # Explicitly access line tokens to avoid dealing with varying number
             # of data columns in ASCII format of the forecast
             min_lon = line_tokens[CSEPGeneric.Forecast.Format.MinLongitude]
             max_lon = line_tokens[CSEPGeneric.Forecast.Format.MinLongitude]
             min_lat = line_tokens[CSEPGeneric.Forecast.Format.MinLatitude]
             max_lat = line_tokens[CSEPGeneric.Forecast.Format.MaxLatitude]
             depth_top = line_tokens[CSEPGeneric.Forecast.Format.DepthTop]
             depth_bottom = line_tokens[CSEPGeneric.Forecast.Format.DepthBottom]
             min_mag = line_tokens[CSEPGeneric.Forecast.Format.MinMagnitude]
             max_mag = line_tokens[CSEPGeneric.Forecast.Format.MaxMagnitude]
             rate = line_tokens[CSEPGeneric.Forecast.Format.Rate]
             mask_bit = line_tokens[CSEPGeneric.Forecast.Format.MaskBit]
             
             # Check that depth values are within the range
             if float(depth_top) < depth_range_top or \
                float(depth_bottom) > depth_range_bottom:
                error_msg = "RateForecastHandler.toXML(): model '%s' contains bin for the depth \
out of '%s' template range [%s;%s] (%s)." %(model_file, 
                                            template_file,
                                            depth_range_top, 
                                            depth_range_bottom,
                                            line)
                RateForecastHandler.XML.__logger.error(error_msg)
                
                raise RuntimeError, error_msg
             
             # To handle floating point number representation by different programs
             # (such as Matlab when used to convert forecast model to ASCII), use
             # round() function to the 2nd point of precision
             lon_value = CSEPXML.FloatFormatStr %(float(min_lon) + lon_range)
             
             lat_value = CSEPXML.FloatFormatStr %(float(min_lat) + lat_range)
             
             mag_value = CSEPXML.FloatFormatStr %(float(min_mag) + mag_range)
             
             #logger.debug("Long=%s, lat=%s, magn=%s" \
             #             %(lon_value, lat_value, mag_value))
             
             # Append tuple of magnitude, rate and mask bit for the bin
             model_dict.setdefault((lon_value, lat_value), []).append(RateForecastHandler.BinInfo(mag_value, 
                                                                                                  rate, 
                                                                                                  CSEPXML.FloatFormatStrZeroDigit %float(mask_bit)))
          
          # Set provided input metadata for the model if such was not provided in
          # the ASCII format file
          if meta_in_file is False:
             
             # Model name
             if name is not None:
                xml_elements = self.elements(ForecastHandler.XML.ModelName)
                xml_elements[0].text = name
             
             # Start date of the forecast
             if start_date is not None:
                xml_elements = self.elements(ForecastHandler.XML.StartDate)
                xml_elements[0].text = "%sT%s" %(start_date.date(), start_date.time())
             
             # End date of the forecast
             if end_date is not None:
                xml_elements = self.elements(ForecastHandler.XML.EndDate)
                xml_elements[0].text = "%sT%s" %(end_date.date(), end_date.time())
             
             # Capture issue date
             now = datetime.datetime.now()
             xml_elements = self.elements(ForecastHandler.XML.IssueDate)
             xml_elements[0].text = "%sT%s" %(now.date(), now.time())
             
    
          #logger.debug("Parsed %s lines of model file %s" %(counter, model_file))
          
          ### DEBUG
          #logger.debug("Lon_keys: %s" %model_dict.keys())
          #for key, value in model_dict.items():
          #   print "Lat keys for ", key, " = ", value.keys()
          
             
          # Step through all cell elements in the template
          for cell in self.elements(ForecastHandler.XML.Cell):
             
             lon = CSEPXML.FloatFormatStr %(float(cell.attrib[ForecastHandler.XML.Lon]))
             lat = CSEPXML.FloatFormatStr %(float(cell.attrib[ForecastHandler.XML.Lat]))
             
             #logger.debug("Cell: long=%s lat=%s" %(lon, lat))
    
             if (lon, lat) not in model_dict:
                
                # The whole cell is missing in the model, set cell mask to False,
                # and continue the 'cell' loop
                RateForecastHandler.XML.__logger.warning("%s model is missing cell for lon=%s lat=%s"
                                                         %(model_file, lon, lat))
                      
                   
                cell.attrib[ForecastHandler.XML.CellMaskAttribute] = MatlabLogical.Boolean[False]
                continue
             
             # There are some/all bins available for the cell in the model
             cell.attrib[ForecastHandler.XML.CellMaskAttribute] = MatlabLogical.Boolean[True]
             
             
             # Step through all bin elements, and populate them with model values
             cell_bins = self.children(cell, ForecastHandler.XML.Bin) 
             num_bins = len(cell_bins) # number of bins per cell
             mask_zero_bins = 0 # number of bins that have mask bit set to False
             
             for bin in cell_bins:
                mag = CSEPXML.FloatFormatStr %(float(bin.attrib[ForecastHandler.XML.Magn]))
          
                found_model_bin = None
                
                for bin_info in model_dict[(lon, lat)]:
    
                   if bin_info.magnitude == mag:
                      found_model_bin = bin_info
                      break
                   
                if found_model_bin is not None:
                   
                   # Populate bin values with model's bin
                   #bin.clear()
                   bin.text = found_model_bin.rate
                   
                   # Set model's mask bit if it's not set to "True",
                   # otherwise it inherits the 'mask' attribute value from parent
                   # 'cell' element
                   if found_model_bin.mask != mask_on:
                      bin.attrib[ForecastHandler.XML.BinMaskAttribute] = str(found_model_bin.mask)
                      mask_zero_bins += 1
                      
                   # Remove found bin from next iteration: no need to check on it
                   model_dict[(lon, lat)].remove(found_model_bin)
                   
                else:
                   # model doesn't have a template bin
                   bin.attrib[ForecastHandler.XML.BinMaskAttribute] = MatlabLogical.Boolean[False]
                   mask_zero_bins += 1
    
                   
             # All bins within a cell have 'False' mask --->
             if mask_zero_bins == num_bins:
                # Instead set mask attribute to False for the whole cell
                cell.attrib[ForecastHandler.XML.CellMaskAttribute] = MatlabLogical.Boolean[False]
                
                # And remove mask attribute from all bins
                for bin in cell_bins:
                   del bin.attrib[ForecastHandler.XML.BinMaskAttribute]
      
          # Set "verified by CSEP" attribute of issueDate element
          self.elements(ForecastHandler.XML.IssueDate)[0].attrib[ForecastHandler.XML.VerifiedBy] = ForecastHandler.XML.verifyInfo()    
          self.elements(ForecastHandler.XML.IssueDate)[0].attrib[ForecastHandler.XML.VerifiedOn] = '%s' %datetime.datetime.now()
             
          # Save populated template with model to the file
          fhandle = CSEPFile.openFile(CSEPFile.Name.xml(model_file), 
                                      CSEPFile.Mode.WRITE)
          self.write(fhandle)
          fhandle.close()
          
          
          return CSEPFile.Name.xml(model_file)




        #-----------------------------------------------------------------------------
        #
        # toASCII
        # 
        def _toASCII (self,
                      fhandle):
            """ Convert XML forecast data into ASCII format."""

            # Extract cell dimensions
            cell_dims = self.elements(ForecastHandler.XML.CellDimension)
              
            # Compute half of range to get to the corner point as for original Matlab
            # template
            lat_range = float(cell_dims[0].attrib[ForecastHandler.XML.LatRange]) * 0.5
            lon_range = float(cell_dims[0].attrib[ForecastHandler.XML.LonRange]) * 0.5
              
            # Extract bin dimensions
            bin_dims = self.elements(ForecastHandler.XML.BinDimension)
            
            # Compute half of range to get to the corner point      
            mag_range = float(bin_dims[0].text) * 0.5
        
            # Extract depth element
            depth_elem = self.elements(ForecastHandler.XML.DepthLayer)
              
            # Extract top and bottom depth values
            depth_range_top = depth_elem[0].attrib['min']
            depth_range_bottom = depth_elem[0].attrib['max']
              
            # Extract flag for last magnitude bin - open or not
            mag_bin_elem = self.elements(ForecastHandler.XML.LastMagBinOpen)[0]
            mag_bin_is_open = MatlabLogical.Boolean[mag_bin_elem.text.strip()]
              
            # Step through all cell elements in the model
            for cell in self.elements(ForecastHandler.XML.Cell):
                 
                lon = float(cell.attrib[ForecastHandler.XML.Lon])
                lat = float(cell.attrib[ForecastHandler.XML.Lat])
        
                cell_mask = "1"
                if cell.attrib.has_key(ForecastHandler.XML.CellMaskAttribute):
                    cell_mask = cell.attrib[ForecastHandler.XML.CellMaskAttribute]
                 
                # Step through all bin elements, and populate them with model values
                cell_bins = self.children(cell, 
                                          ForecastHandler.XML.Bin) 
                 
                last_bin_index = len(cell_bins) - 1
                 
                for bin_index, bin in enumerate(cell_bins):
                    mag = float(bin.attrib[ForecastHandler.XML.Magn])
                    
                    bin_mask = cell_mask
                    if ForecastHandler.XML.BinMaskAttribute in bin.attrib:
                       bin_mask = bin.attrib[ForecastHandler.XML.BinMaskAttribute]
                       
                    max_mag = str(mag + mag_range)
                    
                    if bin_index == last_bin_index and \
                       mag_bin_is_open == MatlabLogical.Boolean[True]:
                       
                       # If last bin magnitude is open, set to the highest value
                       max_mag = '10.0'
        
                    # Create a tuple of forecast values for the bin and write it to the
                    # file
                    values = (str(lon - lon_range), 
                              str(lon + lon_range),
                              str(lat - lat_range),
                              str(lat + lat_range),
                              depth_range_top,
                              depth_range_bottom,
                              str(mag - mag_range),
                              max_mag,
                              bin.text,
                              bin_mask)
                    
                    fhandle.write('\t'.join(values))
                    fhandle.write('\n')
        

        #-----------------------------------------------------------------------------
        #
        # _toASCIIMap
        # 
        def _toASCIIMap (self,
                         fhandle,
                         scale_rate):
            """ Convert XML forecast data into map-ready ASCII format."""
    
            # Step through all cell elements in the model
            for cell in self.elements(ForecastHandler.XML.Cell):
                 
                 cell_mask = "1"
                 if ForecastHandler.XML.CellMaskAttribute in cell.attrib:
                    cell_mask = cell.attrib[ForecastHandler.XML.CellMaskAttribute]
                    
                 cell_rate = 0   
                 
                 # Sum up all bin rates within the cell - disregard the masking bit for
                 # the bin
                 
                 # Step through all bin elements, and populate them with model values
                 cell_bins = self.children(cell, 
                                           ForecastHandler.XML.Bin) 
                 
                 for bin in cell_bins:
                    
                    cell_rate += float(bin.text.strip())*scale_rate
                          
                 # Create a tuple of forecast values for the bin and write it to the
                 # file
                 values = (cell.attrib[ForecastHandler.XML.Lon], 
                           cell.attrib[ForecastHandler.XML.Lat],
                           repr(cell_rate),
                           cell_mask)
                 
                 fhandle.write('\t'.join(values))
                 fhandle.write('\n')
        

        #=======================================================================
        # Validate XML object
        #=======================================================================
        def _validate (self, 
                       master_xml):
            """ Validate XML representation of the forecast."""
            
            # Extract cell dimensions
            cell_dims = master_xml.elements(ForecastHandler.XML.CellDimension)[0]
                  
            # Compute range
            master_lat_range = CSEPXML.FloatFormatStr %float(cell_dims.attrib[ForecastHandler.XML.LatRange])
            master_lon_range = CSEPXML.FloatFormatStr %float(cell_dims.attrib[ForecastHandler.XML.LonRange])
              
            # Extract bin dimensions
            bin_dims = master_xml.elements(ForecastHandler.XML.BinDimension)[0]
            
            # Compute half of range to get to the center point      
            master_mag_range = CSEPXML.FloatFormatStr %float(bin_dims.text)
            cell_dims = self.elements(ForecastHandler.XML.CellDimension)[0]
                  
            # Compute half of range to get to the center point
            if master_lat_range != (CSEPXML.FloatFormatStr %float(cell_dims.attrib[ForecastHandler.XML.LatRange])):
                error_msg = "Inconsistent value for latitude range: '%s' value provided by '%s' vs. \
'%s' value provided by '%s'" %(master_lat_range,
                               master_xml.name,
                               cell_dims.attrib[ForecastHandler.XML.LatRange],
                               self.name)
            
                RateForecastHandler.XML.__logger.error(error_msg)
                raise RuntimeError, error_msg
                      
                      
            if master_lon_range != CSEPXML.FloatFormatStr %float(cell_dims.attrib[ForecastHandler.XML.LonRange]):
                error_msg = "Inconsistent value for longitude range: '%s' value provided by '%s' vs. \
'%s' value provided by '%s'" %(master_lon_range,
                               master_xml.name,
                               cell_dims.attrib[ForecastHandler.XML.LonRange],
                               self.name)
            
                RateForecastHandler.XML.__logger.error(error_msg)
                raise RuntimeError, error_msg
            
                  
            # Extract bin dimensions
            bin_dims = self.elements(ForecastHandler.XML.BinDimension)[0]
                  
            # Compute half of range to get to the center point      
            if master_mag_range != CSEPXML.FloatFormatStr %float(bin_dims.text):
                error_msg = "Inconsistent value for magnitude range: '%s' value provided by '%s' vs. \
'%s' value provided by '%s'" %(master_mag_range,
                               master_xml.name,
                               bin_dims.text,
                               self.name)
            
                RateForecastHandler.XML.__logger.error(error_msg)
                raise RuntimeError, error_msg
                  
        
            ### Populate template with model rates and report any automatic conversions
            ### to the cell coordinates if necessary
                  
            # Create dictionary of template cells:
            # key: tuple of (lon, lat) for the cell 
            # value: cell object
            # Once cell has been populated with model's rates, remove it from the dictionary
            master_dict = {}
            for cell_obj in master_xml.elements(ForecastHandler.XML.Cell):
                # Extract cell coordinates
                lon = float(cell_obj.attrib[ForecastHandler.XML.Lon])
                lat = float(cell_obj.attrib[ForecastHandler.XML.Lat])
                
                # Store string representation of the values with fixed precision
                master_dict[(CSEPXML.FloatFormatStr %lon, 
                             CSEPXML.FloatFormatStr %lat)] = cell_obj
            
            
            # Extract flag for last magnitude bin - open or not
            mag_bin_elem = master_xml.elements(ForecastHandler.XML.LastMagBinOpen)[0]
            mag_bin_is_open = MatlabLogical.Boolean[mag_bin_elem.text.strip()]
            
            # How many bins very first cell of the model provides
            num_model_bins = None
                  
            # Accumulate warnings associated with validation of the original model
            # XML format: warning and cells
            model_warnings = {}
            for cell in self.elements(ForecastHandler.XML.Cell):
            
                # Process model's cell
                lon = CSEPXML.FloatFormatStr %float(cell.attrib[ForecastHandler.XML.Lon])
                lat = CSEPXML.FloatFormatStr %float(cell.attrib[ForecastHandler.XML.Lat])
                     
                #logger.debug("Cell: long=%s lat=%s" %(lon, lat))
            
                if (lon, lat) not in master_dict:
                         
                    # Check if automatic adjustment need to be made to the cell coordinates:
                    # According to Jeremy (email on Aug 31, 2009):
                    # automatically reinterpret values outside this range so that they
                    # fall within the range (i.e., 181 longitude should be -179)             
                    # latitude: [-90;90]
                    # longitude: [-180; 180]
                    if float(lon) > RateForecastHandler.XML.MaxLongitude:
                        lon = CSEPXML.FloatFormatStr %(float(lon) - RateForecastHandler.XML.MaxReinterpretLon)
                             
                             
                        # Report the adjustment
                        RateForecastHandler.XML.__logger.warning("%s: '%s' cell lon='%s' lat='%s' is reinterpreted as lon='%s' lat='%s'" \
                                                                 %(CSEPLogging.CSEPLogging.frame(RateForecastHandler.XML),
                                                                   self.name,
                                                                   cell.attrib[ForecastHandler.XML.Lon],
                                                                   cell.attrib[ForecastHandler.XML.Lat],
                                                                   lon, lat))
                     
                if (lon, lat) not in master_dict:
                    # Fix for Trac ticket #255: Error condition caused by forecast's
                    # extra cells should be downgraded to a warning condition:
                    # Forecast provided a cell outside of the forecast grid,
                    # report as warning
                    RateForecastHandler.XML.__logger.warning("Forecast '%s' provided a cell lon='%s' lat='%s' (adjusted: lon='%s' lat='%s') outside of defined template '%s'" \
                                                             %(self.name,
                                                               cell.attrib[ForecastHandler.XML.Lon],
                                                               cell.attrib[ForecastHandler.XML.Lat],
                                                               lon,
                                                               lat,
                                                               master_xml.name))
            
                # If re-interpreted value in master dictionary, continue:
                else:
                    master_cell = master_dict[(lon, lat)]
                    master_bins = master_xml.children(master_cell,
                                                      ForecastHandler.XML.Bin)
                         
                         
                    # Step through all bin elements, and populate them with model values
                    cell_bins = self.children(cell, ForecastHandler.XML.Bin)
                         
                    if num_model_bins is None:
                        num_model_bins = len(cell_bins)
                             
                    # Expected number of bins per cell 
                    num_bins = len(master_bins) 
                         
                    # Flag to remove master template bins that don't have corresponding 
                    # bins in the model: to support alarm-based forecasts 
                    remove_master_bins = False
                         
                    if num_bins != len(cell_bins):
                        # Model provided less magnitude bins for the cell than defined
                        # by the template --> generate a warning (for example, alarm-based
                        # forecasts provide only one bin with lastMagBinOpen set to True)
                        msg = "Forecast '%s' provided different number of magnitude bins (num=%s) vs. master template '%s' (num='%s')" \
                               %(self.name,
                                 len(cell_bins),
                                 master_xml.name,
                                 num_bins)
                        
                        model_warnings.setdefault(msg, []).append((lon, lat))
                             
                        # To support alarm-based forecasts that provide rate for one open bin
                        # using templates with multiple bins within cell:
                        # must be very first bin in the cell and have open bin flag set to True
                        if len(cell_bins) == 1 and \
                           mag_bin_is_open == MatlabLogical.Boolean[True] and \
                           (CSEPXML.FloatFormatStr %float(master_bins[0].attrib[ForecastHandler.XML.Magn])) == \
                           (CSEPXML.FloatFormatStr %float(cell_bins[0].attrib[ForecastHandler.XML.Magn])):
                                 
                           remove_master_bins = True
                
                
                    if len(cell_bins) != num_model_bins:
                        # Model provides inconsistent number of bins throughout it's own cells
                        msg = "Forecast '%s' provided inconsistent number of bins (vs. first cell with %s bins)" \
                              %(self.name,
                                num_model_bins)
                        model_warnings.setdefault(msg, []).append((lon, lat))
                             
                    
                    # Step through all magnitude bins of model cell and set cell mask
                    if ForecastHandler.XML.CellMaskAttribute in cell.attrib:
                        master_cell.attrib[ForecastHandler.XML.CellMaskAttribute] = cell.attrib[ForecastHandler.XML.CellMaskAttribute]
                             
                    for bin in master_bins:
                        mag = CSEPXML.FloatFormatStr %float(bin.attrib[ForecastHandler.XML.Magn])
                        found_model_bin = None
                        
                        for each_model_bin in cell_bins:
            
                           if (CSEPXML.FloatFormatStr %float(each_model_bin.attrib[ForecastHandler.XML.Magn])) == mag:
                              found_model_bin = each_model_bin
                              break
                           
                        if found_model_bin is not None:
                           
                           # Populate template bin with model's bin
                           bin.text = found_model_bin.text
                           
                           # Set mask bit if it's not set to "True",
                           # otherwise it inherits the 'mask' attribute value from parent
                           # 'cell' element
                           if ForecastHandler.XML.BinMaskAttribute in found_model_bin.attrib:
                               # Masking bit is provided by the model
                               bin.attrib[ForecastHandler.XML.BinMaskAttribute] = found_model_bin.attrib[ForecastHandler.XML.BinMaskAttribute]
                               
                           # Delete model's bin since it was propagated to the master template
                           cell.remove(found_model_bin)
                     
                        else:
                            ### Model didn't provide bin defined by master template
                            if remove_master_bins is True:
                                # The only bin provided by the model is the very first bin
                                # as defined by the template, and it's an open bin --->
                                # OK to get rid of not provided by model bins in master template
                                master_cell.remove(bin)
                            else:
                                # Generate a warning and set masking bit for the bin to False
                                bin.attrib[ForecastHandler.XML.BinMaskAttribute] = MatlabLogical.Boolean[False]
            
                                # model bin does not have corresponding template bin
                                msg = "'%s' is missing bin for magnitude='%s' as defined by master template '%s'" \
                                      %(self.name,
                                        mag, 
                                        master_xml.name)
                                     
                                model_warnings.setdefault(msg, []).append((cell.attrib[ForecastHandler.XML.Lon],
                                                                           cell.attrib[ForecastHandler.XML.Lat]))                                
            
                        
                    # Step through remaining bins in model cell and report ones that
                    # didn't have corresponding master template's bins
                    for remaining_bin in self.children(cell, ForecastHandler.XML.Bin):
                        # model bin does not have corresponding template bin
                        msg = "'%s' provided bin for magnitude='%s' that does not exist in master template '%s'" \
                              %(model_xml.name,
                                remaining_bin.attrib[ForecastHandler.XML.Magn], 
                                master_xml.name)
                             
                        model_warnings.setdefault(msg, []).append((cell.attrib[ForecastHandler.XML.Lon],
                                                                   cell.attrib[ForecastHandler.XML.Lat]))                                
                     
                    # End of bin iteration for the cell      
                
                    # Remove cell from template dictionary, meaning that model provided
                    # values for it
                    del master_dict[(lon, lat)]
                     
            
            # Report cells which model didn't provide
            msg = "Based on '%s' master template '%s' model has not provided rates" \
                   %(master_xml.name,
                     self.name)
               
            for each_cell_coords, each_cell in master_dict.iteritems():
                # The whole cell is missing in the model, set cell mask to False,
                # and continue the 'cell' loop
                model_warnings.setdefault(msg, []).append((each_cell.attrib[ForecastHandler.XML.Lon],
                                                           each_cell.attrib[ForecastHandler.XML.Lat]))
             
                each_cell.attrib[ForecastHandler.XML.CellMaskAttribute] = MatlabLogical.Boolean[False]
            
            return model_warnings
            
      
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    # 
    def __init__ (self):
        """ Initialization for RateForecastHandler class"""
        
        ForecastHandler.__init__(self)
    
    
    #----------------------------------------------------------------------------
    #
    # Load forecast data from ASCII or Matlab format file 
    #
    # Input: 
    #        forecast_file - Path to the forecast file in Matlab format
    #
    # Output:
    #          numpy.array with forecast data
    #
    def load (self,
              forecast_file):
        """ Load forecast data from the file."""
        
        forecast_data = None

                
        # Matlab format of the forecast is provided
        if CSEPFile.Extension.toFormat(forecast_file) == CSEPFile.Format.MATLAB:
            # Get rid of warning by setting 'struct_as_record' argument
            fh = scipy.io.loadmat(forecast_file,
                                  struct_as_record=True)
            
            if CSEPGeneric.Forecast.Format.MatlabVar not in fh:
                
                error_msg = "Forecast file in Matlab format %s does not contain expected \
    variable '%s' (contains %s)" %(forecast_file,
                                   CSEPGeneric.Forecast.Format.MatlabVar,
                                   fh.keys()) 
                CSEPLogging.CSEPLogging.getLogger(RateForecastHandler.__name__).error(error_msg)
                raise RuntimeError, error_msg
    
    
            forecast_data = fh[CSEPGeneric.Forecast.Format.MatlabVar]
            
        # ASCII format of the forecast is provided
        elif CSEPFile.Extension.toFormat(forecast_file) == CSEPFile.Format.ASCII:

            forecast_data = CSEPFile.read(forecast_file)
        
        # Unknown forecast format is provided:
        else:
            error_msg = "%s: Unsupported file format is provided by %s file. \
Please provide forecast in one of (%s, %s) formats." %(CSEPLogging.CSEPLogging.frame(self.__class__),
                                                       forecast_file,
                                                       CSEPFile.Format.MATLAB,
                                                       CSEPFile.Format.ASCII)

            CSEPLogging.CSEPLogging.getLogger(RateForecastHandler.__name__).error(error_msg)
            raise RuntimeError, error_msg

            
        # Re-shape 1-row forecast into 2-dim array: numpy loads 1-row data into
        # 1-dim array
        if forecast_data.ndim == 1:
            forecast_data.shape = (1, forecast_data.size)
            
        num_rows, num_cols = forecast_data.shape
        
        # Forecast data does not contain column for observations, add it
        if num_cols <= CSEPGeneric.Forecast.Format.Observations:
            new_array = np.append(forecast_data, np.zeros((num_rows, 1)), axis=1)
            forecast_data = new_array

        num_rows, num_cols = forecast_data.shape

        # Forecast data does not contain column for pre-computed zero-likelihoods,
        # add it
        if num_cols <= CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood:
            new_array = np.append(forecast_data, np.zeros((num_rows, 1)), axis=1)
            forecast_data = new_array
            
        return forecast_data
    

    #---------------------------------------------------------------------------
    #
    # Compute vector of forecast realization.
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
        
        forecast_num_rows, forecast_num_cols = forecast.shape
        
        # Delete any observation in forecast
        forecast[:, CSEPGeneric.Forecast.Format.Observations] = 0

        # Get the number of earthquakes in catalog
        catalog_num_rows, catalog_num_cols = catalog.shape
        
        # Create a deep copy of pre-computed log-likelihood to avoid modifying 
        # the vector by various calls to the method
        log_likelihood = forecast[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood].copy()
        #print "Pre-computed sum=", RELMTest.numberEvents(log_likelihood)
        
        # Fix for Trac ticket #232: 
        # ATTN: catalog uncertainties will be initialized to one-element of '0'
        # if empty catalog is passed to CSEPGeneric.Catalog.modifications()
        
        #print "ADDING OBSERVATIONS"
        if catalog_num_cols > 1:
            
            for index in xrange(0, catalog_num_rows):
                __x = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Longitude]
                __y = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Latitude]
                __z = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Depth]
                __m = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Magnitude]
                
                #print 'x=', __x, 'y=', __y, "z=", __z, "__m=", __m
                selection, = np.where((forecast[:, CSEPGeneric.Forecast.Format.MinLongitude] <= __x) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MaxLongitude] > __x) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MinLatitude] <= __y) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MaxLatitude] > __y) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.DepthTop] <= __z) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.DepthBottom] > __z) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] <= __m) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MaxMagnitude] > __m))
                
                #print "Selection=", selection, selection.shape
                if selection.size != 0:
                    #print "Found match:", forecast[selection, :]
                    
                    forecast[selection, 
                             CSEPGeneric.Forecast.Format.Observations] += 1

                    #print "After adding observation: ", forecast[selection, :] 
                             
                    if compute_likelihood is True:
                       log_likelihood[selection] = \
                          CSEPUtils.logPoissonPDF(forecast[selection, 
                                                           CSEPGeneric.Forecast.Format.Observations],
                                                  forecast[selection, 
                                                           CSEPGeneric.Forecast.Format.Rate])
    #                   print 'computed log-likelihood=', log_likelihood[selection], \
    #                         'for forecast observations=', forecast[selection, 
    #                                                                CSEPGeneric.Forecast.Format.Observations] 
    
                       if true_likelihood is not None:
                          # Capture log-likelihood per event
                          # Verified by Jeremy (email from 02/24/2010) the case 
                          # when multiple events occur in the same bin - should use 
                          # 1,2,3, etc. as observed number of events for log-likelihood:
                          # "...So, rather than thinking of it as storing the likelihood
                          # of each target eqk, you can think of it as storing the likelihood in
                          # each bin that contains one or more target eqks..."
    #                      observation_vector = np.ones(selection.shape, 
    #                                                   dtype=np.float)
    #                      __true_log_likelihood = CSEPUtils.logPoissonPDF(observation_vector,
    #                                                                      forecast[selection, 
    #                                                                               CSEPGeneric.Forecast.Format.Rate])
                          
                          true_likelihood[index] = ForecastHandler.numberEvents(log_likelihood[selection])
    #                      print "True log-likelihood=",  true_likelihood[index]
    
    #                   print "forecast[selection]: observations=", forecast[selection, 
    #                                                                       CSEPGeneric.Forecast.Format.Observations], \
    #                         "rate=", forecast[selection, CSEPGeneric.Forecast.Format.Rate]
    #                   print 'logL=', log_likelihood[selection,:]

        result = forecast[:, CSEPGeneric.Forecast.Format.Observations]
        if compute_likelihood is True:
            result = log_likelihood

        return result 

