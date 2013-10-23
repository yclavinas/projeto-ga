"""
Module CSEPLock
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os, time, shutil, socket, ConfigParser

import CSEPLogging, CSEPFile


class DirLock (object):
    """ This class represents an interface to create and to remove lock pid 
        files for directories."""

    # Static data of the class
    
    # Logger for the class
    __logger = None
    
    # Sub-directory that is used as "lock" for the directory
    __lock = 'lock'
    
    # File that stores process information that issued an existing lock
    __config = 'config.txt'
    
    # Keywords used to store process id in configuration file
    __processSection = "process"
    __pidElement = 'pid'
    __hostElement = 'host'
    
    # Number of seconds to sleep b/w re-tries to create a lock
    __sleepSeconds = 5
    
    # How often to report if directory is locked by another process
    __reportSeconds = 300

    # Expected exception when directory lock is already created by other process
    __exceptionMsg = 'File exists'
    

    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #
    #        dir_path - Path to the directory to be locked.
    # 
    def __init__ (self, 
                  dir_path):
        """ Initialization for DirLock class"""

        if DirLock.__logger is None:
           DirLock.__logger = CSEPLogging.CSEPLogging.getLogger(DirLock.__name__)
           
        # ID and hostname of the process acquiring the lock
        self.__pid = os.getpid()
        self.__host = socket.gethostname()
           
        # Full path to the sub-directory that repsents a "lock" 
        self.__lockDir = os.path.join(dir_path,
                                      DirLock.__lock)
        
        # File with latest process id that acquired the lock
        self.__configFile = os.path.join(self.__lockDir,
                                         DirLock.__config)
        
        # Flag if lock was successfully created
        created_lock = False
        last_time_checked = time.time()
        
        DirLock.__logger.info("Process '%s@%s' acquiring lock for directory '%s'" 
                              %(self.__pid, self.__host,
                                dir_path))
        
        while created_lock is False:
           
           # Try to acquire the lock for the directory
           try:

              # Create lock sub-directory in atomic operation
              os.makedirs(self.__lockDir)
              created_lock = True

              DirLock.__logger.info("Process '%s@%s' created a lock for directory '%s'" 
                                    %(self.__pid, self.__host,
                                      dir_path))
              
           except OSError, exc:
              
              # Re-raise exception if it's not of expected content
              if DirLock.__exceptionMsg not in exc:
                 raise
                 
                 
              # Lock exists, try again later
              time.sleep(DirLock.__sleepSeconds)
              
              # Report once in a while if directory is still locked by some other
              # process
              time_passed = time.time() - last_time_checked
              if time_passed > DirLock.__reportSeconds:
                 
                 last_time_checked = time.time()
                 
                 # Check if file already exists - if a race condition in 
                 # creating the lock 
                 pid, host = self.__read()
                 if pid is not None:
                    
                    DirLock.__logger.info("Process '%s@%s': directory '%s' is locked by '%s@%s'" 
                                          %(self.__pid, self.__host,
                                            dir_path, pid, host))
                    
                    if pid == self.__pid and host == self.__host:
                       # Directory is locked by the same process that acquires
                       # the lock
                       DirLock.__logger.info("Process '%s@%s': directory '%s' is already locked by itself '%s@%s'" 
                                             %(self.__pid, self.__host,
                                               dir_path, pid, host))
                       created_lock = True
                       
        
        # Create the process information file
        pid_config = ConfigParser.ConfigParser()
         
        # set a number of parameters
        pid_config.add_section(DirLock.__processSection)
        pid_config.set(DirLock.__processSection, 
                       DirLock.__pidElement, "%s" %self.__pid)        
        pid_config.set(DirLock.__processSection, 
                       DirLock.__hostElement, self.__host)        
        
        
        # Write process info to the "lock" directory
        process_file = CSEPFile.openFile(self.__configFile,
                                         CSEPFile.Mode.WRITE)

        pid_config.write(process_file)
        process_file.close()
              

    #----------------------------------------------------------------------------
    #
    # Remove lock for the directory.
    #
    # Input: None
    #
    # Output: None
    # 
    def release (self):
       """ Remove lock directory if it exists."""
       
       pid, host = self.__read()
       
       # Lock was created by "this" process
       if pid == self.__pid and host == self.__host:
          
          DirLock.__logger.info("Process '%s@%s' released a lock for '%s"
                                %(self.__pid, self.__host, 
                                  self.__lockDir))
          shutil.rmtree(self.__lockDir)
       
       # Lock exists, but was created by other than "this" process
       elif os.path.exists(self.__lockDir):
          
          error_msg = "Process '%s@%s' can't release the lock for '%s': \
it is locked by other process '%s@%s'" %(self.__pid, self.__host,
                                         self.__lockDir,
                                         pid, host)
                                  
          DirLock.__logger.error(error_msg)
          raise RuntimeError, error_msg


    #----------------------------------------------------------------------------
    #
    # Read configuration file from lock directory
    #
    # Input: None
    #
    # Output:
    #        Tuple of process id and hostname if file exists, tuple of None's
    #        otherwise  
    # 
    def __read (self):
       """ Read configuration file from lock directory."""

       # Check if lock configuration file exists:
       if os.path.exists(self.__configFile) is True:
          
          # Read process configuration file - to make sure that it was created by
          # the same process:
          pid_config = ConfigParser.ConfigParser()
          pid_config.read(self.__configFile)
          
          return (int(pid_config.get(DirLock.__processSection,
                                     DirLock.__pidElement)),
                  pid_config.get(DirLock.__processSection,
                                     DirLock.__hostElement))                   
             
       # File does not exist - return None values
       return (None, None)

          
# Invoke the module
if __name__ == '__main__':

   import CSEPOptionParser

   parser = CSEPOptionParser.CSEPOptionParser()
        
   # List of requred options
   options = parser.options()
   
   lock = DirLock(options.test_dir)

   time.sleep(100)
   lock.release()
   