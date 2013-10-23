"""
Module DataSourceProxy
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import CSEPLogging
from CatalogDataSource import CatalogDataSource


#--------------------------------------------------------------------------------
#
# DataSourceComposite
#
# This class represents an interface for composite of data sources 
# used by processing within testing framework. It was introduced to the CSEP
# testing framework to support multiple data sources by the same end-to-end
# processing. 
# 
class DataSourceComposite (CatalogDataSource, dict):


    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    # 
    def __init__ (self):
        """ Initialization for DataSourceComposite object"""

        # Can't derive from Python's dictionary since CatalogDataSource is 
        # derived from CSEPEventHandler which is derived from Python's list:
        # causes "TypeError: Error when calling the metaclass bases
        #                    multiple bases have instance lay-out conflict"
        # ===> Use BorgIdiom instead to share the state of the class: 
        # dictionary of created objects
        CatalogDataSource.__init__(self)
        dict.__init__(self, {})
        

    #----------------------------------------------------------------------------
    #
    # Extract catalog data from specified source.
    #
    # Input:
    #        test_date - Date for raw catalog data.
    #        data_dir - directory with raw data file if download_raw_data 
    #                   is set to False. Default is None.
    #
    # Output: Filename for pre-processed catalog data.
    #
    def extract (self, test_date, data_dir = None):
       """ Extract raw data from the source, and pre-process into catalog
           ZMAP format. Method arguments allow optional download and 
           pre-processing of the data."""
           
       data_file = None
       for each_source in self.values():
           data_file = each_source.extract(test_date, 
                                           data_dir)
        
       return data_file 
   

    #----------------------------------------------------------------------------
    #
    # Set search criteria for original directory of existing data products 
    # within CSEP testing framework. Use metadata for specified data product
    # to locate runtime directory with existing data products.
    #
    # Input:
    #        filenanme - Full path to the file (forecast or observation catalog)
    #                    which metadata should be used to identify runtime
    #                    directory for the file of interest.
    #        original_data_dir - Directory where files are archived.  
    #                            Default is None, which means that original files
    #                            are located under the same directory where they
    #                            should be staged.
    #
    # Output: None.
    # 
    def dirSearchCriteria (self, 
                           filename, 
                           original_data_dir = None):
       """ Set search criteria for original directory of existing data products 
            within CSEP testing framework."""

       for each_source in self.values():
           CSEPLogging.CSEPLogging.getLogger(DataSourceComposite.__name__).info("dirSearchCriteria for %s" %each_source)
           
           each_source.dirSearchCriteria(filename, 
                                         original_data_dir)
            

    #----------------------------------------------------------------------------
    #
    # Return source type as defined by the class.
    #
    # Input: None.
    #
    # Output: string representing the type of the source.
    #
    def type (self):
        """ Return string representation of the source."""

        # Raise an exception if multiple data sources are available,
        if len(self) > 1:
            error_msg = "Type is requested for more than one data source within composite: %s" \
                        %(self.keys())
                        
            CSEPLogging.CSEPLogging.getLogger(DataSourceComposite.__name__).error(error_msg)
            raise RuntimeError, error_msg

        # Raise an exception if data source is not set up
        elif len(self) == 0:
            error_msg = "Type is requested for empty data source composite, please set up specific \
authorized data source"

            CSEPLogging.CSEPLogging.getLogger(DataSourceComposite.__name__).error(error_msg)
            raise RuntimeError, error_msg

        # otherwise return type of only data source available within composite
        return self.keys()[0]
   
