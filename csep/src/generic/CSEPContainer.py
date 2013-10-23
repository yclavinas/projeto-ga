"""
CSEPContainer module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import copy

from CSEPSchedule import CSEPSchedule
from CSEPInputParams import CSEPInputParams
import CSEPLogging


#--------------------------------------------------------------------------------
#
# This module contains CSEP container class that is derived from Python standard
# list class and serves as a set of related objects with associated CSEPSchedule
# element.
#
class CSEPContainer (list): 
   
   # Static data of the class

   __logger = None
   
   
   #-----------------------------------------------------------------------------
   #
   # Initialization.
   #
   # Input:
   #        schedule - Schedule for container objects. Default is "every day".   
   #        obj_factory - Factory to use to construct objects. Default is None.
   #        obj_types - String of keywords identifying types of container 
   #                    objects to construct. Default is None.
   #        common_inputs - Common input arguments for all objects. Default is
   #                        an empty list.
   #        obj_inputs - String of inputs used to construct container objects. 
   #                     Default is None.
   # 
   def __init__ (self, 
                 schedule = CSEPSchedule(),
                 obj_factory = None,
                 obj_types = None,
                 common_inputs = [],
                 obj_inputs = None):
      """ Initialization for CSEPContainer class."""
      
      # Construct empty list
      list.__init__(self, [])
   
      if CSEPContainer.__logger is None:
         CSEPContainer.__logger = CSEPLogging.CSEPLogging.getLogger(CSEPContainer.__name__)
         
      # Set schedule
      if schedule is None:
         
         error_msg = "Null CSEPSchedule object is specified for %s factory." \
                     %obj_factory
                     
         CSEPContainer.__logger.error(error_msg)
         raise RuntimeError, error_msg
      
      self.__schedule = schedule

      self.addObjects(obj_factory, 
                      obj_types, 
                      common_inputs,
                      obj_inputs)
      
         
   #-----------------------------------------------------------------------------
   #
   # Create and add new objects to the container.
   #
   # Input: 
   #        obj_factory - Factory to use to construct objects. Default is None.
   #        obj_types - String of keywords identifying types of container 
   #                    objects to construct. Default is None.
   #        obj_inputs - String of inputs used to construct container objects. 
   #                     Default is None.
   #        input_separator - Character to use as object inputs separator. 
   #                          Default is CSEPInputParams.InputSeparator.
   #    
   # Output: None
   #
   def addObjects(self,
                  obj_factory = None,
                  obj_types = None,
                  common_inputs = [],
                  obj_inputs = None,
                  inputs_separator = CSEPInputParams.InputSeparator):
      """Create and add new objects to the container."""

      if obj_factory is not None and \
         obj_types is not None and \
         len(obj_types.strip()) != 0:
         
         types = obj_types.split()

         CSEPContainer.__logger.info("%s: objects of %s types" \
                                     %(obj_factory.type(),
                                       types))
       
         # If input arguments were not provided, generate None entry per model
         inputs = [None] * len(types)
         
         if obj_inputs is not None:
            inputs = obj_inputs.split(inputs_separator)
            
            if len(types) != len(inputs):
               error_msg = "Inconsistent number of object types %s vs. number of \
   object inputs %s is provided." %(types, inputs)
   
               CSEPContainer.__logger.error(error_msg)
               raise RuntimeError, error_msg
              
            # Strip preceeding and trailing spaces
            inputs = [key.strip() for key in inputs]
            CSEPContainer.__logger.info("%s: object inputs are: %s" \
                                        %(obj_factory.type(), 
                                          inputs))
      
         # Instantiate models objects
         for each_type, input_args in zip(types, inputs):
            # A list of input arguments for each model:
            # one required argument - directory path for the forecast files
            # string that represents optional input arguments for the model
            args = copy.copy(common_inputs)
            if input_args is not None and len(input_args) != 0:
               args.append(input_args)
            
            CSEPContainer.__logger.info("Adding %s object with inputs %s" 
                                        %(each_type, args))   
            self.append(obj_factory.object(each_type,
                                           args))
      

   #-----------------------------------------------------------------------------
   #
   # Sets new schedule for the objects of container.
   #
   # Input: 
   #        new_schedule - New schedule object.
   #    
   # Output:
   #        List of indices.
   #
   def __setSchedule(self, new_schedule):
      """Sets new schedule for container objects."""
      
      self.__schedule = new_schedule


   def __getSchedule(self):
      """Gets schedule for container objects."""
      
      return self.__schedule
      
         
   schedule = property(__getSchedule, 
                       __setSchedule,
                       doc = "Schedule for container object")


   #-----------------------------------------------------------------------------
   #
   # Checks if specified date is in the schedule for container objects if any.
   #
   # Input: 
   #        test_date - datetime object. Default is None.
   #    
   # Output:
   #        True if date is in the schedule or date is not specified, 
   #        False otherwise.
   #
   def hasDate(self, test_date = None):
      """Checks if specified date is in the schedule for container objects if any."""

      result = True
        
      if test_date is not None:
         result = self.__schedule.has(test_date)
       
      return (result and len(self) != 0)
      

   #----------------------------------------------------------------------------
   # any()-like implementation for CSEPContainer given method name of all 
   # elements within container
   #
   # Inputs: 
   # method_name - Method to invoke for each element of the container to
   #               get return value of any()
   # 
   # Output: True if any object.method_name() is True within container,
   #         False otherwise
   # 
   def any(self, method_name):
      """any() implementation for specified method of all objects within container."""
      
      # Step through all objects of the container
      for each_elem in self:
          if getattr(each_elem, method_name)() is True:
              return True
          
      return False

