"""
Utility to validate existing observation catalogs for one-day forecasts groups.  
Due to time interval filtering problem described in Trac ticket #187, some
CMT-based observation catalogs for one-day forecasts may include qualified 
events from the day following the test date (see Global/one-day-models- 
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, datetime, glob, sys, time
import CSEPFile, CSEP, CSEPLogging
from CSEPPropertyFile import CSEPPropertyFile
from RELMCatalog import RELMCatalog


#--------------------------------------------------------------------------------
#
# ObservationCatalogs
#
# This module is designed to extract dates for existing observation catalogs
# for one-day forecasts and verify validity of these events (see Trac ticket 187
# for the description of the problem) 
#
class ObservationCatalogs (object):

    # Static data members

    # Logger for the class
    __logger = None
   
    
    #===============================================================================
    # Constructor for RestoreMetadata class
    #
    # Inputs:
    #         dirpath - Directory path to model files.
    #
    #===============================================================================
    def __init__ (self, dirpath):
        """ Initialize ObservationCatalogs class."""
   
        if ObservationCatalogs.__logger is None:
           ObservationCatalogs.__logger = CSEPLogging.CSEPLogging.getLogger(ObservationCatalogs.__name__)
           
   
        # Find test dates sub-directories within specified directory
        self.__dir = dirpath
        self.__catalogs = os.listdir(dirpath)
         
        if len(self.__catalogs) == 0:
            raise RuntimeError, "Specified '%s' directory is empty" %dirpath  
        
        
    #================================================================================
    #  validate
    # 
    # Inputs: None
    #================================================================================
    def validate (self):
        """Verify that existing observation catalogs contain events for corresponding \
test dates."""


        for each_path in self.__catalogs:
            
            dir_path = os.path.join(self.__dir, each_path)
            ObservationCatalogs.__logger.info("Processing %s" %each_path)
            

            # Catalog directory for each test date follows 'YYYY-MM-DD' format
            dir_test_date = datetime.datetime.strptime(each_path,  '%Y-%m-%d')
         
            # Collect metadata files for existing observation catalogs
            meta_files = glob.glob('%s/*%s' %(dir_path,
                                              CSEPPropertyFile.Metadata.Extension))
            if len(meta_files) == 0:
    
               ObservationCatalogs.__logger.info("__getMetadata(): no metadata files found under %s directory" 
                                                 %dir_path)

             
            # Create time-to-file map of existing metadata files
            meta_dates = {}
            for each_file in meta_files:
    
               meta_obj = CSEPPropertyFile.Metadata(each_file)
               meta_dates.setdefault(meta_obj.info[CSEPPropertyFile.Metadata.DateKeyword], 
                                     []).append(meta_obj)
              
           
            # Traverse metadata files in reverse order - newest will be listed first
            dates = meta_dates.keys()
            dates.sort(reverse=True)
            ObservationCatalogs.__logger.info('===>Metadata files dates: %s' %dates) 

            # Examine only latest observation catalog:
            for each_meta in meta_dates[dates[0]]:
                
                if 'catalog.nodecl.mat' in each_meta.originalDataFilename:

                    ObservationCatalogs.__logger.info("===>Loading %s meta for %s" %(each_meta.file,
                                                                                     each_meta.originalDataFilename))
                    
                    # Load catalog in
                    catalog = RELMCatalog.load(each_meta.info[CSEPPropertyFile.Metadata.DataFileKeyword])
                    
                    # Extract date of each event in the catalog:
                    num_rows, num_cols = catalog.shape
        
                    # Catalog is non-empty
                    if num_rows > 0:

                        for each_row in xrange(0, num_rows):
                            
                            # Create datetime object for event date and time
                            event_date = datetime.datetime(int(catalog[each_row, CSEPGeneric.Catalog.ZMAPFormat.DecimalYear]),
                                                           int(catalog[each_row, CSEPGeneric.Catalog.ZMAPFormat.Month]),
                                                           int(catalog[each_row, CSEPGeneric.Catalog.ZMAPFormat.Day]))
                        if event_date != dir_test_date: 
                           ObservationCatalogs.__logger.error("!!!Unexpected date %s found in catalog for %s" %(event_date,
                                                                                                                dir_test_date))

                else:
                    ObservationCatalogs.__logger.info("===>Skipping %s meta for %s" %(each_meta.file,
                                                                                      each_meta.originalDataFilename))


# Invoke the module
if __name__ == '__main__':


    import optparse
    
    
    command_options = optparse.OptionParser()
    
    command_options.add_option('--catalogDir',
                               dest='catalog_dir',
                               default=None,
                               help="Top-level directory with observations catalogs files")

    (values, args) = command_options.parse_args()

    observations = ObservationCatalogs(values.catalog_dir)
    observations.validate()    
