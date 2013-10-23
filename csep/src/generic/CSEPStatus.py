"""
Module CSEPStatus
"""

__version__ = "$Revision: 3287 $"
__revision__ = "$Id: CSEPStatus.py 3287 2011-03-31 19:00:49Z  $"


import sys, os, inspect

import CSEPFile, Environment, CSEP
from CSEPPropertyFile import CSEPPropertyFile
from ForecastFactory import ForecastFactory


#--------------------------------------------------------------------------------
#
# CSEPStatus.
#
# This class is designed to acquire current CSEP system and software status.
#
class CSEPStatus:

    # Static data members
    
    # Name of the file with system status information.
    SystemType = "SystemStatus"

    # Name of the file with CSEP software status information.
    SoftwareType = "SoftwareStatus"

    # Dictionary of commands that used to capture external software version and
    # flag if command output is on stderr (True). If command output is redirected
    # to the stderr, the flag should be set to 'True' so CSEP would not trigger
    # it as a failure
    __allPackages = {"awk --version" : False, # awk version
                     "sed --version" : False, # sed version
                     "java -version" : True,  # Java output info to stderr
                     "R --version" : False,
                     "python -c 'import matplotlib; print matplotlib.__version__;'" : False,
                     "python -c 'import numpy; print numpy.__version__;'" : False,
                     "python -c 'import scipy; print scipy.__version__;'" : False,
                     "python -c 'import mpl_toolkits.basemap; print mpl_toolkits.basemap.__version__;'" : False}
    
    __classMethodForExternalSoftware = 'externalSoftwareVersions'
    __ifortVersionFile = 'ifort.version'
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    #        options - Command-line options including defaults ones used
    #                  by caller program. Default is None.
    # 
    def __init__ (self, options = None):
        """ Initialization for CSEPStatus class"""
        
        self.__options = options
        
        ifort_command = 'ifort --version'
        ifort_version_path = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                          'ReasenbergDecluster',
                                          CSEPStatus.__ifortVersionFile) 
        if os.path.exists(ifort_version_path) is True and \
           ifort_command not in CSEPStatus.__allPackages:
                           
            version_file = CSEPFile.openFile(ifort_version_path)
            CSEPStatus.__allPackages[ifort_command] = version_file.read()
        

    #--------------------------------------------------------------------
    #
    # Get names of the files for system status.
    #
    # Input: None.
    #
    # Output: A tuple of data and corresponding metadata filenames. 
    #            
    def systemFilename (self):
        """ Get the name of the system status file."""

        filenames = CSEPPropertyFile.filenamePair(CSEPStatus.SystemType)
        
        return filenames
     
     
    #--------------------------------------------------------------------
    #
    # Get names of the files for system status.
    #
    # Input: None.
    #
    # Output: A list of data filename and corresponding metadata filename. 
    #            
    def softwareFilename (self):
        """ Get the name of the software status file."""

        filenames = CSEPPropertyFile.filenamePair(CSEPStatus.SoftwareType)
                
        return filenames     
     

    #--------------------------------------------------------------------
    #
    # Capture status of the system.
    #
    # Input:
    #          filenames - Names of the file and metadata file to capture status 
    #                          information to. Default is None.
    #
    # Output: None.
    #
    def system (self, filenames = None):
        """ Capture system status to the file."""

        if filenames == None:
           filenames = self.systemFilename()

        # Unpack the sequence
        datafile, metafile = filenames

        # Create data file
        fhandle = CSEPFile.openFile(datafile, 
                                    CSEPFile.Mode.WRITE)
        
        # Store host info
        CSEPPropertyFile.write(fhandle, "os.uname", os.uname())
        
        # Store user info
        command = "id"
        CSEPPropertyFile.write(fhandle, command, Environment.commandOutput(command))
        
        # Store environment variables
        CSEPPropertyFile.write(fhandle, "os.environ", os.environ)

        # Store executable and command-line options
        CSEPPropertyFile.write(fhandle, "sys.argv", sys.argv)
        
        # Store executable and command-line options including the default ones
        if self.__options is not None:
           CSEPPropertyFile.write(fhandle, 
                                  "command-line options (including defaults)", 
                                  self.__options)
        
        # Close the file
        fhandle.close()


        # Create metadata file
        comment = "System status file."
        CSEPPropertyFile.createMetafile(metafile, 
                                        comment,
                                        CSEPFile.Format.ASCII,
                                        comment)
        

    #--------------------------------------------------------------------
    #
    # Capture status of the software used by the system.
    #
    # Input:
    #          program_name - Name of the calling program.
    #          program_version - Version of the calling program.
    #          filenames - Names of the file and metadata file to capture status 
    #                          information to. Default is None.
    #
    # Output: None.
    #
    def software (self, program_name, program_version, filenames = None):
        """ Capture software status to the file."""

        # Collect commands from installed forecasts models to capture versions of
        # software packages they depend on
        for each_type in ForecastFactory().keys():
            
            # Examine class if it has static function with commands for external
            # packages versions
            class_func = inspect.getmembers(ForecastFactory().classReference(each_type), 
                                            inspect.isfunction)
            for name, func in class_func:
                if name == CSEPStatus.__classMethodForExternalSoftware:
                    sw_dict = func()

                    # Check if returned dictionary:
                    # dict of command and boolean flag if command output is redirected
                    # to stdout ---> commands are provided to capture the version of
                    #    external sofware
                    # dict of command and version string ---> command was already 
                    #    issued to capture the version
                    for key, value in sw_dict.iteritems():
                       if key not in CSEPStatus.__allPackages:
                           CSEPStatus.__allPackages[key] = value  
                
                
        if filenames == None:
           filenames = self.softwareFilename()

        # Unpack the sequence
        datafile, metafile = filenames

        # Create data file
        fhandle = CSEPFile.openFile(datafile, 
                                    CSEPFile.Mode.WRITE)

        # Store version of calling program
        CSEPPropertyFile.write(fhandle, program_name, program_version)
        
        # Store python version
        CSEPPropertyFile.write(fhandle, "python sys.version", sys.version)

        for command, output_on_stderr in CSEPStatus.__allPackages.iteritems():
            if isinstance(output_on_stderr, bool) is True:
                # Version command is provided
                CSEPPropertyFile.write(fhandle, 
                                       command,
                                       Environment.commandOutput(command,
                                                                 output_on_stderr))
            else:
                # Version string is provided in 'output_on_stderr' local variable
                CSEPPropertyFile.write(fhandle, command, output_on_stderr)
        
        # GMT version if map generation is enabled
        if CSEP.Forecast.GenerateMap is True:
           command = "%s -v" %os.path.join(os.environ[Environment.GMT_HOME_ENV],
                                           "GMT")
           # GMT version information is output to stderror instead of stdout (?)
           output_on_stderr = True
           CSEPPropertyFile.write(fhandle, 
                                  command, 
                                  Environment.commandOutput(command,
                                                            output_on_stderr))

        # Close the file
        fhandle.close()

       
        # Create metadata file
        comment = "Software status file."
        CSEPPropertyFile.createMetafile(metafile, 
                                        comment,
                                        CSEPFile.Format.ASCII,
                                        comment)
        
        
    #--------------------------------------------------------------------
    #
    # Get user name of the running process.
    #
    # Input: None.
    #
    # Output: A username.
    #            
    def userName ():
        """ Get the user name of the running process."""

        name = Environment.commandOutput("whoami")
        
        # Strip newline if any
        return name.replace("\n", "")
     
    userName = staticmethod(userName) 
    

# Invoke the module
if __name__ == '__main__':

   status = CSEPStatus()

   CSEP.Forecast.GenerateMap = True
   
   # System status
   filenames = status.systemFilename()
   status.system(filenames)
        
   # Software status
   filenames = status.softwareFilename()
   status.software(CSEPStatus.SoftwareType, "0.0.1", filenames)     

# end of main     
                        
