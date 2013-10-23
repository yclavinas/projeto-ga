"""
Module CatalogRetrieval
"""

__version__ = "$Revision: 3632 $"
__revision__ = "$Id: CatalogRetrieval.py 3632 2012-02-21 21:40:32Z liukis $"


import os, unittest, datetime, time, glob, pysvn

from CSEPTestCase import CSEPTestCase
from RELMCatalog import RELMCatalog
from ANSSDataSource import ANSSDataSource
from CMTDataSource import CMTDataSource
from CatalogDataSource import CatalogDataSource
from CSEPPropertyFile import CSEPPropertyFile


#--------------------------------------------------------------------------------
# 
# Year generator.
# 
# This generator function reads a specific entry from the file line that
# represents a year.
#
# Inputs:
#         filepath - Path to the catalog file.
# Output:
#         Integer representation of year from the line of file.     
#
def yearOfLine(filepath, line_of_words = str.split):
   """ Generator to return integer representation of decimal year from 
       each line of specified file."""
   
   # Year position for the line entries
   __YEAR = 2
       
   fhandle = open(filepath)
   for line in fhandle:
      words = line_of_words(line)
      
      # Return year string
      yield int(words[__YEAR])
   
   fhandle.close() 
       

#--------------------------------------------------------------------------------
# 
# Date generator for CMT catalog in 'ndk' format.
# 
# This generator function reads a date entry from the 'ndk' format file line that
# represents an event date.
#
# Inputs:
#         filepath - Path to the catalog file.
# Output:
#         date object that represents an event date
#
def dateOfCMTLine(filepath, line_of_words = str.split):
   """ Generator to return integer representation of decimal year from 
       each line of specified file."""
   
       
   for count, line in enumerate(open(filepath, 'rU')):
      
      if count % CMTDataSource.LinesPerEvent == 0:
    
         words = line_of_words(line)
         
         # Check if hypocenter reference catalog token is missing - first token
         # will be date instead:
         date_pos = CMTDataSource.DateIndex
         if words[0][:1].isdigit():
            date_pos -= 1
            
         yield datetime.date(*time.strptime(words[date_pos], '%Y/%m/%d')[:3])


#-------------------------------------------------------------------------------
#
# Test retrieval of the catalog data.
#
class CatalogRetrieval (CSEPTestCase):
    
    #---------------------------------------------------------------------------
    #
    # Download ANSS catalog with default start date of 1985-1-1 and confirm that
    # non-empty raw and pre-processed files are generated.
    #
    # Inputs: None.
    #    
    def testANSSDownload(self):
        """ Test retrieval of raw ANSS catalog data and succeed. \
Download data for the previous month with default start date of 1985-1-1 \
and check for non-empty raw and pre-processed catalog file."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff


        data_source = ANSSDataSource()
        start_date = data_source.StartDate
        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
   
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago)


        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
        
        # Check for raw data metafile
        meta_files = glob.glob('%s/*%s' %(CSEPTestCase.TestDirPath,
                                          CSEPPropertyFile.Metadata.Extension))
        found_raw_data = False
         
        for each_meta in meta_files:
            meta_obj = CSEPPropertyFile.Metadata(each_meta)
            meta_path, meta_file = os.path.split(meta_obj.originalDataFilename)
            if meta_file == CatalogDataSource._RawFile:
                found_raw_data = True
             
        self.failIf(found_raw_data is False,
                    'Could not find metadata file corresponding to %s raw catalog data in run-time directory %s' 
                     %(data_source.RawFile,
                       CSEPTestCase.TestDirPath))

                
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(CSEPTestCase.TestDirPath, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
        # Check that start and end years of the time period have been downloaded
        
        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        years = [data_source.StartDate.year, 
                 month_ago.year]
        self.__checkForANSSYears(years)


    #---------------------------------------------------------------------------
    #
    # Download ANSS catalog with default start date of 1985-1-1 and confirm that
    # non-empty raw and pre-processed files are generated.
    #
    # Inputs: None.
    #    
    def testANSSDownloadWithRuntimeDirectory(self):
        """ Test retrieval of raw ANSS catalog data and succeed. \
