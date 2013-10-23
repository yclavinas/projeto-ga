"""
Module CSEPEventHandler
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import CSEPLogging


#--------------------------------------------------------------------------------
#
# CSEPEventHandler.
#
# This class is designed for handling events within CSEP testing framework.
#
class CSEPEventHandler (object):

    # Static data of the class
      
    # Logger object for the class  
    __logger = None 
    
      
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        other_handler - Event handler to copy. Default is an empty list.
    # 
    def __init__ (self, other_handler = []):
        """ Initialization for CSEPEventHandler class"""

        if CSEPEventHandler.__logger is None:
           CSEPEventHandler.__logger = CSEPLogging.CSEPLogging.getLogger(CSEPEventHandler.__name__)

#        for index in xrange(1,4):
#            CSEPEventHandler.__logger.info("%s: Initializing %s handler for %s: %s"
#                                           %(index, self, other_handler,
#                                             CSEPLogging.CSEPLogging.frame(self.__class__, 
#                                                                           index)))

        # Registered handlers for the event
        self.__handlers = other_handler
        
        if isinstance(other_handler, CSEPEventHandler):
            self.__handlers = other_handler.copy()
        
        if isinstance(other_handler, dict):
            # To support DataSourceComposite which is a dictionary of CatalogDataSource
            # (introduced for Transient Detection project that uses multiple data
            #  sources)
            self.__handlers = []
            
            for each_handler in other_handler.values():
                self.__handlers.extend(each_handler.copy())
        

    #----------------------------------------------------------------------------
    #
    # Fire event handler if there are any registered
    #
    # Input: 
    #        input_variables - Input variables to be passed to the event handler.
    #                          Default is None.
    # 
    # Output: None
    # 
    def fire (self, input_variables = None):
        """ Fire event handler if there are any registered."""

        for each_event in self.__handlers:
            
            CSEPEventHandler.__logger.info("Invoking %s.%s registered handler for %s."
                                           %(each_event.im_self.__class__.__name__,
                                             each_event.__name__,
                                             input_variables))
            if input_variables is not None:
                each_event(*input_variables)
            else:
                each_event()
                

    #----------------------------------------------------------------------------
    #
    # Register event handler.
    #
    # Input: 
    #        event_handler - Event handler
    # 
    # Output: None
    # 
    def registerHandler (self, event_handler):
        """ Register event handler."""

        # Check if handler is not registered yet
        if event_handler not in self.__handlers:
              
            self.__handlers.append(event_handler)


    #----------------------------------------------------------------------------
    #
    # Return registered event handlers
    #
    # Input: 
    #        event_handler - Event handler
    # 
    # Output: None
    # 
    def copy (self):
        """ Register event handler."""

        # Check if handler is not registered yet
        return list(self.__handlers)

