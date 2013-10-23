"""
Utility to archive raw catalogs that have been downloaded by testing framework 

"""

import os, glob, datetime, calendar, shutil

import CSEPFile, ANSSDataSource, CMTDataSource, CSEP
from CatalogDataSource import CatalogDataSource
from CSEPPropertyFile import CSEPPropertyFile
from DataSourceFactory import DataSourceFactory
from CSEPLogging import CSEPLogging


# Class to locate existing raw catalog files and to archive them in SVN repository
class CatalogFiles:

   # Search file system for all dates within [StartDate, NowDate] interval
   # Initialize tags directory with import_raw.dat as downloaded on 2007/08/31 manually
   StartDate = datetime.datetime(2007, 9, 1)
   #NowDate = datetime.datetime.now()
   NowDate = datetime.datetime(2007, 10, 1)

   DataSourceType = ANSSDataSource.ANSSDataSource.Type
   
   __dryRun = True
  
   __pidPattern = 'pid_*'
   __runtimeDirFormatString = "%Y%m%d%H%M%S"
   
   __topDirSeparator = ':'
    
   # If start date of raw catalog can't be learned from the file (file contains
   # earlier events (1976) than catalog start date (1977) for CMT)
   __catalogStartDate = {CMTDataSource.CMTDataSource.Type: 1977}
   

   def __init__ (self):

       # Open file to keep track of which raw catalogs need to be removed
       self.__filesToRemoveHandle = CSEPFile.openFile(CatalogFiles.DataSourceType + 'ToRemove%s_%s.txt' %(CatalogFiles.StartDate.date(),
                                                                                                          CatalogFiles.NowDate.date()),
                                                      CSEPFile.Mode.WRITE)

       
   def __del__ (self):
       self.__filesToRemoveHandle.close()
       
   
   def commit (self,
               top_dir, 
               dry_run):        # dry run: don't actually archive the files 
     """ Search file system for directories with raw catalogs - step through defined
         date interval [StartDate; NowDate]."""

     self.__dryRun = dry_run
     
     all_top_dirs = top_dir.split(CatalogFiles.__topDirSeparator)
     
     all_days_calendar = calendar.Calendar()
     start_month = CatalogFiles.StartDate.month
     
     for each_year in xrange(CatalogFiles.StartDate.year, CatalogFiles.NowDate.year + 1):
         
         if each_year != CatalogFiles.StartDate.year:
             start_month = 1

         for each_month in xrange(start_month, 13):

             all_days = [d for d in all_days_calendar.itermonthdays(each_year, 
                                                                    each_month) if d != 0]
             
             if each_year == CatalogFiles.StartDate.year and \
                each_month == CatalogFiles.StartDate.month:
                 # Start from specified day of start month
                 all_days = filter(lambda x: x>= CatalogFiles.StartDate.day, 
                                   all_days)
             
             # Find directories that correspond to the day
             for each_day in all_days:
                 
                 # Dictionary to keep runtime directories organized by test date and time
                 date_dirs = {}
                 test_date = datetime.datetime(each_year,
                                               each_month,
                                               each_day)
                 
                 # Don't continue if test date passed the interval of interest
                 if test_date > CatalogFiles.NowDate:
                     break
             
                 for each_top_dir in all_top_dirs:
                     # Support nested directory structure introduced later in CSEP to
                     # organize data by year_month and pid:
                     # time.strftime("%Y_%m"),
                     # time.strftime("%Y%m%d%H%M%S"),
                     # 'pid_%s' %os.getpid()))
                     # At some point Dispatcher runtime directories became organized by YYYY_MM folders
                     # to avoid too many files under the same directory 
                     month_directory = os.path.join(each_top_dir,
                                                    test_date.strftime("%Y_%m"))
                     if os.path.exists(month_directory) is False:
                         # Search for runtime directory under there
                         month_directory = None
            
                     # ATTN: test date may not be under YYYY_MM sub-directory if switch happened
                     # in a middle of the month, so first check for runtime directory directly
                     # under top level directory 
                     runtime_dirs = glob.glob(os.path.join(each_top_dir,
                                                           "%s*" %test_date.strftime("%Y%m%d")))
                     
                     if len(runtime_dirs) == 0:
                         # Check if directories exist under YYYY_MM folder
                         if month_directory is not None:
                             runtime_dirs = glob.glob(os.path.join(month_directory,
                                                                   "%s*" %test_date.strftime("%Y%m%d")))
                             
                     if len(runtime_dirs) == 0:
                         
                         CSEPLogging.getLogger(__name__).warning("No runtime directories are found for %s under %s" %(test_date,
                                                                                                                      each_top_dir))
                         continue
                     
                     # Found directories that correspond to the processing date
                     for each_dir in runtime_dirs:
                         dir_path, dir_name = os.path.split(each_dir)
                         
                         # Extract datetime stamp from the name
    #                     dir_date = datetime.datetime.strptime(dir_name,
    #                                                           CatalogFiles.__runtimeDirFormatString)
                         
                         # At some point CSEP added "pid_*" subdirectory to store
                         # raw catalogs to - to prevent multiple processes using
                         # the same runtime directory
                         pid_dirs = glob.glob(os.path.join(each_dir,
                                                           CatalogFiles.__pidPattern))
                         for each_pid in pid_dirs:
                             date_dirs.setdefault(dir_name, []).append(each_pid)
    
                         # If no pid sub-directories exist, just append runtime directory
                         # named after date-time stamp
                         if len(pid_dirs) == 0:
                             date_dirs.setdefault(dir_name, []).append(each_dir)

                 
                 ### Check for raw catalog existence under each runtime directory
                 # ATTN: Some runtime directories won't have raw catalog files
                 for each_date in sorted(date_dirs.keys()):
                     
                     for each_dir in date_dirs[each_date]:

                         start_year, raw_catalog, is_archived = self.catalogStartYear(each_dir)
                         
                         if raw_catalog is None:
                             # Raw catalog is not present in runtime directory
                             CSEPLogging.getLogger(__name__).warning("===>No catalog is found for %s under %s" %(each_date,
                                                                                                                 each_dir))

                         else:

                             CSEPLogging.getLogger(__name__).info("+++>Catalog %s starts with %s" %(raw_catalog,
                                                                                                    start_year))
                             
                             if dry_run is False and \
                                is_archived is None: 
                                 # Commit catalog to SVN and tag with directory's name (datetime stamp)
                                 data_source = DataSourceFactory().object(CatalogFiles.DataSourceType,
                                                                          [datetime.date(start_year, 1, 1)])
                                 data_source.SVN.mainBranch('import') 
                                 data_source.SVN.setTag(each_date)
                                 tag_url = data_source.SVN.tagURL()
                                 
                                 # Copy file to working copy
                                 shutil.copyfile(raw_catalog, 
                                                 os.path.join(data_source.SVN.workingCopyDir(),
                                                              CatalogDataSource._RawFile))
                                 
                                 data_source.SVN.commit("Archiving original %s file" %raw_catalog)
                                 
                                 # Update metadata with SVN tag
                                 meta_file = raw_catalog + CSEPPropertyFile.Metadata.Extension
                                 
                                 
                                 if os.path.exists(meta_file) is False:
                                     
                                     # Metadata does not exist for raw catalog,
                                     # create it
                                     CSEPLogging.getLogger(__name__).warning("!!!Creating metadata file %s for raw catalog to correspond to %s SVN tag" %(meta_file,
                                                                                                                                                       tag_url))
                                     CSEPPropertyFile.createMetafile(meta_file, 
                                                                     raw_catalog,
                                                                     CSEPFile.Format.ASCII,
                                                                     "Raw catalog as archived on %s" %datetime.datetime.now(),
                                                                     raw_catalog,
                                                                     in_svn = True,
                                                                     svn_tag = tag_url)
             
                                 else:
                                     CSEPLogging.getLogger(__name__).info("+++Updating metadata file %s with SVN tag %s" %(meta_file,
                                                                                                                           tag_url))
                                     fhandle = CSEPFile.openFile(meta_file,
                                                                 CSEPFile.Mode.APPEND)
                                     CSEPPropertyFile.write(fhandle,
                                                            CSEPPropertyFile.Metadata.SVNKeyword,
                                                            tag_url)
                                     fhandle.close()
         

   #----------------------------------------------------------------------------
   # Locate raw catalog files under directory and extract catalog start date
   #----------------------------------------------------------------------------
   def catalogStartYear (self, 
                         dir_path): 
     """ Read start date of very first event in raw catalog"""

     raw_catalog = os.path.join(dir_path,
                                CatalogDataSource._RawFile)
     found_catalog = None
     start_year = None
     is_archived = None

     if os.path.exists(raw_catalog) and \
        (os.path.getsize(raw_catalog) != 0):
         
         self.__filesToRemoveHandle.write('%s\n' %raw_catalog)
         found_catalog = raw_catalog

         # Check if corresponding metadata file exists, and if file is already
         # archived in SVN
         is_archived = self.__isArchived(raw_catalog)

         
     # Catalog does not exist, check metadata files if 
     # unique filename was generated for raw catalog
     raw_catalog = self.__findByMetadataFile(dir_path)

     if raw_catalog is not None:
         # Some catalogs won't have absolute path to the file provided
         if os.path.isabs(raw_catalog) is False:
             raw_catalog = os.path.join(dir_path,
                                        raw_catalog)
             
         if os.path.exists(raw_catalog) and \
            (os.path.getsize(raw_catalog) != 0):
             # Keep track of file for later removal
             self.__filesToRemoveHandle.write('%s\n' %raw_catalog)
             found_catalog = raw_catalog

             is_archived = self.__isArchived(raw_catalog)


     if CatalogFiles.DataSourceType in CatalogFiles.__catalogStartDate:
         start_year = CatalogFiles.__catalogStartDate[CatalogFiles.DataSourceType]
         
     elif found_catalog is not None:
         # Catalog exists, check for start date of catalog
         fhandler = CSEPFile.openFile(found_catalog)
         line = fhandler.readline()
         fhandler.close()
         
         start_year = int(line[5:9])
         
     return (start_year, found_catalog, is_archived)


   #----------------------------------------------------------------------------
   # Check if corresponding metedata file exists and has SVNTag keyword meaning
   # that file has been already archived in SVN
   #----------------------------------------------------------------------------
   def __isArchived (self, 
                     raw_catalog): 
       """ Check if catalog is archived in SVN already (based on SVNTag keyword
           in corresonding metadata file if it exists)"""
           
       is_archived = None
       
       meta_file = raw_catalog + CSEPPropertyFile.Metadata.Extension

       if os.path.exists(meta_file):
           meta_obj = CSEPPropertyFile.Metadata(meta_file)
           if CSEPPropertyFile.Metadata.SVNKeyword in meta_obj.info.keys() and \
              meta_obj.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:

               CSEPLogging.getLogger(__name__).warning("Raw catalog %s is already archived in SVN: %s" %(raw_catalog,
                                                                                                         meta_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]))
               is_archived = meta_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]
               
       return is_archived 


   #----------------------------------------------------------------------------
   # Locate raw catalog files based on existing metedata files under provided
   # directory
   #----------------------------------------------------------------------------
   def __findByMetadataFile (self, 
                             dir_path): 
       """ Search metadata files for raw catalog in 'dir_path'"""
     
       ### Search for metadata files - latest created are checked first
       meta_files = glob.glob('%s/%s*%s' %(dir_path,
                                           CSEP.NAMESPACE,
                                           CSEPPropertyFile.Metadata.Extension))
       
       data_file = None
       if len(meta_files) == 0:

           # File does not exist
           CSEPLogging.getLogger(__name__).warning("No metadata files exist under %s directory" %dir_path)
           return data_file
          
       
       # Find metadata file that corresponds to raw catalog
       for each_file in meta_files:

          meta_obj = CSEPPropertyFile.Metadata(each_file)
          meta_path, meta_file = os.path.split(meta_obj.originalDataFilename)
          
          if meta_file == CatalogDataSource._RawFile:
             
              CSEPLogging.getLogger(__name__).info("Found metadata file for raw catalog in %s: %s" %(dir_path,
                                                                                                     meta_obj.info[CSEPPropertyFile.Metadata.DataFileKeyword]))
              
              data_file = meta_obj.info[CSEPPropertyFile.Metadata.DataFileKeyword]
              CSEPLogging.getLogger(__name__).info("Found raw catalog by metadata: %s" %data_file)
              
              # Check if file is a link to other existing data file which 
              # is already archived
              link_datafile = None
              while meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword] is not None:
                   
                  # Extract information from metadata file that represents "linked" data file
                  # current metadata file refers to
                  CSEPLogging.getLogger(__name__).info("__findByMetadataFile: %s metafile for %s contains a link to %s" 
                                                       %(meta_obj.file, meta_obj.originalDataFilename,
                                                         meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]))
                   
                  link_datafile = meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]
                  
                  link_path, link_file = os.path.split(link_datafile)
                  
                  if link_file == CatalogDataSource._RawFile:
                      # Original 'import_raw.dat' is used as link filename, search
                      # link_dir for unique filename that represents raw catalog
                      link_datafile = self.__findByMetadataFile(link_path)
                      
                      if os.path.isabs(link_datafile) is False:
                          # No path is provided within metadata file
                          link_datafile = os.path.join(link_path,
                                                       link_datafile)
                      
                  meta_obj = CSEPPropertyFile.Metadata(link_datafile + CSEPPropertyFile.Metadata.Extension) 
              
              if link_datafile is not None:
                  # Check if original raw catalog is archived in SVN, use that tag
                  # for raw catalog "data_file" without archiving
                  
                  # Get SVN tag from metadata file that corresponds to the "linked" file
                  link_tag = self.__isArchived(link_datafile)
                  CSEPLogging.getLogger(__name__).info("%s link file contains SVN tag %s" %(link_datafile,
                                                                                            link_tag))
                  
                  if link_tag is not None and self.__dryRun is False:
                      # Update original raw catalog metadata with the SVN tag
                      # the link file it points to
                      
                      meta_file = data_file + CSEPPropertyFile.Metadata.Extension
                      # Some catalogs won't have absolute path to the file provided
                      if os.path.isabs(meta_file) is False:
                          meta_file = os.path.join(dir_path,
                                                   meta_file)
                                 
                      CSEPLogging.getLogger(__name__).info("+++Updating metadata file %s with SVN tag %s" %(meta_file,
                                                                                                            link_tag))
                      fhandle = CSEPFile.openFile(meta_file,
                                                  CSEPFile.Mode.APPEND)
                      CSEPPropertyFile.write(fhandle,
                                             CSEPPropertyFile.Metadata.SVNKeyword,
                                             link_tag)
                      fhandle.close()

                  elif link_tag is None:
                       raise RuntimeError, "Link file %s is not archived in SVN" %link_datafile 
              
              break
              
       return data_file


