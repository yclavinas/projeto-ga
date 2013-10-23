"""
Module BatchInitFile
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os
import CSEPInitFile, CSEPLogging, Environment
from CSEPSchedule import CSEPSchedule


#--------------------------------------------------------------------------------
#
# BatchInitFile
#
# This module is designed for parsing of XML format files that represent
# initialization parameters for the batch processing of test dates sequencially.
# These files consist of any combination of the following elements:
#    1. dispatcherConfig - Configuration parameters for Dispatcher process to spawn
#       - Schedule - 'cronjob'-like schedule of dates when to create/evaluate 
#                    group models as defined in Dispatcher configuration file.
#
# NOTE: The purpose of the schedule within BatchInitFile is rather to specify
#       a testing interval than exact test dates for reprocessing. Configuration
#       file for the group specifies exact processing schedule for the group 
#       already. 
#
class BatchInitFile (CSEPInitFile.CSEPInitFile):

    # Static data members

    # Top level directory for the batch processing
    DirectoryElement = 'directory'
    
    ShellResourceElement = 'resourceFile'
    
    # Command-line option prefix
    OptionPrefix = '--'

    __logger = None
    

    # Structure-like class to hold common arguments for processes specified in the
    # configuration file
    class OptionsInfo (dict):

       # Static data of the class
       
       # XML name of element that represents common to all processes command-line
       # options
       XMLElement = "commandLineOptions"

       #
       # Inputs:
       #         doc - ElementTree object representing configuration file
       #         element_name - Tag of xml element
       #
       def __init__(self, doc):
          """ Initialization for OptionsInfo class"""
          
          dict.__init__(self, {})
          
          nodes = doc.elements(BatchInitFile.OptionsInfo.XMLElement)
          xml_elem = nodes[0]
          
          # Apply command-line formatting to each option: 
          # prepend '--' to option name 
          for key, value in xml_elem.attrib.items():
             self[BatchInitFile.OptionPrefix + key] = Environment.replaceVariableReference(Environment.CENTER_CODE_ENV,
                                                                                           value)
          

    # Structure-like class to represent configuration parameters for Dispatchers 
    class ProcessInfo (dict):

       # Static data of the class
       
       # XML name of configuration element for the process
       XMLElement = 'process'

       # XML element attritubes
       __executableAttribute = 'executable'


       #-------------------------------------------------------------------------
       #
       # Initialization
       #
       # Inputs:
       #         doc - ElementTree object representing configuration file
       #         xml_elem - XML element that represents process configuration
       #
       def __init__(self, doc, xml_elem):
          """ Initialization for ProcessInfo class"""

          dict.__init__(self, {})
          
          # Executable for the process
          self.executable = None
          self.schedule = None
          self.__processedDates = []
          
          # XML element attributes
          attribs = xml_elem.attrib
          
          # Extract configuration file 
          if BatchInitFile.ProcessInfo.__executableAttribute not in attribs:
              
             error_msg = "%s attribute is missing for %s element" \
                         %(BatchInitFile.ProcessInfo.__executableAttribute,
                           xml_elem.tag)
                         
             BatchInitFile.__logger.error(error_msg)             

             raise RuntimeError, error_msg
              

          # Store options if any that are specific to the process
          for key, value in attribs.iteritems():
              
             value = Environment.replaceVariableReference(Environment.CENTER_CODE_ENV,
                                                          value)
             
             # Skip name of executable
             if key != BatchInitFile.ProcessInfo.__executableAttribute:
                # Replace occurrences of CENTERCODE environment variable with
                # actual value 
                self[BatchInitFile.OptionPrefix + key] = value
                
             else:
                self.executable = value
                
                if os.path.isabs(self.executable) is False:
                    
                   # Prepend $CENTERCODE to the executable if absolute path is not 
                   # provided
                   self.executable = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                                                  self.executable)
                
          
          # Extract schedule
          self.schedule = doc.schedule(xml_elem)


       #-------------------------------------------------------------------------
       #
       # Register specified date as processed date for the configuration.
       #
       # Inputs:
       #         test_date - Processed test date for the configuration
       #
       def processed(self, test_date):
          """ Register specified date as processed date for the configuration."""
          
          self.__processedDates.append(test_date)
          return


       #-------------------------------------------------------------------------
       #
       # Return list of processed dates
       #
       # Inputs: None
       #
       def __getProcessedDates(self):
          """ Return list of processed test dates."""
          
          return self.__processedDates

       dates = property(fget=__getProcessedDates,
                        doc="Processed test dates")


    # Names for XML format elements
    __XMLTopLevelElements = [ProcessInfo.XMLElement,
                             OptionsInfo.XMLElement,
                             DirectoryElement]

    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #       dir_path - Directory path for the forecast group.
    #       filename - Filename for the input parameters. Default is
    #                  "forecast.init.xml".
    # 
    def __init__ (self, filename = "batch.init.xml"):    
        """ Initialization for BatchInitFile class."""

        CSEPInitFile.CSEPInitFile.__init__(self, filename, 
                                           self.__XMLTopLevelElements)

        if BatchInitFile.__logger is None:
           BatchInitFile.__logger = CSEPLogging.CSEPLogging.getLogger(BatchInitFile.__name__)
           
        
        if self.exists() is False:
           error_msg = "%s configuration file does not exist." \
                       %(filename)
                         
           BatchInitFile.__logger.error(error_msg)             

           raise RuntimeError, error_msg
           

        # Extract publish info
        self.__optionsInfo = BatchInitFile.OptionsInfo(self)
        
        # Extract Dispatcher info
        self.__processInfo = []
        for elem in self.elements(BatchInitFile.ProcessInfo.XMLElement):
           self.__processInfo.append(BatchInitFile.ProcessInfo(self,
                                                               elem))
           
        self.__directory = self.elementValue(BatchInitFile.DirectoryElement) 

        self.__resourceFile = '~/.tcshrc'
        resource_from_config_file = self.elementValue(BatchInitFile.ShellResourceElement)
        if resource_from_config_file is not None:
            self.__resourceFile = resource_from_config_file
            

    #----------------------------------------------------------------------------
    #
    # Get common to all processes command-line arguments
    # 
    # Input: None
    #
    # Output:
    #         OptionsInfo object.
    #
    def __getOptionsInfo (self):
        """ Acquire common command-line arguments."""

        return self.__optionsInfo

    optionsInfo = property(__getOptionsInfo, 
                           doc="Common to all processes command-line arguments") 
    

    #----------------------------------------------------------------------------
    #
    # Get configuration for processes to spawn
    # 
    # Input: None
    #
    # Output:
    #         List of ProcessInfo objects.
    #
    def __getProcessInfo (self):
        """ Acquire configuratin parameters for all processes to spawn."""

        return self.__processInfo

    processInfo = property(__getProcessInfo, 
                           doc="All processes configurations") 

    #----------------------------------------------------------------------------
    #
    # Get top level directory for the batch processing
    # 
    # Input: None
    #
    # Output:
    #         Directory path.
    #
    def __getDirectory (self):
        """ Acquire top level directory for batch processing."""

        return self.__directory

    directory = property(__getDirectory, 
                         doc="Top level directory for batch processing") 


    #----------------------------------------------------------------------------
    #
    # Get top level directory for the batch processing
    # 
    # Input: None
    #
    # Output:
    #         Directory path.
    #
    def __getResourceFile (self):
        """ Acquire shell resouce file for batch processing."""

        return self.__resourceFile

    resourceFile = property(__getResourceFile, 
                            doc="Shell resource file for batch processing") 


# Invoke the module
if __name__ == '__main__':

   import DispatcherOptionParser
   from CSEPOptions import CommandLineOptions

   parser = DispatcherOptionParser.DispatcherOptionParser()
        
   # List of requred options
   required_options = [CommandLineOptions.CONFIG_FILE]
   init_file = BatchInitFile(parser.options(required_options).config_file)
   
   CSEPLogging.CSEPLogging.getLogger(BatchInitFile.__name__).debug("Init file exists: %s" \
                                                                   %init_file.exists())

   print "Directory=", init_file.directory
   
   common_info = init_file.optionsInfo
   print "CommonInfo=", common_info

   all_info = init_file.processInfo
   for info in all_info:
      print "Process: executable=", info.executable, \
            "opions=", info
   
# end of main

