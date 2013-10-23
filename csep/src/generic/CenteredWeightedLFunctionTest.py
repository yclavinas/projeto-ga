"""
Module CenteredWeightedLFunctionTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

from pylab import *

from EvaluationTest import EvaluationTest
from DiagnosticsTest import DiagnosticsTest


#-------------------------------------------------------------------------------
#
# CenteredWeightedLFunctionTest
#
# This class is designed to invoke centered weighted L-function evaluation test
# which is introduced to the CSEP Testing Framework by Robert Clements et al.
#
class CenteredWeightedLFunctionTest (DiagnosticsTest):

     # Static data

    # Keyword identifying the class
    Type = "LW"

    
    # Data fields of test result
    __r = 'r'
    __lFunction = 'l.function'
    __lowerBound = 'l.bound'
    __upperBound = 'u.bound'
    __yAxisLabel = r'$L_\mathrm{W}(r)-r$'

    
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
        """ Initialization for CenteredWeightedLFunctionTest class."""
        
        DiagnosticsTest.__init__(self, group, args)


    #-----------------------------------------------------------------------------
    #
    # Returns description word for the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: Description of the test (such RELMTest, AlarmTest, etc.)
    #
    def type (self):
        """ Returns test type identifier."""

        return CenteredWeightedLFunctionTest.Type


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

        return None


    #===========================================================================
    # Write input catalog information to the parameter file for the test
    #===========================================================================
    def writeMagnitudeRangeInfo(self, fhandle):
        """Write magnitude range for the test."""
        
        return fhandle


    #===========================================================================
    # Write R function to invoke for the test
    #===========================================================================
    def execFunction(self):
        """Return R source function for the test."""
        
        return 'weighted_l_function.R'


    #===========================================================================
    # Return list of XML elements that represent test results
    #===========================================================================
    @classmethod
    def xmlElements(cls):
        """Return list of XML elements that represent test results"""
        
        return [CenteredWeightedLFunctionTest.__r,
                CenteredWeightedLFunctionTest.__lFunction,
                CenteredWeightedLFunctionTest.__lowerBound,
                CenteredWeightedLFunctionTest.__upperBound]
    

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

        # Plot data specific to the test, and set up the labels
        name = doc.elementValue(EvaluationTest.Result.Name)
        
        r_value = doc.elementValue(CenteredWeightedLFunctionTest.__r)
        if r_value is None:
            # Empty results are provided (using empty observation catalog)
            return []
            
        r_values_str = doc.elementValue(CenteredWeightedLFunctionTest.__r).split()
        r_values = map(float, r_values_str)
        
        lFunc_values_str = doc.elementValue(CenteredWeightedLFunctionTest.__lFunction).split()
        lFunc_values = map(float, lFunc_values_str)
        
        lowerBound_values_str = doc.elementValue(CenteredWeightedLFunctionTest.__lowerBound).split()
        lowerBound_values = map(float, lowerBound_values_str)
        
        upperBound_values_str = doc.elementValue(CenteredWeightedLFunctionTest.__upperBound).split()
        upperBound_values = map(float, upperBound_values_str)
        
        # plot test curves
        plot (r_values, 
              lFunc_values, 
              color=DiagnosticsTest.Matplotlib._plotCurve['color'], 
              linestyle=DiagnosticsTest.Matplotlib._plotCurve['linestyle'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
              label='_nolegend_' )

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
                                           "Centered weighted L-function (%s)" %name,
                                           CenteredWeightedLFunctionTest.__r, 
                                           CenteredWeightedLFunctionTest.__yAxisLabel)

