"""
Module ForecastGroup
"""

__version__ = "$Revision: 4150 $"
__revision__ = "$Id: ForecastGroup.py 4150 2012-12-19 03:08:43Z liukis $"


import os, sys, datetime, re, copy

import CSEPGeneric, CSEPFile, CSEP, Environment, CSEPLogging, \
       CSEPPropertyFile, CSEPLock, GeographicalRegions
from ForecastFactory import ForecastFactory
from EvaluationTestFactory import EvaluationTestFactory
from Forecast import Forecast
from ForecastGroupInitFile import ForecastGroupInitFile
from PostProcessFactory import PostProcessFactory
from EvaluationTest import EvaluationTest
from CSEPStorage import CSEPStorage
from CSEPContainer import CSEPContainer
from CSEPSchedule import CSEPSchedule
from CatalogDataSource import CatalogDataSource
from RELMTest import RELMTest
from CSEPOptions import CommandLineOptions
from PostProcess import PostProcess
from ForecastHandlerFactory import ForecastHandlerFactory 


#--------------------------------------------------------------------------------
#
# ForecastGroup.
#
# This class represents a group of comparable forecast models. Initialization
# parameters are provided on a command line or through an initialization file
# defined by ForecastGroupInitFile class.
# 
class ForecastGroup (CSEPStorage):

    # Static data of the class
    
    # Sub-directory used for archiving of old forecast files
    __archiveDir = "archive"

    # Logger for the class - instantiated by first object of the class
    __logger = None


    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input:
    #         dir_path - Directory for the group forecast files or directory
    #                    that stores initialization file for the group.
    #         post_process - Keyword identifying Python post-processing module
    #                        used to prepare observations for the forecast
    #                        evaluation. Default is None. This input argument
    #                        represents command-line option.
    #         test_list - List of evaluation tests to run.    
    #         test_inputs - String representation of input parameters 
    #                       dictionaries for the tests as specified by
    #                       the 'test_list' argument. Default is None.
    #         model_list - List of forecast models to invoke. Default
    #                      is None. This input argument represents command-line
    #                      option.
    #         models_inputs - String representation of input parameters 
    #                        dictionaries for the models as specified by
    #                        the 'model_list' argument. Default is None.
    #                        This input argument represents command-line
    #                        option.
    #         post_process_inputs - Optional list of input arguments for
    #                               post-processing. Default is None.
    # 
    def __init__ (self, dir_path, 
                        post_process = None,
                        test_list = None,
                        test_inputs = None,
                        model_list = None, 
                        models_inputs = None,
                        post_process_inputs = None):
       """ Initialization for ForecastGroup class. Forecast models to be invoked
          can be specified through a command-line (input variable) or through
          initialization file.
          Constructor method checks for existence of initialization file, and
          extracts forecast group specific values if it exists to initialize 
          internal data members."""

       # Lock directory that stores forecasts files if there are models defined
       # for the group: group that does not have models defined, includes
       # file-based forecasts only
       self.__lock = None


       if ForecastGroup.__logger is None:
          ForecastGroup.__logger = CSEPLogging.CSEPLogging.getLogger(ForecastGroup.__name__)
          
       # Check for valid path
       if dir_path is None or len(dir_path) == 0:
          error_msg = "Directory must be provided to instantiate a ForecastGroup \
object."
          ForecastGroup.__logger.error(error_msg)
         
          raise RuntimeError, error_msg  
       

       # Directory for the forecast group
       self.__dir = dir_path

       ### ATTN: Forecast group can be initialized only by command-line arguments
       #         (ONLY if invoked in stand-alone mode - values are passed as 
       #          arguments to the constructor) OR through configuration file
       #         Initialization is based on an assumption: if configuration file
       #         exists, then command-line arguments were not provided
       
       # Group configuration file if any 
       self.__initFile = ForecastGroupInitFile(self.__dir)

       self.__forecastDir, self.__catalogDir, self.__resultDir = self.__initDirs(self.__initFile)

       # Models container for the forecast group
       self.__models = self.__initModels(model_list,
                                         models_inputs,
                                         self.__initFile)

       # List of file-based forecasts available in the forecast group directory
       self.__modelsFiles = []     

       # Initialize base class once directory for the forecasts files is known
       CSEPStorage.__init__(self,
                            self.__forecastDir)
       
       # Post-processing object for the forecast group
       if isinstance(post_process, PostProcess):
           # PostProcess object was provided (module's stand-alone mode)
           self.__postProcess = post_process
       else:
           self.__postProcess = self.__initPostProcessing(post_process,
                                                          post_process_inputs,
                                                          self.__initFile)

       # List of evaluation tests to be invoked for the models
       self.__evaluationTests = self.__initTests(test_list,
                                                 test_inputs,
                                                 self.__initFile)
        
       # Check for existence of the forecast directory if no models will be 
       # invoked
       if os.path.exists(self.__forecastDir) is False and \
          len(self.__models) == 0:
          
          # No models will be invoked, directory must contain some existing 
          # forecast files for evaluation
          error_msg = "Specified ForecastGroup directory '%s' does not exist." \
                      %(self.__forecastDir)
          ForecastGroup.__logger.error(error_msg)
                      
          raise RuntimeError, error_msg


       ### If invoked in stand-alone mode or there are no evaluation tests for 
       ### the group, don't require postProcessing
       if __name__ != '__main__' and \
          self.__postProcess is None and \
          len(self.__evaluationTests) != 0 and \
          self.__evaluationTests.any('observationRequired') is True:
           
           # Must specify post-processing Python module for the group:
           # through command-line or configuration file
           error_msg = "PostProcessing module must be specified for the \
forecast group identified by '%s' directory." %self.__dir
           ForecastGroup.__logger.error(error_msg)
          
           raise RuntimeError, error_msg

       
    #----------------------------------------------------------------------------
    #
    # Object cleanup.
    #
    # Input: None
    # 
    def __del__ (self):
       """ Cleanup for ForecastGroup class. Removes locks (if any) created by 
           the object."""
         
       self.__unlockForecasts()
       
       
    #----------------------------------------------------------------------------
    #
    # Parse input file if any.
    #
    # Input:
    #         init_file - Configuration file object for the group.
    # 
    # Output: tuple of directories for forecasts, observations and test results.
    #
    def __initDirs (self,
                    init_file):
       """ Initialize directories to store forecast files, observation catalogs,
           and results files from evaluation tests."""


       # Directory for forecast files - set it to be the same as for 
       # the whole group. Initialization file (if present) may specify other 
       # location for the model files.
       forecast_dir = self.__dir

       # Full path to the directory to store observations for evaluation tests:
       # defaults to the "catalogs" sub-directory under ForecastGroup directory.
       catalog_dir = os.path.join(self.__dir, 'catalogs')

       # Directory for evaluation tests results - 
       # defaults to the "results" sub-directory under ForecastGroup directory.
       # Initialization file (if present) may specify other location.
       result_dir = os.path.join(self.__dir, 'results')

       if init_file.exists():

          # - directory for forecast files
          dir_path = init_file.elementValue(ForecastGroupInitFile.ForecastDirectoryElement) 

          # Check if specified directory is an absolute path. If not - prepend
          # group directory.
          if dir_path is not None and os.path.isabs(dir_path) is False:
             forecast_dir = os.path.join(self.__dir, dir_path)
          elif dir_path is not None:
             forecast_dir = dir_path
          
          
          # - directory for observations
          dir_path = init_file.elementValue(ForecastGroupInitFile.CatalogDirectoryElement)

          # Check is specified catalog directory is an absolute path. If not -
          # prepend group directory
          if dir_path is not None and os.path.isabs(dir_path) is False:
             catalog_dir = os.path.join(self.__dir, dir_path)
          elif dir_path is not None:
             catalog_dir = dir_path

          # - directory for evaluation tests results
          dir_path = init_file.elementValue(ForecastGroupInitFile.ResultDirectoryElement)
          
          # Check if specified directory is an absolute path. If not - prepend
          # group directory.
          if dir_path is not None and os.path.isabs(dir_path) is False:
             result_dir = os.path.join(self.__dir, dir_path)
          elif dir_path is not None and \
               os.path.dirname(dir_path) == self.__dir:
             # Full path to the ForecastGroup sub-directory is provided             
             result_dir = dir_path
          elif dir_path is not None:
             # Don't allow absolute paths for results directory that are outside
             # of the ForecastGroup "root" directory.
             # It's done for the purpose of the system integrity - different 
             # ForecastGroups will not be able to combine results under the same
             # directory.
             error_msg = "ForecastGroup identified by %s directory can not have \
results directory outside of it's directory structure: %s. Results directory must be \
a child of the ForecastGroup directory (done for the publishing reasons)." \
                         %(self.__dir, dir_path)

             ForecastGroup.__logger.error(error_msg)
                         
             raise RuntimeError, error_msg
                         
       return (forecast_dir, catalog_dir, result_dir)
          
             
    #----------------------------------------------------------------------------
    #
    # Parse forecast models arguments and instantiate objects that
    # represent specified models.
    #
    # Input: 
    #         model_list - List of forecast models to invoke.
    #         models_inputs - String representation of input parameters 
    #                        dictionaries for the models as specified by
    #                        the 'model_list' argument. 
    #         init_file - Configuration file object for the group.
    # 
    # Output: None.
    #
    def __initModels (self, 
                      model_list, 
                      models_inputs,
                      init_file):
       """ Parse input arguments specific to the forecast models,
           and instantiate objects that represent these models."""

       models = model_list
       inputs = models_inputs
       schedule = CSEPSchedule()

       if init_file.exists():

          file_models = init_file.elementValue(ForecastGroupInitFile.ModelElement)
          file_inputs = init_file.elementValue(ForecastGroupInitFile.InputsElement,
                                               ForecastGroupInitFile.ModelElement)

          # Check if it's another attempt to instantiate models objects
          if file_models is not None:

             # Models specified as command-line argument overwrite models specified
             # in configuration file
             if models is None:
                 models = file_models
                 inputs = file_inputs

             # Extract schedule for forecast generation if any
             schedule = init_file.schedule(ForecastGroupInitFile.ModelElement)
             

       all_models = CSEPContainer(schedule,
                                  ForecastFactory(),
                                  models,
                                  [self.__forecastDir],
                                  inputs)
       
       # Add hybrid models if any
       all_models.extend(ForecastFactory.addHybridModels(self,
                                                         init_file,
                                                         ForecastGroupInitFile.HybridModelElement))
           
       return all_models 
         

    #----------------------------------------------------------------------------
    #
    # Parse forecast models arguments and instantiate objects that
    # represent specified models.
    #
    # Input: 
    #         test_list - List of evalutaion tests to invoke if provided on a
    #                     command-line.
    #         test_inputs - String representation of input parameters 
    #                       dictionaries for the tests as specified by
    #                       the 'test_list' argument. Default is None.
    #         init_file - Configuration file object for the group.
    # 
    # Output: None.
    #
    def __initTests (self, 
                     test_list, 
                     test_inputs,
                     init_file):
       """ Parse input arguments specific to the forecast models,
           and instantiate objects that represent these models."""

       tests = test_list
       inputs = test_inputs
       schedule = CSEPSchedule()

       if init_file.exists():

          # Check if any of the forecast group parameters are specified:
          # Parse evaluation tests keywords
          file_tests = init_file.elementValue(ForecastGroupInitFile.EvaluationTestElement)
          file_inputs = init_file.elementValue(ForecastGroupInitFile.InputsElement,
                                               ForecastGroupInitFile.EvaluationTestElement)
          
          if file_tests is not None:
             
             # Tests specified as command-line argument overwrite tests specified
             # in configuration file
             if test_list is None:
                tests = file_tests
                inputs = file_inputs

             # Extract schedule for forecast evaluation
             schedule = init_file.schedule(ForecastGroupInitFile.EvaluationTestElement)
          

       # ForecastGroup object is a common input for all tests
       common_inputs = [self]
       
       return CSEPContainer(schedule,
                            EvaluationTestFactory(),
                            tests,
                            common_inputs,
                            inputs)
         
         
    #----------------------------------------------------------------------------
    #
    # Parse post_processing arguments and instantiate object that
    # represents specified filtering Python module for forecast observations.
    #
    # Input: 
    #         post_process - Keyword identifying Python post-processing 
    #                        module for preparing forecast observations.
    #         post_process_inputs - Optional list of input arguments for 
    #                               post-processing object to generate.
    #         init_file - Configuration file object for the group.
    # 
    # Output: PostProcessing object
    #
    def __initPostProcessing (self, 
                              post_process, 
                              post_process_inputs,
                              init_file):
       """ Parse input arguments specific to the post-processing,
           and instantiate object that represents specified Python module."""

       token = post_process
       
       args = post_process_inputs
       
       # Input arguments can be passed as list of start and end dates, or 
       # string representation of these dates
       if isinstance(post_process_inputs, str):
           args = [datetime.datetime.strptime(each_date, "%Y-%m-%d") for each_date in
                   post_process_inputs.split()]
       
       if init_file.exists():
          
          # - post-processing Python module
          file_post_process = init_file.elementValue(ForecastGroupInitFile.PostProcessElement)
          
          # Read post-processing information from the file if it's not provided
          # as a command-line arguments
          if post_process is None and file_post_process is not None:
              token = file_post_process

          # No start and end dates are provided on a command-line
          if args is None:
              
              # group models entry/expiration dates into the testing center
              start_date = init_file.elementValue(ForecastGroupInitFile.StartDateElement)
              end_date = init_file.elementValue(ForecastGroupInitFile.EndDateElement)
              
              if (start_date is not None and end_date is None) or \
                 (start_date is None and end_date is not None):
      
                 error_msg = "Post-processing for '%s' directory is missing one of the values for time period: \
startDate='%s' endDate='%s'." %(self.__dir, start_date, end_date)
                 ForecastGroup.__logger.error(error_msg)
                 raise RuntimeError, error_msg
    
              if start_date is not None:
    
                 # convert start date and time as provided in config file
                 # to datetime object          
                 args = [datetime.datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S"),
                         datetime.datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")]

              # Check for group entry date into Testing Center
              entry_date = init_file.elementValue(ForecastGroupInitFile.EntryDateElement)

              if entry_date is not None:
                  
                 entry_date_obj = datetime.datetime.strptime(entry_date, 
                                                            "%Y-%m-%d %H:%M:%S")  
                 # If start/end dates are provided 
                 if args is not None:
                     args.append(entry_date_obj)
                     
                 else:
                     # Class method will raise an exception if specified 
                     # argument is not defined as input argument
                     args = {'cumulative_start_date' : entry_date_obj}


       if token is not None:

          # Create the object
          ForecastGroup.__logger.info("%s ForecastGroup: creating PostProcess object %s with args: %s" %(self,
                                                                                                         token,
                                                                                                         args))
          return PostProcessFactory().object(token, 
                                             args)
       else:
           
          return None 
           

    #----------------------------------------------------------------------------
    #
    # Scan forecast directory for existing model files.
    #
    # Input: None.
    #
    def __scanDirectory (self):
        """ Scan directory for existing forecasts files. This method 
            will be called every time forecasts models are invoked. This
            guarantees that newly created forecasts files are included for
            evaluation tests."""

        # Lock directory before scanning it
        self.__lockForecasts()
        
        # Identify available forecasts
        self.__modelsFiles = []
        dir_list = os.listdir(self.__forecastDir)
        
        # The same directory listing returns files in different order on 
        # different machines - makes acceptance tests to fail. 
        dir_list.sort()

        # RULES for forecast files:
        # 1. For ASCII format forecasts:
        #     - check if the same forecast file exists in Matlab format
        #     - convert ASCII format forecast to the Matlab one if it doesn't 
        #       exist already
        # 2. Ignore forecast group configuration file if any (default is
        #    forecast.init.xml)
        # 3. Ignore metadata files for forecasts (*.meta files)
        # 4. Ignore original files for forecasts (as generated by the model)
        #
        ignore_extension = [CSEPPropertyFile.CSEPPropertyFile.Metadata.Extension,
                            CSEPFile.Extension.ORIGINAL]
        
        # Archive directory to check for already existing data files if any
        model_archive_dir = None
        
        for model in dir_list:
           
            model_path = os.path.join(self.__forecastDir, model)

            if Forecast.isFile(model_path, 
                               self.__initFile.name, 
                               ignore_extension):
               
                # Construct archive directory for the model
                if model_archive_dir is None and \
                   Forecast.archiveDir(model_path) is not None:
                   
                   model_archive_dir = os.path.join(self.__forecastDir,
                                                    ForecastGroup.__archiveDir,
                                                    Forecast.archiveDir(model_path))
                   
                if CSEP.Forecast.UseXMLMasterTemplate:
                   
                   # Check if corresponding ASCII file based on XML forecast
                   # template exists (ASCII format file was created by 
                   # populating master XML template)
                   #
                   ascii_from_xml_path = CSEP.Forecast.fromXMLTemplateFilename(model_path)

                   #============================================================
                   # ASCII format of the model based on XML template does not exist
                   #============================================================
                   if self.fileExists(ascii_from_xml_path,
                                      model_archive_dir) is False:
                      
                      ForecastGroup.__logger.info("Creating ASCII \
format file for '%s' based on XML template." %model_path)
                      
                      xml_path = CSEPFile.Name.xml(model_path)
                      ForecastGroup.__logger.info("Forecast XML file '%s' for model %s" \
                                                  %(xml_path, model_path))
                      
                      # Fix for Trac ticket #177
                      # If XML format of the forecast exists, make sure that it's
                      # the one generated by the CSEP testing framework (to guarantee
                      # that forecast passes through master ForecastML template)
                      if self.fileExists(xml_path,
                                         model_archive_dir) is True:
                          
                           _val_file = ForecastHandlerFactory().CurrentHandler.XML(xml_path)
                           _val_file.validate(self.__postProcess,
                                              model_archive_dir)
                      
                      else:
                         #======================================================
                         # XML format of the model does not exist, create one
                         #======================================================
                         # Check for ASCII format forecast file existence - 
                         # it will be required to create XML format forecast
                         ascii_path = CSEPFile.Name.ascii(model_path)
                         
                         if self.fileExists(ascii_path,
                                            model_archive_dir) is False:
                            
                            # Forecast is in Matlab format, convert to ASCII 
                            CSEPGeneric.Forecast.toASCII(model_path)
                            
                            # Create metadata file for the forecast 
                            comment = "Forecast file in %s format used to create XML format forecast file" \
                                       %CSEPFile.Format.ASCII
                            
                            Forecast.metadata(ascii_path,
                                              comment,
                                              os.path.join(self.__forecastDir, 
                                                           ForecastGroup.__archiveDir))
                                                  
                         # Create XML format file of the forecast
                         template = ForecastHandlerFactory().CurrentHandler.XML(self.__postProcess.template)
                         xml_path = template.toXML(ascii_path, 
                                                   self.__postProcess.start_date,
                                                   self.__postProcess.end_date,
                                                   model)
                         
                         # Create metadata file for the forecast 
                         comment = "Forecast file in %s format that is based on XML master template %s" \
                                    %(CSEPFile.Format.XML, 
                                      self.__postProcess.template)
                         
                         Forecast.metadata(xml_path,
                                           comment,
                                           os.path.join(self.__forecastDir, 
                                                        ForecastGroup.__archiveDir))
                         
                      
                      # Convert XML format forecast to ASCII
                      _model = ForecastHandlerFactory().CurrentHandler.XML(xml_path)
                      _model.toASCII(ascii_from_xml_path)
                      
                      # Create metadata file for the forecast 
                      comment = "Forecast file in %s format that is based on XML master template %s" \
                                 %(CSEPFile.Format.ASCII, 
                                   self.__postProcess.template)
                      
                      Forecast.metadata(ascii_from_xml_path,
                                        comment,
                                        os.path.join(self.__forecastDir, 
                                                     ForecastGroup.__archiveDir))
                   
                   ### if self.fileExists(ascii_fromXML_path, 
                      
                   # Register the file and continue
                   register_file = os.path.basename(ascii_from_xml_path)
                   not_registered = (self.__modelsFiles.count(register_file) == 0)
                   
                   if not_registered is True:
                      self.__modelsFiles.append(register_file)
                      
                      
                   continue
                # end of 'if CSEP.Forecast.UseXMLMasterTemplate'
                       
                
                #===============================================================
                ### XML forecast template is disabled
                #===============================================================
                # Check if ASCII format file of the forecast exists
                ascii_path = CSEPFile.Name.ascii(model_path)
                ForecastGroup.__logger.info("ASCII format of forecast file '%s' for model %s"
                                            %(ascii_path, model))
                
                if self.fileExists(ascii_path,
                                   model_archive_dir) is False:

                   # Convert XML format of the forecast to ASCII
                   if CSEPFile.Extension.toFormat(model_path) == CSEPFile.Format.XML:
                       _model = ForecastHandlerFactory().CurrentHandler.XML(model_path)
                       _model.toASCII(ascii_path)

                   elif CSEPFile.Extension.toFormat(model_path) == CSEPFile.Format.MATLAB:
                       # Convert Matlab format forecast to ASCII
                       CSEPGeneric.Forecast.toASCII(model_path,
                                                    result_file = ascii_path)
                   else:
                       error_msg = 'Unknown forecast format %s is provided, one of %s is supported' \
                                   %(model, (CSEPFile.Format.ASCII,
                                             CSEPFile.Format.XML, 
                                             CSEPFile.Format.MATLAB))

                   # Create metadata file for the forecast 
                   comment = "Forecast file in %s format" %(CSEPFile.Format.ASCII) 
                  
                   Forecast.metadata(ascii_path,
                                     comment,
                                     os.path.join(self.__forecastDir, 
                                                  ForecastGroup.__archiveDir))
                       
                if os.path.basename(ascii_path) not in self.__modelsFiles:
                   
                    # - If directory didn't include Matlab format forecast file, 
                    # the newly created one will be included
                    self.__modelsFiles.append(os.path.basename(ascii_path))

                
        ForecastGroup.__logger.info("%s: Identified forecast files: %s" \
                                    %(self.__dir, self.__modelsFiles))
                
        if (len(self.__modelsFiles) == 0) and self.__models is None:
            error_msg = "Specified forecast directory '%s' does not contain any models." \
                        %self.__dir
                        
            ForecastGroup.__logger.error(error_msg)
            
            raise RuntimeError, error_msg


        ### See Trac ticket #211: Add support for new web service
        # Update configuration file with current forecasts files within the group
        if self.__initFile.exists():
           
           init_file = ForecastGroupInitFile(self.__dir)
           
           # Set attributes for the 'models' element 
           elements = init_file.updateModels(self.__modelsFiles)

           # Overwrite existing file
           fhandle = CSEPFile.openFile(self.__initFile.name, 
                                       CSEPFile.Mode.WRITE)
           init_file.write(fhandle)
           fhandle.close()


    #----------------------------------------------------------------------------
    #
    # Checks if file of interest exists: in 'forecasts' or in 'forecasts/archive/YYYY_MM'
    # directory. 
    #
    # Input: 
    #        forecast_file - Forecast file of interest
    #        archive_dir - Archive directory for the file of interest.
    #
    # Output:
    #        True if file exists, False otherwise.
    #
    def fileExists (self,
                    forecast_file,
                    archive_dir):
       """ Checks if file of interest exists: in 'forecasts' or in 
           'forecasts/archive/YYYY_MM' directory."""
       
       return (os.path.exists(forecast_file) is True or \
               (archive_dir is not None and \
                CSEPStorage.stage(self, 
                                  [os.path.basename(forecast_file)],
                                  archive_dir) is True))


    #----------------------------------------------------------------------------
    #
    # Returns name of archived forecast file for specified test date given
    # name of known forecast file for the current test period.
    #
    # Input: 
    #        forecast_file - Forecast file of interest
    #        archive_dir - Archive directory for the file of interest.
    #
    # Output:
    #        True if file exists, False otherwise.
    #
    def archivedName (self,
                      forecast_file,
                      test_date):
        """ Returns name of archived forecast file for specified test date given
            name of known forecast file for the current test period."""
        
            
        # Replace start date in forecast file
        test_date_forecast = re.sub(r'_[0-9]+_[0-9]+_[0-9][0-9][0-9][0-9]',
                                    '_%s_%s_%s' %(test_date.month, 
                                                  test_date.day, 
                                                  test_date.year),
                                    forecast_file)
        
        return os.path.join(self.__forecastDir,
                            ForecastGroup.__archiveDir,
                            Forecast.archiveDir(test_date_forecast),
                            test_date_forecast)
            

    #----------------------------------------------------------------------------
    #
    # Return list of available models files.
    #
    # Input: None.
    #
    # Output:
    #         List of existing forecasts files.
    #
    def files (self):
       """ Returns list of available forecasts files."""
       
       # Scan for available files
       if len(self.__modelsFiles) == 0: 
          self.__scanDirectory() 
       
       return self.__modelsFiles
     
     
    #----------------------------------------------------------------------------
    #
    # Return directory with available models files.
    #
    # Input: None.
    #
    # Output:
    #           Directory name.
    #
    def dir (self):
        """ Returns directory for available forecasts files."""
        
        return self.__forecastDir
        

    #----------------------------------------------------------------------------
    #
    # Return directory that represents forecast group.
    #
    # Input: None.
    #
    # Output:
    #           Directory name.
    #
    def rootDir (self):
        """ Returns directory that represents forecast group."""
        
        return self.__dir


    #----------------------------------------------------------------------------
    #
    # Return directory for evaluation tests results.
    #
    # Input: None.
    #
    # Output:
    #           Directory name.
    #
    def resultDir (self):
       """ Returns directory for evaluation tests results."""

       # If directory path has been requested, generate it if it does not exist
       if (os.path.exists(self.__resultDir) is False):
          ForecastGroup.__logger.info("Creating result directory '%s'..." %self.__resultDir)

          os.mkdir(self.__resultDir)             
        
       return self.__resultDir
     

    #----------------------------------------------------------------------------
    #
    # Return directory for observations used for the evaluation tests.
    #
    # Input: None.
    #
    # Output:
    #           Directory name.
    #
    def catalogDir (self):
        """ Returns directory for observations used by the evaluation tests."""
        
        return self.__catalogDir


    #----------------------------------------------------------------------------
    #
    # Return post-processing object to be used for catalog filtering.
    #
    # Input: None.
    #
    # Output:
    #         PostProcess object or None.
    #
    def postProcess (self):
        """ Returns post-processing object used to generate observations or
            None."""
        
        return self.__postProcess


    #----------------------------------------------------------------------------
    #
    # Return list of evaluation tests objects defined for the group 
    #
    # Input: None.
    #
    # Output:
    #         CSEPContainer of evaluation tests objects for the models.
    #
    def __getEvaluationTests (self):
        """ Returns list of evaluation tests for the models."""
        
        return self.__evaluationTests

    tests = property(__getEvaluationTests, doc = "Evaluation tests for forecast group")
    

    #----------------------------------------------------------------------------
    #
    # Return list of forecasts models objects defined for the group 
    #
    # Input: None.
    #
    # Output:
    #         List of forecasts models objects defined for the group
    #
    def __getModels (self):
        """ Returns list of forecasts models within the group."""
        
        return self.__models

    models = property(__getModels, doc = "Models for forecast group")


    #----------------------------------------------------------------------------
    #
    # Return list of evaluation tests keywords for the models. 
    #
    # Input: None.
    #
    # Output:
    #         Keywords identifying evaluation tests for the models.
    #
    def __getEntryDate (self):
        """ Returns forecast group entry date into the testing center."""

        if (self.__entryDate is None) and (self.__postProcess is not None):
            # If group entry date is not known, return start date of 
            # current testing period
            return self.__postProcess.start_date
        
        return self.__entryDate

    entryDate = property(__getEntryDate, doc = "Date of entry for the forecast group into the testing center")


    #----------------------------------------------------------------------------
    #
    # Returns name of forecast group configuration file 
    #
    # Input: None.
    #
    # Output:
    #         Name of forecast group configuration file
    #
    def __getConfigFile (self):
        """ Returns name of forecast group configuration file."""
        
        return self.__initFile

    configFile = property(__getConfigFile, 
                          doc = "Configuration file object for forecast group")
    
        
    #----------------------------------------------------------------------------
    #
    # Return True if forecasts for the group should be generated for a 
    # specific date, False if otherwise. If date is not specified, then
    # method only checks if any models are set for the group. If schedule
    # is not set, than specified date is ignored.
    #
    # Input:
    #        date - datetime object for the test date. Default is None.
    #
    # Output:
    #        True if forecasts should be generated, False otherwise.
    #
    def hasModels (self, date = None):
        """ Returns True if forecasts should be generated for the group,
            False otherwise."""
        
        return self.__models.hasDate(date)


    #----------------------------------------------------------------------------
    #
    # Return True if passed in date is the last day in forecast period for the 
    # group.
    #
    # Input:
    #        test_date - datetime object for the test date. Default is None.
    #
    # Output:
    #        True if forecasts should be generated, False otherwise.
    #
    def isLastDay (self, test_date):
        """ Returns True if forecasts should be generated for the group,
            False otherwise."""
        
        if test_date is None or self.__postProcess is None:
           return False
        
        # Tomorrow's date   
        tomorrow_date = test_date + datetime.timedelta(days=1)
        
        # Flag if true result has been generated
        is_last_testing_day = False
        
        # Expiration day assumes 00:00:00 time of the day - meaning that last day of
        # the forecast period doesn't include that expiration day --> check
        # for "tomorrow's" expiration - meaning today is the last day of the forecast
        # Should do final evaluation of the forecast "today" including the data for
        # "today" into observation catalog
        if self.__postProcess.expires(tomorrow_date) or \
           self.hasModels(tomorrow_date):
           is_last_testing_day = True
           
        return is_last_testing_day
      

    #----------------------------------------------------------------------------
    #
    # Return True if forecasts for the group should be evaluated for a 
    # specific date, False otherwise. If date is not set, then method
    # only checks if evaluation tests are set for the group. If schedule
    # is not set, that specified date is ignored.
    #
    # Input:
    #        date - datetime object for the test date. Default is None.
    #
    # Output:
    #        True if forecasts should be evaluated, False otherwise.
    #
    def hasTests (self, date = None):
        """ Returns True if forecasts should be evaluated for the group,
            False otherwise."""
        
        result = self.__evaluationTests.hasDate(date)
        
        # Check if test date is the last day in forecast period ("tomorrow" new
        # forecasts will be generated) that might not
        # be covered by the schedule ---> force the processing
        if (self.isLastDay(date) is True) and (len(self.__evaluationTests) != 0):
           result = True 
           
        return result
     

    #----------------------------------------------------------------------------
    #
    # Generate forecast file for the test.
    #
    # Input: 
    #        test_date - datetime object that represents a test date.
    #        catalog_dir - Directory with raw catalog data.
    #        data_source - Optional catalog data source. Default is None.
    #                      In a case when raw data download is disabled, need
    #                      to stage existing raw catalog data based on metadata
    #                      of existing data product. 
    #
    # Output:
    #        List of created forecast filenames.
    #
    def create (self, 
                test_date, 
                raw_catalog_dir, 
                data_source = CatalogDataSource()):
        """ Invoke forecast model and generate a forecast file."""

        
        ### Forecast creation is disabled or not scheduled for the date
        if self.hasModels(test_date) is False:
           return

        self.__lockForecasts()

        ### Go through the list of forecast models to be generated
        new_files = []
        for model in self.__models:
           new_files.extend(model.create(test_date, 
                                         raw_catalog_dir,
                                         os.path.join(self.__forecastDir, 
                                                      ForecastGroup.__archiveDir),
                                         data_source))

           # Set start and end dates for post-processing (if format conversions
           # are needed)
           if self.__postProcess is not None:
               self.__postProcess.startDate(model.start_date)
               self.__postProcess.endDate(model.end_date)        
           
           # Scan for newly available files, and convert them to Matlab/XML format
           # if necessary: hybrid models rely on "fromXML" version of the model
           # if XML template is enabled
           self.__scanDirectory()
           

        # No forecasts files have been generated, no need to update metadata 
        # for the group
        if len(new_files) == 0:
            return new_files
        
        
        # Reset forecast start and end times in the configuration file for the
        # forecast group - to be used by evaluation tests, and to trigger next
        # forecast generation
        # Change configuration file only for the models that have their start and
        # end time specified (one-day models don't have them)
        if self.__initFile.exists():
           
           init_file = ForecastGroupInitFile(self.__dir)
           
           # Change value of startDate
           elements = init_file.elements(ForecastGroupInitFile.StartDateElement)
           
           # Flag if there are modifications to the configuration file
           updated_file = False
           
           if len(elements) != 0:

              # All models within the group have the same time interval for new
              # forecast    
              elements[0].text = '%s' %self.__models[0].start_date
              updated_file = True
           
           # Change value of endDate
           elements = init_file.elements(ForecastGroupInitFile.EndDateElement)
           
           if len(elements) != 0:

              # All models within the group have the same time interval for new
              # forecast    
              elements[0].text = '%s' %self.__models[0].end_date
              
              # Check if both start and end dates are updated
              if updated_file is False:
                 # There must be a corresponding startDate element in the file
                 error_msg = "create(): %s file is missing %s element that \
corresponds to the %s element." %(self.__initFile.name, 
                                  ForecastGroupInitFile.StartDateElement,
                                  ForecastGroupInitFile.EndDateElement)

                 ForecastGroup.__logger.error(error_msg)
                 raise RuntimeError, error_msg

           # Check if startDate has been updated   
           elif updated_file is True:

                 # There must be a corresponding startDate element in the file
                 error_msg = "create(): %s file is missing %s element that \
corresponds to the %s element." %(self.__initFile.name, 
                                  ForecastGroupInitFile.EndDateElement,
                                  ForecastGroupInitFile.StartDateElement)

                 ForecastGroup.__logger.error(error_msg)
                 raise RuntimeError, error_msg
                 

           # Overwrite the file if there are any changes to it   
           if updated_file is True:   
                          
              # Overwrite existing file
              fhandle = CSEPFile.openFile(self.__initFile.name, 
                                          CSEPFile.Mode.WRITE)
              init_file.write(fhandle)
              fhandle.close()
           
        
        # Scan for newly available files, and convert them to Matlab/XML format
        # if necessary.
        self.__scanDirectory()
        
        # Reset list of forecast files specific to the group (multiple forecast 
        # groups might use the same directory) -  the same directory might
        # contain forecasts for different groups
        if CSEP.Forecast.UseXMLMasterTemplate is True:
           self.__modelsFiles = [CSEP.Forecast.fromXMLTemplateFilename(model) for 
                                 model in new_files]
        else:
           self.__modelsFiles = new_files
           #[CSEPFile.Name.matlab(model) for model in new_files]

        self.__modelsFiles = list(set(self.__modelsFiles))
        
        # return just generated forecasts files
        return self.__modelsFiles


    #----------------------------------------------------------------------------
    #
    # Archive forecast files if "tomorrow" new files are to be generated.
    # This is done to prevent evaluation of old files along with new ones.
    #
    # Input: 
    #        test_date - datetime object that represents "today" test date.
    #
    # Output: None.
    #
    def archive (self, test_date):
        """ Archive forecast files if "tomorrow" (of test_date) new files will
            be generated."""
        
        # Tomorrow's date
        tomorrow_date = test_date + datetime.timedelta(days=1)

        ### Forecast creation is scheduled for tomorrow
        if self.hasModels(tomorrow_date) is True:

           # If lock has been already released (by previous call to archive)
           # ===> don't archive forecasts: forecasts directory might be 
           # already used by another group
           if self.__lock is None:
              return
           
           # Archive all of the files in 'forecasts' and it's top-level archive 
           # directory: even if only some of the models are referenced by the group.
           # Can't leave any existing forecasts there once new files will be 
           # placed under the same directory.
           archive_dir = None
           
           for each_dir in [self.__forecastDir, 
                            os.path.join(self.__forecastDir,
                                         ForecastGroup.__archiveDir)]:
               
               # "archive" directory might not yet exists
               if os.path.exists(each_dir):
                   
                   dir_list = os.listdir(each_dir)
                   ForecastGroup.__logger.info("%s directory list: %s" %(each_dir,
                                                                         dir_list))

                   for model in dir_list:
                      
                       model_path = os.path.join(each_dir, model)
                   
                       # Ignore configuration file for the group
                       if Forecast.isFile(model_path, 
                                          self.__initFile.name) is True:
        
                          # Check if file is a soft link - it was staged ===>
                          # remove the link, since forecast files is already archived
                          if os.path.islink(model_path) is True:
        
                             msg = "archive(): removing soft link %s to already archived data file" \
                                   %model_path 
                             ForecastGroup.__logger.info(msg)
        
                             os.remove(model_path)
                                                  
                          else:
                             
                             # Based on first model filename, construct archive directory
                             # that is based on forecast start date - all CSEP generated
                             # forecast files follow the same naming convention that is based
                             # on start date of the forecast period
                             if archive_dir is None:
                                 
                                ForecastGroup.__logger.info("Model=%s; archiveDir(model)=%s" %(model,
                                                                                               Forecast.archiveDir(model)))
                                # Get rid of optional '-fromXML' keyword and any extension
                                archive_dir = os.path.join(self.__forecastDir, 
                                                           ForecastGroup.__archiveDir,
                                                           Forecast.archiveDir(model))
                                
                             new_path = os.path.join(archive_dir, model)
                             
                             msg = "archive(): renaming '%s' to '%s'" \
                                   %(model_path, new_path)
                             ForecastGroup.__logger.info(msg)
                             
                             os.renames(model_path, 
                                        new_path)
                  
           
        # Remove lock from forecasts directory
        self.__unlockForecasts() 
        
        
    #----------------------------------------------------------------------------
    #
    # Create a map of a forecast model, scaled down to the test date (if any),
    # and overlay observed events.
    #
    # This method identifies XML format file of the specified forecast file, and
    # creates such file if it does not exist. It scales down forecast rates
    # according to the scale factor found in 'ForecastGroup.__scaleFactorFile'
    # file, and creates new ASCII file that contains forecast data required for
    # the map generation. If observed events are provided, they will be overlayed
    # onto mapped forecast data.
    #
    # Input: 
    #        forecast_file - Forecast file as used by evaluation test.
    #        results_dir - Directory to store result files to.
    #        catalog_file - Optional observation catalog file to display observed
    #                       events. Default is None.
    #        test_name - Optional test name for which map is generated. Default
    #                    is None.
    #        scale_factor - Scale factor to apply to the forecast. Default value
    #                       is 1.0 (don't scale)
    #
    # Output: 
    #         Filename for the map file
    #
    def createMap (self, 
                   forecast_file, 
                   results_dir, 
                   catalog_file = None, 
                   test_name = None,
                   scale_factor = 1.0):
        """ Create map of the forecast given observed earthquake events (optional)."""
        
        # Don't generate map if it's disabled
        if CSEP.Forecast.GenerateMap is False:
           return ''
        
        
        forecast_path = os.path.join(self.__forecastDir,
                                     forecast_file)
        
        model_archive_dir = None
        if Forecast.archiveDir(forecast_file) is not None:
           
           model_archive_dir = os.path.join(self.__forecastDir,
                                            ForecastGroup.__archiveDir,
                                            Forecast.archiveDir(forecast_file))

        # Check if XML format file exists for the model under forecast directory
        xml_path = CSEPFile.Name.xml(forecast_path,
                                     CSEP.Forecast.FromXMLPostfix)

        # Create XML format file if it does not exist for the model under archive
        # directory - this way it can be re-used by all tests that might need it
        if self.fileExists(xml_path,
                           model_archive_dir) is False:
           
           model_path, model_name = os.path.split(xml_path)
           
           # Add archive sub-directory
           xml_path = os.path.join(model_path, 
                                   ForecastGroup.__archiveDir,
                                   model_name)
        
           # Create XML format file if it does not exist for the model under archive
           # directory - this way it can be re-used by all tests that might need it
           if os.path.exists(xml_path) is False:
              
              ForecastGroup.__logger.info(
                 "createMap(): Creating XML format file '%s' required for map \
generation" %xml_path)
              
              # Check for ASCII format forecast file existence - 
              # it will be required to create XML format forecast
              ascii_path = CSEPFile.Name.ascii(forecast_path)

              archive_dir = os.path.join(self.__forecastDir,
                                         ForecastGroup.__archiveDir)
              
              if os.path.exists(archive_dir) is False:
                 os.mkdir(archive_dir)
              
              if self.fileExists(ascii_path,
                                 model_archive_dir) is False:

                 # Have to create a link to the original forecast file under
                 # archive sub-directory
                 archive_forecast_path = os.path.join(archive_dir, 
                                                      forecast_file)
                 
                 # Create soft link to the file
                 os.symlink(forecast_path,
                            archive_forecast_path)

                 ForecastGroup.__logger.info(
                    "createMap(): Creating ASCII format file for '%s' required for map \
generation" %archive_forecast_path)

   
                 ascii_path  = CSEPGeneric.Forecast.toASCII(archive_forecast_path)
                 
                 # Remove symbolic link to original forecast file
                 os.remove(archive_forecast_path)
                
                 # Create metadata file for the forecast 
                 comment = "ASCII forecast file to create XML format file for map generation." 

                 Forecast.metadata(ascii_path,
                                   comment)
                           
                           
              else:

                 # Create link to the ASCII file under archive directory
                 model_path, model_name = os.path.split(ascii_path)
                 
                 archive_ascii_path = os.path.join(model_path,
                                                   ForecastGroup.__archiveDir,
                                                   model_name)
                 os.symlink(ascii_path,
                            archive_ascii_path)
                 
                 ascii_path = archive_ascii_path
                 
                                      
              # Create XML format file of the forecast
              template = ForecastHandlerFactory().CurrentHandler.XML(self.__postProcess.template)
              xml_path = template.toXML(ascii_path, 
                                        self.__postProcess.start_date,
                                        self.__postProcess.end_date,
                                        forecast_file)
              
              if os.path.islink(ascii_path) is True:
                 
                 # Remove symbolic link to original ascii file
                 os.remove(ascii_path)


              # Create metadata file for the forecast 
              comment = "XML forecast file required for map generation." 

              Forecast.metadata(xml_path,
                                comment)

        start_date = None
        if self.__postProcess is not None:
            start_date = self.__postProcess.start_date
            
        # Create a map
        return GeographicalRegions.Region.createMap(xml_path,
                                                    results_dir,
                                                    start_date,
                                                    test_name,
                                                    catalog_file,
                                                    scale_factor)

    
    #----------------------------------------------------------------------------
    #
    # Lock forecasts directory.
    #
    # This method locks forecasts directory if it was not locked yet.
    #
    # Input: None
    #
    # Output: 
    #         True if directory has been locked, False otherwise.
    #
    def __lockForecasts (self):
        """ Lock forecasts directory."""
     
        if len(self.__models) and self.__lock is None:
           self.__lock = CSEPLock.DirLock(self.__forecastDir)
           return True

        return False


    #----------------------------------------------------------------------------
    #
    # Unlock forecasts directory.
    #
    # This method unlocks forecasts directory if it was locked before.
    #
    # Input: None
    #
    # Output: 
    #         True if directory has been unlocked, False otherwise.
    #
    def __unlockForecasts (self):
        """ Unlock forecasts directory."""
     
        if self.__lock is not None:
           self.__lock.release()
           
           # Re-set the lock object to None once it's released
           self.__lock = None
           return True

        return False
        

# Invoke the module
if __name__ == '__main__':

   import EvaluationTestOptionParser
   
   
   parser = EvaluationTestOptionParser.EvaluationTestOptionParser()
   parser.add_option('--catalog',
                     type='string',
                     dest='catalog_file',
                     default=None,
                     help='Catalog file that represents observed events for the testing period. \
Default is None, meaning there are no observations available.')
   
        
   # List of requred options
   required_options = [CommandLineOptions.FORECASTS]
   options = parser.options(required_options)

   forecast_group = ForecastGroup(options.forecast_dir,
                                  options.post_process,
                                  options.test_list,
                                  options.test_inputs,
                                  options.generate_forecast,
                                  options.forecasts_inputs,
                                  options.post_process_args)
   
   #============================================================================
   # Only if maps are enabled for the forecast group
   #============================================================================
   # If catalog file was not provided on the command-line, check if
   # it exists through forecast group specified PostProcessing module
   existing_catalog = options.catalog_file
   
   if CSEP.Forecast.GenerateMap is True and \
      existing_catalog is None and \
      forecast_group.postProcess() is not None:

      catalog = os.path.join(options.test_dir,
                             forecast_group.postProcess().files.catalog)
      
      if os.path.exists(catalog):
         existing_catalog = catalog
         
         # ASCII format of the catalog is required for map generation
         if CSEPFile.Extension.toFormat(existing_catalog) != CSEPFile.Extension.ASCII:
              existing_catalog = CSEPGeneric.Catalog.toASCII(existing_catalog)
       
        
   # Create map for each existing forecast model within the group
   for each_model in forecast_group.files():

      forecast_group.createMap(os.path.join(forecast_group.dir(),
                                            each_model),
                               options.test_dir,
                               existing_catalog)
      
   
   # Create forecasts if specified on a command-line or
   # through the initialization file
   if (options.generate_forecast is not None or \
       forecast_group.hasModels()) and forecast_group.postProcess() is not None:

      # Test date must be specified
      required_options.append(CommandLineOptions.YEAR)
      required_options.append(CommandLineOptions.MONTH)
      required_options.append(CommandLineOptions.DAY)
      options = parser.options(required_options)

      # Test date for the test
      test_date = datetime.datetime(options.year, 
                                    options.month,
                                    options.day)
     
      forecast_group.create(test_date,
                            options.test_dir)
# end of main
