"""
GeographicalRegions module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, glob
import numpy as np
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon
from matplotlib.colors import rgb2hex 
import matplotlib.mpl as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib


import CSEPLogging, CSEPFile, CSEP, Environment
from CSEPBorgIdiom import CSEPBorgIdiom
from RegionInfo import RegionInfo
from GeographicalRegionsInitFile import GeographicalRegionsInitFile
from CSEPPolygon import CSEPPolygon
from ForecastHandlerFactory import ForecastHandlerFactory


California = 'California'
SWPacific = 'SWPacific'
NWPacific = 'NWPacific'
Global = 'Global'
OceanicTransformFaults = 'OceanicTransformFaults'


# Logger object for the module
__logger = None

#-------------------------------------------------------------------------------
# Function to access logger object for the module.
#-------------------------------------------------------------------------------
def _moduleLogger():
    """ Get logger object for the module, initialize one if it does not exist"""
    
    global __logger
    if __logger is None:
        __logger = CSEPLogging.CSEPLogging.getLogger(__name__)
    
    return __logger


#-------------------------------------------------------------------------------
#
# Structure-like class to store variables specific to the CSEP California 
# testing region.
# 
class CaliforniaRegionInfo (RegionInfo):
   
   def __init__(self,
                collection_area, 
                testing_area):
      
      RegionInfo.__init__(self,
                          collection_area,
                          testing_area,
                          'forecast.gmt -p bf')
      

   #-----------------------------------------------------------------------------
   #
   # areaCoordinates
   # 
   # Returns minimum and maximum latitude/longitude coordinates that
   # define a testing geographical region.
   #
   # Inputs:
   #         is_for_map - Flag if area coordinates are requested for mapping 
   #                      purposes. Default is False.   
   #    
   def areaCoordinates(self, 
                       area_file = None, 
                       is_for_map = False):  
      """Returns tuple with minimum latitude, maximum
         latitude, minimum longitude, and maximum longitude of test area for the
         region."""
          

      min_lat, max_lat, min_lon, max_lon = RegionInfo.areaCoordinates(self,
                                                                      area_file,
                                                                      is_for_map)
      __cellHalfDim = 0.05
          
      return (min_lat - __cellHalfDim, max_lat + __cellHalfDim,
              min_lon - __cellHalfDim, max_lon + __cellHalfDim)  


#-------------------------------------------------------------------------------
#
# Structure-like class to store variables and methods specific to the CSEP 
# OceanicTransformFaults testing region.
# 
class OceanicTransformFaultsRegionInfo (RegionInfo):
   
   
   #============================================================================
   # Initialization 
   #============================================================================
   def __init__(self):
      
       RegionInfo.__init__(self,
                           None,
                           None,
                           None,
                           None)
      
      
   #-----------------------------------------------------------------------------
   #
   # areaCoordinates
   # 
   # Returns lists of minimum and maximum latitude/longitude coordinates that
   # define a testing geographical region.
   #
   # Inputs:
   #         area_file - Area file, default is None meaning that test area of
   #                     of the region should be used.
   #         is_for_map - Flag if area coordinates are requested for mapping 
   #                      purposes. Default is False.
   #    
   def areaCoordinates(self, 
                       area_file = None, 
                       is_for_map = False):  
      """Returns tuple of lists that represent minimum latitude, maximum
         latitude, minimum longitude, and maximum longitude of test area for the
         region."""
          
      min_lat = []
      max_lat = []
      min_lon = []
      max_lon = []

      __area = area_file
      
      # Use test area of the region by default
      if area_file is not None:
          # Area file is not supported for the region, raise an exception
          error_msg = "Area file (%s) cannot be provided to the %s.areaCoordinates()" \
                      %(area_file,
                        OceanicTransformFaults) 
          _moduleLogger().error(error_msg)
         
          raise RuntimeError, error_msg
      
      # Polygon definition with Latitude,Longitude pairs per Margaret's model:
#      <postList>-4.4494,-105.1555     -4.377277,-105.4163     -4.622699,-105.2037     -4.550599,-105.4645</postList>
#      <postList>-4.4724,-105.828     -4.412209,-106.0918     -4.647766,-105.8682     -4.587534,-106.132</postList>
#      <postList>-4.5424,-105.5279     -4.482209,-105.7918     -4.717766,-105.5682     -4.657534,-105.8321</postList>
#      <postList>10.4895,-103.7585      10.44821,-104.0295      10.31174,-103.7305      10.27046,-104.0015</postList>
#      <postList>43.5512,-128.0539      43.63867,-128.4058      43.38104,-128.1343      43.46853,-128.4863</postList>
#      <postList>43.6212,-127.5537      43.70867,-127.9059      43.45104,-127.6341      43.53852,-127.9865</postList>      
      
      # return tuple of values: (min_lat, max_lat, min_lon, max_lon)
      return (-5.0, 44.0, -129.0, -103.0)
      
      
      
   #------------------------------------------------------------------------
   #
   # Generate map of the forecast specific to the testing region.
   #
   # Input: 
   #        forecast_file - File path to the forecast in XML format
   #        results_dir - Directory to store result files to. Default is a
   #                      current directory.
   #        test_name - Name of the test for each forecast map is generated.
   #                    Default is None.
   #        catalog_file - Optional observation catalog file to display observed
   #                       events. Default is None.
   #        scale_factor - Scale factor to apply to the forecast. Default value
   #                       is 1.0 (don't scale)
   # Output: 
   #         Filename for the map file
   #
   @classmethod
   def createMap (cls,
                  region,
                  image_file,
                  forecast_data_file,
                  catalog_data_file): 
        """ Create a map of the forecast model."""



        min_lat, max_lat, min_lon, max_lon = region.areaCoordinates(is_for_map = True)

        grid_meridians, grid_parallels = region.grid()
        
        fig = plt.figure(figsize = (9, 9))        

        ### Generate map of the observed seismicity using ANSS catalog and
        ### specified magnitude threshold
        __map = Basemap(llcrnrlon=min_lon - 1.0, urcrnrlon=max_lon + 1.0, 
                        llcrnrlat=min_lat - 1.0, urcrnrlat=max_lat + 1.0, 
                        resolution='f')
        
        __map.fillcontinents(color = '0.95',
                             zorder = 10)
        __map.drawrivers(zorder=20, 
                         color = 'b', 
                         linewidth = 0.3)
        __map.drawstates(zorder=30, 
                         linewidth = 0.3)
        
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

        # Access axis
        ax = fig.gca()

        # Use reverted version of standard "autumn" colormap
        #__cmap = mpl.cm.autumn_r
        __cmap = mpl.cm.cool

        # Need to extract rates values to know how to normalize these values to
        # get corresponding colormap color (that will be representing 
        # [minRate;maxRate] range only)
        rates = [float(each_line.split()[-1]) for each_line in CSEPFile.openFile(forecast_data_file)]
        min_rate = min(rates)
        max_rate = max(rates)
        
        # Load forecast map-ready ASCII file
        for index, each_line in enumerate(CSEPFile.openFile(forecast_data_file)):
            # Parse out Polygon's info
            lat, lon = [], []
            
            line_tokens = each_line.split()
            rate = (rates[index] - min_rate)/(max_rate - min_rate)
            
            # Last entry of each line is polygon's rate
            for each_token in line_tokens[:-1]:
                lat_value, lon_value = [float(token.strip()) for token in each_token.split(CSEPPolygon.XML.Separator)]
                lat.append(lat_value)
                lon.append(lon_value)
                
            __x, __y = __map(lon, 
                             lat) 
            # Add polygon to the map colored according to the rate
            #color = rgb2hex(__cmap(np.sqrt(rate))[:3])
            color = rgb2hex(__cmap(rate)[:3])
            
            # Fill polygon with color
            ax.add_patch(Polygon(zip(__x, __y),
                                 facecolor=color,
                                 edgecolor=color,
                                 fill = True,
                                 zorder=70))
                
        cax = fig.add_axes([0.2, 0.05, 0.6, 0.02])

        # Determine the step for the color bar:
        __bounds_delta_log10 = np.floor(np.log10(max_rate))
        if __bounds_delta_log10 < 0.0:
            __bounds_delta_log10 = np.floor(__bounds_delta_log10)
        else:
            __bounds_delta_log10 = np.ceil(__bounds_delta_log10)

        __bounds_delta = 10.0**__bounds_delta_log10

        __bounds = []
        
        while len(__bounds) < 5:
            __bounds = np.arange(0.0,
                                 max_rate + __bounds_delta, 
                                 __bounds_delta).tolist()
            __bounds_delta /= 2.0  

        __cmap_norm = mpl.colors.BoundaryNorm(__bounds,
                                              __cmap.N)

        
        colorbar = mpl.colorbar.ColorbarBase(cax, 
                                             cmap=__cmap,
                                             norm=__cmap_norm,
                                             ticks=__bounds,
                                             format='%3.1e',
                                             orientation='horizontal',
                                             drawedges=False)
        colorbar.set_label("Rate ($\lambda$)")
       
        plt.savefig(image_file)
        plt.close()
        plt.clf()
                        
        return image_file



# Available geographical regions within SCEC testing center      
class Region (CSEPBorgIdiom):      
      
   # Static data

   # Instances of the class will be sharing the same state 
   # (see CSEPBorgIdiom class)
   _shared_state = {}      
   
   # Current geographical region for the testing center. Defaults to California.
   Selected = California
   
   # Dictionary with available testing regions within the framework
   __all = {California : CaliforniaRegionInfo(os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV], 
                                                           'data', 
                                                           'areas', 
                                                           'RELMCollectionArea.dat'),
                                              os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                                           'data', 
                                                           'areas', 
                                                           'RELMTestArea.dat')),

            NWPacific : RegionInfo(None,
                                   os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV], 
                                                'data', 
                                                'areas', 
                                                'NWPacificTestArea.dat'),
                                   'forecast.nw.gmt'),
            
            SWPacific : RegionInfo(None,
                                   os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV], 
                                                'data',
                                                'areas',
                                                'SWPacificTestArea.dat'),
                                   'forecast.sw.gmt'),

            Global : RegionInfo(None,
                                None,
                                'forecast.global.gmt'),
                                
            OceanicTransformFaults : OceanicTransformFaultsRegionInfo()}
   

   # Default configuration file is not specified by the caller  
   __configFilePattern = '*GeographicalRegions.init.xml'
   

   # Set of configuration files that were used to initialize available geographical
   # regions for the testing center
   __configFiles = set()
   
   
   #----------------------------------------------------------------------------
   #
   # Initialization.
   #
   # Input: config_files_dir - Directory to look for configuration files that
   #                           match Region.__configFilePattern pattern. Default
   #                           is None meaning use $CENTERCODE/TestingCenterConfiguration
   #                           directory to search for configuration files. 
   # 
   def __init__ (self, config_files_dir = None): 
       """ Initialization for Region class"""

       CSEPBorgIdiom.__init__(self)

       # Check for files that match the pattern for factory configuration file
       search_dir = config_files_dir
       if search_dir is None:
           search_dir = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                     CSEP.TestingCenterConfigDir)
           
       existing_config_files =  glob.glob(os.path.join(search_dir,
                                                       Region.__configFilePattern))
       
       for each_file in existing_config_files:
            
           if each_file not in Region.__configFiles:
               config_file = GeographicalRegionsInitFile(each_file)
               Region.__configFiles.add(each_file)
               
               # Iterate through all regions in configuration file
               for each_region in config_file.eachRegion():
                   
                   name, region_class, collection_area, test_area, script_name, script_dir = each_region
                   Region.__all[name] = region_class(collection_area, 
                                                     test_area,
                                                     script_name, 
                                                     script_dir)
       
   
   #-----------------------------------------------------------------------------
   #
   # Returns information about current geographical region for the testing center
   #
   @staticmethod 
   def info ():
      
      return Region.__all[Region.Selected]
      

   #-----------------------------------------------------------------------------
   #
   # Returns available geographical regions for the testing center
   #
   @staticmethod 
   def all ():
      
      return Region.__all.keys()


   #--------------------------------------------------------------------------------
   #
   # Sets current geographical region for the testing center
   #
   def set (self, region):
      
      # No region is specified
      if region is None:
         return
      
      if not region in Region.__all:

         error_msg = "Unknown '%s' geographical region is specified. Please select one of %s." \
                     %(region, Region.__all.keys())
         _moduleLogger().error(error_msg)
         
         raise RuntimeError, error_msg
      
      else:
         Region.Selected = region

         msg = "Setting geographical region to '%s'." %region
         _moduleLogger().info(msg)

      return
   

   #----------------------------------------------------------------------------
   #
   # Invoke GMT script specific to the testing region to generate the map of the
   # forecast. 
   # This method creates and invokes a bash script to generate the map.
   #
   # Input: 
   #        forecast_file - File path to the forecast in XML format
   #        results_dir - Directory to store result files to. Default is a
   #                      current directory.
   #        test_name - Name of the test for each forecast map is generated.
   #                    Default is None.
   #        catalog_file - Optional observation catalog file to display observed
   #                       events. Default is None.
   #        scale_factor - Scale factor to apply to the forecast. Default value
   #                       is 1.0 (don't scale)
   # Output: 
   #         Filename for the map file
   #
   @staticmethod
   def createMap (forecast_file,
                  results_dir = '.',
                  start_date = None,
                  test_name = None,
                  catalog_file = None,
                  scale_factor = 1.0): 
        """ Create a map of the forecast model based on selected geographical region."""


        import CSEPGeneric
        
        ### Create map-ready ASCII format data
        _val_file = ForecastHandlerFactory().CurrentHandler.XML(forecast_file)
        forecast_data_file = _val_file.toASCIIMap(results_dir,
                                                  test_name, 
                                                  scale_factor)
        
        catalog_data_file = None
        
        # Create map-ready ASCII file for observation catalog
        if catalog_file is not None:

           # Generate map-ready catalog data
           catalog_data_file = CSEPGeneric.Catalog.toASCIIMap(catalog_file,
                                                              start_date)

        # Create filename for the map file
        # Replace extension with '.png' for the image file
        image_file = forecast_data_file.replace(CSEPFile.Extension.ASCII,
                                                CSEPFile.Extension.PNG)
        if CSEP.Forecast.MapReadyPrefix in image_file:
            image_file = image_file.replace(CSEP.Forecast.MapReadyPrefix,
                                            CSEP.Forecast.MapPrefix)
        else:
            image_file = CSEP.Forecast.MapPrefix + image_file
        
        if not os.path.exists(image_file):

           Region.info().createMap(Region.info(),
                                   image_file,
                                   forecast_data_file,
                                   catalog_data_file) 
                
        return image_file
     

if __name__ == '__main__':
    
    ### Stand-alone functionality to be used by miniCSEP distribution
    import optparse
    from CSEPOptions import CommandLineOptions
    
    
    #===========================================================================
    # Command-line options for the module when invoked in stand-alone mode
    #===========================================================================
    class GeographicalRegionsOptions (optparse.OptionParser):
        
        ForecastOption = "--forecast"
        ScaleFactorOption = "--scaleFactor"
        CatalogOption = "--catalog"
        
        
        #-----------------------------------------------------------------------
        # Initialization.
        #        
        def __init__ (self):
            """ Initialization for CSEPOptionParser class"""
            
            # Report CSEP version on request (--version option)        
            optparse.OptionParser.__init__(self, version = CSEP.Version)
            
            # Define options
            self.add_option(GeographicalRegionsOptions.ForecastOption, 
                            dest="forecast",
                            default=None,
                            help="Filename of input forecast. Default is None.") 

            self.add_option(GeographicalRegionsOptions.CatalogOption, 
                            dest="catalog",
                            default=None,
                            help="Filename of observation catalog. Default is None.") 
     
            help_message = "Enable map-view of the forecast. Default \
behavior is to skip map generation for forecasts."
            self.add_option(CommandLineOptions.FORECAST_MAP, 
                            action="store_true", 
                            dest="forecast_map",
                            default=False, 
                            help=help_message)        
     
            self.add_option(CommandLineOptions.TEST_DIR,
                            dest="test_dir", 
                            type="string",
                            default=".",
                            help="Directory to store results files to. \
Default is '.' (current run-time directory).", 
                            metavar="DIR") 
     
            self.add_option(GeographicalRegionsOptions.ScaleFactorOption, 
                            dest="scale_factor", 
                            default=1.0,
                            type="float",
                            help="Scale factor to apply to the forecast rates. \
Default is 1.0", 
                            metavar="SCALE_FACTOR")

            self.add_option(CommandLineOptions.REGION, 
                            dest="region",
                            type="string",
                            help="Geographical region for the forecast models and \
evaluation tests. One of %s. Default is %s." %(Region.all(),
                                               Region.Selected),
                            metavar="REGION")

            self.add_option(CommandLineOptions.LOG_FILE, 
                            dest="log_file", 
                            type="string",
                            help="Log file used to capture progress and error \
messages to. This option is used only to make the software aware of the file \
where it's output was redirected to. Caller has to explicitly redirect output \
and error streams to the specified file. Default is stdout stream handler.", 
                            metavar="FILE",
                            default=None)


        #--------------------------------------------------------------------
        #
        # Get command line options values.
        #
        # Input: None
        # 
        # Output:
        #        Map of command line options and their values.
        #
        def options (self):
            """Get command line options and their values."""
    
            # Parse command line arguments
            (values, args) = self.parse_args()
            
            # Set geographical region if it's specified
            Region().set(values.region)
            
            return values

    # end of GeographicalRegionsOptions class
    

    parser = GeographicalRegionsOptions()
    options = parser.options()
    
    ### Generate 
    if options.forecast_map is True:
        
        # Forecast filename will be used to populate 'name' element of the 
        # XML template
        map_file = Region.createMap(options.forecast,
                                    options.test_dir,
                                    catalog_file = options.catalog,
                                    scale_factor = options.scale_factor)
        
        _moduleLogger().info("Map-view of the %s forecast is stored in %s file." %(options.forecast,
                                                                                   map_file)) 

