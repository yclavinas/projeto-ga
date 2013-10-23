"""
Module DataSourceFactory
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import glob, os

import CSEP, DataSourceComposite, CSEPLogging
from CatalogDataSource import CatalogDataSource
from CSEPFactory import CSEPFactory
from ANSSDataSource import ANSSDataSource
from CMTDataSource import CMTDataSource
from Environment import *


#--------------------------------------------------------------------------------
#
# DataSourceFactory.
#
# This class represents an interface for the factory of existing data source 
# modules that are defined for the CSEP Natural Laboratory (NL).
# It is implemented as a singleton.
# 
class DataSourceFactory (CSEPFactory):

    # Static data of the class

    Type = "DataSourceFactory"
    
    DefaultType = ANSSDataSource.Type
    
    # Instances of the class will be sharing the same state 
    # (see CSEPBorgIdiom class)
    _shared_state = {}      
    
    # Pattern for configuration file used to initialize data source factory  
    __configFilePattern = '*DataSourceFactory.init.xml'
    

    # Parent class for registered classes
    __parentClass = CatalogDataSource

    # Remember configuration files that were used to initialize the factory
    # (to avoid re-initialization using the same files)
    __configFiles = set()

    # Capture created data sources used by processing (to support 
    # Transient Detection project) - "lazy initialization" + "composite" approach
    __objects = DataSourceComposite.DataSourceComposite()
    

    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    # 
    def __init__ (self):
        """ Initialization for DataSourceFactory class"""

        # Dictionary of registered data sources in the testing center
        my_modules = {ANSSDataSource.Type : ANSSDataSource,
                      CMTDataSource.Type : CMTDataSource}

        config_file = None
        CSEPFactory.__init__(self, 
                             config_file,
                             my_modules,
                             DataSourceFactory.__parentClass)
        
        # Check for files that match the pattern for factory configuration file
        existing_config_files =  glob.glob(os.path.join(Environment.Variable[CENTER_CODE_ENV],
                                                        CSEP.TestingCenterConfigDir,
                                                        DataSourceFactory.__configFilePattern))

        for each_file in existing_config_files:
            
           if each_file not in DataSourceFactory.__configFiles:
               
               self.loadPythonModules(each_file,
                                      DataSourceFactory.__parentClass)
                   
               DataSourceFactory.__configFiles.add(each_file)
        

    #----------------------------------------------------------------------------
    #
    # Return factory string identifier.
    # 
    # Input: None
    # 
    # Output:
    #         Keyword identifying the factory.
    # 
    def type (self):
        """ Return type of the factory."""
              
        return DataSourceFactory.Type
     

    #----------------------------------------------------------------------------
    #
    # Create new object. Overwritten to define default type for the object to be
    # created.
    #
    # Input:
    #          type - Keyword identifying Python module to use for object 
    #                 generation. Default is 'ANSS' type.
    #          input_variables - An optional list of input variables for new object. 
    #                            Default is None.
    #          isObjReference - Request for existing object reference, meaning
    #                           that request is made for reference to existing
    #                           object. Default is False (create object if it
    #                           does not exist). 
    # 
    # Output:
    #          Newly created object
    #
     
    def object (self, 
                type = DefaultType, 
                input_variables = None,
                isObjReference = False):
        """ Instantiate object of specified type."""

        # Request for existing object of a type is made
        if (isObjReference is True) and \
           (type in DataSourceFactory.__objects):
                return DataSourceFactory.__objects[type]
        
        DataSourceFactory.__objects[type] = CSEPFactory.object(self, 
                                                               type, 
                                                               input_variables) 
        
        return DataSourceFactory.__objects[type]
     

    #---------------------------------------------------------------------------
    # Return composite of created data source objects
    #
    # Output: DataSourceComposite object
    #
    @staticmethod 
    def composite ():
        """ Return composite of created data source objects"""
        
        return DataSourceFactory.__objects


    #----------------------------------------------------------------------------
    #
    # Return reference to the class
    #
    # Input:
    #          type - Keyword identifying Python class. Default is None, meaning
    #                 that type of currently instantiated CatalogDataSource
    #                 object should be used
    # 
    # Output:
    #          Class reference that corresponds to the specified type.
    # 
    def classReference (self, type = None):
        """ Return reference to the class."""
        
        use_type = type
        if type is None:
            use_type = DataSourceFactory.__objects.type()
           
        return CSEPFactory.classReference(self, 
                                          use_type)
        
        