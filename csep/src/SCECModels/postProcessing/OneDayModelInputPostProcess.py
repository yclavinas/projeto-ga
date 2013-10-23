"""
Module OneDayModelInputPostProcess
"""

__version__ = "$Revision: 4219 $"
__revision__ = "$Id: OneDayModelInputPostProcess.py 4219 2013-03-04 22:02:53Z liukis $"

import datetime, operator

import PostProcess, GeographicalRegions, CSEP
from DataSourceFactory import DataSourceFactory
#from ReproducibilityFiles import ReproducibilityFiles


#--------------------------------------------------------------------------------
#
# OneDayModelInputPostProcess.
#
# This class is designed to post-process a catalog data that is used as an input for 
# the one day short-term forecasts models. It post-processes the observation data in 
# preparation for the forecast generation.
#
class OneDayModelInputPostProcess (PostProcess.PostProcess):
        
    # Key identifying the type of post-processing
    Type = "OneDayModelInput"
    
    # Magnitude threshold for the forecast models
    MinMagnitude = 3.95
    
    # Depth threshold for the forecast models
    MaxDepth = 30
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None
    # 
    def __init__ (self):
        """ Initialization for OneDayModelInputPostProcess class"""
 
        __catalog_file = "OneDayModelInputCatalog.dat"
        
        PostProcess.PostProcess.__init__(self, 
                                         OneDayModelInputPostProcess.MinMagnitude,
                                         OneDayModelInputPostProcess.MaxDepth,
                                         catalogs = PostProcess.PostProcess.Files(__catalog_file,
                                                                                  None,
                                                                                  None))
        
        # Fix for Trac ticket #306: Don't preserve OneDayModelInputCatalog data products within testing framework
        required, optional = self.reproducibility
        required[__catalog_file].preserve = False
        required[__catalog_file].comment += " (Region=%s; MinMagnitude=%s; MaxDepth=%s)" %(GeographicalRegions.Region.Selected,
                                                                                           OneDayModelInputPostProcess.MinMagnitude,
                                                                                           OneDayModelInputPostProcess.MaxDepth)

    
    #--------------------------------------------------------------------
    #
    # Get the type of post-processing.
    #
    # Input: None.
    # 
    # Output:
    #         Post-processing type.
    # 
    def type (self):
        """ Get type of the post-processing."""
            
        return self.Type
     
     
    #--------------------------------------------------------------------
    #
    # Post-process catalog data in preparation for the forecast generation.
    #
    # Input: 
    #        test_date - datetime object that represents the test date.    
    #        raw_file - Filename for raw catalog data.
    #
    # Output:
    #        Name of the result catalog file. 
    #
    def apply (self, test_date, raw_file):
        """ Post-process catalog data in preparation for the evaluation tests of the
            one day forecasts models."""

        # Create forecast initialization line for Matlab script
        PostProcess.PostProcess.startDate(self, test_date)
        
        # Acquire reference to catalog data source class used by the framework
        for each_source in DataSourceFactory.composite().values():
            
            data_class = DataSourceFactory().classReference(each_source.type())

            # Import catalog data into Matlab format
            np_catalog = data_class.importToCSEP(raw_file)
            
            # Cut catalog according to collection area
            np_catalog = data_class.cutToArea(np_catalog,
                                              GeographicalRegions.Region.info().collectionArea)
            
            # Cut catalog excluding the testing day
            start_date = DataSourceFactory().object(data_class.Type,
                                                    isObjReference = True).StartDate  # download start date
            end_date = test_date
            
            np_catalog = data_class.cutToTimePeriod(np_catalog, 
                                                    start_date, end_date, 
                                                    self.files.catalog,
                                                    stop_time_sign = operator.lt)
                  
