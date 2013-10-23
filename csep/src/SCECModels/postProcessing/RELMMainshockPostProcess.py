"""
Module RELMMainshockPostProcess
"""

__version__ = "$Revision: 3430 $"
__revision__ = "$Id: RELMMainshockPostProcess.py 3430 2011-08-09 05:43:18Z liukis $"


import os, datetime, operator

import CSEPFile, PostProcess, CSEP, Environment, \
       GeographicalRegions
from DataSourceFactory import DataSourceFactory       


#--------------------------------------------------------------------------------
#
# RELMMainshockPostProcess.
#
# This class is designed to post-process a catalog data that is used as observations for 
# the RELM 5-year mainshock models. It post-processes the observation data in preparation
# for the evaluation tests of the forecasts models.
#
class RELMMainshockPostProcess (PostProcess.PostProcess):
        
    # Key identifying the type of post-processing
    Type = "RELMMainshock"
    
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
                        end_date = datetime.datetime(2011, 1, 1)):
        """ Initialization for RELMMainshockPostProcess class.
        
            Input arguments:
            start_date - datetime object that represents forecast start date
                         (default is datetime(2006, 1, 1))
            end_date - datetime object that represents forecast end date
                       (default is datetime(2011, 1, 1))
        """
 
        PostProcess.PostProcess.__init__(self, 
                                         RELMMainshockPostProcess.MinMagnitude,
                                         RELMMainshockPostProcess.MaxDepth,
                                         RELMMainshockPostProcess.__duration,
                                         PostProcess.PostProcess.Files(CSEP.Catalog.Filename.Declustered,
                                                                       cumulative_catalog = None),
                                         RELMMainshockPostProcess.ForecastTemplate)

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
            RELM five-year mainshock models."""
        

        # Acquire reference to catalog data source class used by the framework
        data_class = DataSourceFactory().classReference()
        
        # Import catalog data into Matlab format
        np_catalog = data_class.importToCSEP(raw_file)
        
        # Cut catalog according to collection area
        np_catalog = data_class.cutToArea(np_catalog,
                                          GeographicalRegions.Region.info().collectionArea) 
        
        # Cut according to last testing day
        start_date = DataSourceFactory().object(data_class.Type,
                                                isObjReference = True).StartDate  # download start date
        end_date = test_date + datetime.timedelta(hours=24)
        
        np_catalog = data_class.cutToTimePeriod(np_catalog, 
                                                start_date, end_date,
                                                result_file = 'cut_to_time',
                                                stop_time_sign = operator.lt)

        ### Decluster catalog
        np_catalog, np_suppl_catalog, \
        indep_probability_file = data_class.declusterReasenberg(np_catalog) 

        # Register reproducibility file
        info = "'%s' random seed used by de-cluster algorithm in '%s' post-processing." \
               %(CSEP.Catalog.Filename.DeclusterParameter, 
                 self.Type)
               
        PostProcess.PostProcess.add(self,
                                    CSEP.Catalog.Filename.DeclusterParameter,
                                    info,
                                    CSEPFile.Format.ASCII)

        # Second catalog generated by declustering algorithm - original catalog
        # with supplemental independence probability column
        info = "'%s' original catalog with supplemental independence probability \
column introduced by Reasenberg declustering algorithm for '%s' post-processing." \
               %(indep_probability_file, 
                 self.Type)
               
        PostProcess.PostProcess.add(self,
                                    indep_probability_file,
                                    info,
                                    CSEPFile.Format.ASCII)
        
        ### Apply uncertainties to catalog
        # Kludgy way of specifying column index into the data - nothing to
        # do about it while still using Matlab code. 
        result_dir = data_class.modifications(np_suppl_catalog, 
                                              GeographicalRegions.Region.info().testArea,
                                              self.threshold,
                                              self.files.uncertainties,
                                              probability_column = 15)
 
        PostProcess.PostProcess.registerUncertaintiesDir(self,
                                                         result_dir)

        ### Cut declustered catalog according to the test area, filter events
        data_class.filter(np_catalog, 
                          GeographicalRegions.Region.info().testArea,
                          self.threshold,
                          self.files.catalog)

        ### Cut catalog with supplemental independence probability according to 
        #   the test area, filter events
        filtered_indep_probability_file = "decluster_indep_probability_filtered.dat"
        
        data_class.filter(np_suppl_catalog, 
                          GeographicalRegions.Region.info().testArea,
                          self.threshold,
                          filtered_indep_probability_file)

        info = "Filtered '%s' original catalog with supplemental independence \
probability column for '%s' post-processing." %(indep_probability_file, 
                                                self.Type)
               
        PostProcess.PostProcess.add(self,
                                    filtered_indep_probability_file,
                                    info,
                                    CSEPFile.Format.ASCII)

