"""
EvaluationTest module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, re, shutil, glob, datetime, matplotlib
from pylab import *
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt

import CSEP, CSEPLogging, Environment, CSEPFile, CSEPPropertyFile, CSEPUtils, \
       CSEPInitFile 
from PostProcess import PostProcess
from Forecast import Forecast
from ResultsSummary import ResultsSummary
from ResultsCumulativeSummary import ResultsCumulativeSummary
from ResultsSummaryFactory import ResultsSummaryFactory
from AllModelsSummary import AllModelsSummary
from CSEPOptions import CommandLineOptions


#--------------------------------------------------------------------------------
#
# This module contains base class for evaluation tests within CSEP testing center.
#
class EvaluationTest (object): 
   
   # Static data of the class

   #===========================================================================
   # Nested class with matplotlib settings for the test     
   #===========================================================================
   class Matplotlib (object):

      # Static data
      plotZOrder = {'modification' :   1,
                    'shade'        :  10,
                    'bounds'       :  20,  
                    'vertical'     :  30,
                    'grid'         :  40,
                    'rejection'    :  50,
                    'trajectory'   :  60,
                    'legend'       : 149,
                    'axes'         : 150}
   
      # Color abbreviations used by matplotlib
      # b - blue, g - green, r - red, c - cyan, m - magenta, y - yellow, k - black
        
      # Line marker abbreviations used by matplotlib
      # o     # circle symbols
      # ^     # triangle up symbols
      # v     # triangle down symbols
      # <     # triangle left symbols
      # >     # triangle right symbols
      # s     # square symbols
      # +     # plus symbols
      # x     # cross symbols
      # D     # diamond symbols
      # d     # thin diamond symbols
      # 1     # tripod down symbols
      # 2     # tripod up symbols
      # 3     # tripod left symbols
      # 4     # tripod right symbols
      # h     # hexagon symbols
      # H     # rotated hexagon symbols
      # p     # pentagon symbols
      _plotColorMarker = {'marker': ['o', 'D', '^', 'v', '<', '>', 's',
                                     '+', 'x', 'd', '1', '2', '3', '4'],
                          'colors': ['g', 'b', 'r', 'm', 'c', 'y'] }
      
      _plotLabelsFont = {'fontname'   : 'monospace',
                         'fontweight' : 'normal',
                         'fontsize'   : 13}
      
      _plotLegend = {'loc'            : 3,
                     'bbox_to_anchor' : (0.0, 1.02, 1.0, 0.102),
                     'mode'           :"expand", 
                     'columnspacing'  : 2.0,
                     'prop'           : FontProperties(size='x-small',
                                                       style='normal',
                                                       family='monospace')}
      
      _titleFont = {'fontname':'monospace',
                    'fontsize': 10,
                    'weight' : 'normal',
                    'zorder' : 90}


      #------------------------------------------------------------------------
      #
      # Given index of the trajectory to be plotted, compute matplotlib marker 
      # type and color for the trajectory on the plot. 
      #
      # Input: 
      #        traj_index - Trajectory index to plot.
      #
      # Output: tuple of matplotlib marker type and color for the trajectory
      #  
      @classmethod
      def colorMarker(cls, traj_index):
         """ Given index of the trajectory to be plotted, compute matplotlib 
             marker type and color for the trajectory on the plot."""
       
         color_index = None
         marker_index = None
          
         num_colors = len(EvaluationTest.Matplotlib._plotColorMarker['colors'])
          
         # Assign color and marker to the trajectory
         color_index = traj_index % num_colors
         marker_index = traj_index / num_colors
    
         if marker_index >= len(EvaluationTest.Matplotlib._plotColorMarker['marker']):
             error_msg = "%s: There are more trajectories in the %s test result than \
number of unique trajectory identifiers are available. Please expand plot color or marker \
selection. Trajectory index is '%s' vs. number of available colors '%s' and \
number of available markers '%s' for the plot." %(CSEPLogging.CSEPLogging.frame(cls),
                                                  cls.__name__,
                                                  traj_index,
                                                  num_colors, 
                                                  len(EvaluationTest.Matplotlib._plotColorMarker['marker']))
    
             EvaluationTest.__logger.error(error_msg)
             raise RuntimeError, error_msg
          
         return (EvaluationTest.Matplotlib._plotColorMarker['marker'][marker_index],
                 EvaluationTest.Matplotlib._plotColorMarker['colors'][color_index])


   # Sub-directory to store "old" result files that were already published
   # (to be used only if test day is re-processed)
   _archiveDir = "archive"

   # Postfix used for input parameters file
   _paramFilePostfix = "_input" + CSEPFile.Extension.TEXT
   
   # Postfix used for result file
   _resultFilePostfix = "_result" + CSEPFile.Extension.XML

   # Postfix used for random seed file
   _randomSeedFile = 'randomSeed' + CSEPFile.Extension.ASCII

   __logger = None

   # Pattern used to match map PNG files for forecast models
   __mapPattern = '%s*%s' %(CSEP.Forecast.MapPrefix,
                            CSEPFile.Extension.PNG)


   # Prefix for result filename    
   FilePrefix = 'Test'
   
   # Number of simulations for the test.
   NumberSimulations = 1000
   
   # Flag if plots corresponding to tests results should be generated. Default
   # is True - to generate the plots (to support new web viewer which
   # will generate plots on demand) 
   GenerateResultPlot = True
   

   #============================================================================
   # Nested class that represents evaluation test result data as dictionary type.
   # Derived classes should derive from the class to provide specifics of the
   # test results.    
   #============================================================================
   class Result (dict):
        
       # Names of results variables
       Root = 'CSEPResult'
       ResultData = 'resultData'
       Name = 'name'
       FileAttribute = 'file'
       Description = 'description'
       CreationInfo = 'creationInfo'
       Version = 'CSEPVersion'

       # Names of attributes
       PublicID = 'publicID'
       CreationTime = 'creationTime'
       
       _plotFont = {'size' : 'small', 
                    'style' : 'normal',
                    'weight' : 'normal', 
                    'family' : 'monospace'}            

        
       def __init__ (self):
           """ Initialize method for EvaluationTest.Result object"""
           dict.__init__(self, {})


       #=======================================================================
       # writeXML
       # 
       # Write test results to XML format file
       #
       # Inputs:
       #         test_name - Name of evaluation test
       #         model_filename - Filename of the model for the test
       #         dirpath - Directory to write XML format file to
       #         file_prefix - Prefix to use for XML format filename
       #
       # Output: Tuple of test_node and xml document objects
       #  
       #=======================================================================
       def writeXML (self, 
                     test_name, 
                     model_filename, 
                     dirpath,
                     file_prefix,
                     result_file = None):
            """Write test results to XML format file"""
          
          
            # Strip file extension from model filename
            model_name = ''

            # Do nothing if tuple of model filenames are provided - all of the
            # participating forecasts are listed: should be captured inside of
            # XML file, but not in filename
            if isinstance(model_filename, list) is True:
                model_name = '_'.join([CSEPFile.Name.extension(name) for name in model_filename])
            elif isinstance(model_filename, str) is True:
                model_name = CSEPFile.Name.extension(model_filename)

            # RTT test provides name for cumulative XML file
            result_file_path = result_file
            if result_file_path is None:
                name_keywords = [file_prefix,
                                 test_name]
                
                if len(model_name):
                    name_keywords.append(model_name)
                     
                # Construct filename for the test result
                result_file_path = os.path.join(dirpath,
                                                "%s%s" %('_'.join(name_keywords),
                                                         CSEPFile.Extension.XML))
                
            xml = CSEPInitFile.CSEPInitFile(result_file_path)
            xml.addElement(EvaluationTest.Result.Root)
            
            result_node = xml.addElement(EvaluationTest.Result.ResultData)
            result_node.attrib[EvaluationTest.Result.PublicID] = 'smi://org.scec/csep/results/1'
            
            # XML format of test name
            xml_test_name = test_name.replace('-', '')
            
            test_node = xml.addElement(xml_test_name, 
                                       result_node)
            test_node.attrib[EvaluationTest.Result.PublicID] = 'smi://org.scec/csep/tests/%s/1' \
                                                                %xml_test_name.lower()

            # Create description element
            description_node = xml.addElement(EvaluationTest.Result.Description,
                                              test_node)

            # Create name element
            if isinstance(model_filename, str) is True or \
               isinstance(model_filename, tuple) is True:
                name_node = xml.addElement(EvaluationTest.Result.Name,
                                           test_node)
                
                num_models_str = ''
                if isinstance(model_filename, tuple) is True:
                    # Have to capture names of all participating models for the test
                    model_name = ' '.join([CSEPFile.Name.extension(name) for name in model_filename])
                    if len(model_filename) > 1:
                        num_models_str = 's'
                    
                name_node.text = model_name
                
                # Preserve filename of the forecast contribution to the result
                if isinstance(model_filename, str):
                    name_node.attrib[EvaluationTest.Result.FileAttribute] = model_filename
                    
                description_node.text = 'This is %s for %s model%s.' %(test_name, 
                                                                       model_name,
                                                                       num_models_str)

            else:
                 description_node.text = 'This is %s for %s models.' %(test_name, 
                                                                       ' '.join([CSEPFile.Name.extension(name) for name in model_filename]))
            
            # Add creationInfo element
            creation_node = xml.addElement(EvaluationTest.Result.CreationInfo,
                                           test_node)
                                   
            # Set creation time
            creation_node.attrib[EvaluationTest.Result.CreationTime] = datetime.datetime.now().strftime(CSEP.Time.ISO8601Format)                                 
      
            # Capture CSEP version directly (even though it can be traced through runtime log file
            # associated with test result)
            creation_node.attrib[EvaluationTest.Result.Version] = CSEP.Version
      
            return (test_node, xml)
        

   #========================================================================
   # Utility class to store information about the file: file path and 
   # numpy.array object that represents downloaded data
   #========================================================================
   class FileInfo (object):
       
       def __init__ (self, file_path=None, file_object=None):
           """Initialize FileInfo object"""
           
           self.name = file_path
           
           self.npObject = file_object
           
           # A place holder to store intermediate data product for observation catalog.
           # Used by following classes:
           # 1. DiagnosticsTest.py:
           #    In case when prepared (for example, filtered catalog) should be
           #    written to the file (for example, file path is passed to original 
           #    evaluation test code), use this place holder to store filename for
           #    such intermediate data product. Default is None, meaning self.name
           #    filename is used to store data product
           # 2. StatisticalTest.py: 
           #    Stores dictionary of dates for observed events
           self.intermediateObj = None


   #-----------------------------------------------------------------------------
   #
   # Initialization.
   #
   # Input: 
   #        group - ForecastGroup object. This object identifies forecast
   #                models to be invoked.
   # 
   def __init__ (self, group):
      """ Initialization for EvaluationTest class."""
   
      if EvaluationTest.__logger is None:
         EvaluationTest.__logger = CSEPLogging.CSEPLogging.getLogger(EvaluationTest.__name__)
         
      # Initialize forecast group for the test
      self.forecasts = group      
      if self.forecasts is None:
         error_msg = "ForecastGroup must be specified for the evaluation test."
           
         EvaluationTest.__logger.error(error_msg)
         raise RuntimeError, error_msg
        
      # Filename to be used for catalog data - defined by post-processing
      # module
      self.catalogFile = EvaluationTest.FileInfo()
        
      # Filename to store optional catalogs with applied uncertainties
      self.catalogModificationsFile = EvaluationTest.FileInfo()

      # Filename to store optional cumulative catalog
      self.cumulativeCatalogFile = EvaluationTest.FileInfo()

      # Test date
      self.testDate = None
     
      # Test directory to store results to
      self.testDir = None
      
      # Scale factor for the forecast that represents test date
      self.scaleFactor = None


   #----------------------------------------------------------------------------
   #
   # Initialize settings as provided on a command-line
   #
   @staticmethod
   def initialize(num_test_simulations,
                  result_plot = True):
       """ Initialize settings as provided on a command-line"""
       
       EvaluationTest.NumberSimulations = num_test_simulations
       EvaluationTest.GenerateResultPlot = result_plot
        

   #-----------------------------------------------------------------------------
   #
   # Return test type as extracted from the results filename.
   #
   # Input: 
   #        filename - Filename for test results.
   #    
   # Output:
   #        Token representing the test type.
   #
   @staticmethod
   def typeFromFilename(filename):
      """ Extract type of evaluation test from result filename."""
          
      # Extract test type from the filename of results summary:
      # RELM test: N, L, or R 
      # Alarm-based test: ROC, ASS
      test_type = re.search('(?<=.%s_)[A-Z]+' % EvaluationTest.FilePrefix,
                            filename)
     
      if test_type is None:
         error_msg = "Could not extract evaluation test identifier \
from the filename '%s'. Unexpected result filename format." % (filename)

         EvaluationTest.__logger.error(error_msg)
         raise RuntimeError, error_msg
      
      return test_type.group(0)


   #-----------------------------------------------------------------------------
   #
   # Returns keyword identifying the test. Implemented by derived classes.
   #
   # Input: None
   #
   # Output: String representation of the test type.
   #
   def type (self):
       """ Returns test type."""

       pass


   #----------------------------------------------------------------------------
   #
   # Formats filename for the evaluation test summary of all models in the 
   # forecast group.
   #
   # Input: None
   #
   # Output: Filename for all-models summary file
   #
   def allModelsSummaryFile (self):
       """ Formats filename for the evaluation test summary of all models in the 
           forecast group."""

       # Path to the all models summary file
       return AllModelsSummary.Type + \
              self.filePrefixPattern() + \
              CSEPFile.Extension.XML


   #----------------------------------------------------------------------------
   #
   # Returns default type for the evaluation test summary that represents
   # intermediate results ("out of interest"). These results are generated
   # when evaluation tests are invoked in a middle of the testing period and
   # don't represent "final" result for the whole testing period.
   #
   # Input: None
   #
   # Output: Results summary type for intermediate results
   #
   def intermediateSummaryType (self):
       """ Returns class type to be used to create evaluation test 
           intermediate (out-of-interest) summaries."""

       return ResultsSummary.Type



   #----------------------------------------------------------------------------
   #
   # Formats filename for the evaluation test summary of all models in the 
   # forecast group.
   #
   # Input: None
   #
   # Output: Filename for all-models summary file
   #
   @classmethod
   def resultsSummaryType (cls):
       """ Returns class type to be used to calculate evaluation test summaries."""

       return ResultsCumulativeSummary.Type


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


       ### Update test summary for all models
       # Path to the all models summary file
       summary_file = self.allModelsSummaryFile()
       
       if summary_file is not None:
           summary_path = os.path.join(self.testDir,
                                       summary_file)
           
           self.updateAllModelsSummary(summary_path,
                                       result_file,
                                       self.testDate,
                                       self.forecasts.postProcess().start_date,
                                       self.forecasts.postProcess().end_date)

       
       ### Type of summary data per model 
       summary_type = self.intermediateSummaryType()
        
       # "True" result has been generated
       if self.forecasts.isLastDay(self.testDate) is True:
          summary_type = self.resultsSummaryType()
           
       # Some evaluation tests don't have corresponding cumulative summaries 
       if summary_type is None:
           return 
           
       # Create/update cumulative/intermediate results that corresponds to the
       # daily result file
       # Strip path from the filename
       cum_entry = os.path.basename(result_file)
       
       # Strip forecast date from the result filename if any
       cum_entry = re.sub(Forecast.NameSeparator.join(['',
                                                       '[0-9]+',
                                                       '[0-9]+',
                                                       '[0-9][0-9][0-9][0-9]']), 
                          "", cum_entry)

       
       summary_file = os.path.join(self.forecasts.resultDir(),
                                   summary_type + cum_entry)
       
       # Input arguments for summary file object
       args = [summary_file, 
               self.__class__]
       results_summary = ResultsSummaryFactory().object(summary_type,
                                                        args)
       
       # Some cumulative results require test to be invoked on cumulative data
       results_summary.evaluationTest(self)
       
       results_summary.update(result_file, 
                              self.testDate.date(),
                              self.forecasts.postProcess().start_date.date(),
                              self.forecasts.postProcess().end_date.date())
       
       # Generate plot of summary results
       image_files = self.__class__.plotSummary(summary_file)
       
       if results_summary.preserve() is True:
           # Preserve summary files into daily results directory
           shutil.copyfile(summary_file,
                           os.path.join(self.testDir,
                                        os.path.basename(summary_file)))

           # If only one image file is generated by summaries, treat it as 
           # single element list
           if isinstance(image_files, list) is False:
               image_files = [image_files]
           
           for each_image in image_files:
               shutil.copyfile(each_image,
                               os.path.join(self.testDir,
                                            os.path.basename(each_image)))


   #----------------------------------------------------------------------------
   #
   # Update evaluation test result (per all participating models) with daily 
   # result. This method can be overwritten by derived classes. 
   # Alarm-based evaluation tests don't have
   # cumulative test results, therefore the class overwrites the method not to 
   # update test results.
   #
   # Input: 
   #        summary_file - Path to the evaluation test summary for all models
   #                       participating in the forecast group
   #        result_file - Daily result file to be used to update 
   #                      all model result file.
   #        test_date - datetime.date object that represents the test date
   #                    for the result file
   #        start_date - Start date for the forecast period
   #        end_date - End date for the forecast period
   #
   # Output: None.
   #
   @classmethod
   def updateAllModelsSummary (cls, 
                               summary_file,
                               result_file,
                               test_date,
                               start_date,
                               end_date):
       """ Update "all-models" test result with result for particular model(s)."""
       
       summary_doc = AllModelsSummary(summary_file, 
                                      cls)
       
       summary_doc.update(result_file,
                          test_date,
                          start_date,
                          end_date)          

   #----------------------------------------------------------------------------
   #
   # Create plot of evaluation test summary for all participating model of 
   # the forecast group. This method should be implemented by derived classes.
   # Default behavior is don't generate any plots. 
   #
   # Input: 
   #        summary_path - Path to the summary file for the test
   #        output_dir - Directory to place plot file to. Default is None.
   #        test_object - EvaluationTest object for which method is invoked.
   #                      Default is None.
   #
   # Output: List of plot files
   #
   @classmethod
   def plotAllModelsSummary(cls,
                            summary_path,
                            output_dir = None,
                            test_obj = None):
       
       return []
   

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

       pass
   

   #-----------------------------------------------------------------------------
   #
   # Returns flag if forecasts are required by the evaluation test. Default is
   # to require forecasts by evaluation test.
   #
   # Input: None
   #
   # Output: True if forecasts are required by the evaluation test, False
   #         otherwise.
   #
   def forecastsRequired (self):
       """ Returns flag if forecasts are required by the evaluation test."""

       return True


   #---------------------------------------------------------------------------
   #
   # Returns flag if observation data is required by the evaluation test.
   #
   # Input: None
   #
   # Output: True if observation data is required by the evaluation test, False
   #         otherwise.
   #
   def observationRequired (self):
       """ Returns flag if observation data is required by the evaluation test."""

       return True


   #----------------------------------------------------------------------------
   #
   # Prepare RELM evaluation test based on provided test date, and result 
   # directories
   #
   # Input: 
   #        test_date - datetime object that represents a test date.
   #        catalog_dir - Directory to store (read) catalog data to (from). 
   #                      This option is introduced to provide flexibility 
   #                      on where to store/read catalog data to/from. Could
   #                      use ForecastGroup.catalogDir() - but it defaults to
   #                      'forecastDirectory/catalogs' if none is provided in
   #                      the ForecastGroup config file.
   #        test_dir - Test directory to write output data to.    
   #
   def prepare (self, 
                test_date,
                catalog_dir,
                test_dir):
        """ Prepare evaluation test based on provided test date, and result 
            directories"""
    
    
        self.testDate = test_date
        self.testDir = test_dir
   
        # To support TD project - evaluation tests don't require any observation
        if self.observationRequired() is True:
   
            ### Exit the test if catalog file doesn't exist or was not generated
            post_process = self.forecasts.postProcess()
            self.catalogFile.name = os.path.join(catalog_dir,
                                                 post_process.files.catalog)
            
            # Optional catalog uncertainties file
            self.catalogModificationsFile.name = os.path.join(catalog_dir,
                                                              post_process.files.uncertainties.catalog)
            
            if post_process.files.cumulativeCatalog is not None:
                # Cumulative catalog exists for the test
                self.cumulativeCatalogFile.name = os.path.join(catalog_dir,
                                                               post_process.files.cumulativeCatalog)
            else:
                # Use observation catalog as cumulative (for file-based forecasts)
                self.cumulativeCatalogFile.name = os.path.join(catalog_dir,
                                                               post_process.files.catalog)
                
            # Initialize post-processing: fix for Trac ticket #181: Re-store ability
            # to re-process one-day forecasts with existing observation catalogs
            post_process.startDate(test_date)
       
            if not os.path.exists(self.catalogFile.name):
                error_msg = "Expected catalog file %s does not exist. Exiting the %s test." \
                            %(self.catalogFile.name,
                              self.type())
                            
                EvaluationTest.__logger.error(error_msg)
                raise RuntimeError, error_msg
   
   
        if not os.path.exists(self.testDir):
            EvaluationTest.__logger.info("Creating directory '%s'..." \
                                         %self.testDir)
   
            os.mkdir(self.testDir)
        else:
           
           # Result directory already exists - check if any old result files 
           # need to be archived (check by evaluation test type)
           # NOTE: all-models summaries will match the pattern
           old_files = glob.glob(os.path.join(self.testDir,
                                              '%s*%s*' %(CSEP.NAMESPACE, 
                                                         self.filePrefixPattern())))
           
           # Failed runs may leave result files with original names - archive them to 
           # avoid renaming by process that didn't create them and appending new
           # result elements to existing files
           old_files.extend(glob.glob(os.path.join(self.testDir,
                                                   '%s*%s' %(self.filePrefixPattern(),
                                                             CSEPFile.Extension.XML))))

           # Sometimes failed runs leave all-models summary files with original
           # filename which doesn't get picked up by previous glob pattern,
           # check for it explicitly 
           __summary_file = self.allModelsSummaryFile()
           if __summary_file is not None:
               old_files.extend(glob.glob(os.path.join(self.testDir,
                                                       __summary_file)))
           
           # Archive forecasts maps - they will be generated again
           if CSEP.Forecast.GenerateMap is True:
              old_files.extend(glob.glob('%s/*%s*' %(self.testDir,
                                                     CSEP.Forecast.MapPrefix)))
              old_files.extend(glob.glob('%s/%s*' %(self.testDir,
                                                    CSEP.Forecast.MapReadyPrefix)))
           
           
           if len(old_files) != 0:
              
              # Move files to archive directory - not to be published again
              archive_dir = os.path.join(self.testDir,
                                         EvaluationTest._archiveDir)
              
              for entry in old_files:
                 EvaluationTest.__logger.info('Renaming %s to %s' %(entry,
                                                                    os.path.join(archive_dir, os.path.basename(entry))))
                 os.renames(entry,
                            os.path.join(archive_dir, os.path.basename(entry)))
    
        return
    
    
   #--------------------------------------------------------------------
   #
   # Run evaluation test for specified forecast models.
   #
   # Input: 
   #        test_date - datetime object that represents a test date.
   #        catalog_dir - Directory to store (read) catalog data to (from). 
   #                      This option is introduced to provide flexibility 
   #                      on where to store/read catalog data to/from. Could
   #                      use ForecastGroup.catalogDir() - but it defaults to
   #                      'forecastDirectory/catalogs' if none is provided in
   #                      the ForecastGroup config file.
   #        test_dir - Test directory to write output data to.    
   #
   def run (self, test_date,
                  catalog_dir,
                  test_dir):
        """ Invoke test for specified forecast models."""
   
        # Evaluate forecast models if test date is within the schedule
        if not self.forecasts.hasTests(test_date):
           return


        self.prepare(test_date, 
                     catalog_dir, 
                     test_dir)
        
        files_to_email = None
        
        ### To support EEW project:
        # If forecasts are not required for the evaluation test, invoke the test
        if self.forecastsRequired() is False:
            files_to_email = self.evaluate()
            
        else:
            # Invoke evaluation test for each model
            for forecast_model in self.forecasts.files():
    
               # Compute scale factor for the forecast
               if self.scaleFactor is None and \
                  self.forecasts.postProcess() is not None:
                   self.scaleFactor = self.forecasts.postProcess().scaleFactor(self.testDate,
                                                                               self.testDir)
                
               # Generate map of the forecast
               self.createMap(forecast_model)
               
               # Invoke the test
               files_to_email = self.evaluate(forecast_model) 
            
                
        EvaluationTest.__logger.info("Done with %s test." % self.type())
        return files_to_email


    #----------------------------------------------------------------------------
    #
    # Invoke evaluation test for the model. To be implemented by child classes.
    #
    # Input: 
    #        forecast_file - Forecast file to test
    #
    # Output:
    #        None
   def evaluate (self, forecast_file = None):
      """ Invoke evaluation test for the model. This method should be implemented
          by derived classes."""

      # Raise an exception if method is not implemented by child class
      error_msg = "evaluate() method is not implemented by %s class (invoked for %s model)." \
                  %(self.type(),
                    forecast_file)
      
      EvaluationTest.__logger.error(error_msg)
      raise RuntimeError, error_msg


    #----------------------------------------------------------------------------
    #
    # Create forecast map.
    #
    # Input: 
    #        forecast_file - Forecast file to test
    #
    # Output:
    #        Forecast map file.
    #
   def createMap (self, forecast_file):
      """ Create forecast map."""

      # Create map file for scaled down forecast and observed events
      self.forecasts.createMap(forecast_file,
                               self.testDir,
                               CSEPFile.Name.ascii(self.catalogFile.name),
                               scale_factor = self.scaleFactor)
   

   #----------------------------------------------------------------------------
   #
   # Returns file prefix pattern for test result file.
   #
   # Input: None
   #
   # Output: File prefix used by test results.
   #
   def filePrefixPattern (self):
       """ Returns file prefix pattern for test result file."""
    
       return '%s_%s-%s' % (self.filePrefix(),
                           self.type(),
                           EvaluationTest.FilePrefix)


   #----------------------------------------------------------------------------
   #
   # Returns file prefix for test result file. This method is implemented by 
   # children classes.
   #
   # Input: None
   #
   # Output: File prefix used by test results.
   #
   @classmethod
   def filePrefix (cls):
       """ Returns file prefix for test result file."""
        
       pass


   #----------------------------------------------------------------------------
   #
   # Returns list of file patterns to exclude from being published.
   #
   # Input: None
   #
   # Output: Empty list of file patterns.
   #
   def excludePatterns (self):
       """ Returns list of file patterns to exclude from being published."""

       return []
     
     
   #----------------------------------------------------------------------------
   #
   # Returns list of file patterns to be published.
   #
   # Input: None
   #
   # Output: Empty list of file patterns.
   #
   def publishPatterns (self):
       """ Returns list of file patterns to publish."""

       # SVG images are published only
       return ['*%s*' %CSEPFile.Extension.SVG]


   #----------------------------------------------------------------------------
   #
   # Returns list of file patterns to email in status message by processing
   # Dispatcher process
   #
   # Input: None
   #
   # Output: Empty list of file patterns.
   #
   def emailPatterns (self):
       """ Returns list of file patterns to email in status message by 
           processing Dispatcher process."""

       return []


   #----------------------------------------------------------------------------
   #
   # Create copies of test results files with unique filenames 
   # and generate corresponding metadata files. New files are generated
   # under the same directory as original result files.
   #
   # Input: None.
   #
   # Output: 
   #        True if result data is available, False - otherwise.
   #
   def resultData (self):
      """ Copy test result and related data to files with unique names, 
          and generate corresponding metadata files."""

      # There is no directory with tests results
      if self.testDir is None or (not os.path.exists(self.testDir)):
         return False
     

      # XML results files for the test - cumulative results and plots are based
      # on XML format of test results
      pattern = os.path.join(self.testDir,
                             "%s*%s" %(self.filePrefixPattern(),
                                       CSEPFile.Extension.XML))
      file_list = glob.glob(pattern)
      
      
      email_files = []
      email_patterns = self.emailPatterns()
      
      for entry_path in file_list:
           
         entry = os.path.basename(entry_path)
           
         # Use filename as a descriptor
         datafile, metafile = CSEPPropertyFile.CSEPPropertyFile.filenamePair(self.typeDescriptor(),
                                                                             entry)
         
         # Pass result file to the forecast group, and update corresponding
         # cumulative or intermediate summary if necessary
         self.updateCumulativeResultData(entry_path)

         if EvaluationTest.GenerateResultPlot is True:

             ### Generate plot file for the test result based on XML format data:
             #   plot method is a classmethod 
             plots = self.__class__.plot(entry_path)
              
             for each_plot in plots:
                  
                plot_file = os.path.basename(each_plot)
               
                # Create unique copy of the plot file
                plot_datafile, plot_metafile = CSEPPropertyFile.CSEPPropertyFile.filenamePair(self.typeDescriptor(),
                                                                                              plot_file) 
                plot_format = CSEPFile.Extension.toFormat(plot_file)             
                plot_comment = "Plot for %s %s evaluation test result file '%s'." \
                                %(self.typeDescriptor(),
                                  self.type(),
                                  datafile) 
       
                CSEPFile.copy(each_plot,
                              os.path.join(self.testDir, plot_datafile))
               
                # Create metadata file
                CSEPPropertyFile.CSEPPropertyFile.createMetafile(os.path.join(self.testDir,
                                                                              plot_metafile),
                                                                 each_plot,
                                                                 plot_format,
                                                                 plot_comment)
                
                for each_pattern in email_patterns:
                    if each_pattern.search(plot_datafile) is not None:
                        email_files.append(os.path.join(self.testDir,
                                                        plot_datafile))
               
                # Remove original file
                EvaluationTest._cleanup(each_plot)
           
           
           
         # Create copy of data file
         file_format = CSEPFile.Format.XML
         comment = "%s %s evaluation test result file '%s' in %s format." \
                   %(self.typeDescriptor(),
                     self.type(),
                     entry,
                     file_format)

         CSEPFile.copy(entry_path,
                       os.path.join(self.testDir, datafile))
        
         # Create metadata file
         CSEPPropertyFile.CSEPPropertyFile.createMetafile(os.path.join(self.testDir,
                                                                       metafile),
                                                          entry,
                                                          file_format,
                                                          comment)

         for each_pattern in email_patterns:
             if each_pattern.search(datafile) is not None:
                 email_files.append(os.path.join(self.testDir,
                                                 datafile))
                 
         # Remove original file
         EvaluationTest._cleanup(entry_path)


      # Handle all-models summary files
      if self.allModelsSummaryFile() is not None:
           
           # Path to the all models summary file
           summary_file = self.allModelsSummaryFile()
           summary_path = os.path.join(self.testDir,
                                       summary_file)

           # Generate plots if applicable for all-models summary
           if EvaluationTest.GenerateResultPlot is True:

               plots = self.__class__.plotAllModelsSummary(summary_path,
                                                           test_obj = self)
    
               for each_plot in plots:
                   plot_file = os.path.basename(each_plot)
                   
                   # Create unique copy of the plot file
                   plot_datafile, plot_metafile = CSEPPropertyFile.CSEPPropertyFile.filenamePair(AllModelsSummary.__name__,
                                                                                                 plot_file) 
                   plot_format = CSEPFile.Extension.toFormat(plot_file)              
                   plot_comment = "Plot for %s %s evaluation test summary for all models of %s forecast group" \
                                   %(self.typeDescriptor(),
                                     self.type(),
                                     self.forecasts.rootDir()) 
           
                   CSEPFile.copy(each_plot,
                                 os.path.join(self.testDir, plot_datafile))
                   
                   # Create metadata file
                   CSEPPropertyFile.CSEPPropertyFile.createMetafile(os.path.join(self.testDir,
                                                                                 plot_metafile),
                                                                    each_plot,
                                                                    plot_format,
                                                                    plot_comment)
 
                   for each_pattern in email_patterns:
                       if each_pattern.search(plot_datafile) is not None:
                           email_files.append(os.path.join(self.testDir,
                                                           plot_datafile))
                   
                   # Remove original file
                   EvaluationTest._cleanup(each_plot)


           # Not all evaluation tests generate a summary for all models in the 
           # foreacast group 
           if os.path.exists(summary_path) is True and \
              summary_path not in plots:
                
               # Create unique copy of summary file
               datafile, metafile = CSEPPropertyFile.CSEPPropertyFile.filenamePair(AllModelsSummary.__name__,
                                                                                   summary_file) 
               summary_format = CSEPFile.Format.XML              
               summary_comment = "%s %s evaluation test summary for all models of the %s forecast group" \
                                 %(self.typeDescriptor(),
                                   self.type(),
                                   self.forecasts.rootDir())
       
               CSEPFile.copy(summary_path,
                             os.path.join(self.testDir, datafile))
               
               # Create metadata file
               CSEPPropertyFile.CSEPPropertyFile.createMetafile(os.path.join(self.testDir,
                                                                             metafile),
                                                                 summary_file,
                                                                 summary_format,
                                                                 summary_comment)

               for each_pattern in email_patterns:
                   if each_pattern.search(datafile) is not None:
                       email_files.append(os.path.join(self.testDir,
                                                       datafile))
               
               # Remove original file
               EvaluationTest._cleanup(summary_path)
        

      # Create unique copies of forecast maps in PNG format
      comment = "Forecast map file "
      EvaluationTest._storeResultData(self,
                                      self.typeDescriptor(),
                                      EvaluationTest.__mapPattern,
                                      CSEPFile.Format.PNG,
                                      comment)
     
      if len(email_files):
          return (True, email_files)
      
      
      return True
 
     
   #--------------------------------------------------------------------
   #
   # Publish daily plots along with summary files to the provided web
   # server.
   #
   # Input: None.
   #
   # Output: 
   #         string - Path to the tar ball with plots if any were generated,
   #                  or None if no evaluation tests were ran for the test date.
   #
   def publish (self, publish_server, publish_dir):
       """ Publish daily plots along with summary files to the provided web
           server."""

       # There are three formats of result data: Matlab, XML, ASCII, SVG and PNG
        
        
       # There is no directory with tests results or test date directory
       # does not contain any SVG files to be published - nothing to publish
       if self.testDir is None or \
          (not os.path.exists(self.testDir)):
           return None
       
       # If result directory exists, but no publishing products are available yet -
       # nothing to publish
       publish_files = []
       for each_pattern in self.publishPatterns():
           publish_files.extend(glob.glob('%s/%s' %(self.testDir, each_pattern)))
           
       if len(publish_files) == 0:
          return None
        

       # ForecastGroup top level results directory: contains cumulative files
       # and sub-directories based on test date
       root_dir = self.forecasts.rootDir()
        
       # Change directory to the parent of ForecastGroup's dir
       # to preserve dir structure during rsync
       # It's guaranteed by definition of the results directory to be
       # child of the ForecastGroup directory
       working_dir = os.path.dirname(root_dir)

       # cd to the parent directory of ForecactGroup, 
       # remember current directory 
       start_dir = os.getcwd()
       os.chdir(working_dir)

       # Extract RESULTS directory basename
       daily_path, daily_dir = os.path.split(self.testDir)
       results_path, results_dir = os.path.split(daily_path)
       group_dir = os.path.basename(results_path)

        
       try:

          # Create command to create archive of test results svg and map
          # png files: summary svg's under
          # RESULTS directory, daily svg's under RESULTS/self.__testDate
          # sub-directory, and daily png's under RESULTS/self.__testDate (only
          # if forecast map generation is enabled)
          command = "rsync -apv --relative --delete "
          
          for pattern in self.excludePatterns():
             
             command += "--exclude '%s' " % pattern
          
          
          # Add forecast group configuration file - to support Trac ticket #211 
          # (new web application)
          command += os.path.join(group_dir,
                                  os.path.basename(self.forecasts.configFile.name))
          command += ' '
          
          # Directory with observations catalogs belongs to the group,
          # publish it as well
          if root_dir == os.path.dirname(self.forecasts.catalogDir()) and \
             self.catalogFile.name is not None:

              # Publish observation catalogs if they belong to the forecast group
              # (reside directly under forecast group directory)
              command += '%s ' %os.path.dirname(self.catalogFile.name).replace(working_dir + os.sep, 
                                                                               '')

          # Publish forecasts - check if they belong to the forecast group
          # (reside directly under forecast group directory)
          forecasts_dir = self.forecasts.dir()
          if forecasts_dir == root_dir:
              
              ### File-based forecasts: use wildcard to capture all formats of
              ### the forecasts
              for each_model in self.forecasts.files():
                  command += '%s* ' %os.path.join(group_dir,
                                                  CSEPFile.Name.extension(CSEPFile.Name.xml(each_model,
                                                                                            CSEP.Forecast.FromXMLPostfix)))
          else:
              
              ### Forecasts directory is outside of the forecast group, or
              ### belongs to the group --> publish that directory
              command += '%s ' %forecasts_dir.replace(working_dir + os.sep,
                                                      '')
              
          # Check if summary files exist:
          for each_type in ResultsSummaryFactory().keys():
              
              summary_pattern = '%s/%s*' %(os.path.join(group_dir, results_dir),
                                           each_type) 
              summary_files = glob.glob(summary_pattern)
              
              if len(summary_files):
                  command += summary_pattern
                  command += ' '
    

          command += " %s %s:%s" \
                      %(os.path.join(group_dir, results_dir, daily_dir),
                        publish_server, publish_dir)

          Environment.invokeCommand(command)
        
       finally:
          os.chdir(start_dir)            

       return 


   #----------------------------------------------------------------------------
   #
   # Plot test results. Child classes should overwrite the method.
   #
   # Input: 
   #        result_file - Path to the result file in XML format
   #        fig_size - Figure size. Default is (12, 9).
   #
   # Output: 
   #        ElementTree object for result file and plot
   #
   @classmethod
   def plot (cls, 
             result_file, 
             fig_size = (12, 8), 
             num_subplots = 111,
             fig_size_num_tags = None):
       """ Plot test results in XML format."""

       plt.clf()
       plt.cla()
 
       # Read the whole file in
       doc = CSEPInitFile.CSEPInitFile(result_file)
       
       __fig_size = fig_size
       if fig_size_num_tags is not None:
           num_elements = len(doc.elements(fig_size_num_tags)) + 1
           
           if num_elements < fig_size[1]:
               __fig_size = (fig_size[0], num_elements)

      
       # set figsize, clear figure
       matplotlib.rcParams['figure.figsize'] = __fig_size
       fig = plt.figure()
       plot_obj = fig.add_subplot(num_subplots)
       # Clear the figure

       return (doc, plot_obj)


   #----------------------------------------------------------------------------
   #
   # Create copies of test results files with unique filenames 
   # and generate corresponding metadata files. New files are generated
   # under the same directory as original result files.
   #
   # Input: 
   #        file_type - Identifier used by unique filename
   #        file_pattern - File pattern to search results directory for.
   #        file_format - Format of the file
   #        file_comment - Comment for the file to store in corresponding 
   #                       metadata file
   #        file_archive - Optional argument to specify if archive of the entry
   #                       should be created. Default is False.
   #
   # Output: 
   #        None.
   #
   def _storeResultData (self,
                         file_type,
                         file_pattern,
                         file_format,
                         file_comment,
                         file_archive = False):
      """ Copy result data to files with unique names, 
          and generate corresponding metadata files."""


      file_list = glob.glob(os.path.join(self.testDir,
                                         file_pattern))
        
      for entry_path in file_list:
           
         entry = os.path.basename(entry_path)

         # Update comment with entry
         comment = "%s '%s' in %s format." \
 % (file_comment, entry, file_format)

         # Use filename as a descriptor
         datafile, metafile = CSEPPropertyFile.CSEPPropertyFile.filenamePair(file_type,
                                                                             entry) 
                     
         CSEPFile.copy(entry_path,
                       os.path.join(self.testDir, datafile),
                       file_archive)
        
         # Create metadata file
         CSEPPropertyFile.CSEPPropertyFile.createMetafile(os.path.join(self.testDir,
                                                                       metafile),
                                                          entry,
                                                          file_format,
                                                          comment)
           
         # Remove original file
         EvaluationTest._cleanup(entry_path)
    
    
   #--------------------------------------------------------------------
   #
   # Remove specified file.
   #
   # Input:
   #        filename - Name of the file to remove.
   #
   # Output: None.
   #
   @staticmethod   
   def _cleanup (filename):
      """ Remove file after is has been copied to the file with unique name."""

      if os.path.isdir(filename):
         EvaluationTest.__logger.info("__cleanup(): Removing directory %s" \
 % filename)
         shutil.rmtree(filename)
           
      else: 

         EvaluationTest.__logger.info("__cleanup(): Removing file %s" \
 % filename)
         os.remove(filename)
     

# Invoke the module
if __name__ == '__main__':

     import datetime, logging
     
     import EvaluationTestOptionParser
     from RELMCatalog import RELMCatalog
     from ForecastGroup import ForecastGroup
     

     parser = EvaluationTestOptionParser.EvaluationTestOptionParser()
     
     ### Work on Trac ticket #215: Provide simplified Python scripts to 
     ### invoke miniCSEP advertized functionality
     #==========================================================================
     # Allow simple interface to invoke evaluation test: specify forecast and 
     # related metadata, catalog, and type of test to invoke
     #==========================================================================
     parser.add_option('--startDate', 
                       dest="start_date",
                       default=None,
                       help="Start date of the forecast in YYYY-MM-DD format. \
Default is None.") 

     parser.add_option('--endDate', 
                       dest="end_date",
                       default=None,
                       help="End date of the forecast in YYYY-MM-DD format. \
Default is None.") 

     parser.add_option('--catalog',
                       type='string',
                       dest='catalog_file',
                       default=None,
                       help='Catalog file that represents observed events for \
the testing period. Default is None, meaning there are no observations available.')

     parser.add_option('--maxDepth', 
                       dest="max_depth", 
                       type="float",
                       default=30.0,                        
                       help="Catalog maximum depth in km. Default is 30km.")

     parser.add_option('--minMagnitude', 
                       dest="min_magnitude", 
                       type="float",
                       default=3.95,                        
                       help="Catalog minimum magnitude. Default is 3.95.")

     parser.add_option('--xmlTemplate',
                       type='string',
                       dest='xml_template',
                       default=None,
                       help='ForecastML master template file to use for validation.\
Default is None. Please provide template file only if %s option is omitted.' 
                       %CommandLineOptions.VALIDATE_XML_FORECAST)
     
     # List of requred options for the test
     required_options = [CommandLineOptions.YEAR,
                         CommandLineOptions.MONTH,
                         CommandLineOptions.DAY,
                         CommandLineOptions.FORECASTS]

     options = parser.options(required_options)
     
     # Test date for the test
     test_date = datetime.datetime(options.year,
                                   options.month,
                                   options.day)

     # Check if catalog, and forecast metadata are provided as command-line options.
     # If they are, then create abstract PostProcess object and use it for 
     # evaluation
     post_process = options.post_process
     
     # Simplified interface for miniCSEP distribution - see Trac ticket #215
     if options.post_process is None and options.start_date is not None and \
        options.end_date is not None:
         
         start_date = datetime.datetime.strptime(options.start_date, 
                                                 CSEP.Time.DateFormat)
         end_date = datetime.datetime.strptime(options.end_date, 
                                               CSEP.Time.DateFormat)
         forecast_duration = CSEPUtils.decimalYear(end_date) - \
                             CSEPUtils.decimalYear(start_date) 
 
         # Create PostProcess object and pass it to the ForecastGroup
         post_process = PostProcess(options.min_magnitude,
                                    options.max_depth,
                                    forecast_duration,
                                    options.catalog_file,
                                    options.xml_template)
         post_process.startDate(start_date)
         post_process.endDate(end_date)
          
     
     # Instantiate forecast group for the tests
     forecast_group = ForecastGroup(options.forecast_dir,
                                    post_process,
                                    options.test_list,
                                    options.test_inputs,
                                    post_process_inputs=options.post_process_args)
        
     # Run evaluation tests        
     for each_test in forecast_group.tests:
        # Use the same directory for catalog data and test results: options.test_dir
        each_test.run(test_date,
                      options.test_dir, # OR should use catalog directory as defined by the group?
                      options.test_dir)
     
        # Update cumulative summaries if any
        each_test.resultData()
       

     # Shutdown logging 
     logging.shutdown()
        
# end of main
     