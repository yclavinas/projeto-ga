"""
Module ROCTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, matplotlib
from matplotlib.pylab import *

from EvaluationTest import EvaluationTest
from AlarmBasedTest import AlarmBasedTest
import CSEPFile


#--------------------------------------------------------------------------------
#
# MASSTest.
#
# This class is designed to evaluate available earthquake and alarm-based 
# forecasts models with the Receiver Operating Characteristic (ROC) test.
#
class ROCTest (AlarmBasedTest): 

    # Static data

    # Keyword identifying the class
    Type = "ROC"
    
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    #        args - Optional input arguments for the test. Default is None.    
    # 
    def __init__ (self, group, args = None):
        """ Initialization for ROCTest class."""
        
        # Constructors for base classes
        AlarmBasedTest.__init__(self, group, args)
        
        
    #----------------------------------------------------------------------------
    #
    # Writes comma-separated list of other forecasts models participating in the
    # test.
    #
    # Input:
    #        forecast_name - Forecast model for which evaluation test is invoked.
    #
    # Output: None
    #
    def otherForecastsFiles (self, forecast_name):
        """ Returns empty list of all other forecasts in the same forecast group 
            for the test: other models don't participate in the test."""
        
        return []


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

        return ROCTest.Type
     

    #----------------------------------------------------------------------------
    #
    # Plot test results.
    #
    # Input: 
    #        result_file - Path to the result file in XML format
    #        output_dir - Directory to place plot file to. Default is None.    
    #
    # Output: 
    #        Name for generated image file
    #
    @classmethod
    def plot (cls, 
              result_file,
              output_dir = None):
        """ Plot test results."""
 
        # Get DOM object for the result
        doc = AlarmBasedTest.plot(result_file)
         
        rcParams['figure.figsize'] = (9, 9)

        # clear figure
        ax = subplot(111)
        clf()

        name = doc.elementValue("name")

        # if names end with '.mat', '.dat', or '.xml', chop off suffix
        if name[-4:] in ( '.mat', '.MAT', '.dat', '.DAT', '.xml', '.XML' ):
            name = name[:-4]
            
        # get ordinate = hit rate
        ordinate_str   = doc.elementValue("hitRate")
        ordinate_array = ordinate_str.split()
        ordinate       = map( float, ordinate_array )

        # get abscissa - false alarm rate
        data_str_1     = doc.elementValue("falseAlarmRate")
        data_array_1   = data_str_1.split()
        abscissa_1 = map( float, data_array_1 )

        # get lower confidence bound
        lowerConfidence_str      = doc.elementValue("lowerConfidence")
        lowerConfidence_array    = lowerConfidence_str.split()
        lowerConfidence_abscissa = map( float, lowerConfidence_array )
        
        # get upper confidence bound
        upperConfidence_str      = doc.elementValue("upperConfidence")
        upperConfidence_array    = upperConfidence_str.split()
        upperConfidence_abscissa = map( float, upperConfidence_array )

        ax = gca()
        ax.set_zorder( EvaluationTest.Matplotlib.plotZOrder['axes'] )
        ax.set_axisbelow( False )
        
        # plot lower confidence bound
        plot( lowerConfidence_abscissa, 
              ordinate, 
              color=AlarmBasedTest.Matplotlib._plotConfidenceBounds['color'], 
              linestyle=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linestyle'], 
              linewidth=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linewidth'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['bounds'], 
              label='_nolegend_' )
        
        # shade region
        xs, ys = poly_between( lowerConfidence_abscissa, 
                               AlarmBasedTest.Matplotlib._plotConfidenceBounds['shadeUpperLimit'], 
                               ordinate )
        fill( xs, 
              ys, 
              facecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['facecolor'], 
              edgecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['edgecolor'],
              alpha=AlarmBasedTest.Matplotlib._plotConfidenceBounds['alpha'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['shade'] )
        
        # plot upper confidence bound
        plot( upperConfidence_abscissa, 
              ordinate, 
              color=AlarmBasedTest.Matplotlib._plotConfidenceBounds['color'], 
              linestyle=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linestyle'], 
              linewidth=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linewidth'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['bounds'], 
              label='_nolegend_' )
        
        # shade region
        xs, ys = poly_between( upperConfidence_abscissa, 
                               AlarmBasedTest.Matplotlib._plotConfidenceBounds['shadeLowerLimit'], 
                               ordinate )
        fill( xs, 
              ys, 
              facecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['facecolor'], 
              edgecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['edgecolor'], 
              alpha=AlarmBasedTest.Matplotlib._plotConfidenceBounds['alpha'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['shade'] )
        
        # plot data set
        # Combine color and marker into one string, using 'color' and 'marker'
        # attributes trims trajectories markers for some reason 
        plot( abscissa_1, 
              ordinate,  
              '%s%s' %(EvaluationTest.Matplotlib._plotColorMarker['colors'][0],
                       EvaluationTest.Matplotlib._plotColorMarker['marker'][0]),              
              markersize=AlarmBasedTest.Matplotlib._plotTrajectory['markersize'][1],
              zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
              label=name )

        # set x and y dimension of plot
        xlim( 0.0, 1.0 )
        ylim( 0.0, 1.0 )

        # plot legend
        l = legend(bbox_to_anchor = EvaluationTest.Matplotlib._plotLegend['bbox_to_anchor'],
                   loc = EvaluationTest.Matplotlib._plotLegend['loc'],
                   mode = EvaluationTest.Matplotlib._plotLegend['mode'], 
                   prop = EvaluationTest.Matplotlib._plotLegend['prop'])

        l.set_zorder(EvaluationTest.Matplotlib.plotZOrder['legend'] )
        
        xlabel( 'False alarm rate', EvaluationTest.Matplotlib._plotLabelsFont )
        ylabel( 'Hit rate', EvaluationTest.Matplotlib._plotLabelsFont )
        
        #show()

        image_file = result_file
        if output_dir is not None:
            image_file = os.path.join(output_dir,
                                      os.path.basename(result_file))

        image_file = image_file.replace(CSEPFile.Extension.XML,
                                        CSEPFile.Extension.SVG)
          
        savefig(image_file)
        close()
         
        return [image_file]

