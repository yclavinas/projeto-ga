"""
Module CSEPStorage
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os, glob, pysvn

from CSEPPropertyFile import CSEPPropertyFile
import CSEPLogging


#--------------------------------------------------------------------------------
#
# CSEPStorage.
#
# This class represents an interface for staging of the data required by a
# specific processing step within CSEP. The class is responsible for staging
# requested data if it's already exists within the system, or reporting of 
# missing data if it does not.
# 
class CSEPStorage (object):

    # Static data of the class
    
    # Logger for the class
    __logger = None
    
    # Flag if staging of existing data products is allowed. Default is True.
    __allowStaging = True


    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #
    #        stage_data_dir - Directory where the files should be staged.
    #                         Default is current directory.
    #        original_data_dir - Directory where files are archived.  
    #                            Default is None, which means that original files
    #                            are located under the same directory where they
    #                            should be staged.
    # 
    def __init__ (self, 
                  stage_data_dir = '.',
                  original_data_dir = None):
        """ Initialization for CSEPStorage class"""

        if CSEPStorage.__logger is None:
           CSEPStorage.__logger = CSEPLogging.CSEPLogging.getLogger(CSEPStorage.__name__)
           
        self.__stageDir = stage_data_dir
        self.__dir = original_data_dir
        
        # If data was staged based on SVN tag, capture the tag
        self.__SVNTag = None
        
        # Use staging data directory for archive data search if directory is not
        # provided
        if self.__dir is None:
           self.__dir = self.__stageDir
           
        if (os.path.exists(self.__stageDir) is False):
           CSEPStorage.__logger.info("Creating directory '%s'..." %self.__stageDir)

           os.makedirs(self.__stageDir)
        
        # Search criteria to determine a directory where original data is stored
        # (self.__dir)
        # In a case when requested file should be staged (raw catalog file) 
        # based on metadata of existing data product (forecast file or 
        # observation catalog), the filename of such existing data product is 
        # specified. Based on metadata file of that data product, run-time
        # directory is extracted which stores already downloaded raw catalog as
        # it was used to create specified data product (forecast or observation
        # catalog). The raw catalog that is stored in found run-time directory 
        # is staged for the current process then.
        self.__dirSearchCriteria = {}
           

    #----------------------------------------------------------------------------
    #
    # Set flag that enables staging of existing data products within CSEP
    # testing framework.
    #
    # Input:
    #        allow_staging - Flag if set to True is to allow staging of existing
    #                        data products, False - otherwise. 
    #
    # Output: None.
    # 
    @staticmethod
    def allowStaging (allow_staging):
        """ Set flag that enables/disables staging of existing data products 
            within testing framework."""
            
        CSEPStorage.__allowStaging = allow_staging
     
     
    #--------------------------------------------------------------------------- 
    def __getSVNTag (self):
        """Get SVN tag that was used to stage raw data."""
           
        return self.__SVNTag
    
    SVNTag = property(__getSVNTag,
                      doc = 'SVN repository tag for staged raw data.')
     

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
            
            
        self.__dirSearchCriteria[filename] = original_data_dir

        CSEPStorage.__logger.info("dirSearchCriteria(%s): updated to %s" 
                                  %(self, self.__dirSearchCriteria)) 
        
        
    #----------------------------------------------------------------------------
    #
    # Stage specified files if such have been archived before.
    #
    # Input:
    #        file_list - List of original filenames that should exist under the 
    #                    staging directory.
    #        data_dir - Optional directory for original data files. Default is 
    #                   None.
    #
    # Output:
    #
    #        True if all files have been staged, False otherwise.
    # 
    def stage (self, 
               file_list, 
               data_dir = None):
       """ Stage specified files if such have been created and archived some 
           time in the past. This method
           searches for metadata files under staging directory, and creates
           soft links to the corresponding archived files if such exist under 
           the same directory. It uses latest created files if there are 
           multiple archived copies of the same file."""
       
       
       # Check if specified files already exist under staging directory
       files_exist = True
       
       # List of file entries (without a path) to stage
       search_entries = []
       for entry_path in file_list:
           entry_dir, entry = os.path.split(entry_path)
           
           search_entries.append(entry)
           
           # If full path is provided for the file of interest,
           # reset staging directory
           if len(entry_dir) != 0:
               self.__stageDir = entry_dir
               
           files_exist = files_exist and os.path.exists(os.path.join(self.__stageDir,
                                                                     entry))

       # Requested files already exist
       if files_exist is True:
          CSEPStorage.__logger.info("stage(): Requested files '%s' exist" 
                                    %file_list)
          
          return True


       # If files don't exist, check if staging of existing ("archived") files
       # is allowed  
       if CSEPStorage.__allowStaging is False:
           
          if len(self.__dirSearchCriteria) == 0:         
              
              # search criteria is not provided
              return False
          
          else:
              
              # If search criteria is provided, try to identify runtime directory that
              # corresponds to the criteria file: found runtime directory will
              # be used as original data directory for archived file of interest
              # that will be staged
              for each_criteria, each_dir in self.__dirSearchCriteria.items():
                  
                  if self.__traceDir(each_criteria, each_dir) is True:
                      
                      break
              
       
       if data_dir is not None:
          self.__dir = data_dir
          

       # Try to stage files based on archived filenames
       all_staged = self.__stageByFilename(search_entries)       
       
       if all_staged is False:
          
          # Try to stage files based on archived metadata filenames
          all_staged = self.__stageByMetadata(search_entries)       
          
       return all_staged


    #----------------------------------------------------------------------------
    #
    # Trace down a runtime directory for specified file based on information 
    # found in corresponding metadata file.
    #
    # Input: 
    #        search_criteria - Full path to the file (forecast or observation catalog)
    #                    which metadata should be used to identify runtime
    #                    directory for the file of interest.
    #        search_dir - Directory with original data files.
    #
    # Output:
    #        True if runtime directory was identified, False otherwise
    # 
    def __traceDir (self, search_criteria, search_dir): 
       """ Trace down a runtime directory for specified file based on information 
           found in corresponding metadata file."""


       criteria_path, criteria_name = os.path.split(search_criteria)
       
       if search_dir is not None:
           self.__dir = search_dir
           
       CSEPStorage.__logger.info("Original data dir %s" %self.__dir)
           
       # Collect available metadata files
       meta_files, meta_dates = self.__getMetadata()

       for same_date_metas in [meta_files[key] for key in meta_dates]:
          
          # Iterate though all metadata files with the same time stamp
          for meta_obj in same_date_metas:
             
#             print "DEBUG:", meta_obj.print_info()
             
             # Extract original data filename that metadata file corresponds to
             found_path, found_name = os.path.split(meta_obj.originalDataFilename)
             if found_name == criteria_name:
                
                # Check if file is a link to other existing data file
                while meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword] is not None:
                   
                   # Extract information from metadata file that represents "linked" data file
                   # current metadata file refers to
                   CSEPStorage.__logger.info("__traceDir(): %s metafile for %s contains a link to %s" 
                                             %(meta_obj.file, meta_obj.originalDataFilename,
                                               meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]))
                   
                   link_datafile = meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]
                                   
                   meta_obj = CSEPPropertyFile.Metadata(link_datafile + CSEPPropertyFile.Metadata.Extension) 

                # Report resolved runtime directory 
                CSEPStorage.__logger.info("__traceDir(): identified runtime directory %s for %s" 
                                          %(meta_obj.dispatcherRuntimeDir,
                                            search_criteria))
                
                self.__dir = meta_obj.dispatcherRuntimeDir
                return True
       
       return False
   

    #----------------------------------------------------------------------------
    #
    # Collect information about available metadata files
    #
    # Input: None
    #
    # Output: Tuple of metadata files and sorted date keys that correspond
    #         to these metadata files 
    # 
    def __getMetadata (self,
                       search_dir = None): 
       """ Collect information about available metadata files."""

       
       dir_to_search = search_dir
       if dir_to_search is None:
           dir_to_search = self.__dir
           
       ### Search for metadata files - latest created are checked first
       meta_files = glob.glob('%s/*%s' %(dir_to_search,
                                         CSEPPropertyFile.Metadata.Extension))
       
       if len(meta_files) == 0:

          CSEPStorage.__logger.info("__getMetadata(): no metadata files found under %s directory" 
                                    %dir_to_search)
          
       
       # Create time-to-file map of existing metadata files
       meta_dates = {}
       for each_file in meta_files:

          meta_obj = CSEPPropertyFile.Metadata(each_file)
          meta_dates.setdefault(meta_obj.info[CSEPPropertyFile.Metadata.DateKeyword], 
                                []).append(meta_obj)
          
       
       # Traverse metadata files in reverse order
       dates = meta_dates.keys()
       dates.sort(reverse=True)
       
       return (meta_dates, dates)
       

    #----------------------------------------------------------------------------
    #
    # Stage specified files based on information found in metadata files.
    #
    # Input:
    #        file_list - List of original filenames that should exist under the 
    #                    staging directory.
    #
    # Output:
    #        True if all files have been staged, False otherwise.
    # 
    def __stageByMetadata (self, 
                           file_list):
       """ Stage specified files if such have been created and archived some 
           time in the past. Perform the search for original files based on
           corresponding metadata files if any."""

       
       ### Search for metadata files - latest created are checked first
       meta_dates, dates = self.__getMetadata()
       if len(meta_dates) == 0:
           return False

       # Dictionary of requested file and file that has been staged
       staged_files = {}

       # All staged files should be generated by the same instance of Dispatcher
       dispatcher_dir = None
       
       for same_date_metas in [meta_dates[key] for key in dates]:
          
          # Iterate though all metadata files with the same time stamp
          for meta_obj in same_date_metas:
             
             # DEBUG: meta_obj.info()
             # Sometimes original filename includes full path to it
             meta_path, meta_file = os.path.split(meta_obj.originalDataFilename)
             
             # Extract original data filename that metadata file corresponds to
             if meta_file in file_list:
                
                # Check if file has been already staged
                if meta_file in staged_files:
                   continue
                
                # All files have to be generated by the same instance of Dispatcher,
                # remember dispatcher instance from very first staged file
                if dispatcher_dir is None:
                   dispatcher_dir = meta_obj.dispatcherRuntimeDir
                   
                if dispatcher_dir != meta_obj.dispatcherRuntimeDir:
                   continue
                
                staged_files[meta_file] = os.path.join(self.__stageDir, 
                                                       meta_file)

                #===============================================================
                # Identify original file to create a soft link to  
                #===============================================================
                original_file = meta_obj.info[CSEPPropertyFile.Metadata.DataFileKeyword]
                
                
                ### Check if file metadata contains a link to SVN working copy
                ### Can stage the file only if:
                #     1) SVN tag is provided in metadata file
                #     2) SVN tag with runtime directory timestamp exists in SVN
                if meta_obj.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:
                    ### Checkout copy from SVN
                    self.__SVNTag = meta_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]
                    
                    CSEPStorage.__logger.info("__stageByMetadata(): %s metafile for %s contains SVN tag %s, exporting the copy to %s directory" 
                                             %(meta_obj.file, 
                                               meta_file,
                                               self.__SVNTag,
                                               self.__stageDir))
                    
                    pysvn.Client().export(os.path.join(self.__SVNTag, meta_file),
                                          os.path.join(self.__stageDir, meta_file),
                                          recurse = False) # have to specify to export only one file
                    
                    continue
                

                # Check if file is a link to other existing data file  
                elif meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword] is not None:
                   
                   # Extract information from metadata file that represents "linked" data file
                   # current metadata file refers to
                   CSEPStorage.__logger.info("__stageByMetadata(): %s metafile for %s contains a link to %s" 
                                             %(meta_obj.file, 
                                               meta_obj.originalDataFilename,
                                               meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]))
                   
                   # Link information provides a full path to original filename
                   original_file = meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]


                   #============================================================
                   # If original file has been archived in SVN repository,
                   # it does not exist anymore ===> need to check for metadata
                   # files under original directory 
                   #============================================================
                   if not os.path.exists(original_file):
                        
                       # Check for metadata file to correspond to the data file
                       original_meta_file = original_file + CSEPPropertyFile.Metadata.Extension
                       
                       # If it does not exist, search all metadata files for 
                       # the one corresponding to the file of interest
                       if not os.path.exists(original_meta_file):
                           # Search metadata files under original directory that 
                           # corresponds to original data file
                           original_path, original_data = os.path.split(original_file)
                           
                           CSEPStorage.__logger.info("__stageByMetadata(): metadata file %s does not exist, trying to locate corresponding to %s metadata files in %s" 
                                                     %(original_meta_file,
                                                       meta_file,
                                                       original_path))
                       
                           original_file_meta_dates, original_file_dates = self.__getMetadata(original_path)
                    
                           # Metadata files are sorted by date: list of meta files
                           for all_original_meta_files in [original_file_meta_dates[key] for key in original_file_dates]:
                               
                               for each_original_meta_file in all_original_meta_files:
                                   __meta_path, __meta_file = os.path.split(each_original_meta_file.originalDataFilename)
                                   
                                   # Found the one to correspond to the file of interest
                                   if __meta_file == meta_file:
                                       original_file = each_original_meta_file.info[CSEPPropertyFile.Metadata.DataFileKeyword]
                                       original_meta_file = each_original_meta_file.file
                                       break

                       # Check out the file if it's stored in SVN
                       original_meta = CSEPPropertyFile.Metadata(original_meta_file)
                       if original_meta.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:
                            ### Checkout copy from SVN
                            self.__SVNTag = original_meta.info[CSEPPropertyFile.Metadata.SVNKeyword]
                            
                            CSEPStorage.__logger.info("__stageByMetadata(): %s metafile for %s contains SVN tag %s, exporting the copy to %s directory" 
                                                     %(original_meta.file, 
                                                       meta_file,
                                                       self.__SVNTag,
                                                       self.__stageDir))
                            
                            pysvn.Client().export(os.path.join(self.__SVNTag, meta_file),
                                                  os.path.join(self.__stageDir, meta_file),
                                                  recurse = False) # have to specify to export only one file
                            continue
                   
                # Stage the file
                CSEPStorage.__logger.info("__stageByMetadata(): creating '%s' link to original '%s' entry" 
                                          %(staged_files[meta_file],
                                            original_file))
                
                # if full path to original filename is not given, 
                # prepend directory the file is staged from
                if os.path.isabs(original_file) is False and self.__dir is not None:
                    original_file = os.path.join(self.__dir,
                                                 original_file)
                    
                os.symlink(original_file,
                           os.path.join(self.__stageDir, 
                                        meta_file))
             
       return self.__allStaged(staged_files,
                               file_list,
                               '__stageByMetadata')


    #----------------------------------------------------------------------------
    #
    # Stage specified files based on original filenames.
    #
    # Input:
    #        file_list - List of original filenames that should exist under the 
    #                    staging directory.
    #
    # Output:
    #        True if all files have been staged, False otherwise.
    # 
    def __stageByFilename (self, 
                           file_list):
       """ Stage specified files if such have been created and archived some 
           time in the past. Perform the search for original files based on
           archived filenames if any."""


       # Dictionary of requested file and file that has been staged
       staged_files = {}
    
       ### Search for files under archive dir
       for entry in file_list:
    
          found_files = glob.glob(os.path.join(self.__dir,
                                               entry))
    
          if len(found_files):
             
             # Found the file, create a symbolic link to it
             CSEPStorage.__logger.info("__stageByFilename(): creating '%s' link to original '%s' entry in '%s'" 
                                       %(os.path.join(self.__stageDir, entry),
                                         found_files[0],
                                         self.__dir))
                
             
             os.symlink(found_files[0],
                        os.path.join(self.__stageDir, entry))
                
             staged_files[entry] = os.path.join(self.__stageDir, entry)

             
       return self.__allStaged(staged_files,
                               file_list, 
                               '__stageByFilename')


    #----------------------------------------------------------------------------
    #
    # Check if all requested files have been staged, clean up staged files if 
    # only some of them have been staged.
    #
    # Input:
    #        staged_files - Dictionary of staged filenames to clean up
    #        file_list - List of original filenames that should exist under the 
    #                    staging directory.    
    #        method_name - Caller method
    #
    # Output: True if all files have been staged, False otherwise.
    #
    def __allStaged (self,
                     staged_files,
                     file_list, 
                     method_name):
       """ Check if all requested files have been staged, remove partially 
           staged files."""

       # If some files have been staged, those must be part of "optional" files
       if len(staged_files) != len(file_list):
          
          CSEPStorage.__logger.info("__allStaged(%s): Not all files have been \
staged %s (in %s directory) vs. required %s (from %s directory)" %(method_name,
                                                                   staged_files,
                                                                   self.__stageDir,
                                                                   file_list, 
                                                                   self.__dir))
          
          return False
       
       else:
          # All files have been staged
          return True
       
          
# Invoke the module
if __name__ == '__main__':

   import EvaluationTestOptionParser
   import CSEPOptionParser

   parser = EvaluationTestOptionParser.EvaluationTestOptionParser()
        
   # List of requred options
   options = parser.options()
   
   storage = CSEPStorage(options.test_dir)

   # Only for testing
   #storage.stage(['catalog.nodecl.mat', 
   #               'catalog.nodecl.dat', 
   #               'catalog.modifications.mat'])
   
   