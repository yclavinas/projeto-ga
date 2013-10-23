"""
Module DispatcherOptionParser
"""

__version__ = "$Revision: 2910 $"
__revision__ = "$Id: DispatcherOptionParser.py 2910 2010-04-16 06:02:42Z liukis $"


import sys

import CSEPOptionParser
from CSEPOptions import CommandLineOptions


#--------------------------------------------------------------------------------
#
# DispatcherOptionParser.
#
# This class is designed to parse command line options specific to Dispatcher.
# This class is inherited from CSEPOptionParser.
#
class DispatcherOptionParser (CSEPOptionParser.CSEPOptionParser):

    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: None.     
    # 
    def __init__ (self):
        """ Initialization for DispatcherOptionParser class."""
        
        CSEPOptionParser.CSEPOptionParser.__init__(self)
        
        # Define generic options
        self.add_option(CommandLineOptions.CONFIG_FILE, 
                        dest="config_file", 
                        type="string",
                        help="Configuration file. Default is \"dispatcher.init.xml\".", 
                        metavar="FILE",
                        default="dispatcher.init.xml")
        
        self.add_option(CommandLineOptions.WAITING_PERIOD, 
                        dest="waiting_period", 
                        type="int",
                        help="Waiting period for the test in days - by how many days \
to offset specified test date into the past. Default is 30 days.", 
                        metavar="DAYS",
                        default=30)

        self.add_option(CommandLineOptions.PUBLISH_SERVER, 
                        dest="publish_server", 
                        type="string",
                        help="Username and server for publishing \
results plots to the external web server. Default is None.", 
                        metavar="USER@SERVER",
                        default=None)

        self.add_option(CommandLineOptions.PUBLISH_DIR, 
                        dest="publish_dir", 
                        type="string",
                        help="Directory on remote server to publish \
results plots to. Default is an empty string (home directory on remote server will \
be used).", 
                        metavar="DIR",
                        default='')

        self.add_option(CommandLineOptions.PUBLISH_RUNTIME_SERVER, 
                        dest="publish_runtime_info_server", 
                        type="string",
                        help="Username and server for publishing \
runtime information (directory with raw data and log file) to the external web server. Default is None.", 
                        metavar="USER@SERVER",
                        default=None)

        self.add_option(CommandLineOptions.PUBLISH_RUNTIME_DIR, 
                        dest="publish_runtime_info_dir", 
                        type="string",
                        help="Directory on remote server to publish \
runtime information (directory with raw data and log file) to. Default is an empty string (the same directory on remote server will \
be used as the one on publishing server).", 
                        metavar="DIR",
                        default='')
# end of class

        
# Invoke the module
if __name__ == '__main__':

   import CSEPLogging
   
   
   parser = DispatcherOptionParser()
        
   # List of requred options
   required_options = [CommandLineOptions.YEAR,
                       CommandLineOptions.MONTH,
                       CommandLineOptions.DAY]
   options = parser.options(required_options)
  
   CSEPLogging.CSEPLogging.getLogger(DispatcherOptionParser.__name__).info("Options: %s" %options)

