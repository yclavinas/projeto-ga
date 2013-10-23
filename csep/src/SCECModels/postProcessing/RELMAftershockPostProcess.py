"""
Module RELMAftershockPostProcess
"""

__version__ = "$Revision: 4126 $"
__revision__ = "$Id: RELMAftershockPostProcess.py 4126 2012-12-06 01:15:09Z liukis $"


import os, datetime, operator

import PostProcess, GeographicalRegions, CSEP
from DataSourceFactory import DataSourceFactory


#--------------------------------------------------------------------------------
#
# RELMAftershockPostProcess.
#
# This class is designed to post-process a catalog data that is used as observations for 
# the RELM 5-year aftershock models. It post-processes the observation data in preparation
# for the evaluation tests of the forecasts models.
#
class RELMAftershockPostProcess (PostProcess.PostProcess):
        
    # Key identifying the type of post-processing
    Type = "RELMAftershock"
    
    # Magnitude threshold for the forecast models
    MinMagnitude = 4.95
    
    # Depth threshold for the forecast models
    MaxDepth = 30.0
    
    # Forecast duration in years
    __duration = 5.0
  
    # Name of the XML forecast template file 
    ForecastTemplate = os.path.join(PostProcess.PostProcess.CenterCode, 
                                    'data',
                                    'templates', 
                                    'csep-forecast-template-M5.xml')
        
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    def __init__ (self, start_date = datetime.datetime(2006, 1, 1),
                        end_date = datetime.datetime(2011, 1, 1),
                        cumulative_start_date = None):
        """ Initialization for RELMAftershockPostProcess class
        
            Input arguments:
            start_date - datetime object that represents forecast start date
                         (default is datetime(2006, 1, 1))
            end_date - datetime object that represents forecast end date
                       (default is datetime(2011, 1, 1))
        """
 
        files = PostProcess.PostProcess.Files(cumulative_catalog = None)
        if cumulative_start_date is not None:
            # Use default settings for cumulative catalog
            files = PostProcess.PostProcess.Files()
            
        PostProcess.PostProcess.__init__(self, 
                                         RELMAftershockPostProcess.MinMagnitude,
                                         RELMAftershockPostProcess.MaxDepth,
                                         RELMAftershockPostProcess.__duration,
                                         files,
                                         xml_template = RELMAftershockPostProcess.ForecastTemplate)

        # Set starting date for the testing period
        PostProcess.PostProcess.startDate(self, start_date)
        
        # Set expiration date for the models
        PostProcess.PostProcess.endDate(self, end_date)

        if cumulative_start_date is not None:
            # Set start date for cumulative testing period if any
            PostProcess.PostProcess.cumulativeStartDate(self, 
                                                        cumulative_start_date)
        
    
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
    # Post-process catalog data in preparation for the evaluation test.
    #
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
            RELM five-year aftershock models."""
        

        # Acquire reference to catalog data source class used by the framework
        data_class = DataSourceFactory().classReference()
        
        # Import catalog data into CSEP generic format
        np_catalog = data_class.importToCSEP(raw_file)
        
        # Cut catalog according to collection area
        np_catalog = data_class.cutToArea(np_catalog,
                                          GeographicalRegions.Region.info().collectionArea)
        
        # Cut according to last testing day
        start_date = DataSourceFactory().object(data_class.Type,
                                                isObjReference = True).StartDate  # download start date
        end_date = test_date + datetime.timedelta(hours=24)
        
        # Create cumulative catalog if requested
        if self.files.cumulativeCatalog is not None and \
           self.cumulative_start_date is not None:
            
           np_cumulative_catalog = data_class.cutToTimePeriod(np_catalog, 
                                                              self.cumulative_start_date, 
                                                              end_date, 
                                                              stop_time_sign = operator.lt)
           
           cumulative_threshold = PostProcess.PostProcess.Threshold(self.threshold.MinMagnitude,
                                                                    self.threshold.MaxDepth,
                                                                    self.cumulative_start_date)
           
           data_class.filter(np_cumulative_catalog, 
                             GeographicalRegions.Region.info().testArea,
                             cumulative_threshold,
                             self.files.cumulativeCatalog)
        
        
        np_catalog = data_class.cutToTimePeriod(np_catalog, 
                                                start_date, end_date, 
                                                stop_time_sign = operator.lt)

        ### Apply uncertainties to catalog
        result_dir = data_class.modifications(np_catalog, 
                                              GeographicalRegions.Region.info().testArea,
                                              self.threshold,
                                              self.files.uncertainties)
        
        # Register for reproducibility a directory with random seed files 
        # (if it was generated)
        PostProcess.PostProcess.registerUncertaintiesDir(self,
                                                         result_dir)
                  
        ### Cut catalog according to the test area, filter events
        data_class.filter(np_catalog, 
                          GeographicalRegions.Region.info().testArea,
                          self.threshold,
                          self.files.catalog)
        
        # Create cumulative catalog which is the same as observation catalog
        data_class.filter(np_catalog, 
                          GeographicalRegions.Region.info().testArea,
                          self.threshold,
                          self.files.catalog)