if __name__ == "__main__":
    
    import optparse
    
    command_options = optparse.OptionParser()

    command_options.add_option('--dataSource',
                               dest='data_source',
                               default=ANSSDataSource.ANSSDataSource.Type,
                               help='Catalog data source (ANSS or CMT). Default is ANSS.')
    
    command_options.add_option('--startDate',
                               dest='start_date',
                               default=None,
                               help='Start date for runtime directories with raw catalog data. Default is \
2007-09-01.')

    command_options.add_option('--endDate',
                               dest='end_date',
                               default=None,
                               help='End date for runtime directories with raw catalog data. Default is now().')
    
    command_options.add_option('--topDir',
                               dest='top_dir',
                               default=None,
                               help=':-separated list of top level directories for all runtime Dispatcher directories. Default is None.')

    command_options.add_option('--archive',
                               dest='archive_dir',
                               default=None,
                               help='Directory for working copy of SVN catalog archive')

    command_options.add_option('--disableDryRun',
                               dest='dry_run',
                               default=True,
                               action='store_false',
                               help='Invoke dry run of the program. Default is True.')
    
    
    (values, args) = command_options.parse_args()

    
    if values.data_source == CMTDataSource.CMTDataSource.Type:
        os.environ[CMTDataSource.ARCHIVE_ENV] = values.archive_dir
    else:
        os.environ[ANSSDataSource.ARCHIVE_ENV] = values.archive_dir
        
    os.environ[ANSSDataSource.ARCHIVE_ENV] = values.archive_dir
    
    if values.start_date is not None:
        CatalogFiles.StartDate = datetime.datetime.strptime(values.start_date,
                                                            "%Y%m%d")

    if values.end_date is not None:
        CatalogFiles.NowDate = datetime.datetime.strptime(values.end_date,
                                                          "%Y%m%d")

    CatalogFiles.DataSourceType = values.data_source
    
    c = CatalogFiles()
    c.commit(values.top_dir,
             values.dry_run)
    
