"""
Module MASSTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, matplotlib

from matplotlib.pylab import *

from EvaluationTest import EvaluationTest
from AlarmBasedTest import AlarmBasedTest
import CSEPFile, CSEPLogging


#--------------------------------------------------------------------------------
#
# MASSTest.
#
# This class is designed to evaluate available earthquake and alarm-based 
# forecasts models with a combination of Molchan diagram/Area Skill Score diagram
# (Molchan/ASS) test.
#
class MASSTest (AlarmBasedTest): 

    # Static data

    # Keyword identifying the class
    Type = "MASS"
    
    
    __MolchanPlotName = 'MolchanDiagram'
    __ASSPlotName = 'ASSDiagram'    
    
    
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
        """ Initialization for MASSTest class."""
        
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
        """ Returns list of all other forecasts in the same forecast group 
            for the test."""
        
        return [os.path.join(self.forecasts.dir(), model) for model 
                in self.forecasts.files() if model != forecast_name]


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

        return MASSTest.Type
     
     
    #----------------------------------------------------------------------------
    #
    # Plot test results.
    #
    # Input: 
    #        result_file - Path to the result file in XML format
    #        output_dir - Directory to place plot file to. Default is None.
    #
    # Output: 
    #        List of plots filenames.
    #
    @classmethod
    def plot (cls, result_file, output_dir = None):
        """ Plot test results."""
 
        # Get DOM object for the result
        doc = AlarmBasedTest.plot(result_file)
         
        ### Create 2 plots for the result file: Molchan and ASS diagrams
        plots = []
        
        # Get rid of the extension
        name = CSEPFile.Name.extension(result_file)
        
        # Molchan diagram
        plots.append(cls.__plotMolchan(doc, 
                                       name, 
                                       output_dir))
        
        # ASS diagram
        plots.append(cls.__plotASS(doc, 
                                   name,
                                   output_dir))
        
        return plots
     

    #----------------------------------------------------------------------------
    #
    # Plot Molchan trajectories for the test results.
    #
    # Input: 
    #        doc - DOM object for the result document
    #        result_file_prefix - Path to the result file without file extension
    #        output_dir - Directory to place plot file to.    
    #
    # Output: 
    #        Plot filename.
    #
    @classmethod
    def __plotMolchan (cls, 
                       doc, 
                       result_file_prefix, 
                       output_dir):
        """ Create Molchan diagram for the test results."""
 
        rcParams['figure.figsize'] = (9, 9)

        # clear figure
        ax = subplot(111)
        clf()
        
        # get ordinate = Molchan nu
        ordinate_str   = doc.elementValue("molchanNu")
        ordinate_array = ordinate_str.split()
        ordinate       = map( float, ordinate_array )

        # get lower confidence bound
        lowerConfidence_str      = doc.elementValue("molchanLowerConfidence")
        lowerConfidence_array    = lowerConfidence_str.split()
        lowerConfidence_abscissa = map( float, lowerConfidence_array )
        
        # get upper confidence bound
        upperConfidence_str      = doc.elementValue("molchanUpperConfidence")
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
                               AlarmBasedTest.Matplotlib._plotConfidenceBounds['shadeLowerLimit'], 
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
                               AlarmBasedTest.Matplotlib._plotConfidenceBounds['shadeUpperLimit'], 
                               ordinate )
        fill( xs, 
              ys, 
              facecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['facecolor'], 
              edgecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['edgecolor'], 
              alpha=AlarmBasedTest.Matplotlib._plotConfidenceBounds['alpha'],
              zorder=EvaluationTest.Matplotlib.plotZOrder['shade'] )

        # Plot trajectories
        start_node = doc.elements("molchanTrajectories")[0]
        all_trajectories = doc.children(start_node,
                                        "molchanTrajectory")
        
        
        for traj_index, each_traj_elem in enumerate(all_trajectories):
           name = each_traj_elem.attrib['forecast']

           # if names end with '.mat', '.dat', or '.xml', chop off suffix
           if name[-4:] in ( '.mat', '.MAT', '.dat', '.DAT', '.xml', '.XML' ):
               name = name[:-4]
            
           # get Molchan trajectory values
           data_str = each_traj_elem.text.strip()
           data_array = data_str.split()
           molchan_abscissa = map(float, data_array)

           # Assign color and marker to the trajectory
           marker_type, color_type = EvaluationTest.Matplotlib.colorMarker(traj_index)
              
           # plot data set:
           # Combine color and marker into one string, using 'color' and 'marker'
           # attributes trims trajectories markers for some reason 
           plot(molchan_abscissa, 
                ordinate,
                '%s%s' %(color_type, marker_type),
                markersize=AlarmBasedTest.Matplotlib._plotTrajectory['markersize'][1],
                zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
                label=name)

        # set x and y dimension of plot
        xlim( 0.0, 1.0 )
        ylim( 0.0, 1.0 )

        legend_ncols = len(all_trajectories) % 4
        if legend_ncols == 0:
            legend_ncols = 4

        # plot legend
        l = legend(bbox_to_anchor = EvaluationTest.Matplotlib._plotLegend['bbox_to_anchor'],
                   loc = EvaluationTest.Matplotlib._plotLegend['loc'],
                   mode = EvaluationTest.Matplotlib._plotLegend['mode'], 
                   ncol=legend_ncols,
                   columnspacing = EvaluationTest.Matplotlib._plotLegend['columnspacing'],
                   prop = EvaluationTest.Matplotlib._plotLegend['prop'])

        l.set_zorder(EvaluationTest.Matplotlib.plotZOrder['legend'])
        
        xlabel('Fraction of space-time occupied by alarm (' + r'$\tau$' + ')', 
               EvaluationTest.Matplotlib._plotLabelsFont)
        ylabel('Miss rate (' + r'$\nu$' + ')', 
               EvaluationTest.Matplotlib._plotLabelsFont)
        
        image_file = result_file_prefix
        if output_dir is not None:
            image_file = os.path.join(output_dir,
                                      os.path.basename(result_file_prefix))
            
        image_file += "_%s%s" %(MASSTest.__MolchanPlotName,
                                 CSEPFile.Extension.SVG)
          
        savefig(image_file)
        close()
         
        return image_file
    
      
    #----------------------------------------------------------------------------
    #
    # Plot ASS trajectories for the test results.
    #
    # Input: 
    #        doc - DOM object for the result document
    #        result_file_prefix - Path to the result file without file extension
    #        output_dir - Directory to place plot file to.    
    #
    # Output: 
    #        Plot filename.
    #
    @classmethod
    def __plotASS (cls, 
                   doc, 
                   result_file_prefix,
                   output_dir):
        """ Create ASS diagram for the test results."""
      
      
        rcParams['figure.figsize'] = (12, 9)

        # clear figure
        ax = subplot(111)
        clf()
        
        # get abscissa = ASS tau
        abscissa_str   = doc.elementValue("assTau")
        abscissa_array = abscissa_str.split()
        abscissa       = map( float, abscissa_array )

        # get lower confidence bound
        lowerConfidence_str      = doc.elementValue("assLowerConfidence")
        lowerConfidence_array    = lowerConfidence_str.split()
        lowerConfidence_ordinate = map( float, lowerConfidence_array )
        
        # get upper confidence bound
        upperConfidence_str      = doc.elementValue("assUpperConfidence")
        upperConfidence_array    = upperConfidence_str.split()
        upperConfidence_ordinate = map( float, upperConfidence_array )

        ax = gca()
        ax.set_zorder( EvaluationTest.Matplotlib.plotZOrder['axes'] )
        ax.set_axisbelow( False )
        
        # plot lower confidence bound
        plot( abscissa, 
              lowerConfidence_ordinate, 
              color=AlarmBasedTest.Matplotlib._plotConfidenceBounds['color'], 
              linestyle=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linestyle'],
              linewidth=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linewidth'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['bounds'], 
              label='_nolegend_' )
        
        # shade region
        xs, ys = poly_between( abscissa, 
                               AlarmBasedTest.Matplotlib._plotConfidenceBounds['shadeLowerLimit'], 
                               lowerConfidence_ordinate )
        fill( xs, 
              ys, 
              facecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['facecolor'], 
              edgecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['edgecolor'], 
              alpha=AlarmBasedTest.Matplotlib._plotConfidenceBounds['alpha'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['shade'] )
        
        # plot upper confidence bound
        plot( abscissa, 
              upperConfidence_ordinate, 
              color=AlarmBasedTest.Matplotlib._plotConfidenceBounds['color'], 
              linestyle=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linestyle'], 
              linewidth=AlarmBasedTest.Matplotlib._plotConfidenceBounds['linewidth'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['bounds'], 
              label='_nolegend_' )
        
        # shade region - note: shading will overlap axis, use transparency (alpha)
        xs, ys = poly_between( abscissa, 
                               AlarmBasedTest.Matplotlib._plotConfidenceBounds['shadeUpperLimit'], 
                               upperConfidence_ordinate )
        fill( xs, 
              ys, 
              facecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['facecolor'], 
              edgecolor=AlarmBasedTest.Matplotlib._plotConfidenceBounds['edgecolor'], 
              alpha=AlarmBasedTest.Matplotlib._plotConfidenceBounds['alpha'], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['shade'] )

        # Plot trajectories
        start_node = doc.elements("assTrajectories")[0]
        all_trajectories = doc.children(start_node,
                                        "assTrajectory")
        
        for traj_index, each_traj_elem in enumerate(all_trajectories):
           name = each_traj_elem.attrib['forecast']

           # if names end with '.mat', '.dat', or '.xml', chop off suffix
           if name[-4:] in ( '.mat', '.MAT', '.dat', '.DAT', '.xml', '.XML' ):
               name = name[:-4]

           # get Molchan trajectory values
           data_str = each_traj_elem.text.strip()
           data_array = data_str.split()
           ass_ordinate = map(float, data_array)

           # Assign color and marker to the trajectory
           marker_type, color_type = EvaluationTest.Matplotlib.colorMarker(traj_index)
           

           # Combine color and marker into one string, using 'color' and 'marker'
           # attributes trims trajectories markers for some reason 
           plot(abscissa, 
                ass_ordinate,
                '%s%s' %(color_type, marker_type),
                markersize=AlarmBasedTest.Matplotlib._plotTrajectory['markersize'][0],
                zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
                label=name)

        # set x and y dimension of plot
        xlim( 0.0, 1.0 )
        ylim( 0.0, 1.0 )

        legend_ncols = 2
        if len(all_trajectories) >= 3:
            legend_ncols = 3
            
        # plot legend
        l = legend(bbox_to_anchor = EvaluationTest.Matplotlib._plotLegend['bbox_to_anchor'],
                   loc = EvaluationTest.Matplotlib._plotLegend['loc'],
                   mode = EvaluationTest.Matplotlib._plotLegend['mode'], 
                   ncol=legend_ncols,
                   columnspacing = EvaluationTest.Matplotlib._plotLegend['columnspacing'],
                   prop = EvaluationTest.Matplotlib._plotLegend['prop'])

        l.set_zorder( EvaluationTest.Matplotlib.plotZOrder['legend'] )

        xlabel('Fraction of space-time occupied by alarm (' + r'$\tau$' + ')', 
               EvaluationTest.Matplotlib._plotLabelsFont)
        ylabel('Area skill score', 
               EvaluationTest.Matplotlib._plotLabelsFont)
      
        #show()

        image_file = result_file_prefix
        if output_dir is not None:
            image_file = os.path.join(output_dir,
                                      os.path.basename(result_file_prefix))
            
        image_file += "_%s%s" %(MASSTest.__ASSPlotName,
                                CSEPFile.Extension.SVG)
          
        savefig(image_file)
        close()
         
        return image_file

     