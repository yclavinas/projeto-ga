"""
Module DiagnosticsTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os, shutil, glob, matplotlib, datetime, scipy.stats, re, sys
import numpy as np
from pylab import *
from matplotlib.font_manager import FontProperties

import CSEP, Environment, CSEPPropertyFile, CSEPLogging, \
       CSEPGeneric, CSEPFile, ReproducibilityFiles, CSEPInputParams
from Forecast import Forecast
from RELMCatalog import RELMCatalog
from EvaluationTest import EvaluationTest
from DiagnosticsSummary import DiagnosticsSummary
from ResultsCumulativeSummary import ResultsCumulativeSummary


#-------------------------------------------------------------------------------
#
# DiagnosticsTest
#
# This class is designed to evaluate available models with residual analysis 
# tests which are introduced to the CSEP Testing Framework by Robert Clements
# et al.
#
class DiagnosticsTest (EvaluationTest,
                       ReproducibilityFiles.ReproducibilityFiles):

    #===========================================================================
    # Nested class that represents DiagnosticsTest result data as 
    # dictionary type.
    # Derived classes should derive from the class to provide specifics of the
    # test results.    
    #===========================================================================
    class Result (EvaluationTest.Result):
        
        #===========================================================================
        # Nested class that defines attributes of XML format result data specific
        # to ShakeAlert evaluation test.
        # Each of the derived classes must define an object of the class that sets
        # each of the data attributes.
        #===========================================================================
        class XML (object):
    
            def __init__(self, 
                         root,
                         model_name,
                         result_vars = {},
                         plot_vars = [],
                         stack_vars = [],
                         invoke_test = False):
                # Root element for the test. Corresponding matlab script to invoke the 
                # test uses the same name
                self.Root = root
                
                # Result variable ("true" event in case of RELM tests) for the test
                self.TrueEvent = None
        
                # XML elements that represent names of forecast models involved in test
                self.ModelName = model_name
                if model_name is not None and isinstance(model_name, str):
                    self.ModelName = [model_name]
                
                # XML elements that represent result variables for the evaluation test
                self.TestVars = result_vars
                if isinstance(result_vars, list):
                    self.TestVars = dict(zip(result_vars,
                                             result_vars))
                elif isinstance(result_vars, str):
                    self.TestVars = {}
                    self.TestVars[result_vars] = result_vars
                    
                # Names of extra variables to be preserved from daily results
                # into cumulative summary result: to be used for plotting
                self.PlotVars = plot_vars
                if isinstance(plot_vars, str):
                    self.ExtraVars = plot_vars

                self.StackVars = stack_vars

                # Flag if evaluation test needs to be invoked to generate
                # cumulative summary (based on cumulative results)
                self.InvokeTest = invoke_test
                
        
        #=======================================================================
        #        
        #=======================================================================
        def __init__ (self,
                      ascii_result_file, 
                      xml_elements,
                      test_args):
            """ Initialize method for DiagnosticsTest.Result object"""
            
            EvaluationTest.Result.__init__(self)
            
            # TODO: names=True does not work in Python 2.5,
            # should change to access by name after upgrade to Python 2.6
            __np_result =  np.genfromtxt(ascii_result_file,
                                         names=True)

#                for index, each_xml_tag in enumerate(xml_elements):
#                    # Access by index
#                    self[each_xml_tag] = __np_result[:, index]
                    
            for each_xml_tag in xml_elements:
                
                # If multiple tags are possible for test result field, 
                # check which one is present
                if isinstance(each_xml_tag, list) is True:
                    for each_tag in each_xml_tag:
                        # Numpy removes '.' from embedded names when reading with
                        # np.genfromtxt
                        np_tag_str = each_tag.replace('.', '')
                        
                        if np_tag_str in __np_result.dtype.names:
                            self[each_tag] = __np_result[np_tag_str]
                else:
                    # Only one name tag is provided for data field
                    # Numpy removes '.' from embedded names when reading with
                    # np.genfromtxt
                    np_tag_str = each_xml_tag.replace('.', '')
                    
                    if np_tag_str in __np_result.dtype.names:
                        self[each_xml_tag] = __np_result[np_tag_str]

            # Added in support of cumulative summaries for DiagnosticsTests:
            # k-value of Super-thinned residuals test should be summed up
            # to compute cumulative
            for each_var, each_value in test_args.iteritems():
                if each_value is not None:
                    self[each_var] = each_value
            
        
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
        #         catalog - numpy.array representing observation catalog for
        #                   the test. Default is None.  
        #         forecast_covers_area - Flag if forecast covers the whole testing
        #                                area. If True, sum of true log-likelihoods
        #                                is a valid measure, if False - sum of true
        #                                log-likelihoods is not a valid measure for
        #                                for the test. Default is True.
        #
        # Output: Tuple of test_node and xml document objects
        #  
        #=======================================================================
        def writeXML (self, 
                      test_name, 
                      model_filename, 
                      dirpath,
                      file_prefix,
                      write_file = True,
                      result_file = None,
                      test_date_obj = None):
            """Write test results to XML format file"""
          
          
            test_node, xml = EvaluationTest.Result.writeXML(self,
                                                            test_name,
                                                            model_filename,
                                                            dirpath,
                                                            file_prefix,
                                                            result_file)
            if test_date_obj is not None:
                test_node.attrib[ResultsCumulativeSummary.TestDateAttribute] = "%s" %test_date_obj
                
            # Write test data to the file
            for __key, __value in self.iteritems():
                node = xml.addElement(__key, test_node)
                if isinstance(__value, np.ndarray):
                    node.text = ' '.join([str(i) for i in __value[:]])
                    
                else:
                    node.text = repr(__value)
                
            # write XML format file
            if write_file is True:
                xml.write()
                
            else:
                return test_node, xml


    #===========================================================================
    # Nested class with matplotlib settings for the test     
    #===========================================================================
    class Matplotlib (EvaluationTest.Matplotlib):

        # Static data
        _plotCurve = {'markersize' : None,
                       'color': 'g',
                       'linestyle' : '-'}

        _plotBounds = {'color' : 'k',
                       'linestyle' : '--',
                       'linewidth' : 1,
                       'label': '_nolegend_'}
        
        _plotLabels = {'ylabel_size'     : 14,
                       'ylabel_rotation' : 30 }
    
    # Static data

    # Prefix for the test generated files    
    __filePrefix = 'd' + EvaluationTest.FilePrefix

    # Pattern used to match result files in ASCII format
    __asciiResultPattern = '%s*%s' %(__filePrefix, 
                                     CSEPFile.Extension.ASCII)

    # Pattern used to match result files in XML format
    __xmlResultPattern = '%s*%s' %(__filePrefix, 
                                   CSEPFile.Extension.XML)

    # Keyword identifying the class
    __type = "DiagnosticsTest"
    
    # Common directory for RELM evaluation tests and related files
    _scriptsPath = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV], 
                                'src', 
                                'DiagnosticsTests')

    __logger = None

    # Option to draw random seed value by the system or to read it from specified
    # file
    __randomSeedOption = "seedValue"

    # Option to specify alpha-value for the test (hard-coded at 0.05)
    __alphaOption = "alpha"
    
    # Option to specify k-value for the test (hard-coded at 0.05)
    _kValueOption = "kValue"
    
    # Threshold to use as minimum value for 'kValue' option if less than 100 events
    # are observed for the test 
    __kValueThresholdOption = 100

    # Default values for input parameters
    __defaultArgs = {__randomSeedOption : None,
                     __alphaOption : 0.05,
                     _kValueOption : None}
    
    # Prefix to use for short version (10 columns) of the forecast to be passed to
    # R code
    __shortPrefix = 'short'


    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be invoked.
    #        args - Optional input arguments for the test. Default is None.    
    # 
    def __init__ (self, group, args = None):
        """ Initialization for DiagnosticsTest class."""
        
        EvaluationTest.__init__(self, group)
        ReproducibilityFiles.ReproducibilityFiles.__init__(self)
        
        if DiagnosticsTest.__logger is None:
           DiagnosticsTest.__logger = CSEPLogging.CSEPLogging.getLogger(DiagnosticsTest.__name__)
        
        # Input arguments for the model were provided:
        self.__args = CSEPInputParams.CSEPInputParams.parse(DiagnosticsTest.__defaultArgs,
                                                            args)
        
        # Diagnostics tests don't support more than 10-column forecast format file,
        # create a temporary "short" version if forecast is more than 10 columns
        self._shortFormatForecasts = {}


    #----------------------------------------------------------------------------
    #
    # Object cleanup.
    #
    # Input: None
    # 
    def __del__ (self):
       """ Cleanup for DiagnosticsTest class. Removes short file versions (if any)  
           of forecasts created for the test."""
         
       for each_short_file in self._shortFormatForecasts.values():
           DiagnosticsTest.__logger.info("Checking for existence of %s" %each_short_file)
           if os.path.exists(each_short_file):
               DiagnosticsTest.__logger.info("Removing %s" %each_short_file)
               os.remove(each_short_file)
       


    def _getArgs (self):
        """ Return internal dictionary of input arguments (to be accessed by
            derived classes)."""

        # Test options
        return self.__args
        
        
    #----------------------------------------------------------------------------
    #
    # Returns file prefix for test result file.
    #
    # Input: None
    #
    # Output: File prefix used by test results.
    @classmethod
    def filePrefix (cls):
        """ Returns file prefix for test result file."""
        
        return DiagnosticsTest.__filePrefix 


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

        # No intermediate results are generated by the tests
        return None


    #----------------------------------------------------------------------------
    #
    # Returns a type for the evaluation test summary which is updated by 
    # final test result for each testing period. 
    #
    # Input: None
    #
    # Output: Results summary type for cumulative results
    #
    @classmethod
    def resultsSummaryType (cls):
        """ Returns class type to be used to calculate evaluation test 
            cumulative summaries."""

        return DiagnosticsSummary.Type


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

        return DiagnosticsTest.__type
        

    #----------------------------------------------------------------------------
    #
    # Create cumulative summary for the test (only if test needs to be invoked
    # to generate the summary).
    #
    # Input: None.
    #
    # Output: None
    #
    def updateSummary (self, 
                       summary_file):
        """ Create cumulative summary for the test (only if test needs to be 
            invoked to generate the summary)."""

        # By default, cumulative summary is based on cumulative results, no
        # need to invoke the test
        return False
    
    
    #--------------------------------------------------------------------
    #
    # Invoke evaluation test for the forecast
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def evaluate (self, 
                  forecast_name):
        """ Invoke evaluation test for the forecast."""

        # Catalog is not valid for the test
        DiagnosticsTest.prepareCatalog(self)

        test_name = '%s-%s' %(self.type(),
                              EvaluationTest.FilePrefix)

        DiagnosticsTest.__logger.info('%s for %s' %(test_name,
                                                    forecast_name))
        # Create parameter file for the run
        __script_file, __result_file = self.createParameterFile(forecast_name)

        # Record original ASCII result file as generated by evaluation code
        # with reproducibility registry
        info_msg = "Result file as generated by R code %s \
for %s diagnostics test for '%s' in '%s' directory." %(os.path.join(DiagnosticsTest._scriptsPath,
                                                                    self.execFunction()),
                                                       self.type(),
                                                       forecast_name,
                                                       self.forecasts.dir())
        
        ReproducibilityFiles.ReproducibilityFiles.add(self,
                                                      os.path.basename(__result_file),
                                                      info_msg,
                                                      CSEPFile.Format.ASCII)

        # Invoke test
        # Set executable permissions on the file
        os.chmod(__script_file, 0755)
        
        # R package reports library load messages to stderr, ignore them 
        ignore_stdout_messages = True
        
        Environment.invokeCommand(__script_file,
                                  ignore_stdout_messages)
        
        # Convert ASCII results as generated by original R code to XML format
        test_result = DiagnosticsTest.Result(__result_file,
                                             self.xmlElements(),
                                             self.__args)
        test_result.writeXML(test_name, 
                             forecast_name, 
                             self.testDir,
                             self.filePrefix()) 

        return __result_file
    

    #--------------------------------------------------------------------
    #
    # prepareCatalog
    #
    # This method prepares observation catalog for evaluation test:
    # * Filter observation catalog based on forecast group parameters: magnitude,
    #   depth, beginning of the forecast 
    #
    # Since all forecasts models share the same observation catalog, it should
    # be prepared once per test within the group
    #
    # Input: None
    #
    # Output: Return True if observation catalog satisfies test criteria, and
    #         should be invoked, False otherwise
    #
    def prepareCatalog(self):
        """ Prepare observation catalog for evaluation test"""

        # Numpy object for observation catalog has not been initialized yet
        if self.catalogFile.npObject is None:
            
            # Load catalog
            catalog = RELMCatalog.load(self.catalogFile.name)
    
            # Filter catalog data based on forecast group parameters: 
            # 1. Beginning of forecast (in case the same observation catalog is re-used by
            #    multiple forecast groups with different starting date)
            # 2. Catalog is already filtered by test area, magnitude and depth  
            #    by PostProcessmodule defined for the forecast group
            self.catalogFile.npObject = RELMCatalog.cutToTime(catalog,
                                                              self.forecasts.postProcess().start_date)
            
            
            # Write catalog to the file - it's passed to the R-code of evaluation
            # test as provided by Robert Clements
            if self.catalogFile.intermediateObj is None:
                __path, __name = os.path.split(self.catalogFile.name)
                self.catalogFile.intermediateObj = os.path.join(__path,
                                                             '%s' %self.forecasts.postProcess().start_date.date() + __name)
                
                if os.path.exists(self.catalogFile.intermediateObj) is False:
                    # Diagnostics tests expect 16 columns of data in catalog, 
                    # expand catalog if less columns are present
                    nrows, ncols = self.catalogFile.npObject.shape
                    expected_cols = CSEPGeneric.Catalog.ZMAPFormat.NumColumns + 2
                    
                    if ncols < expected_cols:
                        num_missing_cols = expected_cols - ncols
                        
                        self.catalogFile.npObject = np.append(self.catalogFile.npObject, 
                                                              np.zeros((nrows, num_missing_cols)),
                                                              axis = 1)
                        
                    np.savetxt(self.catalogFile.intermediateObj,
                               self.catalogFile.npObject)
     
        return
        

    #===========================================================================
    # Write input catalog information to the parameter file for the test
    #===========================================================================
    def writeCatalogInfo(self, fhandle, num_catalogs = None):
        """Write input catalog information to the parameter file for the test."""
        
        if num_catalogs is not None:
            for index in xrange (0, num_catalogs):
                fhandle.write("inputCatalog%s=\"%s\"\n" %(index + 1,
                                                          self.catalogFile.intermediateObj))
        else:
            fhandle.write("inputCatalog=\"%s\"\n" %self.catalogFile.intermediateObj)

        return fhandle
     

    #===========================================================================
    # Write input catalog information to the parameter file for the test
    #===========================================================================
    def writeMagnitudeRangeInfo(self, fhandle):
        """Write magnitude range for the test."""
        
        fhandle.write("magnitudeRange=c(%s, 10)\n" %self.forecasts.postProcess().threshold.MinMagnitude)
        return fhandle


    #===========================================================================
    # Write kValue to the parameter file for the test
    #===========================================================================
    def writeKValueInfo(self, fhandle, forecast_name):
        """Write kValue for the test."""
        
        return fhandle


    #===========================================================================
    # Write alpha to the parameter file for the test
    #===========================================================================
    def writeAlphaInfo(self, fhandle):
        """Write alpha for the test."""
        
        fhandle.write("alpha=%s\n" %self.__args[DiagnosticsTest.__alphaOption])
        return fhandle


    #===========================================================================
    # Write random seed value to the parameter file for the test if applicable
    #===========================================================================
    def writeRandomSeedValue(self, fhandle, seed_value):
        """Write random seed value for the test."""
        
        return fhandle


    #===========================================================================
    # Write test specific parameters to the file if any
    #===========================================================================
    def writeTestInfo(self, fhandle, args = None):
        """Write test specific parameters to the file if any."""
        
        return fhandle


    #===========================================================================
    # R function to invoke for the test
    #===========================================================================
    def execFunction(self):
        """Write R source function for the test."""
        
        error_msg = "%s module must define R function for the evaluation test." %self.type()
        DiagnosticsTest.__logger.error(error_msg)
        raise RuntimeError, error_msg


    #===========================================================================
    # Result filename for the model
    #===========================================================================
    def resultFilename(self, forecast_name):
        """Result filename for the model."""
        
        result_prefix = self.filePrefixPattern()
        result_prefix += '_'
         
        if isinstance(forecast_name, list) is True:
            result_prefix += '_'.join([CSEPFile.Name.extension(name) for name in forecast_name])
        else:
            result_prefix += CSEPFile.Name.extension(forecast_name)
        
        return (result_prefix, 
                result_prefix + CSEPFile.Name.ascii(EvaluationTest._resultFilePostfix))


    #===========================================================================
    # Return list of XML elements that represent test results. 
    # NOTE: This method should be overwritten by derived children classes
    #===========================================================================
    @classmethod
    def xmlElements(cls):
        """Return list of XML elements that represent test results"""
        
        return []
    

    #---------------------------------------------------------------------------
    #
    # Create input parameter file for the run.
    #
    # Input: 
    #       forecast_name - Name of forecast model for the test, or list of
    #                       forecasts models for the test.
    #
    # Output: filename for parameter file
    #
    def createParameterFile (self, forecast_name):
        """ Create input parameter file for the run."""
        
        
        result_prefix, result_file = self.resultFilename(forecast_name)
        
        parameter_file = os.path.join(self.testDir,
                                      result_prefix + EvaluationTest._paramFilePostfix)
        
        fhandle = CSEPFile.openFile(parameter_file,
                                    CSEPFile.Mode.WRITE)
        
        fhandle.write("#!%s\n" %Environment.BASH_SHELL)
        fhandle.write("R --no-save << EOT\n")
        
        __num_catalogs = None
        if isinstance(forecast_name, list) is True:
            __num_catalogs = len(forecast_name)
            
        self.writeCatalogInfo(fhandle,
                              __num_catalogs)
     
        # Write forecast info to parameter file
        
        ### Create temporary "short" versions of forecasts for R-code only if
        ### forecast file contains more than 10 expected columns of data
        _test_forecasts = forecast_name
        if isinstance(_test_forecasts, list) is False:
            _test_forecasts = [forecast_name]
            
        for each_forecast in _test_forecasts:
            forecast_data = CSEPFile.read(os.path.join(self.forecasts.dir(),
                                                       each_forecast))
            
            # Check how many columns are in forecast
            if forecast_data.ndim == 1:
                forecast_data.shape = (1, forecast_data.size)
        
            num_rows, num_cols = forecast_data.shape
            
            if num_cols > CSEPGeneric.Forecast.Format.Observations:
                # Create "short" version of the forecast
                short_forecast_file = os.path.join(self.testDir,
                                                   DiagnosticsTest.__shortPrefix + each_forecast)
                if os.path.exists(short_forecast_file) is False:
                
                    np.savetxt(short_forecast_file,
                               forecast_data[:, 0:CSEPGeneric.Forecast.Format.Observations])
                
                self._shortFormatForecasts[each_forecast] = short_forecast_file
                    
                
        if isinstance(forecast_name, list) is True:
            for __index, __forecast in enumerate(forecast_name):
                file_path = os.path.join(self.forecasts.dir(),
                                         __forecast)
                
                # Check if short version exists
                if __forecast in self._shortFormatForecasts:
                    file_path = self._shortFormatForecasts[__forecast]
                    
                fhandle.write("inputForecast%s=\"%s\"\n" %(__index+1,
                                                           file_path))

        else:
            file_path = os.path.join(self.forecasts.dir(),
                                     forecast_name)
            
            # Check if short version exists
            if forecast_name in self._shortFormatForecasts:
                file_path = self._shortFormatForecasts[forecast_name]
            
            fhandle.write("inputForecast=\"%s\"\n" %(file_path))

        # Write kValue is appropriate for the test
        self.writeKValueInfo(fhandle, 
                             forecast_name)

        # Write forecast period proportion
        fhandle.write("forecastPeriodProportion=%s\n" %self.scaleFactor)
        
        # Write alpha parameter for the test
        self.writeAlphaInfo(fhandle)
        
        # Write magnitude range if appropriate for the test
        self.writeMagnitudeRangeInfo(fhandle)
        
        # Construct filename for the test result
        result_file_path = os.path.join(self.testDir,
                                        result_file)
        fhandle.write("resultFile=\"%s\"\n" %result_file_path)

        # Write seed value if applicable for the test (only super-thinned residuals
        # test is using random numbers)
        self.writeRandomSeedValue(fhandle,
                                  self.__args[DiagnosticsTest.__randomSeedOption])

        # Write test specific parameters if any
        self.writeTestInfo(fhandle, forecast_name)
        
        # Write test R code
        fhandle.write("source(\"%s\")\n" %os.path.join(DiagnosticsTest._scriptsPath,
                                                       self.execFunction()))
        
        fhandle.write("EOT\n")
        fhandle.close()

        
        # Register input parameters file for reproducibility
        __forecast_format_str = '' 
        if isinstance(forecast_name, list) is True:
            __forecast_format_str = 's'

        info_msg = "Input parameters file used by %s diagnostics test for forecast%s \
model%s '%s' in '%s' directory." %(self.type(),
                                 __forecast_format_str,
                                 __forecast_format_str,
                                 forecast_name,
                                 self.forecasts.dir())

        # Record parameter file with reproducibility registry
        ReproducibilityFiles.ReproducibilityFiles.add(self,
                                                      os.path.basename(parameter_file),
                                                      info_msg,
                                                      CSEPFile.Format.ASCII)
     
        return (parameter_file, result_file_path)


    #----------------------------------------------------------------------------
    #
    # Create cumulative summary for the test (only if test needs to be invoked
    # to generate the summary).
    #
    # Input: None.
    #
    # Output: None
    #
    def createSummary (self, 
                       summary_file):
        """ Create cumulative summary for the test (only if test needs to be 
            invoked to generate the summary)."""

        return False
                
    
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

        # Base class implementation of the method takes care of XML format
        # test results, and forecast maps in PNG format
        if EvaluationTest.resultData(self) is False:
            return False
        
        
        # There are more formats of result data: ASCII
        comment = "Evaluation test result file "

        EvaluationTest._storeResultData(self,
                                        DiagnosticsTest.__type,
                                        "%s*%s" %(self.filePrefixPattern(),
                                                  CSEPFile.Extension.ASCII),
                                        CSEPFile.Format.ASCII,
                                        comment)
              
        return True


    #----------------------------------------------------------------------------
    #
    # Finish test specific plot. This method displays legend and axis labels.
    #
    # Input: 
    #        result_file - Path to the result file in XML format
    #        output_dir - Directory to place plot file to.
    #        x_axis_label - Label for the x-axis. Default is None
    #        y_axis_label - Label for the y-axis
    #
    # Output: List of generated plot files.
    #
    @classmethod
    def _finishPlot (cls,
                     result_file,
                     output_dir,
                     plot_title,
                     x_axis_label = None, 
                     y_axis_label = None):
        """ Finish test specific plot: legend and axis labels for already 
            plotted test result data."""
      
        plt.title(plot_title,
                  EvaluationTest.Matplotlib._titleFont)

        #----------------------------------------------------------------------
        if x_axis_label is not None:
            xlabel(x_axis_label, 
                   EvaluationTest.Matplotlib._plotLabelsFont)

        if y_axis_label is not None:
            ylabel(y_axis_label, 
                   EvaluationTest.Matplotlib._plotLabelsFont)

        a = gca()
        a.set_zorder(EvaluationTest.Matplotlib.plotZOrder['axes'])
      
        # Use provided output directory if any
        image_file = result_file
        
        if output_dir is not None:
            image_file = os.path.join(output_dir,
                                      os.path.basename(result_file))
    
        # Replace extension with '.svg' for the image file
        image_file = image_file.replace(CSEPFile.Extension.XML, '')
        image_file += CSEPFile.Extension.PNG
      
        savefig(image_file)
        close()
        clf()
      
        # Return name of generated plot file
        return [image_file]
      

