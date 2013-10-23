"""
Module OneDayModelDeclusInputPostProcess
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import operator, os, datetime
import numpy as np

import PostProcess, GeographicalRegions, CSEP, CSEPGeneric, CSEPFile, CSEPLogging
from DataSourceFactory import DataSourceFactory


#--------------------------------------------------------------------------------
#
# OneDayModelInputPostProcess.
#
# This class is designed to post-process a catalog data that is used as an input for 
# the one day short-term forecasts models. It post-processes the observation data in 
# preparation for the forecast generation.
#
class OneDayModelDeclusInputPostProcess (PostProcess.PostProcess):
        
    # Key identifying the type of post-processing
    Type = "OneDayModelDeclusInput"
    
    # Magnitude threshold for the forecast models
    MinMagnitude = 3.95
    
    # Depth threshold for the forecast models
    MaxDepth = 30
    
    Logger = CSEPLogging.CSEPLogging.getLogger(__name__)
    
    # This is written with NZTC functionality in mind since only NSHMBGOneYear model
    # is using it
    __catalogSplitDate = datetime.datetime(1963, 1, 1)
    __numYearsForCatalogOverlap = 10.0 
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None
    # 
    def __init__ (self):
        """ Initialization for OneDayModelDeclusInputPostProcess class"""
 
        PostProcess.PostProcess.__init__(self, 
                                         OneDayModelDeclusInputPostProcess.MinMagnitude,
                                         OneDayModelDeclusInputPostProcess.MaxDepth,
                                         catalogs = PostProcess.PostProcess.Files("OneDayModelDeclusInputCatalog.dat",
                                                                                  None,
                                                                                  None))

    
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
        
        if CSEP.Catalog.NumDeclusterSimulations:
            # Decluster simulations are not supported for input catalog,
            # raise an exception
            error_msg = "Can not specify decluster simulations for input catalog that is declustered in chunks"
            OneDayModelDeclusInputPostProcess.Logger.error(error_msg)
            
            raise RuntimeError, error_msg
        
            
        # Acquire reference to catalog data source class used by the framework
        print "Values=", DataSourceFactory.composite().values()
        
        for each_source in DataSourceFactory.composite().values():
                        
            data_class = DataSourceFactory().classReference(each_source.type())

            # Import catalog data into Matlab format
            np_catalog = data_class.importToCSEP(raw_file)
            
            # Cut catalog according to collection area
            np_catalog = data_class.cutToArea(np_catalog,
                                              GeographicalRegions.Region.info().collectionArea)
            
            # Cut catalog excluding the testing day
            start_date_pre = DataSourceFactory().object(data_class.Type,
                                                        isObjReference = True).StartDate  # download start date
                                                    
            # Since there is Y2K problem with declustering code, 
            # need to decluster in chunks of less than 100 years and concatenate
            # catalogs
            end_date_pre = OneDayModelDeclusInputPostProcess.__catalogSplitDate
            
            # Decluster initial chunk of input catalog
            np_catalog_pre = data_class.cutToTimePeriod(np_catalog, 
                                                        start_date_pre, end_date_pre, 
                                                        stop_time_sign = operator.lt)
            
            np_catalog_pre, np_suppl_catalog_pre, \
            indep_probability_file_pre = data_class.declusterReasenberg(np_catalog_pre) 
            
            # Rename declustering files after 1st chunk to guarantee that new ones will b
            # generated by declustering of the next chunk
            cleanup_file = 'hypo71Catalog.dat'
            os.rename(cleanup_file, "pre1963" + cleanup_file)
            
            # Go back 98 years from catalog end date to Jan 1
            start_date = datetime.datetime(test_date.year - 98,
                                           1,
                                           1)
            end_date = test_date
            
            if start_date > OneDayModelDeclusInputPostProcess.__catalogSplitDate:
                error_msg = "There is a gap in catalogs that should overlap: split date = %s vs. start date of last 98 years of catalog = %s" \
                            %(OneDayModelDeclusInputPostProcess.__catalogSplitDate,
                              start_date)
                OneDayModelDeclusInputPostProcess.Logger.error(error_msg)
                raise RuntimeError, error_msg

            np_catalog = data_class.cutToTimePeriod(np_catalog, 
                                                    start_date, end_date, 
                                                    stop_time_sign = operator.lt)
                  
            ### Decluster catalog: since Fortran code is not Y2K compatible, can only pass
            ### 100 years of catalog, treat pre-100 years of data as declustered
            ### catalog 
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

            # Merge catalogs at second chunk + 10 years
            join_date = datetime.datetime(start_date.year + 10,
                                          1,
                                          1)
            
            np_catalog_pre = data_class.cutToTimePeriod(np_catalog_pre, 
                                                        start_date_pre, join_date, 
                                                        stop_time_sign = operator.lt)
            
            np_catalog = data_class.cutToTimePeriod(np_catalog, 
                                                    join_date, test_date, 
                                                    stop_time_sign = operator.lt)
            
            
            np_catalog_pre = np.append(np_catalog_pre,
                                       np_catalog,
                                       axis = 0)
    
            CSEPGeneric._write_catalog(self.files.catalog,
                                       np_catalog_pre)
            