Download data for the previous month with default start date of 1985-1-1 \
and check for non-empty raw and pre-processed catalog file. Check for existence \
of metadata file in runtime directory."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff


        data_source = ANSSDataSource()
        # Setup test name
        CSEPTestCase.setTestName(self,
                                 self.id())
   
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)

        # Create runtime directory to store data products to (to test
        # Dispatcher's runtime directory)
        runtime_dir = os.path.join(CSEPTestCase.TestDirPath,
                                   'runtimedir')
        os.makedirs(runtime_dir)
        catalog.create(month_ago,
                       runtime_dir)


        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
        
        # Check for raw data metafile
        meta_files = glob.glob('%s/*%s' %(runtime_dir,
                                          CSEPPropertyFile.Metadata.Extension))
        found_raw_data = False
        link_file = None
        
        for each_meta in meta_files:
            meta_obj = CSEPPropertyFile.Metadata(each_meta)
            meta_path, meta_file = os.path.split(meta_obj.originalDataFilename)
            if meta_file == CatalogDataSource._RawFile:
                found_raw_data = True
            
            if CSEPPropertyFile.Metadata.DataLinkKeyword in meta_obj.info.keys() and \
               meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword] is not None:
                link_file = meta_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]

        
        if data_source.SVN.isWorkingCopy is True:
            # Check that raw data file is a link to original file in SVN working copy
            self.failIf(link_file != os.path.realpath(data_source.RawFile),
                        "Expected link to SVN working copy %s in metadata file in %s directory, got %s" \
                        %(os.path.realpath(data_source.RawFile),
                          runtime_dir,
                          link_file))
             
        self.failIf(found_raw_data is False,
                    'Could not find metadata file corresponding to %s raw catalog data in run-time directory %s' 
                     %(data_source.RawFile,
                       runtime_dir))

                
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(runtime_dir, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
        # Check that start and end years of the time period have been downloaded
        
        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        years = [data_source.StartDate.year, 
                 month_ago.year]
        self.__checkForANSSYears(years,
                                 runtime_dir)


    #---------------------------------------------------------------------------
    #
    # Download ANSS catalog with default start date of 1985-1-1 and tag
    # catalog in repository based on runtime test date. Tag should be based on 
    # runtime information to avoid identical tags being generated by multiple
    # runs of acceptance tests.
    #
    # Inputs: None.
    #
    @unittest.skipIf(ANSSDataSource().SVN.isWorkingCopy is False,
                     "ANSS data source is not using SVN repository to store raw catalog data")
    def testANSSDDownloadCommitToSVN(self):
        """ Test retrieval of raw ANSS catalog data and succeed. \
Download data for the previous month with default start date of 1985-1-1, \
tag catalog in SVN repository and check for non-empty raw and \
pre-processed catalog files."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff


        data_source = ANSSDataSource()
        
        # Create SVN tag
        svn_tag = month_ago.strftime("%Y%m%d%H%M%S") 
        data_source.SVN.setTag(svn_tag)
        svn_tag_url = data_source.SVN.tagURL()
        
        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
   
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago)

        # Check if raw catalog has been tagged in the repository
        try:
            svn_client = pysvn.Client()
            svn_client.ls(data_source.SVN.tagURL())
            
        except pysvn._pysvn.ClientError, error:
            
            msg = "Tagging of ANSS data with default start date failed with error: %s" %error
            self.fail(msg)
        
        # Check that metadata file is generated for raw catalog in runtime directory,
        # and contains svn tag information within
        meta_files = glob.glob('%s/*meta' %CSEPTestCase.TestDirPath)
        
        svn_tag_from_file = None
        
        for each_file in meta_files:
            file_obj = CSEPPropertyFile.Metadata(each_file)
            
            if CSEPPropertyFile.Metadata.SVNKeyword in file_obj.info.keys() and \
               file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:
                svn_tag_from_file = file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]
            
            
        self.failIf(svn_tag_url != svn_tag_from_file,
                    "Expected %s SVN tag in metadata file in %s directory, got %s" \
                    %(svn_tag_url,
                      CSEPTestCase.TestDirPath,
                      svn_tag_from_file))

        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
                
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(CSEPTestCase.TestDirPath, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
        # Check that start and end years of the time period have been downloaded
        
        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        years = [data_source.StartDate.year, 
                 month_ago.year]
        self.__checkForANSSYears(years)


    #---------------------------------------------------------------------------
    #
    # Download ANSS catalog with default start date of 1985-1-1 and tag
    # catalog in repository based on runtime test date. Tag should be based on 
    # runtime information to avoid identical tags being generated by multiple
    # runs of acceptance tests.
    #
    # Inputs: None.
    #
    @unittest.skipIf(ANSSDataSource().SVN.isWorkingCopy is False,
                     "ANSS data source is not using SVN repository to store raw catalog data")
    def testANSSDownloadCommitToSVNWithRuntimeDir(self):
        """ Test retrieval of raw ANSS catalog data and succeed. \
Download data for the previous month with default start date of 1985-1-1, \
tag catalog in SVN repository and check for non-empty raw and \
pre-processed catalog files."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff


        data_source = ANSSDataSource()
        
        # Create SVN tag
        svn_tag = month_ago.strftime("%Y%m%d%H%M%S") 
        data_source.SVN.setTag(svn_tag)
        svn_tag_url = data_source.SVN.tagURL()
        
        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
   
        # Create runtime directory to store data products to (to test
        # Dispatcher's runtime directory)
        runtime_dir = os.path.join(CSEPTestCase.TestDirPath,
                                   'runtimedir')
        os.makedirs(runtime_dir)

        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago,
                       runtime_dir)

        # Check if raw catalog has been tagged in the repository
        try:
            svn_client = pysvn.Client()
            svn_client.ls(data_source.SVN.tagURL())
            
        except pysvn._pysvn.ClientError, error:
            
            msg = "Tagging of ANSS data with default start date failed with error: %s" %error
            self.fail(msg)
        
        # Check that metadata file is generated for raw catalog in runtime directory,
        # and contains svn tag information within and file is a link to SVN 
        # working copy of raw catalog
        meta_files = glob.glob('%s/*meta' %runtime_dir)
        
        svn_tag_from_file = None
        link_file = None
        for each_file in meta_files:
            file_obj = CSEPPropertyFile.Metadata(each_file)
            
            if CSEPPropertyFile.Metadata.SVNKeyword in file_obj.info.keys() and \
               file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:
                svn_tag_from_file = file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]
            
            if CSEPPropertyFile.Metadata.DataLinkKeyword in file_obj.info.keys() and \
               file_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword] is not None:
                link_file = file_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]
                
        self.failIf(svn_tag_url != svn_tag_from_file,
                    "Expected %s SVN tag in metadata file in %s directory, got %s" \
                    %(svn_tag_url,
                      runtime_dir,
                      svn_tag_from_file))
        
        # Check that raw data file is a link to original file in SVN working copy
        self.failIf(link_file != os.path.realpath(data_source.RawFile),
                    "Expected link to SVN working copy file %s in metadata file in %s directory, got %s" \
                    %(os.path.realpath(data_source.RawFile),
                      runtime_dir,
                      link_file))
        
        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
                
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(runtime_dir, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of ANSS catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed ANSS catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
        # Check that start and end years of the time period have been downloaded
        
        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        years = [data_source.StartDate.year, 
                 month_ago.year]
        self.__checkForANSSYears(years,
                                 runtime_dir)
        

    #----------------------------------------------------------------------------
    #
    # Download ANSS catalog with other than default start date (use 1932-1-1)
    #  and confirm that non-empty raw and pre-processed files are generated.
    #
    # Inputs: None.
    #    
    def testANSSDownload_1932_1_1_StartDate(self):
        """ Test retrieval of raw ANSS catalog data and succeed. \
Download data for the previous month with start date other than default \
(1932-1-1) and check for non-empty raw and pre-processed catalog file."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff

        start_date = datetime.date(1932, 1, 1)
        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())

        data_source = ANSSDataSource(start_date)
   
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago)


        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of ANSS catalog with start date of %s failed.' \
                    %start_date)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded ANSS catalog file with start date %s is empty.' \
                    %start_date)
        
                
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(CSEPTestCase.TestDirPath, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of ANSS catalog with start date of %s failed.' \
                    %start_date)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed ANSS catalog file with start date of %s is empty.' \
                    %start_date)

        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        years = [start_date.year, 
                 month_ago.year]
        self.__checkForANSSYears(years)


    #----------------------------------------------------------------------------
    #
    # Download ANSS catalog with other than default start date (use 1932-1-1)
    # and tag catalog in repository based on runtime test date. 
    # Tag should be based on runtime information to avoid identical tags being
    # generated by multiple runs of acceptance tests.
    #
    # Inputs: None.
    #
    @unittest.skipIf(ANSSDataSource().SVN.isWorkingCopy is False,
             "ANSS data source is not using SVN repository to store raw catalog data")
    def testANSSDownload_1932_1_1_StartDateCommitToSVN(self):
        """ Test retrieval of raw ANSS catalog data with start date of \
1932-01-01 and tag catalog in repository based on runtime test date."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff

        start_date = datetime.date(1932, 1, 1)
        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())

        data_source = ANSSDataSource(start_date)

        # Create SVN tag
        svn_tag = month_ago.strftime("%Y%m%d%H%M%S") 
        data_source.SVN.setTag(svn_tag)
        svn_tag_url = data_source.SVN.tagURL()
        
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago)


        # Check if raw catalog has been tagged in the repository
        try:
            svn_client = pysvn.Client()
            status = svn_client.ls(data_source.SVN.tagURL())
            
        except pysvn._pysvn.ClientError, error:
            
            msg = "Tagging of ANSS data with %s start date failed with error: %s" %(start_date,
                                                                                    error)
            self.fail(msg)
        
        # Check that metadata file is generated for raw catalog in runtime directory,
        # and contains svn tag information within
        meta_files = glob.glob('%s/*meta' %CSEPTestCase.TestDirPath)
        
        svn_tag_from_file = None
        for each_file in meta_files:
            file_obj = CSEPPropertyFile.Metadata(each_file)
            
            if CSEPPropertyFile.Metadata.SVNKeyword in file_obj.info.keys() and \
               file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:
                svn_tag_from_file = file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]
            
        self.failIf(svn_tag_url != svn_tag_from_file,
                    "Expected %s SVN tag in metadata file in %s directory, got %s" \
                    %(svn_tag_url,
                      CSEPTestCase.TestDirPath,
                      svn_tag_from_file))

        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of ANSS catalog with start date of %s failed.' \
                    %start_date)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded ANSS catalog file with start date %s is empty.' \
                    %start_date)
        
                
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(CSEPTestCase.TestDirPath, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of ANSS catalog with start date of %s failed.' \
                    %start_date)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed ANSS catalog file with start date of %s is empty.' \
                    %start_date)

        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        years = [start_date.year, 
                 month_ago.year]
        self.__checkForANSSYears(years)

    #----------------------------------------------------------------------------
    #
    # Download CMT catalog and confirm that non-empty raw file is generated.
    #
    # Inputs: None.
    #    
    def testCMTDownload(self):
        """ Test retrieval of raw CMT catalog data in 'ndk' format and succeed."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())
   
        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        start_date = datetime.datetime(1977, 1, 1)
        download_data = True
        pre_process_data = True
        args = 'includePreliminary=True'
        data_source = CMTDataSource(start_date,
                                    download_data,
                                    pre_process_data,
                                    args)
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago)


        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of CMT catalog with start date of %s failed.' \
                    %start_date)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded CMT catalog file with start date %s is empty.' \
                    %start_date)
        
                
        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        dates = {start_date.year : [start_date.month], 
                 month_ago.year : [month_ago.month]}
        self.__checkForCMTDates(dates,
                                data_source.RawFile)


    #----------------------------------------------------------------------------
    #
    # Download CMT catalog and confirm that non-empty raw file is generated.
    #
    # Inputs: None.
    #    
    @unittest.skipIf(CMTDataSource().SVN.isWorkingCopy is False,
                     "CMT data source is not using SVN repository to store raw catalog data")
    def testCMTDownloadCommitToSVN(self):
        """ Test retrieval of raw CMT catalog data in 'ndk' format, committing
            it to SVN repository, tagging it in SVN, and succeed."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())

        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        start_date = datetime.datetime(1977, 1, 1)
        download_data = True
        pre_process_data = True
        args = 'includePreliminary=True'
        data_source = CMTDataSource(start_date,
                                    download_data,
                                    pre_process_data,
                                    args)
        
        # Create SVN tag for data source
        svn_tag = month_ago.strftime("%Y%m%d%H%M%S") 
        data_source.SVN.setTag(svn_tag)
        svn_tag_url = data_source.SVN.tagURL()
        
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago)

        # Check if raw catalog has been tagged in the repository
        try:
            svn_client = pysvn.Client()
            svn_client.ls(data_source.SVN.tagURL())
            
        except pysvn._pysvn.ClientError, error:
            
            msg = "Tagging of CMT data with default start date failed with error: %s" %error
            self.fail(msg)

        # Check that metadata file is generated for raw catalog in runtime directory,
        # and contains svn tag information within
        meta_files = glob.glob('%s/*meta' %CSEPTestCase.TestDirPath)
        
        svn_tag_from_file = None
        
        for each_file in meta_files:
            file_obj = CSEPPropertyFile.Metadata(each_file)
            
            if CSEPPropertyFile.Metadata.SVNKeyword in file_obj.info.keys() and \
               file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:
                svn_tag_from_file = file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]
            
        self.failIf(svn_tag_url != svn_tag_from_file,
                    "Expected %s SVN tag in metadata file in %s directory, got %s" \
                    %(svn_tag_url,
                      CSEPTestCase.TestDirPath,
                      svn_tag_from_file))

        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of CMT catalog with start date of %s failed.' \
                    %start_date)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded CMT catalog file with start date %s is empty.' \
                    %start_date)
        
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(CSEPTestCase.TestDirPath, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of CMT catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed CMT catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
                
        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        dates = {start_date.year : [start_date.month], 
                 month_ago.year : [month_ago.month]}
        self.__checkForCMTDates(dates,
                                data_source.RawFile)


    #----------------------------------------------------------------------------
    #
    # Download CMT catalog and confirm that non-empty raw file is generated.
    #
    # Inputs: None.
    #    
    @unittest.skipIf(CMTDataSource().SVN.isWorkingCopy is False,
                     "CMT data source is not using SVN repository to store raw catalog data")
    def testCMTDownloadCommitToSVNWithRuntimeDir(self):
        """ Test retrieval of raw CMT catalog data in 'ndk' format, committing
            it to SVN repository, tagging it in SVN, and succeed."""

        # Download data for the last month (use 31 days for a month)
        now = datetime.datetime.now()
        month_diff = datetime.timedelta(days=31)
        month_ago = now - month_diff

        # Setup test name
        CSEPTestCase.setTestName(self, 
                                 self.id())

        # Don't invoke any kind of post-processing for the catalog data.
        # Instantiating of catalog object takes care of generating a test directory
        start_date = datetime.datetime(1977, 1, 1)
        download_data = True
        pre_process_data = True
        args = 'includePreliminary=True'
        data_source = CMTDataSource(start_date,
                                    download_data,
                                    pre_process_data,
                                    args)

        # Create runtime directory to store data products to (to test
        # Dispatcher's runtime directory)
        runtime_dir = os.path.join(CSEPTestCase.TestDirPath,
                                   'runtimedir')
        os.makedirs(runtime_dir)
        
        # Create SVN tag for data source
        svn_tag = month_ago.strftime("%Y%m%d%H%M%S") 
        data_source.SVN.setTag(svn_tag)
        svn_tag_url = data_source.SVN.tagURL()
        
        catalog = RELMCatalog(CSEPTestCase.TestDirPath,
                              data_source)
                
        catalog.create(month_ago,
                       runtime_dir)

        # Check if raw catalog has been tagged in the repository
        try:
            svn_client = pysvn.Client()
            svn_client.ls(data_source.SVN.tagURL())
            
        except pysvn._pysvn.ClientError, error:
            
            msg = "Tagging of CMT data with default start date failed with error: %s" %error
            self.fail(msg)

        # Check that metadata file is generated for raw catalog in runtime directory,
        # and contains svn tag information within and file is a link to SVN 
        # working copy of raw catalog
        meta_files = glob.glob('%s/*meta' %runtime_dir)
        
        svn_tag_from_file = None
        link_file = None
        for each_file in meta_files:
            file_obj = CSEPPropertyFile.Metadata(each_file)
            
            if CSEPPropertyFile.Metadata.SVNKeyword in file_obj.info.keys() and \
               file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword] is not None:
                svn_tag_from_file = file_obj.info[CSEPPropertyFile.Metadata.SVNKeyword]
            
            if CSEPPropertyFile.Metadata.DataLinkKeyword in file_obj.info.keys() and \
               file_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword] is not None:
                link_file = file_obj.info[CSEPPropertyFile.Metadata.DataLinkKeyword]
                
        self.failIf(svn_tag_url != svn_tag_from_file,
                    "Expected %s SVN tag in metadata file in %s directory, got %s" \
                    %(svn_tag_url,
                      runtime_dir,
                      svn_tag_from_file))
        
        # Check that raw data file is a link to original file in SVN working copy
        self.failIf(link_file != os.path.realpath(data_source.RawFile),
                    "Expected link to SVN working copy file %s in metadata file in %s directory, got %s" \
                    %(os.path.realpath(data_source.RawFile),
                      runtime_dir,
                      link_file))

        # Check if raw catalog file exists and has non-zero size
        self.failIf(os.path.exists(data_source.RawFile) is False, 
                    'Download of CMT catalog with start date of %s failed.' \
                    %start_date)
        self.failIf(os.path.getsize(data_source.RawFile) == 0,
                    'Downloaded CMT catalog file with start date %s is empty.' \
                    %start_date)
        
        # Check if pre-processed catalog file exists and has non-zero size
        result_file = os.path.join(runtime_dir, 
                                   CatalogDataSource.PreProcessedFile)
        
        self.failIf(os.path.exists(result_file) is False, 
                    'Pre-processing of CMT catalog with start date of %s failed.' \
                    %data_source.StartDate)
        self.failIf(os.path.getsize(result_file) == 0, 
                    'Pre-processed CMT catalog file with start date of %s is empty.' \
                    %data_source.StartDate)
        
                
        # Confirm that downloaded start and end years of the range are in final 
        # catalog file:
        dates = {start_date.year : [start_date.month], 
                 month_ago.year : [month_ago.month]}
        self.__checkForCMTDates(dates,
                                data_source.RawFile)


    #----------------------------------------------------------------------------
    #
    # Check that specified years are present in the result file.
    #
    # Inputs:
    #         years - List of years to check for. 
    #    
    def __checkForANSSYears(self, 
                            years, 
                            data_dir = None):
        """ Check for the presence of specified years in pre-processed catalog file. \
If option data directory is provided, use that directory to locate catalog file."""
       
        # Build dictionary of found years from file that are only specified 
        # by 'years'
        found_years = []
        data_file = os.path.join(CSEPTestCase.TestDirPath,
                                 CatalogDataSource.PreProcessedFile)
        
        if data_dir is not None:
            data_file = os.path.join(data_dir,
                                     CatalogDataSource.PreProcessedFile)
            
        for year in yearOfLine(data_file):
           if year in years:
              if year not in found_years:
                 found_years.append(year)

        years.sort()  # Sorted in place
        found_years.sort() # Sorted in place
        
        self.failIf(found_years != years,
                    "Expected to find %s years in pre-processed catalog file, \
found %s" %(years, found_years))
        

    #----------------------------------------------------------------------------
    #
    # Check that specified years are present in the result file.
    #
    # Inputs:
    #         dates - Dictionary of dates to check for. 
    #    
    def __checkForCMTDates(self, 
                           dates,
                           raw_file):
        """ Check for the presence of specified years in the catalog file."""
       
        # Build dictionary of found  from file that are only specified 
        # by 'years'
        found_dates = {}
        for event_date in dateOfCMTLine(raw_file):
           if event_date.year in dates:
              if event_date.month in dates[event_date.year]:
                 
                 found_dates[event_date.year] = event_date.month

        # No need to check for matching month values since year is inserted into
        # the dictionary only if month and year of the event match one in the
        # specified 'dates' dictionary
        reference_years = dates.keys()
        reference_years.sort() # Sorted in place
        
        found_years = found_dates.keys()
        found_years.sort() # Sorted in place

        self.failIf(reference_years != found_years,
                    "Expected to find %s dates in %s catalog file, found %s" %(dates, 
                                                                               raw_file, 
                                                                               found_dates))


# Invoke the module
if __name__ == '__main__':

   # Invoke all tests - must have testXXX method in the class defined
   unittest.main()
   
# end of main
