"""
Module BatchProcessing
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import sys, os, time, datetime, logging, traceback

import DispatcherOptionParser, BatchInitFile, CSEPLogging, CSEPStatus, \
       CSEPOptionParser, CSEPEmail, CSEPFile, Environment, CSEPInitFile
from CSEPOptions import CommandLineOptions


#--------------------------------------------------------------------------------
#
# BatchProcessing.
#
# This class is designed to automate batch processing of testing dates 
# sequencially in the CSEP testing evironment.
#
class BatchProcessing (object):

    # Static data

    # Name of the script to invoke the process
    __scriptName = 'batch_invoke.tcsh'
    
    # Subject to use for email messages
    __emailSubject = "CSEP Batch Processing"
    
    # Logger for the class - instantiated by the first (and only?) instance of 
    # the class
    __logger = None
   
   
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None.
    # 
    def __init__ (self):
        """ Initialization for BatchProcessing class."""
        
        # Start time for the run
        self.__startTime = datetime.datetime.now()
        
        # List of required options for the run - batch configuration file
        required = [CommandLineOptions.CONFIG_FILE] 

        self.__options = DispatcherOptionParser.DispatcherOptionParser().options(required)
        self.__initFile = BatchInitFile.BatchInitFile(self.__options.config_file)
        
        if BatchProcessing.__logger is None:
           BatchProcessing.__logger = CSEPLogging.CSEPLogging.getLogger(BatchProcessing.__name__)

        # Generate unique directory for the run using the following format:
        # RootDir/UserName/YYYYMMDDHHMMSS
        self.__dir = os.path.abspath(os.path.join(self.__initFile.directory,
                                                  CSEPStatus.CSEPStatus.userName(), 
                                                  time.strftime("%Y%m%d%H%M%S")))
        
        if not os.path.exists(self.__dir):
           BatchProcessing.__logger.info("Creating directory '%s' for batch processing...\n" \
                                         %(self.__dir))
           os.makedirs(self.__dir)
           
        else:
            # Raise an exception - unique directory must be generated for each run
            error_msg = "Batch processing directory '%s' already exists, exiting the run." \
                        %(self.__dir)
            BatchProcessing.__logger.error(error_msg) 
                        
            raise RuntimeError, error_msg

        self.__shellResourceFile = self.__initFile.resourceFile

        # Email information (if any) is provided in the initialization file
        self.__email = CSEPEmail.CSEPEmail(self.__initFile)

        # Log if any of spawned processes have failed
        self.__failedProcesses = {}
         

    #----------------------------------------------------------------------------
    #
    # Invoke processes in batch mode.
    #
    # Input: None.   
    #
    def run (self):
        """ Invoke processes in sequence for all test dates as specified
            by the configuration file schedule."""

        try:
           
           # Uncaught exceptions should trigger failure for the run
           try:
     
               for each_config in self.__initFile.processInfo:
                  
                  # If schedule for the process is set to the default one 
                  # (any date of any year), then don't specify test date for 
                  # processing - there is no start and no end dates
                  if each_config.schedule.isDefault() is True:
                      self.__startProcess(each_config)
                      
                  else:    
                      # Step through all dates as specified by the schedule for the
                      # process configuration
                      for each_date in each_config.schedule.dates():
                         
                         self.__startProcess(each_config,
                                             each_date)
                         
                         # Update configuration for the process with processed date
                         each_config.processed(each_date)
                  
           except:
            
              # If exception is raised, report it and print the backtrace
              exc_type, exc_value = sys.exc_info()[:2]
              
              if exc_type is not None and exc_value is not None:
   
                 error_msg = "Exception occured %s = %s" \
                             %(exc_type, exc_value)
                              
                 BatchProcessing.__logger.error(error_msg) 
                 
                 traceback.print_exc()
            
        finally:

           # Send email with status of the run
           self.__sendEmail()


    #----------------------------------------------------------------------------
    #
    # Spawn a process for the test date.
    #
    # Input: 
    #        config - BatchInitFile.ProcessInfo object with configuration
    #                 parameters for Dispatcher process to start.
    #        test_date - Test date to process
    #
    # Output:
    #        None.
    #
    def __startProcess (self, configuration, test_date = None):
       """ Invoke process for the test date."""

       # Write script to be invoked to date-specific script file to preserve
       # content of each script
       __script_name = BatchProcessing.__scriptName
       if test_date is not None:
           __script_name = '%s_%s' %(test_date.date(),
                                     __script_name)
       
       script_path = os.path.join(self.__dir,
                                  __script_name)
       
       fhandle = CSEPFile.openFile(script_path,
                                   CSEPFile.Mode.WRITE)
       
       # Create a script to invoke:
       line = '#!%s\n' %Environment.TCSH_SHELL
       fhandle.write(line)
       
       line = 'source %s;\n' %self.__shellResourceFile
       fhandle.write(line)

       ### Format generic command-line options
       
       # Set date options
       options = ''
       if test_date is not None:
           options = '%s=%s %s=%s %s=%s' %(CommandLineOptions.YEAR,
                                           test_date.year,
                                           CommandLineOptions.MONTH,
                                           test_date.month,
                                           CommandLineOptions.DAY,
                                           test_date.day)

       log_file = None

       # Process common and process specific command-line options
       all_options = self.__initFile.optionsInfo.items()
       all_options.extend(configuration.items())
       
       for key, value in all_options:
          
          if key == CommandLineOptions.LOG_FILE:
             log_file = value 

             if test_date is not None:
                 log_file = "%s_%s-%s-%s" %(value, 
                                            test_date.year, 
                                            test_date.month, 
                                            test_date.day)
             value = log_file
             
             
             # Create directory if it doesn't exist
             dir_path, file_name = os.path.split(log_file)
             
             if os.path.exists(dir_path) is False:
                
                BatchProcessing.__logger.info("Creating directory '%s' for process logs...\n" \
                                              %dir_path)

                os.makedirs(dir_path)
          
          if len(value):
              
              # If test date should appear as part of the option's value,
              # replace it with current date
              if CSEPInitFile.CSEPInitFile.TestDateToken in value:
                 
                 if test_date is not None:
                     value = value.replace(CSEPInitFile.CSEPInitFile.TestDateToken,
                                           '%s' %test_date.date())
 
              options += " %s='%s'" %(key, value)
              
          else:
              options += " %s" %key


       line = 'nohup python %s %s' %(configuration.executable,
                                     options)

       info_msg = "Processing "
       if test_date is not None:
           info_msg += "test date '%s' " %test_date.date()
           
       info_msg += "for process '%s'" %configuration.executable
       
       
       if log_file is not None:

          # Re-direct output and error stream to the log file for the process
          line += ' >& %s' %log_file
          
          info_msg += ' with log file %s' %log_file
          
       BatchProcessing.__logger.info(info_msg)
          
       line += ';\n'   
       
       fhandle.write(line)
       fhandle.close()

       os.chmod(script_path, 0755)
       command_output = Environment.invokeCommand(script_path)

       BatchProcessing.__logger.info("%s output for %s: %s" 
                                     %(configuration.executable,
                                       test_date,
                                       command_output))
       
       # Check if process failed
       if log_file is not None:
           found_errors = [line for line in open(log_file) if \
                           Environment.ErrorHandler.containsError(line)]

           # Remember the failure
           if len(found_errors) != 0:
               self.__failedProcesses[log_file] = found_errors
       
       # Parse process configuration file
       return
       

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
             if len(found_errors) != 0 or len(self.__failedProcesses) != 0:
                # There were errors
                status = "FAILED \n"
                
                if len(found_errors) != 0: 
                    status += "BatchProcessing Errors: %s\n" %"\n".join(found_errors)
                    
                if len(self.__failedProcesses) != 0:
                    
                    for each_log, log_errors in self.__failedProcesses.iteritems():
                        status += "Failed process log file '%s': %s\n" %(each_log, "\n".join(log_errors))
             
             hostname = Environment.commandOutput('hostname').strip()
             now = datetime.datetime.now()

             msg = "CSEP Batch Processing \nStatus: %s\n\n\
Runtime host: %s\n\
Runtime directory: %s\n\n\
Processing start time: %s %s\nProcessing end time: %s %s\
\n\nPlease see %s log file for a detailed report." \
                  %(status,
                    hostname, 
                    self.__dir,
                    self.__startTime.date(), self.__startTime.time(),
                    now.date(), now.time(),
                    self.__options.log_file)
                
             for each_config in self.__initFile.processInfo:
               
                # Report processed date for each configuration
                msg += "\n\nProcessed dates for %s %s: %s" %(each_config.executable,
                                                             each_config[CommandLineOptions.CONFIG_FILE],
                                                             " ".join('%s' %d.date() for d in each_config.dates))  

             
             # Extract status keyword for the email subject
             status_key = status.split('\n')[0]
             
             self.__email.send(msg, 
                               BatchProcessing.__emailSubject, 
                               status_key, 
                               hostname)
             
          except RuntimeError, e:

             # Failed to send email, log the error
             error_msg = "__sendEmail(): failed with error %s." %e
             BatchProcessing.__logger.error(error_msg) 
                        
             raise RuntimeError, error_msg
            

# Invoke the module
if __name__ == '__main__':

   batch_processing = BatchProcessing()
   batch_processing.run()
      
   
   # Shutdown logging
   logging.shutdown()
# end of main
