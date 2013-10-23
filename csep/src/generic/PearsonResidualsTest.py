"""
Module PearsonResidualsTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


from mpl_toolkits.basemap import Basemap
import matplotlib.mpl as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as mpl_cm

from DiagnosticsTest import DiagnosticsTest
from EvaluationTest import EvaluationTest
import GeographicalRegions


#-------------------------------------------------------------------------------
#
# PearsonResidualsTest
#
# This class is designed to invoke Pearson residuals evaluation test
# which is introduced to the CSEP Testing Framework by Robert Clements et al.
#
class PearsonResidualsTest (DiagnosticsTest):

    # Static data

    # Keyword identifying the class
    Type = "RP"

    __minLongitude = "minlon"
    __maxLongitude = "maxlon"
    __minLatitude = "minlat"
    __maxLatitude = "maxlat"
    __mask = "mask"
    __rate = "rate"
    __count = "count"
    __p_residual = "P.residual"
    __raw_residual = "raw.residual"
        
    __residual = {"P.residual" : 'Pearson',
                  "raw.residual" : "Raw"}
    
    __figureSize = (9, 9)


    xml = DiagnosticsTest.Result.XML(Type + EvaluationTest.FilePrefix,
                                     EvaluationTest.Result.Name,
                                     __residual.keys(),
                                     [__minLongitude, __minLatitude])


    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be invoked.
    #        args - Optional input arguments for the test. Default is None.    
    # 
    def __init__ (self, group, args = None):
        """ Initialization for PearsonResidualsTest class."""
        
        DiagnosticsTest.__init__(self, group, args)


    #-----------------------------------------------------------------------------
    #
    # Returns description word for the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: Description of the test (such RELMTest, AlarmTest, etc.)
    #
    def type (self):
        """ Returns test type identifier."""

        return PearsonResidualsTest.Type

    #===========================================================================
    # Write alpha to the parameter file for the test
    #===========================================================================
    def writeAlphaInfo(self, fhandle):
        """Write alpha for the test."""
        
        return fhandle


    #===========================================================================
    # Write R function to invoke for the test
    #===========================================================================
    def execFunction(self):
        """Return R source function for the test."""
        
        return 'pearson_residuals.R'


    #===========================================================================
    # Return list of XML elements that represent test results
    #===========================================================================
    @classmethod
    def xmlElements(cls):
        """Return list of XML elements that represent test results"""
        
        return [PearsonResidualsTest.__minLongitude,
                PearsonResidualsTest.__maxLongitude,
                PearsonResidualsTest.__minLatitude,
                PearsonResidualsTest.__maxLatitude,
                PearsonResidualsTest.__mask,
                PearsonResidualsTest.__rate,
                PearsonResidualsTest.__count,
                PearsonResidualsTest.__residual.keys()]
    
    
    #----------------------------------------------------------------------------
    #
    # This method plots result data of evaluation test.
    #
    # Input: 
    #         result_file - File with daily test results.
    #         output_dir - Directory to place plot file to. Default is None.     
    #
    @classmethod
    def plot (cls, 
              result_file, 
              output_dir = None):
        """ Plot test results in XML format."""

        
        doc, ax = EvaluationTest.plot(result_file,
                                      fig_size = PearsonResidualsTest.__figureSize) 

        # Extract region min/max longitude and latitude for the region
        region = GeographicalRegions.Region.info()
        
        min_lat, max_lat, min_lon, max_lon = region.areaCoordinates(is_for_map = True)

        # Values from result file
        parent_name = cls.xml.Root
        min_lon_values_str = doc.elementValue(PearsonResidualsTest.__minLongitude,
                                              parent_name).split()
        min_lon_values = map(float, min_lon_values_str)

        min_lat_values_str = doc.elementValue(PearsonResidualsTest.__minLatitude,
                                              parent_name).split()
        min_lat_values = map(float, min_lat_values_str)

        # Empty list is returned for regions with no specific area
        if isinstance(min_lat, list) is False:
            # Values are provided for the region
            min_lon -= 1.0
            max_lon += 1.0
            min_lat -= 1.0
            max_lat += 1.0
            
        else:
            # Values are not provided, learn from result file
            min_lon = min(min_lon_values)
            if min_lon > -179.0:
                min_lon -= 1.0

            max_lon = max(min_lon_values)
            if max_lon < 179.0:
                max_lon += 1.0
                            
            min_lat = min(min_lat_values)
            if min_lat > -89.0:
                min_lat -= 1.0

            max_lat = max(min_lat_values)
            if max_lat < 89.0:
                max_lat += 1.0

        grid_meridians, grid_parallels = region.grid(coords=(min_lat, max_lat, min_lon, max_lon))
        
        fig = plt.figure(figsize = PearsonResidualsTest.__figureSize)        

        ### Generate map of the observed seismicity using ANSS catalog and
        ### specified magnitude threshold
        __map = Basemap(llcrnrlon=min_lon, urcrnrlon=max_lon, 
                        llcrnrlat=min_lat, urcrnrlat=max_lat, 
                        resolution='f')
        
#        # Load area coordinates for the testing region
#        area = np.loadtxt(CSEPFile.openFile(CSEPFile.Name.ascii(region.testArea)))
#        x, y = anss_map(area[:, 0], area[:,1])
#        anss_map.plot(x, y, 'y.', alpha = 0.1, zorder=100)
#        
        __map.fillcontinents(color = '0.95',
                             zorder = 10)
        __map.drawrivers(zorder=20, 
                         color = 'b', 
                         linewidth = 0.3)
        __map.drawstates(zorder=30, 
                         linewidth = 0.3)
        
        #map.fillcontinents(zorder=30)
        __map.drawcoastlines(zorder=40)

        # Draw longitude on the map 
        __map.drawmeridians(grid_meridians, 
                            labelstyle='+/-', 
                            labels=[1,1,0,1],
                            zorder=50)

        # Draw latitude on the map
        __map.drawparallels(grid_parallels,
                            labelstyle='+/-', 
                            labels=[1,1,1,1],
                            zorder=60)


        residual_values = None
        residual_str = None
        
        for each_elem, each_str in PearsonResidualsTest.__residual.iteritems():
            residual_values_str = doc.elementValue(each_elem, 
                                                   parent_name)
            if residual_values_str is not None:
                residual_values_str = residual_values_str.split()
                residual_values = map(float, residual_values_str)
                residual_str = each_str

        # Use pcolor with min(residuals)-1 value for not provided bins
        unique_min_lon_values = sorted(set(min_lon_values))
        unique_min_lat_values = sorted(set(min_lat_values))
        
        __xnum = len(unique_min_lon_values)
        __ynum = len(unique_min_lat_values)
        
        __datain = np.array([np.nan] * __xnum*__ynum)
        __datain.shape = (__ynum, __xnum)

        for each_lon, each_lat, each_residual in zip(min_lon_values, 
                                                     min_lat_values, 
                                                     residual_values):
            
            __lon_index = unique_min_lon_values.index(each_lon)
            __lat_index = unique_min_lat_values.index(each_lat)
            
            __datain[__lat_index, __lon_index] = each_residual

        # Create masked array to isolate testing region
        __datain_masked = np.ma.masked_where(np.isnan(__datain), __datain)

        unique_min_lon_values = np.array(unique_min_lon_values)
        unique_min_lat_values = np.array(unique_min_lat_values)
        
        __x, __y = __map(unique_min_lon_values, 
                         unique_min_lat_values)

        __cmap = mpl.cm.cool

        __map.pcolor(__x, __y, 
                     __datain_masked, 
                     cmap = __cmap,
                     zorder = 70, 
                     alpha = 0.3)
        
        cax = fig.add_axes([0.2, 0.05, 0.6, 0.02])

        colorbar = mpl.colorbar.ColorbarBase(cax, 
                                             cmap=__cmap,
                                             format='%2.1f',
                                             orientation='horizontal')
        
        
        name = doc.elementValue(EvaluationTest.Result.Name)
        
        # Return image filename
        return DiagnosticsTest._finishPlot(result_file,
                                           output_dir,
                                           "%s residuals (%s)" %(residual_str,
                                                                 name))
 
 
    #----------------------------------------------------------------------------
    #
    # This method plots summary result data of evaluation test.
    #
    # Input: 
    #         result_file - File with cumulative test results.
    #         output_dir - Directory to place plot file to. Default is None.     
    #
    @classmethod
    def plotSummary (cls, 
                     result_file, 
                     output_dir = None):
        """ Plot test results in XML format."""
 
        
        return cls.plot(result_file, 
                        output_dir)

