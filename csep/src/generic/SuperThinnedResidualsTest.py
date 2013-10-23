"""
Module SuperThinnedResidualsTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib.pylab import *

from Forecast import Forecast
from DiagnosticsTest import DiagnosticsTest
from EvaluationTest import EvaluationTest
from cseprandom import CSEPRandom
from ForecastHandlerFactory import ForecastHandlerFactory
import GeographicalRegions, CSEPFile, CSEPGeneric


#-------------------------------------------------------------------------------
#
# SuperThinnedResidualsTest
#
# This class is designed to evaluate available models with residual analysis 
# tests which are introduced to the CSEP Testing Framework by Robert Clements
# et al.
#
class SuperThinnedResidualsTest (DiagnosticsTest):

    # Pattern used to match directory with random seed files in ASCII format
    __randomSeedPostfix = 'randomSeed'
    __randomSeedPattern = '*%s' %__randomSeedPostfix

    # Keyword identifying the class
    Type = "RT"
    
    # if sum of masked rates within forecast is less than provided threshold value,
    # use that threshold value for the kValue of the test
    __kValueThreshold = 100.0
    
    # R package threshold for random seed value
    __randomSeedThreshold = 2000000000

    # Data fields of tests results
    __tag = 'tag'
    __longitude = 'lon'
    __latitude = 'lat' 
    __magnitude = 'mag'

    # Test result uses "tag" to specify if event is observed or simulated
    # (used by plotting method)
    __tagObserved = 1
    __tagSimulated = 2


    xml = DiagnosticsTest.Result.XML(Type + EvaluationTest.FilePrefix,
                                     EvaluationTest.Result.Name,
                                     DiagnosticsTest._kValueOption,
                                     [], # StackVars are used by plotting method
                                     [__longitude, 
                                      __latitude,
                                      __magnitude, 
                                      __tag])
    

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
        """ Initialization for SuperThinnedResidualsTest class."""
        
        DiagnosticsTest.__init__(self, group, args)
        

    #-----------------------------------------------------------------------------
    #
    # Returns keyword identifying the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: String represenation of the test type.
    #
    def type (self):
        """ Returns test type."""

        return SuperThinnedResidualsTest.Type


    #===========================================================================
    # Write input catalog information to the parameter file for the test
    #===========================================================================
    def writeMagnitudeRangeInfo(self, fhandle):
        """Write magnitude range for the test."""
        
        return fhandle


    #===========================================================================
    # Write alpha to the parameter file for the test
    #===========================================================================
    def writeAlphaInfo(self, fhandle):
        """Write alpha for the test."""
        
        return fhandle


    #===========================================================================
    # Write kValue to the parameter file for the test
    #===========================================================================
    def writeKValueInfo(self, 
                        fhandle, 
                        forecast_name, 
                        value = None):
        """Write kValue for the test."""
        
        k_value = value
        
        if k_value is None:
            k_value = SuperThinnedResidualsTest.__getRatesSum(os.path.join(self.forecasts.dir(),
                                                                           forecast_name))
        
        # Set internal data to the value used
        self._getArgs()[DiagnosticsTest._kValueOption] = float(k_value)
        fhandle.write("kValue=%s\n" %k_value)
        return fhandle


    #===========================================================================
    # Get sum of rates for masked forecast bins
    #===========================================================================
    @staticmethod
    def __getRatesSum (forecast_name):
        """ Compute forecast rates sum of masked magnitude bins"""

        forecast = ForecastHandlerFactory().CurrentHandler.load(forecast_name)
        
        selected_rows = (forecast[:, CSEPGeneric.Forecast.Format.MaskBit].astype(int) != 0)
        
        __forecast_sum = forecast[selected_rows, CSEPGeneric.Forecast.Format.Rate].sum()
        if __forecast_sum < SuperThinnedResidualsTest.__kValueThreshold:
            __forecast_sum = SuperThinnedResidualsTest.__kValueThreshold
        
        return __forecast_sum
        
        
    
    #===========================================================================
    # Write R function to invoke for the test
    #===========================================================================
    def execFunction(self):
        """Write R source function for the test."""
        
        return 'superthinned_residuals.R'


    #===========================================================================
    # Return list of XML elements that represent test results
    #===========================================================================
    @classmethod
    def xmlElements(cls):
        """Return list of XML elements that represent test results"""
        
        return [SuperThinnedResidualsTest.__tag,
                SuperThinnedResidualsTest.__longitude,
                SuperThinnedResidualsTest.__latitude,
                SuperThinnedResidualsTest.__magnitude]


    #===========================================================================
    # Write random seed value to the parameter file for the test if applicable
    # 
    # Inputs:
    #         fhandle - Handle to open parameter file to write seed value to
    #         result_prefix - Prefix to use for random seed file (unique to the
    #                         test and forecast model(s) participating in test
    #         seed_token - Key token to use for seed value within parameter file
    #                      Default is "seed" (seed=VALUE)
    #         seed_value - In order to reproduce test results, random 
    #                              seed value is stored to the file. Name of 
    #                              the file with previously used random seed 
    #                              value. Default is None.
    #
    #===========================================================================
    def writeRandomSeedValue(self, 
                             fhandle, 
                             seed_value):
        """Write random seed value for the test."""
        
        __seed = seed_value
        if seed_value is None:
            # Create seed value
           __seed = CSEPRandom.createSeed()
           
           while np.abs(__seed*3) >= SuperThinnedResidualsTest.__randomSeedThreshold:
               __seed /= 10

        fhandle.write('seedValue=%s\n' %__seed)
       
        return fhandle


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

        
        doc, ax = EvaluationTest.plot(result_file) 

        # Extract region min/max longitude and latitude
        region = GeographicalRegions.Region.info()
        
        min_lat, max_lat, min_lon, max_lon = region.areaCoordinates(is_for_map = True)

        parent_name = cls.xml.Root
        lon_values_str = doc.elementValue(SuperThinnedResidualsTest.__longitude,
                                          parent_name).split()
        lon_values = np.array(map(float, lon_values_str))

        lat_values_str = doc.elementValue(SuperThinnedResidualsTest.__latitude,
                                          parent_name).split()
        lat_values = np.array(map(float, lat_values_str))
        
        if isinstance(min_lat, list) is False:
            # Values are provided for the region
            min_lon -= 1.0
            max_lon += 1.0
            min_lat -= 1.0
            max_lat += 1.0
            
        else:
            # Values are not provided, learn from result file
            min_lon = min(lon_values)
            if min_lon > -179.0:
                min_lon -= 1.0

            max_lon = max(lon_values)
            if max_lon < 179.0:
                max_lon += 1.0
                            
            min_lat = min(lat_values)
            if min_lat > -89.0:
                min_lat -= 1.0

            max_lat = max(lat_values)
            if max_lat < 89.0:
                max_lat += 1.0
        
        print "COORDS:", min_lat, max_lat, min_lon, max_lon
        grid_meridians, grid_parallels = region.grid(coords=(min_lat, max_lat, min_lon, max_lon))
        

        ### Generate map of the observed seismicity using ANSS catalog and
        ### specified magnitude threshold
        __map = Basemap(llcrnrlon=min_lon, urcrnrlon=max_lon, 
                        llcrnrlat=min_lat, urcrnrlat=max_lat, 
                        resolution='f')
        
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

        # Get testing region border
        # Load area coordinates for the testing region
        border_x, border_y = region.areaBorders(region.testArea)
        if len(border_x) != 0:
            # Test area is provided for the region
            x, y = __map(border_x, border_y)
            __map.plot(x, y,
                       'k',
                       linewidth=1.5, 
                       zorder=65,
                       label= '_nolegend_')


        tag_values_str = doc.elementValue(SuperThinnedResidualsTest.__tag,
                                          parent_name).split()
        tag_values = np.array(map(int, map(float, tag_values_str)))

        # Identify observed events vs. simulated events based on tag value
        selection, = np.where(tag_values == SuperThinnedResidualsTest.__tagSimulated)
        
        # Display simulated events
        x, y = __map(lon_values[selection],
                     lat_values[selection])
                
        __map.plot(x, y, 'gx', 
                   markersize = 6.0,
                   mew = 1.5, 
                   zorder = 70, 
                   label = '_nolegend_')
        
        
        selection, = np.where(tag_values == SuperThinnedResidualsTest.__tagObserved)
        
        # Display observed events
        x, y = __map(lon_values[selection],
                     lat_values[selection])
        __map.plot(x, y, 'ro', 
                   markersize = 6.0,                   
                   zorder = 80, 
                   label = '_nolegend_')
            
        name = doc.elementValue(EvaluationTest.Result.Name)

        # Return image filename
        return DiagnosticsTest._finishPlot(result_file,
                                           output_dir,
                                           "Super-thinned residuals (%s)" %name)
 
 
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

