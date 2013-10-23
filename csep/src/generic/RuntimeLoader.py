"""
Module RuntimeLoader

Designed to load Python modules at runtime.
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import sys, re

import CSEPLogging, Environment


class RuntimeLoader:
   
   # Static data of the class
   
   # XML format element to provide module to load at runtime
   __moduleElement = 'module'
   
   # XML format element to provide additional Python path to add at runtime   
   __pathElement = 'path'
   

   #============================================================================
   # Initialize method for RuntimeLoader class
   #
   # Input:
   #        init_file - CSEPInitFile object
   # 
   #============================================================================
   def __init__ (self, init_file):
       """ Initialize method. """
       
       self.__configFile = init_file

       # Update Python path
       self.__updatePythonPath()
       
   
   #============================================================================
   # Extract Python paths (if any) from configuration file and add them to 
   # sys.path at runtime
   #
   # Input: None
   # 
   #============================================================================
   def __updatePythonPath(self):
       """ Extract Python paths (if any) from configuration file and add them to 
           sys.path at runtime"""
           
              
       # Update Python search path before loading the modules
       all_paths = self.__configFile.elements(RuntimeLoader.__pathElement)
       if len(all_paths) != 0:

          # Get additional Python paths required by installed forecasts models
          for each_path in all_paths[0].text.strip().split(':'):
              
             # Replace any occurrences of CENTERCODE with actual path
             norm_path = Environment.replaceVariableReference(Environment.CENTER_CODE_ENV,
                                                              each_path.strip())
             # Insert provided path at the beginning of the PYTHONPATH to
             # guarantee that modules will be loaded from these paths
             # First, check if path is already in the sys.path
             if sys.path.count(norm_path) == 0:
                sys.path.insert(0, norm_path)
                CSEPLogging.CSEPLogging.getLogger(RuntimeLoader.__name__).info("Updating PYTHONPATH with %s" \
                                                                               %norm_path)   


   #============================================================================
   # Generator method that iterates through all module elements and
   # class references specified by each module in configuration 
   # file.
   #
   # Input:
   #        parent_class - Base class for each class loaded from
   #        parent_element - Parent element from configuration file to which
   #                         module element belongs to. Default is None.
   #        num_to_allow - Optional argument to specify how many modules are 
   #                       allowed to be specified (for example, only one module
   #                       for each parent_element). Default is None, meaning 
   #                       unlimited number is allowed.   
   # 
   # Output:
   #        Tuple of CSEPFile module element and class reference as loaded
   #        from that module
   #  
   #============================================================================
   def eachModuleClass(self, 
                       parent_class, 
                       parent_element = None, 
                       num_to_allow = None):
       """ Generator method that iterates through all module elements and
           class references specified by each module in configuration file"""
           
       all_modules = []
       if parent_element is None: 
           all_modules = self.__configFile.elements(RuntimeLoader.__moduleElement)
       else:
           all_modules = self.__configFile.children(parent_element,
                                                    RuntimeLoader.__moduleElement)
       
       if num_to_allow is not None:
           if len(all_modules) > num_to_allow:
               
               error_msg = 'More than %s allowed number of modules is provided by %s file for %s class' \
                           %(num_to_allow,
                             self.__configFile.name,
                             parent_class)
                           
               CSEPLogging.CSEPLogging.getLogger(RuntimeLoader.__name__).error(error_msg)
               raise RuntimeError, error_msg
           
       # Load modules specified by the file
       for module_elem in all_modules:   
          
          yield (module_elem, RuntimeLoader.getClass(module_elem.text.strip(), 
                                                     parent_class))

   
   #-----------------------------------------------------------------------------
   #
   # moduleClassNames
   #
   # This method returns a tuple of parsed out module and it's class names
   #
   # Input:
   #        name - Relative path to the module
   # 
   @staticmethod
   def moduleClassNames(name):
       """ Returns a tuple of parsed out module and it's class names."""

       last_dot_pos = name.rfind(".")
       class_name = name[(last_dot_pos + 1):]
       module_path = name[:last_dot_pos]
       
       return (module_path, class_name)
   
   
   #-----------------------------------------------------------------------------
   #
   # getModule
   #
   # This method imports specified module at runtime.
   #
   # Input:
   #        module_path - Relative path to the module
   #
   @staticmethod 
   def getModule(module_path):
       """ Import specified module at runtime."""
       
       # The last [''] for __import__ is very important: 
       # if the last parameter is empty, loading class "A.B.C.D" actually only 
       # loads "A". If the last parameter is defined, regardless of what its 
       # value is, we end up loading "A.B.C". Once we have "A.B.C", we use 
       # getattr() to reference the function (or class) within the module.
       CSEPLogging.CSEPLogging.getLogger(RuntimeLoader.__name__).info("Loading %s..." \
                                                                      %module_path)
       return __import__(module_path, globals(), locals(), [''])
        
   
   #-----------------------------------------------------------------------------
   #
   # getComponent
   #
   # This function imports specified callable attribute from the module at runtime.
   #
   # Input:
   #        name - Relative Python path to the module
   # 
   # Output:
   #        A reference to the requested module component
   #
   @staticmethod 
   def getComponent(name):
       """ Retrieve a function or class from a full dotted-package name."""
       
       # Parse out the module path, and class
       module_path, class_name = RuntimeLoader.moduleClassNames(name)
       
       module_obj = RuntimeLoader.getModule(module_path)
       CSEPLogging.CSEPLogging.getLogger(RuntimeLoader.__name__).info("Loaded module %s..." \
                                                                      %sys.modules[module_path])        
       component_obj = getattr(module_obj, class_name)
       
       # Check that the function is a "callable" attribute.
       if callable(component_obj) is False:
          error_msg = "Class '%s' is not callable." %name
   
          CSEPLogging.CSEPLogging.getLogger(RuntimeLoader.__name__).error(error_msg) 
          raise RuntimeError, error_msg       
          
       
       # Return a reference to the component itself
       return component_obj
   
   
   #-----------------------------------------------------------------------------
   #
   # getClass
   #
   # This function imports class from module at runtime. It checks for class to
   # be a subclass of specified base class if any.
   #
   # Input:
   #        name - Relative Python path to the module
   # 
   # Output:
   #        A reference to the requested module class
   #
   @staticmethod 
   def getClass(name, parent=None):
       """ Load a module and retrieve a reference to the class.
       
           If the 'parent' class is supplied, 'name' must be of parent
           or a subclass of parent (or RuntimeError exception is raised).
       """
       
       class_ref = RuntimeLoader.getComponent(name)
       
       # Assert that the class is a subclass of parentClass.
       if parent is not None:
           if not issubclass(class_ref, parent):
   
              error_msg = "%s is not a subclass of %s." %(name, parent)
   
              CSEPLogging.CSEPLogging.getLogger(RuntimeLoader.__name__).error(error_msg) 
              raise RuntimeError, error_msg       
              
       
       # Return a reference to the class itself
       return class_ref

