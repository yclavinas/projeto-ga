"""
   PolygonForecastHandler module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import ast
import numpy as np
import shapely.geometry as geometry

import CSEPFile, CSEPLogging, CSEPGeneric, CSEPUtils, MatlabLogical
from ForecastHandler import ForecastHandler
from CSEPPolygon import CSEPPolygon


#-------------------------------------------------------------------------------
#
# PolygonForecastHandler.
#
# This class is designed to represent a handler for the polygon-based forecast file.
# It handles forecast data to be used by evaluation tests, and was introduced
# to the testing framework to support polygon-based and rate-based forecasts by
# the same evaluation tests.
#
class PolygonForecastHandler (ForecastHandler):

    # Static data of the class

    # Logger object for the module
    Logger = CSEPLogging.CSEPLogging.getLogger(__name__)
 
    Type = 'PolygonBased'
    
    VertexSeparator = ','
    
    # Delta to be used in floating point number comparisons 
    Epsilon = 1E-8
    
    
    class Format (object):
        
        Vertex = CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood + 1

    # Functionality specific to XML representation of polygon-based forecasts 
    class XML (ForecastHandler.XML):

        MinMagnitude = 'mMin'
        MaxMagnitude = 'mMax'
        
        __logger = None

        #-----------------------------------------------------------------------
        # Cell information for polygon-based forecast: polygon vertexes and 
        # magnitude bins
        #-----------------------------------------------------------------------
        class CellInfo (object):
            
            def __init__ (self, 
                          cell_xml,
                          polygon_obj, 
                          bins=None):
                
                self.cell = cell_xml
                self.polygon = polygon_obj
                self.bins = []
                
                if bins is not None:
                    self.bins.extend(bins)
                    
                    
        #=======================================================================
        # Initialization of XML object
        #=======================================================================
        def __init__ (self, 
                      file_path):
            """ Initialization for XML class."""
            
            ForecastHandler.XML.__init__(self,
                                         file_path)
            
            if PolygonForecastHandler.XML.__logger is None:
                PolygonForecastHandler.XML.__logger = CSEPLogging.CSEPLogging.getLogger(PolygonForecastHandler.XML.__name__)
            
            # Per each cell: extract polygon and bin information
            for each_cell in self.next(ForecastHandler.XML.Cell):
                
                # Extract Polygon's vertex elements
                polygon_elem = self.children(each_cell, 
                                             CSEPPolygon.XML.Element) 
                                            
                if len(polygon_elem) != 1:
                    # Only one polygon is supported per cell
                    error_msg = "One polygon is expected per each cell within forecast, found %s in %s file" \
                                %(len(polygon_elem),
                                  self.name)
                    PolygonForecastHandler.XML.__logger.error(error_msg)
                    
                    raise RuntimeError, error_msg 
                
                polygon_obj = CSEPPolygon(self,
                                          polygon_elem[0])
                
                # Add magnitude bins that correspond to the polygon cell
                bin_elems = self.children(each_cell, 
                                          ForecastHandler.XML.Bin)
                
                if len(bin_elems) == 0:
                    # Only one polygon is supported per cell
                    error_msg = "At least one magnitude bin is expected per each cell within forecast, found %s for % polygon in %s file" \
                                %(len(bin_elems),
                                  PolygonForecastHandler.XML.polygonId(polygon_obj),
                                  self.name)
                    PolygonForecastHandler.XML.__logger.error(error_msg)
                    
                    raise RuntimeError, error_msg 

                # Add polygon
                self.append(PolygonForecastHandler.XML.CellInfo(each_cell,
                                                                polygon_obj,
                                                                bin_elems))
        
        
        #-----------------------------------------------------------------------
        #        
        #-----------------------------------------------------------------------
        @staticmethod
        def polygonId(polygon_obj):
            """ Define polygon ID based on all vertexes within it"""
            
            # Sort by very first coordinate of vertexes
            return repr(sorted(polygon_obj.ID, key=lambda id: id[0]))
            

        #-----------------------------------------------------------------------
        #
        # Convert Polygon information to map-ready ASCII format
        # 
        def _toASCIIMap (self, 
                         fhandle, 
                         scale_rate = 1.0):
            """ Convert Polygon information to ASCII format."""
    
            # Return string if file handle is not provided to write ASCII 
            # representation of Polygons
            result_str = ''
            
            for cell_info in self:
                
                cell_rate = 0.0
                
                # All bins within the cell
                for each_bin in cell_info.bins:
                    
                    cell_rate += float(each_bin.text)
                        
                values = (cell_info.polygon.toASCIIMap(),
                          repr(cell_rate*scale_rate))
                 
                fhandle.write('\t'.join(values))
                fhandle.write('\n')
                        
            return
        

        #-----------------------------------------------------------------------
        #
        # Convert XML to ASCII format
        # 
        def _toASCII (self, 
                      fhandle):
            """ Convert Polygon information to ASCII format."""
    
            # First 4 fields are just placeholders to have consistent format with
            # rate-based forecasts
            # 0 0 0 0 0.0 30.0 6.0 6.6 0.05 1 0 0 [0.0,0.0],[1.0,2.0],[3.0,3.0],[3.0,1.0]
            
            # Return string if file handle is not provided to write ASCII 
            # representation of Polygons
            result_str = ''
            
            # Extract depth element
            depth_elem = self.elements(ForecastHandler.XML.DepthLayer)[0]
          
            # Extract top and bottom depth values
            master_depth_range_top = depth_elem.attrib['min']
            master_depth_range_bottom = depth_elem.attrib['max']
            
            start_line = "0 0 0 0 %s %s " %(master_depth_range_top,
                                            master_depth_range_bottom)
            
            for cell_info in self:

                cell_mask = MatlabLogical.Boolean[True]
                
                if ForecastHandler.XML.CellMaskAttribute in cell_info.cell.attrib:
                    cell_mask = cell_info.cell.attrib[ForecastHandler.XML.CellMaskAttribute]
                
                for each_bin in cell_info.bins:
                    line = start_line + \
                           each_bin.attrib[PolygonForecastHandler.XML.MinMagnitude] + \
                           ' ' + \
                           each_bin.attrib[PolygonForecastHandler.XML.MaxMagnitude] + \
                           ' ' + \
                           each_bin.text
                           
                    # Check if masking bit is set for the magnitude bin
                    if ForecastHandler.XML.BinMaskAttribute in each_bin.attrib:
                        line += ' '
                        line += each_bin.attrib[ForecastHandler.XML.BinMaskAttribute]
                        
                    else:
                        # Set the whole cell's masking bit attribute
                        line += ' '
                        line += cell_mask

                    # Add placeholders for observations, zeroLikelihood
                    line += " 0 0 "
                    
                    # Add polygon vertexes
                    line += repr(cell_info.polygon)
                    
                    # Finish the line formatting 
                    line += '\n'

                    # Write to the file
                    if fhandle is not None:
                        fhandle.write(line)
                        
                    else:
                        result_str += line
                    
            return result_str

        

        #=======================================================================
        # Validate XML object
        #=======================================================================
        def _validate (self, 
                       master_xml):
            """ Validate XML representation of the forecast."""
            
            # Index into model's cells
            cell_index = 0

            # Per each cell: extract polygon and bin information
            for each_cell in master_xml.next(ForecastHandler.XML.Cell):
                
                # Extract Polygon's vertex elements
                polygon_elem = self.children(each_cell, 
                                             CSEPPolygon.XML.Element) 
                                            
                master_polygon = CSEPPolygon(self,
                                             polygon_elem[0])
                
                # ATTN: For now model must provide the same polygons as master template
#                polygon_key = repr(master_polygon.ID) 
#                
#                if polygon_key not in self:
#                    # Model does not provide polygon
#                    msg = "Model %s does not provide polygon %s as defined by master template %s" \
#                          %(self.name,
#                            polygon_key,
#                            master_xml.name)
#                    PolygonForecastHandler.XML.__logger.warning(msg)
#                    
#                    # Set masking bit for the cell to zero
#                    each_cell.attrib[Forecast.CellMaskAttribute] = MatlabLogical.Boolean[False]
#                
#                else:                     
    
                # print"MASTER Polygon:", master_polygon
                #print"MODEL Polygon:", self[cell_index].polygon
                master_polygon.validate(self[cell_index].polygon)
                    
                # Copy model's rates over
                master_bins = master_xml.children(each_cell, 
                                                  ForecastHandler.XML.Bin)
                
                model_bins = self[cell_index].bins
                
                for each_master, each_model in zip(master_bins,
                                                   model_bins):
                    # Verify min and max limits for magnitude
                    if (each_master.attrib[PolygonForecastHandler.XML.MinMagnitude] != \
                        each_model.attrib[PolygonForecastHandler.XML.MinMagnitude]) or \
                        (each_master.attrib[PolygonForecastHandler.XML.MaxMagnitude] != \
                         each_model.attrib[PolygonForecastHandler.XML.MaxMagnitude]):
                            
                        error_msg = "Magnitude attributes of '%s' Polygon element in %s file are not matching \
attributes of corresponding element in '%s' file: %s vs %s" %(PolygonForecastHandler.XML.polygonId(self[cell_index].polygon),
                                                              self.name,
                                                              master_xml.name,
                                                              each_model.attrib,
                                                              each_master.attrib) 
                        PolygonForecastHandler.XML.__logger.error(error_msg)
                        raise RuntimeError, error_msg

                    each_master.text = each_model.text
                    
                    if PolygonForecastHandler.XML.MinMagnitude in each_model.attrib:
                        # Set master's bin masking bit to the model's provided one:
                        each_master.attrib[PolygonForecastHandler.XML.MinMagnitude] = each_model.attrib[PolygonForecastHandler.XML.MinMagnitude]
            
                cell_index += 1
                
            # No warnings for verification
            return {}
        
      
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    # 
    def __init__ (self):
        """ Initialization for PolygonForecastHandler class"""
        
        ForecastHandler.__init__(self)
    
    
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
    def load (self,
              forecast_file):
        """ Load forecast data from the file."""
        
        forecast_data = None
        
        # ASCII format of the forecast is provided
        if CSEPFile.Extension.toFormat(forecast_file) == CSEPFile.Format.ASCII:
            
            forecast_data = CSEPFile.read(forecast_file,
                                          np.object)
        
        # Unknown forecast format is provided:
        else:
            error_msg = "%s: Unsupported file format is provided by %s file. \
Please provide forecast in %s format." %(CSEPLogging.CSEPLogging.frame(self.__class__),
                                         forecast_file,
                                         CSEPFile.Format.ASCII)

            PolygonForecastHandler.Logger.error(error_msg)
            raise RuntimeError, error_msg
            
        # Re-shape 1-row forecast into 2-dim array: numpy loads 1-row data into
        # 1-dim array
        if forecast_data.ndim == 1:
            forecast_data.shape = (1, forecast_data.size)

        # Number of columns must be greater than "regular" CSEP.Forecast.Format
        # to include vertex information
        num_rows, num_cols = forecast_data.shape
        expected_num_cols = PolygonForecastHandler.Format.Vertex + 1
        if num_cols < expected_num_cols:
            error_msg = "%s: error loading %s, expected number of columns in polygon-based forecast should be %s, got %s" \
                        %(CSEPLogging.CSEPLogging.frame(self.__class__),
                          forecast_file,
                          expected_num_cols,
                          num_cols)

            PolygonForecastHandler.Logger.error(error_msg)
            raise RuntimeError, error_msg

            
        # Convert numerical values of object array to np.float type 
        forecast_values = forecast_data[:, CSEPGeneric.Forecast.Format.MinLongitude:
                                           PolygonForecastHandler.Format.Vertex].astype(np.float)

        forecast_data[:, CSEPGeneric.Forecast.Format.MinLongitude:
                         PolygonForecastHandler.Format.Vertex] = forecast_values
                         
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

        # Extract vertex information from last element of the forecast into numpy array
        for each_index, each_polygon in enumerate(forecast[:, PolygonForecastHandler.Format.Vertex]):
            
            polygon_verts = each_polygon
            
            if isinstance(each_polygon, str):
                # If forecast's vertex information has already passed through
                # evaluation, it should be of expected data type, skip the conversion 
                polygon_verts = ast.literal_eval(each_polygon)
                
            forecast[each_index, PolygonForecastHandler.Format.Vertex] = np.array(polygon_verts)
        
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
                
                selection, = np.where((forecast[:, CSEPGeneric.Forecast.Format.DepthTop] <= __z) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.DepthBottom] > __z) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] <= __m) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MaxMagnitude] > __m))
                
                #print "Selection=", selection, selection.shape
                if selection.size != 0:

                    #print 'x=', __x, 'y=', __y, "z=", __z, "__m=", __m
                    # Iterate through all polygons to determine which one occurred event
                    # belongs to
                    indices_to_remove = []
                    for selection_index, each_bin_index in enumerate(selection):

                        # Don't use inclusion flags of the polygon yet
                        forecast_polygon = forecast[each_bin_index,
                                                    PolygonForecastHandler.Format.Vertex]
                        
                        _geo_polygon = geometry.Polygon(forecast_polygon[:, CSEPPolygon.VertexFormat.Longitude:CSEPPolygon.VertexFormat.IncludeVertex])
                        _geo_point = geometry.Point(__x, __y)
                        
                        # Polygon's outter border is not considered to be
                        # inside of the polygon, use "intersect" method too if
                        # event on one of vertexes or sides of the polygon
                        if _geo_polygon.intersects(_geo_point) or \
                           _geo_polygon.contains(_geo_point): 
                            # Event belongs to polygon, increment observations for the polygon
                            PolygonForecastHandler.Logger.info("Event %s belongs to %s polygon"
                                                               %(catalog[index],
                                                                 forecast[each_bin_index,
                                                                          PolygonForecastHandler.Format.Vertex]))
                            
                            # Trac ticket #305: Polygon's vertex and side 
                            # inclusion flags should be used to identify 
                            # forecast's polygon a target event belongs to
                            
                            # Check if some vertexes or sides of the polygon are excluded
                            exclude_event = False
                            if np.any(forecast_polygon[:, CSEPPolygon.VertexFormat.IncludeVertex] == False) or \
                               np.any(forecast[each_bin_index,
                                               PolygonForecastHandler.Format.Vertex][:, CSEPPolygon.VertexFormat.IncludeSide] == False): 
                               
                               # Some vertexes or sides are excluded
                               vertex_a_index = 0
                               num_vertexes, num_cols = forecast_polygon.shape
                                
                               for each_index in xrange(1, num_vertexes+1):
                                  if each_index == num_vertexes: 
                                      # Last iteration should be to include [last_vertex, first_vertex]
                                      vertex_b_index = 0
                                  else: 
                                      vertex_b_index = each_index
                                      
                                  vertex_a = forecast_polygon[vertex_a_index]
                                  vertex_b = forecast_polygon[vertex_b_index]
                                  
                                  # First vertex of the line segment is to be excluded
                                  if bool(vertex_a[CSEPPolygon.VertexFormat.IncludeVertex]) is False:
                                      # Check if event is at the vertex
                                      if np.abs(__x - vertex_a[CSEPPolygon.VertexFormat.Longitude]) < PolygonForecastHandler.Epsilon and \
                                         np.abs(__y - vertex_a[CSEPPolygon.VertexFormat.Latitude]) < PolygonForecastHandler.Epsilon:
                                          exclude_event = True
                                          break
                                  
                                                           
                                  # The side between vertexes "a" and "b" to be excluded: vertexes are not included
                                  # into "contains()" method:
                                  if bool(vertex_a[CSEPPolygon.VertexFormat.IncludeSide]) is False:

                                      seg_coords = np.array([forecast_polygon[vertex_a_index, 
                                                                              CSEPPolygon.VertexFormat.Longitude:CSEPPolygon.VertexFormat.IncludeVertex],\
                                                             forecast_polygon[vertex_b_index, 
                                                                              CSEPPolygon.VertexFormat.Longitude:CSEPPolygon.VertexFormat.IncludeVertex]])
                                      
                                      # Check if event is on the side
                                      _geo_segment = geometry.LineString(seg_coords)
                                      if _geo_segment.contains(_geo_point):
                                          exclude_event = True
                                          break
                                      
                                  vertex_a_index = vertex_b_index 
                            
                            if exclude_event is False:
                                forecast[each_bin_index,
                                         CSEPGeneric.Forecast.Format.Observations] += 1

                            else:
                                # Report that event was excluded
                                PolygonForecastHandler.Logger.info("Excluding event %s due to vertex/side exclusion flags of %s polygon"
                                                                   %(catalog[index],
                                                                     forecast[each_bin_index,
                                                                              PolygonForecastHandler.Format.Vertex]))
                        
                        else:
                            # Does not belong to the bin, remove from the selection
                            indices_to_remove.append(each_bin_index)

                    #print "After adding observation: ", forecast[selection, :] 
                    if compute_likelihood is True:
                       
                       # Remove polygons from selection which didn't contain any
                       # events
                       if len(indices_to_remove):
                           selection = np.delete(selection,
                                                 indices_to_remove)
                        
                       log_likelihood[selection] = \
                          CSEPUtils.logPoissonPDF(forecast[selection, 
                                                           CSEPGeneric.Forecast.Format.Observations].astype(np.float),
                                                  forecast[selection, 
                                                           CSEPGeneric.Forecast.Format.Rate].astype(np.float))
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

        return result.astype(np.float)

