"""
Module Environment
"""

__version__ = "$Revision: 3217 $"
__revision__ = "$Id: Environment.py 3217 2011-01-08 06:17:33Z  $"


# Specify import entities
#__all__ = ['Environment', 'CENTER_CODE_ENV', 'MPICH2_ENV', 'NAMESPACE',
#          'commandOutput', 'BASH_SHELL', 'NETCDF_HOME_ENV',
#           'GMT_HOME_ENV', 'IMAGE_MAGICK_HOME_ENV']

import os, subprocess, itertools
import CSEPLogging

# Environment variable pointing to the source code top level directory
CENTER_CODE_ENV = "CENTERCODE"

# Environment variable pointing to the MPICH2 top level directory
MPICH2_ENV = "MPICH2"
ETAS_R_PACKAGE_ENV = "ETAS_R_PACKAGE"

# Environment variable pointing to the top-level GMT installation directory
GMT_HOME_ENV = "GMTHOME"

# Environment variable pointing to the top-level netCDF library installation 
# directory
NETCDF_HOME_ENV = "NETCDFHOME"

# Environment variable pointing to the top-level ImageMagick library 
# installation directory
IMAGE_MAGICK_HOME_ENV = "IMAGEMAGICKHOME"


#--------------------------------------------------------------------------------
#
# Environment.
#
# This class is designed to store environment configuration.
#
class Environment:

    # Initialization raises a KeyError if required variable is not in the 
    # dictionary
    Variable = {CENTER_CODE_ENV: os.environ[CENTER_CODE_ENV]}
         

#----------------------------------------------------------------------------
#
# Replace occurrences of environment variable within input string with 
# the value the variable is set to
# 
# Input: var - Environment variable to replace if it appears as part of the 
#              input string
#        value_str - Input string that includes a reference to environment
#                    variable 'var'  
#
# Output:
#         String that has reference to environment variable replaced with
#         it's value
#
def replaceVariableReference (var, 
                              value_str):
    """ Replace occurrences of environment variable within input string with 
    the value the variable is set to."""

    if value_str is None:
        return None
    
    new_str = value_str
    
    if var in os.environ:
        new_str = value_str.replace(var,
                                    os.environ[var])
        
    # If environment variable represents a path --> normalize the path 
    # Check for an empty path: 'normpath' inserts '.' if it's empty
    if len(new_str) != 0:
        new_str = os.path.normpath(new_str)

    return new_str
    
             
#===============================================================================
# Class to handle error strings within CSEP Testing Framework
#===============================================================================
class ErrorHandler (object):

    # Set of tokens that trigger error condition if any of these tokens appear
    # in the log file of running process
    __errorStrings = frozenset(['ERROR',
                                'Error',
                                'fail',
                                'Fail'])
    
    # Ignore word combinations that might contain error triggering tokens
    __ignoreStrings = set(['LOCATION ERRORS IGNORED']) # Message from Reasenberg declustering algorithm
    
                 
    #---------------------------------------------------------------------------
    #
    # Check if specified string contains any of tokens that determine a failure
    # condition.
    #
    @staticmethod
    def containsError(line):
        """Check if specified string contains any of tokens that determine a 
           failure condition."""

           
        for token in itertools.ifilter(line.__contains__, 
                                       ErrorHandler.__errorStrings):
            for ignore_token in itertools.ifilter(line.__contains__, 
                                                  ErrorHandler.__ignoreStrings):
                return False
            
            return True
            
        return False


    #---------------------------------------------------------------------------
    #
    # Expand set of words combinations to ignore when triggering a failure 
    # condition
    #
    @staticmethod
    def addIgnoreString(expression_to_ignore):
        """Expand ErrorHandler.__ignoreStrings"""

        if expression_to_ignore in ErrorHandler.__errorStrings:
            
            error_msg = "Can not exclude provided string '%' from defined error tokens '%s'" \
                        %(expression_to_ignore, 
                          ErrorHandler.__errorStrings)
            CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg) 
           
            raise RuntimeError, error_msg
    
    
        CSEPLogging.CSEPLogging.getLogger(__name__).info("Updating __ignoreStrings with '%s'" \
                                                         %expression_to_ignore)
        ErrorHandler.__ignoreStrings.add(expression_to_ignore)
        return

             
#--------------------------------------------------------------------------------
#
# Invoke command from the shell.
# 
# Input: 
#         command - Command to invoke from the shell
#         ignore_error - Flag if standard error output should be ignored. 
#                        Default is False.
#
# Output: Command output if any
#
def invokeCommand (command, ignore_error = False):
    """ Invoke command from the shell."""
     
    CSEPLogging.CSEPLogging.getLogger(__name__).info("Invoking command: %s" 
                                                     %command)
     
    # Execute command using the UNIX shell
    child = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    child_data, child_error = child.communicate()

    # Output any stdout of the child process even in case of the failure
    if child_data is not None and len(child_data):
        CSEPLogging.CSEPLogging.getLogger(__name__).info("Command stdout: %s" 
                                                         %child_data)
     
    if child_error:
       
       if ignore_error is False:
           error_msg = "Child process '%s' failed with error code %s" \
                       %(command, child_error)
           CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg) 
           
           raise RuntimeError, error_msg
        
       else:
           
           CSEPLogging.CSEPLogging.getLogger(__name__).info('Command stderr: %s' 
                                                            %child_error)
           # Explicitly check for any failures
           if ErrorHandler.containsError(child_error) is True:
               
               error_msg = "Child process '%s' failed with error code %s" \
                           %(command, child_error)
               CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg) 
           
               raise RuntimeError, error_msg

        
    return child_data


#--------------------------------------------------------------------------------
#
# Get output of the command from the shell.
# 
# Input: 
#         command - Command to invoke from the shell
#         output_on_stderr - Flag if expected command output is returned to 
#                            stderr instead of stdout. Default is False.
#
# Output: Command output.
#
def commandOutput (command, 
                   output_on_stderr = False):
    """ Get output from the shell command."""
     
    # Execute command using the UNIX shell
    child = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    child_data, child_error = child.communicate()
     
    if child_error and output_on_stderr is False:
        error_msg = "Child process '%s' failed with error code %s" \
                    %(command, child_error)
        CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg) 
        
        raise RuntimeError, error_msg

    # Check for non-empty result string from the command
    if (child_data is None or len(child_data) == 0) and \
       output_on_stderr is False:
        error_msg = "Child process '%s' returned no data." %command
        
        CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)        
        raise RuntimeError, error_msg
     
    # If command output is on stderr 
    if output_on_stderr is True:
       child_data = child_error
     
    return child_data


# Path to the shell
BASH_SHELL = commandOutput("which bash")
TCSH_SHELL = commandOutput("which tcsh")


