"""
Module OneYearModelPostProcess
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, datetime, operator

import PostProcess, DataSourceFactory, GeographicalRegions, CSEP


#--------------------------------------------------------------------------------
#
# OneYearModelPostProcess
#
# This class is designed to post-process a catalog data that is used as 
# observations for the one-year forecasts models. It post-processes the 
# observation data in preparation for the evaluation tests of the forecasts models.
#
class OneYearModelPostProcess (PostProcess.PostProcess):
        
    # Key identifying the type of post-processing
    Type = "OneYearModel"
    
    # Magnitude threshold for the forecast models
    MinMagnitude = 4.95
    
    # Depth threshold for the forecast models
    MaxDepth = 30
    
    # Forecast duration in decimal years
    __duration = 1.0
    
    # Name of the XML forecast template file 
    ForecastTemplate = os.path.join(PostProcess.PostProcess.CenterCode, 
                                    'data',
                                    'templates', 
                                    'csep-forecast-template-M5.xml')
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    def __init__ (self, 
                  start_date,
                  end_date,
                  cumulative_start_date = None):
        """ Initialization for OneYearModelPostProcess class

            Input arguments:
            start_date - datetime object that represents forecast start date
            end_date - datetime object that represents forecast end date
            cumulative_start_date - Start date for cumulative test period as
                                    datetime.datetime object (default is None).
                                    This value is defined by entry date of the
                                    forecast model into the testing center.
        """
 
        PostProcess.PostProcess.__init__(self, 
                                         OneYearModelPostProcess.MinMagnitude,
                                         OneYearModelPostProcess.MaxDepth,
                                         OneYearModelPostProcess.__duration,
                                         xml_template = OneYearModelPostProcess.ForecastTemplate)

        # Set start date for cumulative testing period if any
        PostProcess.PostProcess.cumulativeStartDate(self, 
                                                    cumulative_start_date)

        # Set starting date for the testing period
        PostProcess.PostProcess.startDate(self, start_date)
        
        # Set expiration date for the models
        PostProcess.PostProcess.endDate(self, end_date)
        
    
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
    # Input: 
    #        test_date - datetime object that represents the test date.   
    #        raw_file - Filename for raw catalog data.
    #
    # Output:
    #        Name of the result catalog file. 
    #
    def apply (self, test_date, raw_file):
        """ Post-process catalog data in preparation for the evaluation tests
            of one-day forecasts models."""


        # Acquire reference to catalog data source class used by the framework
        data_class = DataSourceFactory.DataSourceFactory().classReference()
        
        # Import catalog data into CSEP generic format (specific to selected
        # authorized data source)
        np_catalog = data_class.importToCSEP(raw_file) 
        
        # Cut catalog according to collection area
        np_catalog = data_class.cutToArea(np_catalog,
                                          GeographicalRegions.Region.info().collectionArea)
        
        # Leave only events up to and including testing day in the catalog
        start_date = self.start_date
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
                          
        ### Cut declustered catalog according to the test area, filter events
        data_class.filter(np_catalog, 
                          GeographicalRegions.Region.info().testArea,
                          self.threshold,
                          self.files.catalog)

