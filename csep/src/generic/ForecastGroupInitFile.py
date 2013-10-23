"""
Module ForecastGroupInitFile
"""

__version__ = "$Revision: 3769 $"
__revision__ = "$Id: ForecastGroupInitFile.py 3769 2012-07-24 20:37:27Z liukis $"

import os

import CSEPInitFile


#--------------------------------------------------------------------------------
#
# ForecastGroupInitFile
#
# This module is designed to open and parse XML format files that represent
# initialization parameters for the forecast groups.
# These files consist of any combination of the following elements:
#    1. PostProcessing - Python module used for filtering of catalog data in 
#                        preparation of observations.
#    2. StartDate - Date of models entry into the testing center.
#    3. RunPrediction - Present if forecast models need to be invoked. If 
#       - ForecastDirectory - Directory to store generated forecast files to.
#       - Schedule - 'cronjob'-like schedule on when to invoke forecast model.
#       - Models - Keywords identifying models to invoke.
#       - ModelsInputs - Optional input arguments for the models.
#       - ResultDirectory - Directory to store evaluation tests results.
#
class ForecastGroupInitFile (CSEPInitFile.CSEPInitFile):

    # Static data members

    # Name of post-processing element (Python module to use for catalog preparation)
    PostProcessElement = 'postProcessing'
    
    # Name of forecast group entry date into testing center: if date is not
    # provided by configuration file, start date of very first forecast within the
    # group is treated as group entry date.
    EntryDateElement = 'entryDate'
    
    # Name of start date element (when to start model evaluation in 
    # the testing center)
    StartDateElement = 'startDate'

    # Name of end date element (when to stop model evaluation in 
    # the testing center)
    EndDateElement = 'endDate'
    
    # Name of element to trigger forecast model run (space separated list of 
    # models to invoke)
    ModelElement = 'models'
    HybridModelElement = 'hybridModel'
        
    
    ModelFilesAttribute = 'files'
    IncludesDatesAttribute = 'filenameIncludesStartDate'
    
    # Input arguments for the forecast models or evaluation tests to invoke
    InputsElement = 'inputs'
    
    # Name of output directory for generated forecast files
    ForecastDirectoryElement = 'forecastDir'

    # Name of output directory for evaluation tests results
    ResultDirectoryElement = 'resultDir'
    
    # Name of directory to store observations for the model evaluation
    CatalogDirectoryElement = 'catalogDir'

    # Tests to invoke for the model evaluation
    EvaluationTestElement = 'evaluationTests'

    # Names for required XML format elements
    __XMLTopLevelElements = []

    
    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #       dir_path - Directory path for the forecast group.
    #       filename - Filename for the input parameters. Default is
    #                  "forecast.init.xml".
    # 
    def __init__ (self, dir_path, filename = "forecast.init.xml"):    
        """ Initialization for ForecastGroupInitFile class."""

        CSEPInitFile.CSEPInitFile.__init__(self, os.path.join(dir_path, filename), 
                                           self.__XMLTopLevelElements)


    #---------------------------------------------------------------------------
    #
    # Update models element with provided information
    #
    # Input: 
    #       model_files - List of current forecasts files for the group
    # 
    def updateModels (self, 
                      model_files):
        """ Update models element with provided information."""

        # Nothing to update if there are no models in the group
        if len(model_files) == 0:
            return

            
        models_elem = self.elements(ForecastGroupInitFile.ModelElement)
        
        if len(models_elem) == 0:
            # There is no 'models' element, add one
            models_elem = self.addElement(ForecastGroupInitFile.ModelElement)
            
        else:
            models_elem = models_elem[0] 
        
        models_elem.attrib[ForecastGroupInitFile.ModelFilesAttribute] = ' '.join(model_files)
        
        # Check if any models are installed within testing center (codes are 
        # available to generate forecasts) - then start date of the forecast
        # will be included into forecast filename
        contains_start_date_within_filename = False
        
        models = self.elementValue(ForecastGroupInitFile.ModelElement)
        
        if models is not None and len(models.split()) != 0:
           contains_start_date_within_filename = True
           
        models_elem.attrib[ForecastGroupInitFile.IncludesDatesAttribute] = repr(contains_start_date_within_filename)

        

# Invoke the module
if __name__ == '__main__':

   import EvaluationTestOptionParser, CSEPLogging
   from CSEPOptions import CommandLineOptions   
   

   parser = EvaluationTestOptionParser.EvaluationTestOptionParser()
        
   # List of requred options
   required_options = [CommandLineOptions.FORECASTS]
   init_file = ForecastGroupInitFile(parser.options(required_options).forecast_dir)
   
   CSEPLogging.CSEPLogging.getLogger(ForecastGroupInitFile.__name__).debug("Init file exists: %s" \
                                                                           %init_file.exists())
   CSEPLogging.CSEPLogging.getLogger(ForecastGroupInitFile.__name__).debug("PostProcess value: '%s'" \
                                                                           %init_file.elementValue(ForecastGroupInitFile.PostProcessElement))

# end of main

