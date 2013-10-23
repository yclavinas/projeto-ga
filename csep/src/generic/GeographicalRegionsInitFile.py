"""
Module GeographicalRegionsInitFile
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import Environment, CSEPInitFile, CSEPLogging
from RuntimeLoader import RuntimeLoader
from RegionInfo import RegionInfo


#--------------------------------------------------------------------------------
#
# GeographicalRegionsInitFile
#
# This module is designed to open and parse XML format files that represent
# initialization parameters for the GeographicalRegions module.
#
class GeographicalRegionsInitFile (CSEPInitFile.CSEPInitFile):

    # Static data members

    # Attribute to specify directory paths for geographical region areas
    # (collection and/or test areas)
    __regionElement = 'Region'
    __collectionAreaAttribute = 'collectionArea'  
    __testAreaAttribute = 'testArea'
    __scriptAttribute = 'mapScript'
    __scriptDirectoryAttribute = 'mapScriptDirectory'
    
    __numOfRegionInfoClassesPerRegion = 1
    
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #       filename - Filename for the input parameters.
    # 
    def __init__ (self, filename):    
        """ Initialization for GeographicalRegionsInitFile class."""

        CSEPInitFile.CSEPInitFile.__init__(self,
                                           filename)
        

    #----------------------------------------------------------------------------
    #
    # Generator method that iterates through all regions of configuration file. 
    #
    # Input: download_raw_data - Flag if raw data should be downloaded from
    #                            authorized data source. Default is True.
    #       
    # Output: Tuple of geographical region attributes
    # 
    def eachRegion(self):
       """ Iterate through region information in configuration file."""
       

       # Is data source element provided by the file? - use default source (ANSS)
       # if it's not provided
       region_list = self.elements(GeographicalRegionsInitFile.__regionElement)
       
       loader = RuntimeLoader(self)

       for each_region in region_list:
           
          # Check if class is provided for the testing region (to be loaded
          # at runtime)
          region_class = RegionInfo
          
          for each_module, each_class in loader.eachModuleClass(region_class,
                                                                each_region,
                                                                GeographicalRegionsInitFile.__numOfRegionInfoClassesPerRegion):
              
              # Configuration file provided class that defines geographical region
              region_class = each_class
                   
          __region_name = each_region.text.strip()
          
          if len(__region_name) == 0:
              error_msg = "Region name must be provided in %s file." %self.name
              CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
              
              raise RuntimeError, error_msg
          
          
          # Collect region information
          attribs = each_region.attrib
          
          # Map of region attribute and corresponding attribute in configuration file
          region_info = {GeographicalRegionsInitFile.__collectionAreaAttribute : GeographicalRegionsInitFile.__collectionAreaAttribute,
                         GeographicalRegionsInitFile.__testAreaAttribute : GeographicalRegionsInitFile.__testAreaAttribute,
                         GeographicalRegionsInitFile.__scriptDirectoryAttribute : GeographicalRegionsInitFile.__scriptDirectoryAttribute,
                         GeographicalRegionsInitFile.__scriptAttribute : GeographicalRegionsInitFile.__scriptAttribute}
            
          # Collection area is provided
          for each_tag, each_attr in region_info.iteritems():
              
              if each_attr in attribs:
                  region_info[each_tag] = Environment.replaceVariableReference(Environment.CENTER_CODE_ENV,
                                                                               attribs[each_attr].strip())
              else:
                  region_info[each_tag] = None

          yield (__region_name,
                 region_class,
                 region_info[GeographicalRegionsInitFile.__collectionAreaAttribute],
                 region_info[GeographicalRegionsInitFile.__testAreaAttribute],
                 region_info[GeographicalRegionsInitFile.__scriptAttribute],
                 region_info[GeographicalRegionsInitFile.__scriptDirectoryAttribute])

       # Stop generator
       return   
