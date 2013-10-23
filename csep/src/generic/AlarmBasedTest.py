"""
Module AlarmBasedTest
"""

__version__ = "$Revision: 4150 $"
__revision__ = "$Id: AlarmBasedTest.py 4150 2012-12-19 03:08:43Z liukis $"


import os, datetime, shutil, glob

import CSEP, Environment, CSEPPropertyFile, CSEPLogging, \
       CSEPFile, EvaluationTest, ReproducibilityFiles, \
       CSEPInputParams, CSEPInitFile
       
from Forecast import Forecast
from ForecastHandlerFactory import ForecastHandlerFactory
from cseprandom import CSEPRandom


#--------------------------------------------------------------------------------
#
# AlarmBasedTest.
#
# This class is designed to evaluate available models with alarm-based tests.
#
class AlarmBasedTest (EvaluationTest.EvaluationTest,
                      ReproducibilityFiles.ReproducibilityFiles):

    # Static data

    # Prefix for the test generated files
    __filePrefix = 'a' + EvaluationTest.EvaluationTest.FilePrefix
    
    # Pattern used to match result files in XML format
    __xmlResultPattern = '%s*%s' %(__filePrefix,
                                   CSEPFile.Extension.XML)

    
    # Keyword identifying the class
    __type = "AlarmTest"
    
    # Common directory for alarm-based evaluation tests and related files
    __codePath = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                              'src', 'AlarmBasedTests')
    
    # Name of executable 
    __executableFile = 'Sandbox'
    

    #===========================================================================
    # Nested class with matplotlib settings for the test     
    #===========================================================================
    class Matplotlib (EvaluationTest.EvaluationTest.Matplotlib):

        # Static data
        _plotConfidenceBounds = {'markersize' : None,
                                 'color': 'k',
                                 'facecolor' : '0.80', # 0.90
                                 'edgecolor' : '0.80', # 0.90
                                 'alpha': 0.5,
                                 'linestyle' : '--',
                                 'linewidth' : 1,
                                 'shadeLowerLimit': 0.0, # 0.00
                                 'shadeUpperLimit': 1.0 }    # 0.99
    
        _plotTrajectory = {'markersize' : (4.0, 6.0, 6.0), # ASS, Molchan, ROC
                           'color': 'k'}
    
    
    __logger = None
    
    # Option to draw random seed value by the system or to read it from specified
    # file
    __randomSeedFileOption = "randomSeedFile"

    # Option to specify significance value to use for computation of confidence
    # bounds
    __alphaOption = "alpha"

    # Option to specify if results should be generated in Matlab format. Matlab
    # results are used for reference only. Default is 'false' - don't generate it.
    __matlabResultsOption = "matlabResults"

    # Option to specify the only forecast model to invoke the test for:
    # base class EvalutaionTest will trigger specified test for each model
    # within forecast group. This option allows to invoke the test only for one
    # specified model of the group. Default is None meaning to 
    __forecastOption = "forecast"
    
    # Default values for input parameters
    __defaultArgs = {__randomSeedFileOption : None,
                     __alphaOption : '0.025',
                     __matlabResultsOption : 'false',
                     __forecastOption : None}
    
    
    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    #        args - Optional input arguments for the test. Default is None.
    # 
    def __init__ (self, group, args = None):
        """ Initialization for AlarmBasedTest class."""
        
        # Constructors for base classes
        EvaluationTest.EvaluationTest.__init__(self, group)
        ReproducibilityFiles.ReproducibilityFiles.__init__(self)
        
        if AlarmBasedTest.__logger is None:
           AlarmBasedTest.__logger = CSEPLogging.CSEPLogging.getLogger(AlarmBasedTest.__name__)
        
        # Input arguments for the model were provided:
        self.__args = CSEPInputParams.CSEPInputParams.parse(AlarmBasedTest.__defaultArgs,
                                                            args)
        
        
    #---------------------------------------------------------------------------
    #
    # Returns file prefix for test result file.
    #
    # Input: None
    #
    # Output: File prefix used by test results.
    #
    @classmethod
    def filePrefix (cls):
        """ Returns file prefix for test result file."""
        
        return AlarmBasedTest.__filePrefix
        
        
    #---------------------------------------------------------------------------
    #
    # Formats filename for the evaluation test summary of all models in the 
    # forecast group. This method overwrites base-class implementation of the
    # method since there are no summary files for all models for now.
    #
    # Input: None
    #
    # Output: Filename for all-models summary file
    #
    def allModelsSummaryFile (self):
        """ Formats filename for the evaluation test summary of all models in the 
            forecast group."""

        # Path to the all models summary file - None
        return None
        
        
    #-----------------------------------------------------------------------------
    #
    # Returns description word for the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: Description of the test (such RELMTest, AlarmTest, etc.)
    #
    def typeDescriptor (self):
        """ Returns test type descriptor."""

        return AlarmBasedTest.__type
        

    #----------------------------------------------------------------------------
    #
    # Writes comma-separated list of other forecasts models participating in the
    # test if any
    #
    # Input:
    #        forecast_name - Forecast model for which evaluation test is invoked.
    #
    # Output: List of all other forecasts models participating in the test
    #
    def otherForecastsFiles (self, forecast_name):
        """ Returns list of all other (if any) forecasts in the same forecast group 
            for the test."""
        
        pass  


    #----------------------------------------------------------------------------
    #
    # Create input parameter file for the run.
    #
    # Input: 
    #       forecast_name - Name of forecast model for the test
    #
    # Output: filename for parameter file
    #
    def createParameterFile (self, forecast_name):
        """ Create input parameter file for the run."""
        
        result_prefix = "%s_%s" %(self.filePrefixPattern(),
                                  CSEPFile.Name.extension(forecast_name))
        
        parameter_file = os.path.join(self.testDir,
                                      result_prefix + EvaluationTest.EvaluationTest._paramFilePostfix)
        
        fhandle = CSEPFile.openFile(parameter_file,
                                    CSEPFile.Mode.WRITE)
        
        xml_forecast = os.path.join(self.forecasts.dir(),
                                    CSEPFile.Name.xml(forecast_name,
                                                      CSEP.Forecast.FromXMLPostfix))
        
        if not os.path.exists(os.path.join(self.forecasts.dir(),
                                           xml_forecast)):
            # XML format of the forecast does not exist, create one but use 
            # filename which is derived from existing ASCII file name
            template = ForecastHandlerFactory().CurrentHandler.XML(self.forecasts.postProcess().template)
            xml_forecast = template.toXML(os.path.join(self.forecasts.dir(),
                                                       forecast_name), 
                                          self.forecasts.postProcess().start_date,
                                          self.forecasts.postProcess().end_date)
            # Create metadata file for the forecast 
            comment = "Forecast file in %s format that is based on XML master template %s" \
                      %(CSEPFile.Format.XML, 
                        self.forecasts.postProcess().template)
             
            Forecast.metadata(xml_forecast,
                              comment)
            
            
        fhandle.write("pathToForecastFile=%s\n" %xml_forecast)
        
        # Write forecasts files other than tested model to be included
        other_models = [CSEPFile.Name.xml(model, CSEP.Forecast.FromXMLPostfix) \
                        for model in self.otherForecastsFiles(forecast_name)]
        
        if len(other_models):
            
           # Check if XML format of each forecast exists, and create one based
           # on existing ASCII filenames
           revised_other_models = []

           for each_model, each_ascii in zip(other_models,
                                             self.otherForecastsFiles(forecast_name)):
               xml_model = each_model
               
               if not os.path.exists(each_model):

                   template = ForecastHandlerFactory().CurrentHandler.XML(self.forecasts.postProcess().template)                   
                   xml_model = template.toXML(each_ascii, 
                                              self.forecasts.postProcess().start_date,
                                              self.forecasts.postProcess().end_date)
                   # Create metadata file for the forecast 
                   comment = "Forecast file in %s format that is based on XML master template %s" \
                             %(CSEPFile.Format.XML, 
                               self.forecasts.postProcess().template)
                     
                   Forecast.metadata(xml_model,
                                     comment)
                   
               revised_other_models.append(xml_model)
            
            
           fhandle.write("pathsToOtherForecasts=%s\n" %','.join(revised_other_models))

        fhandle.write("pathToCatalogFile=%s\n" %CSEPFile.Name.ascii(self.catalogFile.name))
        
        result_file = result_prefix + EvaluationTest.EvaluationTest._resultFilePostfix
        fhandle.write("pathToResultsFile=%s\n" %os.path.join(self.testDir,
                                                             result_file))
        
        fhandle.write("alpha=%s\n" %self.__args[AlarmBasedTest.__alphaOption])   
        fhandle.write("produceMatlabResults=%s\n" %self.__args[AlarmBasedTest.__matlabResultsOption])   
        
        # Flag if random seed value should be drawn by the system
        seed_file = os.path.join(self.testDir,
                                 '%s_%s' %(result_prefix,
                                           EvaluationTest.EvaluationTest._randomSeedFile))
        
        if self.__args[AlarmBasedTest.__randomSeedFileOption] is not None:
           seed_file = self.__args[AlarmBasedTest.__randomSeedFileOption]
        else:
           
           # Create seed value and store it in the file to be passed to the test
           seed = CSEPRandom.createSeed()
           
           seed_fhandle = CSEPFile.openFile(seed_file,
                                            CSEPFile.Mode.WRITE)
           seed_fhandle.write('seed=%s\n' %seed)
           seed_fhandle.close()
           
           # Register for reproducibility
           info_msg = "Seed value used by Java random number generator for %s \
alarm-based test for forecast model '%s' in '%s' directory." %(self.type(),
                                                               forecast_name,
                                                               self.forecasts.dir())


           # Record parameter file with reproducibility registry
           ReproducibilityFiles.ReproducibilityFiles.add(self,
                                                         os.path.basename(seed_file),
                                                         info_msg,
                                                         CSEPFile.Format.ASCII)
           
              
        fhandle.write('pathToSeedFile=%s\n' %seed_file)
        
        # Add option for the forecast masking bit
        use_masking_bit = str(CSEP.Forecast.UseWeights).lower()
            
        fhandle.write('useMaskBit=%s\n' %use_masking_bit)
            
        fhandle.close()

        
        # Register input parameters file for reproducibility
        info_msg = "Input parameters file used by %s alarm-based test for forecast \
model '%s' in '%s' directory." %(self.type(),
                                 forecast_name,
                                 self.forecasts.dir())


        # Record parameter file with reproducibility registry
        ReproducibilityFiles.ReproducibilityFiles.add(self,
                                                      os.path.basename(parameter_file),
                                                      info_msg,
                                                      CSEPFile.Format.ASCII)
     
        return parameter_file


    #----------------------------------------------------------------------------
    #
    # Invoke Java code for the test.
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def evaluate (self,
                  forecast_name):
        """ Invoke Java code for the evaluation test."""


        # Invoke the test for each model in the group or only for specified model
        model = CSEPFile.Name.xml(forecast_name,
                                  CSEP.Forecast.FromXMLPostfix)
        
        if self.__args[AlarmBasedTest.__forecastOption] is None or \
           CSEPFile.Name.xml(self.__args[AlarmBasedTest.__forecastOption],
                             CSEP.Forecast.FromXMLPostfix) == model:
           
           AlarmBasedTest.__logger.info("%s alarm-based test for %s" %(self.type(),
                                                                       forecast_name))

           
           # Create parameter file for the run
           parameter_file = self.createParameterFile(forecast_name)
           
           # invoke evaluation test:
           # -Xms128m -Xmx1024m - to increase heap size
           Environment.invokeCommand('java -Xms128m -Xmx1024m -classpath %s %s %s' 
 %(AlarmBasedTest.__codePath,
                                       AlarmBasedTest.__executableFile,
                                       parameter_file))
           
           # Handle files required by reproducibility: create unique copies and 
           # remove original data
           ReproducibilityFiles.ReproducibilityFiles.copyAndCleanup(self,
                                                                    AlarmBasedTest.__type,
                                                                    self.testDir)
        else:
           
           AlarmBasedTest.__logger.info("Skipping %s alarm-based test for %s" %(self.type(),
                                                                                forecast_name))

    #----------------------------------------------------------------------------
    #
    # Plot test results. Child classes should overwrite the method.
    #
    # Input: 
    #        result_file - Path to the result file in XML format
    #
    # Output: 
    #        DOM tree object for result file
    #
    @classmethod
    def plot (cls, result_file):
        """ Plot test results in XML format."""
 
        # Read the whole file in
        return CSEPInitFile.CSEPInitFile(result_file)
           
        
    #-----------------------------------------------------------------------------
    #
    # Update cumulative test result data with daily result. This method can
    # be overwritten by derived classes. Alarm-based evaluation tests don't have
    # cumulative test results, therefore the class overwrites the method not to 
    # update the cumulative results.
    #
    # Input: 
    #        result_file - Daily result file to be used to update 
    #                      corresponding cumulative result file.
    #
    # Output: None.
    #
    def updateCumulativeResultData (self, result_file):
        """ Update cumulative test result data with daily result."""

        pass

