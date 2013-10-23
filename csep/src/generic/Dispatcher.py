"""
Module Dispatcher
"""

__version__ = "$Revision: 4218 $"
__revision__ = "$Id: Dispatcher.py 4218 2013-03-04 21:01:48Z liukis $"


import sys, os, time, shutil, datetime, logging, traceback

import CSEPLogging, Environment, DispatcherOptionParser, CSEP
from CSEPEmail import CSEPEmail
from CSEPStatus import CSEPStatus
from RELMCatalog import RELMCatalog
from CatalogDataSource import CatalogDataSource
from ForecastGroup import ForecastGroup
from DispatcherInitFile import DispatcherInitFile
from CSEPOptions import CommandLineOptions
from OneDayModelInputPostProcess import OneDayModelInputPostProcess
from OneDayModelDeclusInputPostProcess import OneDayModelDeclusInputPostProcess


#--------------------------------------------------------------------------------
#
# Dispatcher.
#
# This class is designed to automate submition and comparison of forecast
# evaluation tests in the CSEP environment.
#
class Dispatcher (object):

    # Static data

    # Class identifier
    __type = "Dispatcher"

    # Logger for the class - instantiated by the first (and only?) instance of 
    # the class
    __logger = None
          
    # Number of seconds to sleep b/w re-tries to create a lock
    __sleepSeconds = 1
    
    # Expected exception when directory lock is already created by other process
    __exceptionMsg = 'File exists'

   
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None.
    # 
    def __init__ (self):
        """ Initialization for Dispatcher class."""
        
        # Start time for the run
        self.__startTime = datetime.datetime.now()
        
        # List of requred options for the run - test date
        required = [CommandLineOptions.YEAR, 
                    CommandLineOptions.MONTH, 
                    CommandLineOptions.DAY]
        
        # Store command-line options
        self.__options = DispatcherOptionParser.DispatcherOptionParser().options(required)
        
        if Dispatcher.__logger is None:
           Dispatcher.__logger = CSEPLogging.CSEPLogging.getLogger(Dispatcher.__name__)

        # Initialize test date for the run: offset the test date by waiting 
        # period if any
        self.__testDate = datetime.datetime(self.__options.year,
                                            self.__options.month,
                                            self.__options.day) - \
                          datetime.timedelta(days=self.__options.waiting_period)
        
        self.__initFile = DispatcherInitFile(self.__options.config_file)
        
        # Set top level directory for runtime directories and log files - 
        # configurable through initialization file
        self.__rootDir = self.__initFile.elementValue(
                            DispatcherInitFile.RootDirectoryElement)
        
        # Status object for the CSEP system
        self.__status = CSEPStatus(self.__options)
        
        # XML nodes that represent directory paths for all forecast groups
        # for the Dispatcher run
        self.__dirNodes = self.__initFile.elements(
                             DispatcherInitFile.ForecastGroupElement)
        
        # Email information (if any) is provided in the initialization file
        self.__email = CSEPEmail(self.__initFile)


        # Catalog data source for the run - default is ANSS
        self.__dataSource = self.__initFile.dataSource(self.__options.download_raw_data,
                                                       self.__options.preprocess_raw_data)
        self.__dataSource.registerHandler(self.__registerForCleanup)

        # Unique directory name for this run
        self.__dir = None
        
        # ForecastGroup objects that represent various groups as specified
        # by the self.__dirNodes data
        self.__forecastsGroups = [] 
        
        # Files generated during the run that don't have unique filenames,
        # and should be removed for the next Dispatcher run
        self.__filesToRemove = []
        
        # Files to attach to status email
        self.__filesToEmail = []


    #===========================================================================
    # Create unique path for runtime directory
    #===========================================================================
    def __runtimeDir (self):
        """ Creates unique path for runtime directory"""
        
        # Generate unique directory for the run using the following format:
        # RootDir/UserName/YYYYMMDDHHMMSS
        return os.path.abspath(os.path.join(self.__rootDir,
                                            self.__status.userName(), 
                                            time.strftime("%Y_%m"),
                                            time.strftime("%Y%m%d%H%M%S"),
                                            'pid_%s' %os.getpid()))
        

    #===========================================================================
    # Create SVN tag based on runtime directory. The tag would be used for
    # 'svn commit' of raw data as downloaded by the Dispatcher process
    #===========================================================================
    def __createSVNTag (self):
        """ Create SVN tag based on runtime directory. The tag would be used for
            'svn commit' of raw data as downloaded by the Dispatcher process."""

        # Return part of runtime directory path that represents date and time 
        # stamp used at a time of raw data download from authorized source. 
        # For example, with self.__dir set of 
        # '/home/csep/operations/dispatcher/runs/csep/2011_12/20111212034202/pid_10190',
        # SVN tag as '20111212034202' would be generated
        # would generate list of tokens: ..., '2011_12', '20111212034202', 'pid_10190'
        tokens = self.__dir.split(os.path.sep)
        return tokens[-2]
    

    #--------------------------------------------------------------------
    #
    # Invoke a single run of Dispatcher for the specified date.
    #
    # Input: None.   
    # 
    # Output: run-time directory path
    #   
    #
    def run (self):
        """ Invoke a single run of Dispatcher. This method generates unique 
            directory to store result files for the run."""

        # Error if any generated by the run
        __error_code = None
        
        # Generate unique directory for the run using the following format:
        # RootDir/UserName/YYYYMMDDHHMMSS
        self.__dir = self.__runtimeDir()
        
        created_dir = False
        
        while created_dir is False:

           try:

               # Unique directory must be generated for each Dispatcher run:
               Dispatcher.__logger.info("Creating dispatcher directory '%s'...\n" \
                                        %(self.__dir))
      
               os.makedirs(self.__dir)
               created_dir = True
                  
           except OSError, exc:
             
              # Re-raise exception if it's not of expected content
              if Dispatcher.__exceptionMsg not in exc:
                 raise

              msg = "Dispatcher directory '%s' already exists" %(self.__dir)
              Dispatcher.__logger.warning(msg) 

              # Directory exists, try again later
              time.sleep(Dispatcher.__sleepSeconds)

              # Re-set directory name
              self.__dir = self.__runtimeDir()
            
        # cd to the working directory, remember current directory 
        start_dir = os.getcwd()
        os.chdir(self.__dir)            


        try:
           
           # Fix for Trac ticket #75: uncaught exceptions should trigger FAIL 
           # status for the run
           try:
              
               # Append unique run-time directory for Dispatcher to sys.argv
               option = "runtimeDirectory=%s" %(self.__dir)
               sys.argv.append(option) 
               
               # Append actual test date to sys.argv
               option = "runtimeTestDate=%s" %(self.__testDate.date())
               sys.argv.append(option) 
                           
               
               # Collect system status
               self.__systemStatus()
   
               # Identify forecast groups - do it before downloading
               # catalog data (report problems early on)
               self.__identifyForecastsGroups()
               
               # Download catalog data
               self.__downloadCatalog()
               
               # For each model group:
               for group in self.__forecastsGroups: 
                  
                   # Generate forecasts
                   self.__generateForecasts(group)
   
                   # Prepare observations by filtering catalog data
                   self.__prepareObservations(group)
                  
                   # Evaluate models for each forecast group
                   tests = self.__evaluateForecasts(group)
                  
                   # Generate summary
                   self.__summary(tests)

                   # Archive forecasts files
                   self.__archiveForecasts(group)
                   
                   # Post results (svg plots for now only) to external web server 
                   # so they are accessible by the users
                   self.__publishResults(tests)

           except:
            
              # If exception is raised, report it and print the backtrace
              exc_type, exc_value = sys.exc_info()[:2]
              
              if exc_type is not None and exc_value is not None:
                 
                 # Return to the caller to indicate the failure of some sort 
                 __error_code = exc_value
                  
                 error_msg = "Exception occured %s = %s" \
                             %(exc_type, exc_value)
                              
                 Dispatcher.__logger.error(error_msg) 
                 
                 traceback.print_exc()
            
        finally:

           # Archive forecasts files if "tomorrow" new files are to be 
           # generated - this is to prevent old files being evaluated along
           # with new ones.
           self.__archiveForecasts()

           # Clean up files that don't have unique names and should not be 
           # present in the common directories shared by all Dispatcher runs.
           self.__cleanup(self.__filesToRemove)

           # cd to the initial directory
           os.chdir(start_dir)

           # Publish runtime directory and log file for the Dispatcher if such
           # option is provided
           self.__publishRuntimeInfo()
      
           # Send email with status of the run
           self.__sendEmail()

        return (self.__dir, __error_code)


    #---------------------------------------------------------------------------
    #
    # Publish runtime information to the remote host
    #
    # Input: 
    #        dirpath - Parent directory.
    #
    def __publishRuntimeInfo(self):
        """ Publish Dispatcher's runtime directory and log file to the remote
            host"""
            
        # Publish runtime directory and log file for the Dispatcher if such
        # option is provided
        if self.__options.publish_runtime_info_server is None:
            return
                
                
        # cd to the parent directory of Dispatcher's runtime directory, 
        # remember current directory 
        working_path, working_dir = os.path.split(self.__dir)
        start_dir = os.getcwd()
        os.chdir(working_path)
        try:

            # Copy runtime directory for the process
            command = "rsync -apv --relative --delete %s" %working_dir
                
            publish_dir = self.__options.publish_runtime_info_dir
            if self.__options.publish_runtime_info_dir is None:
                    
                # Use the same directory on remote server as on publishing
                # server if publish directory was not specified
                publish_dir = working_path
                
            command += ' %s:%s' %(self.__options.publish_runtime_info_server,
                                  publish_dir)
            Environment.invokeCommand(command) 
                
        finally:
               
            os.chdir(start_dir)


        ### Publish runtime log file if present
        if self.__options.log_file is not None:

            # cd to the parent directory of Dispatcher's log file, 
            # remember current directory 
            working_path, log_file = os.path.split(self.__options.log_file)
            os.chdir(working_path)
            
            try:
                # Copy runtime directory for the process
                command = "rsync -apv --relative --delete %s" %log_file
                    
                publish_dir = self.__options.publish_runtime_info_dir
                if self.__options.publish_runtime_info_dir is None:
                        
                    # Use the same directory on remote server as on publishing
                    # server if publish directory was not specified
                    publish_dir = working_path
                    
                command += ' %s:%s' %(self.__options.publish_runtime_info_server,
                                      publish_dir)
                Environment.invokeCommand(command) 
                    
            finally:
                   
                os.chdir(start_dir)
    

    #--------------------------------------------------------------------
    #
    # Generate a sub-directory specific to the test date.
    #
    # Input: 
    #        dirpath - Parent directory.
    #
    def __testDateDir (self, dirpath):
       """ Generate a sub-directory specific to the test date."""

       subdir = os.path.join(dirpath, "%s" %self.__testDate.date())
       return subdir
        

    #--------------------------------------------------------------------
    #
    # Generate an e-mail report to specified addresses.
    #
    # Input: None.
    #
    def __sendEmail (self):
       """ Generate an e-mail report for the current run."""

       # All output was captured in the file,
       # compose report and send it to specified users
       if self.__options.log_file is not None:

          try:
             # search for error keywords in log file
             found_errors = [line for line in open(self.__options.log_file) if \
                             Environment.ErrorHandler.containsError(line)]

             status = "SUCCESSFUL"
             if len(found_errors) != 0:
                # There were errors
                status = "FAILED \nErrors: %s\n" %"\n".join(found_errors)
             
             hostname = Environment.commandOutput('hostname').strip()
             now = datetime.datetime.now()

             msg = "Test date: %s\nStatus: %s\n\n\
Runtime date: %s-%s-%s\nRuntime host: %s\n\
Runtime directory: %s\n\n\
Processing start time: %s %s\nProcessing end time: %s %s\
\n\nPlease see %s log file for a detailed report." \
                  %(self.__testDate.date(),
                    status,
                    self.__options.year, 
                    self.__options.month, 
                    self.__options.day,
                    hostname, 
                    self.__dir,
                    self.__startTime.date(), self.__startTime.time(),
                    now.date(), now.time(),
                    self.__options.log_file)
             
             # Extract status keyword for the email subject
             status_key = status.split('\n')[0]
             
             self.__email.send(msg, 
                               self.__testDate, 
                               status_key, 
                               hostname,
                               self.__filesToEmail)
             
          except Exception, e:

             # Failed to send email, log the error
             error_msg = "__sendEmail(): failed with error %s." %e
             Dispatcher.__logger.error(error_msg) 
                        
             raise RuntimeError, error_msg
            
            

    #--------------------------------------------------------------------
    #
    # Collect and save system and software status.
    #
    # Input: None
    #
    # Output: None
    #
    def __systemStatus (self):
        """ Save current status of the system."""
        
        # System status
        filenames = self.__status.systemFilename()
        self.__status.system(filenames)
        
        # Software status
        filenames = self.__status.softwareFilename()
        self.__status.software(Dispatcher.__type, 
                               CSEP.Version, 
                               filenames)
        

    #--------------------------------------------------------------------
    #
    # Identify forecast classes for evaluation.
    # 
    # This method instantiates ForecastGroup objects based on the groups
    # directories as provided in the Dispatcher configuration file.
    #
    # Input: None.
    #
    def __identifyForecastsGroups (self):
        """ Identify forecast groups available for the evaluation."""

        # Read configuration files found under each group directory, and 
        #      construct forecast groups available for evaluation 
        #      (self.__forecastsGroups)
        for dir_node in self.__dirNodes:
           dir_path = dir_node.text
           
           # If specified directory is a relative path ---> report where
           # exactly executable program thinks forecast files should be:
           if os.path.isabs(dir_path) is False:          
              error_msg = "Specified ForecastGroup directory '%s' can not be a \
path relative to the Dispatcher run directory '%s'. \
Please provide an absolute path." %(dir_path, self.__dir)
              
              Dispatcher.__logger.error(error_msg) 
              
              raise RuntimeError, error_msg         
           
           # For the purpose of re-processing:
           # Allow to overwrite list of evaluation tests, post-processing options,
           # and models to invoke that are normally specified in configuration
           # file from command-line
           self.__forecastsGroups.append(ForecastGroup(dir_path,
                                                       self.__options.post_process,
                                                       self.__options.test_list,
                                                       self.__options.test_inputs,
                                                       self.__options.generate_forecast,
                                                       self.__options.forecasts_inputs,
                                                       self.__options.post_process_args))
        

    #----------------------------------------------------------------------------
    #
    # Download catalog data.
    #
    # Input: None.
    #
    # Output: None.
    def __downloadCatalog (self):
        """ Download catalog data for the tests."""

        # Comment to provide along with SVN tag
        tag_comment = "{runtime_directory: %s, forecasts_groups: %s}" %(self.__dir,
                                                                        repr([group.rootDir() for group in self.__forecastsGroups]))
        
        # Data source is a DataSourceComposite
        for each_data_source in self.__dataSource.values():
            each_data_source.SVN.setTag(self.__createSVNTag(),
                                        tag_comment)

        if self.__options.download_raw_data is True:
        
            catalog = RELMCatalog(self.__dir, 
                                  self.__dataSource)
           
            catalog.create(self.__testDate,
                           self.__dir)
            
        else:
            
            # Check if directory for raw or pre-processed catalog data is
            # provided through configuration file - used by acceptance tests or
            # re-processing only
            root_dir_elem = self.__initFile.elements(DispatcherInitFile.RootDirectoryElement)[0]
            
            for dir_attr, file_name in zip([DispatcherInitFile.RawDataDirAttribute,
                                            DispatcherInitFile.PreProcessedDataDirAttribute,
                                            DispatcherInitFile.InputCatalogAttribute,
                                            DispatcherInitFile.InputCatalogAttribute],
                                            [os.path.basename(self.__dataSource.RawFile),
                                             CatalogDataSource.PreProcessedFile,
                                             OneDayModelInputPostProcess().files.catalog,
                                             OneDayModelDeclusInputPostProcess().files.catalog]):
                if dir_attr in root_dir_elem.attrib:
                
                    if os.path.exists(os.path.join(root_dir_elem.attrib[dir_attr].strip(), 
                                                   file_name)):
                            
                        os.symlink(os.path.join(root_dir_elem.attrib[dir_attr].strip(), 
                                                file_name),
                                   os.path.join(self.__dir,
                                                file_name))
    

    #----------------------------------------------------------------------------
    #
    # Generate forecast.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be invoked.
    #
    def __generateForecasts (self, group):
        """ Generate forecast files by invoking existing models."""

        # Generate forecast files: group captures newly generated forecast files
        group.create(self.__testDate,
                     self.__dir,        # directory with raw catalog data
                     self.__dataSource) # catalog data source
        

    #----------------------------------------------------------------------------
    #
    # Filter catalog data for observations.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies catalog
    #                filtering routines that are used to create observations
    #                for the evaluation tests.
    #
    # Output: None.
    #
    def __prepareObservations (self, group):
       """ Filter catalog according to the forecast group."""
        
       # Prepare observations only if evaluation tests are to 
       # be invoked.
       if group.hasTests(self.__testDate) is False or \
          group.tests.any('observationRequired') is False:
          return
       
       
       # Invoke catalog data post-processing for specified forecast group 
       post_process = group.postProcess()    
                
       # Place post-processed catalog file in group's catalog directory -
       # use test date as subdirectory to prevent the group from using 
       # previously created observations that were not cleaned up if 
       # ran out of disk space, etc...
       working_dir = self.__testDateDir(group.catalogDir())
       
       # Downloaded catalog data has been pre-processed already, use base class
       # for the source to skip download and pre-processing       
       catalog = RELMCatalog(working_dir, 
                             self.__dataSource, 
                             post_process)    
        
       # Generate catalog for the forecast evaluation
       # and apply uncertainties to the catalog.
       raw_data_dir = self.__dir
       original_catalog_filename = post_process.files.catalog
       
       try:
           catalog_files = catalog.create(self.__testDate,
                                          raw_data_dir)
           if len(catalog_files) == 0:
             
               ### Catalog file was not generated ---> make sure file exists
               ### (file was generated by some other group)
               catalog_path = os.path.join(working_dir,
                                           original_catalog_filename)
             
               if not os.path.exists(catalog_path):
                   error_msg = "Observation catalog '%s' file was not generated for \
the group '%s'. File does not exist under specified directory '%s'." \
                               %(original_catalog_filename, group.rootDir(), 
                                 working_dir)
                        
                   Dispatcher.__logger.error(error_msg) 
                
                   raise RuntimeError, error_msg
       except:
          
          # In a case of exception remove registered for reproducibility files
          for each_registry in post_process.reproducibility:
             self.__registerForCleanup([os.path.join(working_dir, entry) for \
                                        entry in each_registry.keys()])
             
          raise
       

    #--------------------------------------------------------------------
    #
    # Evaluate forecast models within specific forecast group.
    #
    # Input:
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    #
    # Output: 
    #        CSEPContainer of evaluation tests for the forecast group.
    #  
    def __evaluateForecasts (self, group):
        """ Evaluate comparable forecast models."""
        
        # Run evaluation tests for the group
        
        # Generate date specific sub-directory for the results and observations
        test_date_result_dir = self.__testDateDir(group.resultDir())
        test_date_catalog_dir = self.__testDateDir(group.catalogDir())
        
        for each_test in group.tests:
           
           each_test.run(self.__testDate,
                         test_date_catalog_dir,
                         test_date_result_dir)
        
        return group.tests


    #----------------------------------------------------------------------------
    #
    # Generate summary of evaluation tests.
    #
    # Input:
    #        tests - CSEPContainer of evaluation tests for the group.
    #
    def __summary (self, tests):
        """ Summarize test results for the group."""

        # Create unique copies of test results if any results were generated,
        # (method will remove original files as soon as copy file with unique
        # filename is generated)
        for each_test in tests:
           
           results = each_test.resultData()
           
           if isinstance(results, tuple) is True:
               # Files to be included into status email are provided
               summary_exists_flag, email_files = results

               self.__filesToEmail.extend(email_files)


    #--------------------------------------------------------------------
    #
    # Post test results to remove machine - publish them to the users.
    #
    # Input: 
    #        tests - List of EvaluationTest objects used for evaluation.
    #
    def __publishResults (self, tests):
        """ Post test results and summary on to the remote machine for 
            display to the users."""
        
        if self.__options.publish_server is not None:
           
           # Invoke publishing of results only once - it uses glob module:
           # will capture results for all evaluation tests performed for the group
           if len(tests):
              
              tests[0].publish(self.__options.publish_server,
                               self.__options.publish_dir)


    #----------------------------------------------------------------------------
    #
    # Archive old forecast files.
    #
    # Input:
    #        group - Forecast group to archive forecasts files for. Default is 
    #                None which means to archive forecasts for all known groups. 
    #
    # Output: None
    #
    def __archiveForecasts (self, group=None):
       """ Archive forecasts files if "tomorrow" new files are to be 
           generated. This is done to prevent old files being evaluated along
           with new ones. """
       
       if group is None:
          # Archive forecasts files for all forecasts groups
          for group in self.__forecastsGroups:
             group.archive(self.__testDate)
       
       else:      
          group.archive(self.__testDate)
            

    #--------------------------------------------------------------------
    #
    # Clean up routines for the Dispatcher run.
    #
    # Input: None.
    #
    def __cleanup (self, files_to_remove):
        """ Clean up files that don't have unique names and should not be 
            present in the common directories shared by all Dispatcher runs
            (such as ForecastGroup directories)."""

        for each_file in files_to_remove:
         
           # Check if file really exists before removing it:
           if not os.path.exists(each_file):
              Dispatcher.__logger.warning("__cleanup(): it appears that file \
'%s' does not exist." %each_file)
              
           else:
                  
              if os.path.isdir(each_file):
                 Dispatcher.__logger.info("__cleanup(): Removing directory %s" \
                                          %each_file)
                 # Causes an error when invoked from within VM image - always 
                 # leaves 1024 files in directory to be removed
                 shutil.rmtree(each_file,
                               ignore_errors = True,
                               onerror = CSEP.OnError.shutil)
              else: 
                 Dispatcher.__logger.info("__cleanup(): Removing file %s" %each_file)
                 os.remove(each_file)


    #---------------------------------------------------------------------------
    #
    # Register files for cleanup at the end of the processing.
    #
    # Input: 
    #        files_to_cleanup - List of files to cleanup at the end of 
    #                           processing
    #
    def __registerForCleanup (self, files_to_cleanup):
        """ Summarize test results for the group."""

        #Dispatcher.__logger.info("DEBUG: __registerForCleanup(): %s" %files_to_cleanup)
        self.__filesToRemove.extend(files_to_cleanup)
        
        # Remove duplicate entries if any from the list
        self.__filesToRemove = list(set(self.__filesToRemove))


# Invoke the module
if __name__ == '__main__':

   dispatcher = Dispatcher()
   dispatcher.run()
      
   
   # Shutdown logging
   logging.shutdown()
# end of main
