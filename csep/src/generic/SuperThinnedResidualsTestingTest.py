"""
Module SuperThinnedResidualsTestingTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os
from pylab import *

import CSEPLogging, CSEPFile, Environment
from ReproducibilityFiles import ReproducibilityFiles
from CSEPInitFile import CSEPInitFile
from Forecast import Forecast
from DiagnosticsTest import DiagnosticsTest
from EvaluationTest import EvaluationTest
from SuperThinnedResidualsTest import SuperThinnedResidualsTest


#-------------------------------------------------------------------------------
#
# SuperThinnedResidualsTestingTest
#
# This class is designed to evaluate available models with residual analysis 
# tests which are introduced to the CSEP Testing Framework by Robert Clements
# et al.
#
class SuperThinnedResidualsTestingTest (SuperThinnedResidualsTest):

    # Keyword identifying the class
    Type = "RTT"
    
    __logger = None
   
    # Data fields of test result
    __r = 'r'
    __wcl = 'w.c.l'
    __lowerBound = 'lower.bound'
    __upperBound = 'upper.bound'
    __yAxisLabel = r'$L_\mathrm{W}(r)-r$'


    xml = DiagnosticsTest.Result.XML(Type + EvaluationTest.FilePrefix,
                                     EvaluationTest.Result.Name,
                                     invoke_test = True)


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
        """ Initialization for SuperThinnedResidualsTest class."""
        
        SuperThinnedResidualsTest.__init__(self, group, args)
        
        if SuperThinnedResidualsTestingTest.__logger is None:
           SuperThinnedResidualsTestingTest.__logger = CSEPLogging.CSEPLogging.getLogger(SuperThinnedResidualsTestingTest.__name__)


    #-----------------------------------------------------------------------------
    #
    # Returns keyword identifying the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: String represenation of the test type.
    #
    def type (self):
        """ Returns test type."""

        return SuperThinnedResidualsTestingTest.Type


    #===========================================================================
    # Write input catalog information to the parameter file for the test
    #===========================================================================
    def writeCatalogInfo(self, fhandle, num_catalogs = None):
        """Write input catalog information to the parameter file for the test."""
        
        return fhandle


    #===========================================================================
    # Write alpha to the parameter file for the test
    #===========================================================================
    def writeAlphaInfo(self, fhandle):
        """Write alpha for the test."""
        
        return DiagnosticsTest.writeAlphaInfo(self, fhandle)


    #===========================================================================
    # Write R function to invoke for the test
    #===========================================================================
    def execFunction(self):
        """Write R source function for the test."""
        
        return 'superthinned_residuals_testing.R'


    #===========================================================================
    # Write test specific parameters to the file if any
    #===========================================================================
    def writeTestInfo(self, fhandle, args = None, input_residuals_file = None):
        """Write test specific parameters to the file if any."""

        __super_thinned_result_file = input_residuals_file
        
        if __super_thinned_result_file is None:
            __super_thinned_test = SuperThinnedResidualsTest(self.forecasts)
            __prefix, __test_file = __super_thinned_test.resultFilename(args)
            __super_thinned_result_file = os.path.join(self.testDir,
                                                       __test_file)
            
        if os.path.exists(__super_thinned_result_file) is False:
            error_msg = "%s evaluation test must be invoked before %s test. %s result file is missing" \
                        %(SuperThinnedResidualsTest.Type,
                          self.type(),
                          __super_thinned_result_file)
            SuperThinnedResidualsTestingTest.__logger.error(error_msg)
            raise RuntimeError, error_msg
        
        
        fhandle.write("inputResiduals=\"%s\"\n" %__super_thinned_result_file)
        return fhandle


    #===========================================================================
    # Return list of XML elements that represent test results
    #===========================================================================
    @classmethod
    def xmlElements(cls):
        """Return list of XML elements that represent test results"""
        
        return [SuperThinnedResidualsTestingTest.__r,
                SuperThinnedResidualsTestingTest.__wcl,
                SuperThinnedResidualsTestingTest.__lowerBound,
                SuperThinnedResidualsTestingTest.__upperBound]


    #===========================================================================
    # Write random seed value to the parameter file for the test if applicable
    # 
    # Inputs:
    #         fhandle - Handle to open parameter file to write seed value to
    #         result_prefix - Prefix to use for random seed file (unique to the
    #                         test and forecast model(s) participating in test
    #         seed_token - Key token to use for seed value within parameter file
    #                      Default is "seed" (seed=VALUE)
    #         seed_value - In order to reproduce test results, random 
    #                              seed value is stored to the file. Name of 
    #                              the file with previously used random seed 
    #                              value. Default is None.
    #
    #===========================================================================
    def writeRandomSeedValue(self, 
                             fhandle, 
                             seed_value):
        """Write random seed value for the test."""
        
        return DiagnosticsTest.writeRandomSeedValue(self, fhandle, seed_value)


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
                       summary_file,
                       test_date):
        """ Create cumulative summary for the test (only if test needs to be 
            invoked to generate the summary)."""


        # Locate RT cumulative to generate ASCII input into RTT test
        rt_cumulative_file = summary_file.replace(self.Type,
                                                  SuperThinnedResidualsTest.Type)
        
        if os.path.exists(rt_cumulative_file) is False:
            error_msg = "%s summary must exist before summary for %s test is created." \
                        %(rt_cumulative_file,
                          summary_file)

            SuperThinnedResidualsTestingTest.__logger.error(error_msg)
            raise RuntimeError, error_msg
        
        # Convert XML to ASCII to prepare input file for the test
        rt_doc = CSEPInitFile(rt_cumulative_file)

        rt_cum_data = {}
        rt_parent_name = SuperThinnedResidualsTest.xml.Root
        for each_col in SuperThinnedResidualsTest.xmlElements():
            rt_cum_data[each_col] = rt_doc.elementValue(each_col,
                                                        rt_parent_name).split()
        
        # Create ASCII version of ST summary for STT run
        rt_cum_ascii_file = CSEPFile.Name.ascii(rt_cumulative_file)
        
        with CSEPFile.openFile(rt_cum_ascii_file, CSEPFile.Mode.WRITE) as fhandle:
            
            fhandle.write('%s\n' %' '.join(['"%s"' %tag for tag in SuperThinnedResidualsTest.xmlElements()]))
            
            num_elems = len(rt_cum_data.values()[0])
            for each_index in xrange(0, num_elems):
                
                line = ''
                for each_col in SuperThinnedResidualsTest.xmlElements():
                    line += rt_cum_data[each_col][each_index]
                    line += ' '
                line += '\n'
                
                fhandle.write(line)
                
        # Forecast file name for the test: stored in xml.ModelName[0] element
        # (without file extension)
        name_elem = rt_doc.elements(SuperThinnedResidualsTest.xml.ModelName[0])[0]
        forecast_name = name_elem.attrib[EvaluationTest.Result.FileAttribute]
        
        # Invoke the test with cumulative result in ASCII format as a result
        test_name = '%s-%s' %(self.type(),
                              EvaluationTest.FilePrefix)

        SuperThinnedResidualsTestingTest.__logger.info('%s summary test for %s' %(test_name,
                                                                                  forecast_name))
        
        __script_file, result_file_path = self.createSummaryParameterFile(forecast_name,
                                                                          rt_doc,
                                                                          summary_file)
        # Set executable permissions on the file
        os.chmod(__script_file, 0755)
        
        # R package reports library load messages to stderr, ignore them 
        ignore_stdout_messages = True
        
        Environment.invokeCommand(__script_file,
                                  ignore_stdout_messages)
        
        # Remove summary file if it already exists
        if os.path.exists(summary_file):
            os.remove(summary_file)
            
        # Convert ASCII results as generated by original R code to XML format
        test_result = DiagnosticsTest.Result(result_file_path,
                                             self.xmlElements(),
                                             self._getArgs())
        test_result.writeXML(test_name, 
                             forecast_name, 
                             self.testDir,
                             self.filePrefix(),
                             result_file = summary_file,
                             test_date_obj = test_date) 

        return summary_file


    #----------------------------------------------------------------------------
    #
    # This method creates parameter file to invoke the test to generate 
    # cumulative summary (dependent on cumulative summary of RT evaluation test).
    #
    # Input: 
    #         result_file - File with daily test results.
    #         output_dir - Directory to place plot file to. Default is None.     
    #
    def createSummaryParameterFile (self, 
                                    forecast_name,
                                    rt_doc,
                                    summary_file_path):
        """ Create parameter file for the test run to create cumulative summary."""
        
        summary_path, summary_file = os.path.split(summary_file_path)
        
        parameter_file = CSEPFile.Name.extension(summary_file)
        parameter_file += EvaluationTest._paramFilePostfix
        parameter_file = os.path.join(self.testDir,
                                      parameter_file)
        
        with CSEPFile.openFile(parameter_file, CSEPFile.Mode.WRITE) as fhandle:
        
            fhandle.write("#!%s\n" %Environment.BASH_SHELL)
            fhandle.write("R --no-save << EOT\n")
            
            # Write forecast info to parameter file
            fhandle.write("inputForecast=\"%s\"\n" %(os.path.join(self.forecasts.dir(),
                                                                  forecast_name)))
    
            # Write kValue is appropriate for the test
            self.writeKValueInfo(fhandle, 
                                 forecast_name,
                                 rt_doc.elementValue(DiagnosticsTest._kValueOption))
    
            # Write forecast period proportion
            fhandle.write("forecastPeriodProportion=%s\n" %self.scaleFactor)
            
            # Write alpha parameter for the test
            self.writeAlphaInfo(fhandle)
            
            # Construct filename for the test result
            result_file_path = os.path.join(self.forecasts.resultDir(),
                                            CSEPFile.Name.ascii(summary_file))
            fhandle.write("resultFile=\"%s\"\n" %result_file_path)
    
            # Write test specific parameters if any
            self.writeTestInfo(fhandle, 
                               input_residuals_file = CSEPFile.Name.ascii(rt_doc.name))
            
            # Write test R code
            fhandle.write("source(\"%s\")\n" %os.path.join(DiagnosticsTest._scriptsPath,
                                                           self.execFunction()))
            
            fhandle.write("EOT\n")
            fhandle.close()
    
            
            # Register input parameters file for reproducibility
            info_msg = "Input parameters file used by %s diagnostics test for cumulative summary of forecast\
model '%s' in '%s' directory." %(self.type(),
                                 forecast_name,
                                 self.forecasts.dir())
    
            # Record parameter file with reproducibility registry
            ReproducibilityFiles.add(self,
                                     os.path.basename(parameter_file),
                                     info_msg,
                                     CSEPFile.Format.ASCII)
     
        return (parameter_file, result_file_path)
        


     
    #----------------------------------------------------------------------------
    #
    # This method plots result data of evaluation test.
    #
    # Input: 
    #         result_file - File with daily test results.
    #         output_dir - Directory to place plot file to. Default is None.     
    #
    @classmethod
    def plot (cls, 
              result_file, 
              output_dir = None):
        """ Plot test results in XML format."""

        
        doc, ax = EvaluationTest.plot(result_file) 

        parent_name = cls.xml.Root
        
        # Plot data specific to the test, and set up the labels
        r_values_str = doc.elementValue(SuperThinnedResidualsTestingTest.__r,
                                        parent_name).split()
        r_values = map(float, r_values_str)
        
        lFunc_values_str = doc.elementValue(SuperThinnedResidualsTestingTest.__wcl,
                                            parent_name).split()
        lFunc_values = map(float, lFunc_values_str)
        
        lowerBound_values_str = doc.elementValue(SuperThinnedResidualsTestingTest.__lowerBound,
                                                 parent_name).split()
        lowerBound_values = map(float, lowerBound_values_str)
        
        upperBound_values_str = doc.elementValue(SuperThinnedResidualsTestingTest.__upperBound,
                                                 parent_name).split()
        upperBound_values = map(float, upperBound_values_str)
        
        # plot test curves
        plot (r_values, 
              lFunc_values, 
              color=DiagnosticsTest.Matplotlib._plotCurve['color'], 
              linestyle=DiagnosticsTest.Matplotlib._plotCurve['linestyle'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
              label='_nolegend_')

        plot (r_values, 
              lowerBound_values, 
              color=DiagnosticsTest.Matplotlib._plotBounds['color'], 
              linestyle=DiagnosticsTest.Matplotlib._plotBounds['linestyle'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
              label='_nolegend_')
        
        plot (r_values, 
              upperBound_values, 
              color=DiagnosticsTest.Matplotlib._plotBounds['color'], 
              linestyle=DiagnosticsTest.Matplotlib._plotBounds['linestyle'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
              label='_nolegend_')

        name = doc.elementValue(EvaluationTest.Result.Name)

        # Return image filename
        return DiagnosticsTest._finishPlot(result_file,
                                           output_dir,
                                           "Super-thinned residuals testing (%s)" %name,
                                           SuperThinnedResidualsTestingTest.__r, 
                                           SuperThinnedResidualsTestingTest.__yAxisLabel)

     
    #----------------------------------------------------------------------------
    #
    # This method plots summary result data of evaluation test.
    #
    # Input: 
    #         result_file - File with cumulative test results.
    #         output_dir - Directory to place plot file to. Default is None.     
    #
    @classmethod
    def plotSummary (cls, 
                     result_file, 
                     output_dir = None):
        """ Plot test results in XML format."""
 
        
        return cls.plot(result_file, 
                        output_dir)

     