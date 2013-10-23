"""
Module RELMNumberTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import matplotlib.pyplot as plt
import os, re
from pylab import *
import matplotlib.font_manager as font_manager

import scipy.stats, re

from Forecast import Forecast
from RELMTest import RELMTest
from EvaluationTest import EvaluationTest
from ForecastHandlerFactory import ForecastHandlerFactory
import CSEPLogging, CSEPUtils, CSEP, CSEPFile, CSEPGeneric


Delta1 = 'delta1'
Delta2 = 'delta2'

#===========================================================================
# Compute delta1 result variable for the test 
#===========================================================================
def computeDelta1 (number_quakes, number_forecast_quakes):
    """Compute result variable delta1 for the test: 
       1 - poisscdf(number_quakes - epsilon, number_forecast_quakes)."""
    
    return (1.0 - CSEPUtils.poissonCDF(number_quakes - RELMNumberTest.Epsilon,
                                       number_forecast_quakes))
    

#===========================================================================
# Compute delta1 result variable for the test 
#===========================================================================
def computeDelta2 (number_quakes, number_forecast_quakes):
    """Compute result variable delta2 for the test: 
       poisscdf(number_quakes + epsilon, number_forecast_quakes)."""
    
    return CSEPUtils.poissonCDF(number_quakes + RELMNumberTest.Epsilon,
                                number_forecast_quakes)


#-------------------------------------------------------------------------------
#
# RELMNumberTest.
#
# This class represents RELM N(umber) evaluation test for forecasts models.
#
class RELMNumberTest (RELMTest):

    # Static data

    # Keyword identifying the class
    Type = "N"
    
    # Some small positive number used to calculate result variables for the test
    Epsilon = 1e-6


    # Data structure to store test results    
    class Result (RELMTest.Result):

        # Names of result variables
        EventCount = 'eventCount'
        EventCountForecast = 'eventCountForecast'
        CDFData = 'cdfData' # top-level element for N-test results
        CDFCount = 'cdfCount'
        CDFValues = 'cdfValues'
        CDFEventCount = 'cdfEventCount'

        
        #=======================================================================
        # Initialize results structure and compute result variables (delta1,
        # delta2) for the test
        # 
        # Inputs:
        #   events - Number of observed events
        #   forecasts_events - Number of forecast events
        #   modificationsevents - Vector containing the numbers of events
        #                         in each modified catalog
        #
        def __init__ (self, 
                      events,
                      forecast_events,
                      modification_events):
            
            # Call base class constructor
            RELMTest.Result.__init__(self, 
                                     modification_events)
            
            self[RELMNumberTest.Result.EventCount] = events
            self[RELMNumberTest.Result.EventCountForecast] = forecast_events

            # Compute value of the cumulative density function
            # at (fEventCount - epsilon) and (fEventCount + epsilon)
            self[Delta1] = computeDelta1(events, 
                                         forecast_events)
            self[Delta2] = computeDelta2(events, 
                                         forecast_events)

            # Compute the number of points we should include in the CDF
            __number_events_atWhichCDFIsNearUnity = int(scipy.stats.poisson.ppf(0.9999, 
                                                                                forecast_events))
        
            # Add 1 - 'range' treats upper boundary exclusively 
            self[RELMNumberTest.Result.CDFEventCount] = range(-1, 
                                                              __number_events_atWhichCDFIsNearUnity + 1)
            self[RELMNumberTest.Result.CDFValues] = scipy.stats.poisson.cdf(self[RELMNumberTest.Result.CDFEventCount], 
                                                             forecast_events)
            self[RELMNumberTest.Result.CDFCount], = self[RELMNumberTest.Result.CDFValues].shape 


        #=======================================================================
        # writeXML
        # 
        # Write test results to XML format file
        #
        # Inputs:
        #         test_name - Name of evaluation test
        #         model_name - Name of the model for the test
        #         dirpath - Directory to write XML format file to
        #         file_prefix - Prefix to use for XML format filename  
        #=======================================================================
        def writeXML (self, 
                      test_name, 
                      model_file, 
                      dir_path, 
                      file_prefix):
            """Write test results to XML format file"""

            test_node, xml = RELMTest.Result.writeXML(self, 
                                                      test_name, 
                                                      model_file,
                                                      dir_path,
                                                      file_prefix)

            # Create cdfData element
            cdf_node = xml.addElement(RELMNumberTest.Result.CDFData,
                                      test_node)
            cdf_node.attrib[RELMTest.Result.PublicID] = 'smi://local/%s/1' \
                                                        %RELMNumberTest.Result.CDFData.lower()
            
            # Create count element for cdfData
            count_node = xml.addElement(RELMNumberTest.Result.CDFCount,
                                        cdf_node)
            count_node.text = repr(self[RELMNumberTest.Result.CDFCount])
            
            # Create cdf values and ticks elements
            values_node = xml.addElement(RELMNumberTest.Result.CDFValues,
                                         cdf_node)
            values_node.text = ' '.join(repr(i) for i in self[RELMNumberTest.Result.CDFValues])
                
            ticks_node = xml.addElement(RELMNumberTest.Result.CDFEventCount,
                                        cdf_node)
            ticks_node.text = ' '.join(repr(i) for i in self[RELMNumberTest.Result.CDFEventCount])
            
            
            # Create true event count element
            event_count_node = xml.addElement(RELMNumberTest.Result.EventCount,
                                              test_node)
            event_count_node.text = repr(self[RELMNumberTest.Result.EventCount])
            
            
            # Create forecast event count element
            event_count_node = xml.addElement(RELMNumberTest.Result.EventCountForecast,
                                              test_node)
            event_count_node.text = '%.5f' %self[RELMNumberTest.Result.EventCountForecast]
            
            ### Create delta elements
            delta_node = xml.addElement(Delta1,
                                        test_node)
            delta_node.text = '%.5f' %self[Delta1]
            
            delta_node = xml.addElement(Delta2,
                                        test_node)
            delta_node.text = '%.5f' %self[Delta2]
            
            
            # write XML format file
            xml.write()

    
    #===========================================================================
    # Definitions of XML elements used by the evaluation test.    
    #===========================================================================
    xml = RELMTest.XML('NTest',
                       Result.EventCount,
                       [RELMTest.Result.Name],
                       {Delta1 : Result.EventCountForecast,
                        Delta2 : Result.EventCountForecast},
                       {Delta1 : computeDelta1,
                        Delta2 : computeDelta2},
                       {'float' : CSEP.Operator['<=']},
                       # the "all-models" summary file for the test
                       # Dictionary of variables and optional function to apply
                       # to the variable (to get variable uncertainty range) 
                       # 
                       # XML element <--> function to apply
                       {Result.EventCountForecast : scipy.stats.poisson.ppf,
                        Result.EventCount : None})

 
    #===========================================================================
    # matplotlib settings for the test     
    #===========================================================================
    MatPlotLib = RELMTest.Matplotlib('Number of Events N',
                                     {Delta1 : 'b-o',   # delta1 - blue circles
                                      Delta2 : 'g-o'},  # delta2 - green circles 
                                     {Delta1 : RELMTest.Result.Name,
                                      Delta2 : RELMTest.Result.Name},
                                     False) # don't plot upper significance area 
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    # 
    def __init__ (self, group):
        """ Initialization for RELMNumberTest class."""
        
        RELMTest.__init__(self, group)


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

        return RELMNumberTest.Type
        
        
    #----------------------------------------------------------------------------
    #
    # Create plot of evaluation test summary for all participating model of 
    # the forecast group. This method plots forecasted number of events against
    # observed interval of events. 
    #
    # Input: 
    #        summary_path - Path to the summary file for the test
    #        output_dir - Directory to place plot file to. Default is None.    
    #
    # Output: List of plot files
    #
    @classmethod
    def plotAllModelsSummary(cls,
                             summary_path,
                             output_dir = None,
                             test_obj = None):
        """ Create a plot of observed number of events vs. forecasted number of
            events with [2.5; 97.5]% uncertainly interval."""
            
        ### Check for existence of the summary file - in case there are no
        # models in the group are available yet
        if summary_path is None or os.path.exists(summary_path) is False:
            return []
            
            
        __forecasted_marker = 'k-|'
        __observed_marker = 's'
        
        __rejected_color = 'r'
        __accepted_color = 'g' 

        __line_width = 1.5
        
        xml_obj, plot_obj = EvaluationTest.plot(summary_path,
                                                fig_size_num_tags = cls.xml.Root)
        
        # Dictionary of trajectory index and corresponding model name
        traj_name = {}
        __y_coord = 0

        traj_zorder = EvaluationTest.Matplotlib.plotZOrder['trajectory']
        
        # Test result for each model
        for traj_index, each_model_xml in enumerate(xml_obj.elements(cls.xml.Root)):
                    
            __y_coord += 0.1
                            
            # Extract forecasted value
            for each_var, each_var_func in cls.xml.AllModelsSummary.iteritems():

                # Extract observed number of events
                var_element = xml_obj.children(each_model_xml,
                                               RELMNumberTest.Result.EventCount)[0]
                event_count = float(var_element.text)
                
                # Extract forecasted number of events
                var_element = xml_obj.children(each_model_xml,
                                               RELMNumberTest.Result.EventCountForecast)[0]
                # Collect range values (uncertainty) for forecasted number of events
                forecasted_value = float(var_element.text)
                var_values = [forecasted_value]
                
                # Append 2.5 and 97.5 percentile of uncertainty for the value
                var_values.append(cls.xml.AllModelsSummary[RELMNumberTest.Result.EventCountForecast](0.025, 
                                                                                                     forecasted_value))
                var_values.append(cls.xml.AllModelsSummary[RELMNumberTest.Result.EventCountForecast](0.975, 
                                                                                                     forecasted_value))
                var_values.sort()

                # Determine the color to use for observed number of events
                marker_format = __observed_marker
                
                if event_count < min(var_values) or event_count > max(var_values):
                    marker_format += __rejected_color
                else:
                    marker_format += __accepted_color
                

                plt.plot([event_count],
                         [__y_coord],
                         marker_format,
                         markersize = 10.0,
                         linewidth = __line_width,
                         zorder = traj_zorder)

                plt.plot(var_values,
                         [__y_coord]*len(var_values), # y coordinate for the interval
                         __forecasted_marker,
                         markersize = 15.0,
                         linewidth = __line_width,
                         zorder = traj_zorder + 1)
                
                # Capture name of the model for the trajectory
                traj_name[__y_coord] = re.sub(CSEP.Forecast.FromXMLPostfix,
                                              '',
                                              xml_obj.children(each_model_xml,
                                                               cls.xml.ModelName[0])[0].text)

        # Disable y-axis ticks and their labels
        y_ticks_vals = traj_name.keys()
        y_ticks_vals.sort()
        plt.yticks(y_ticks_vals, [])
            
        plt.xlabel(cls.MatPlotLib.XLabel)   
        plt.ylim(0, __y_coord + 0.1) 
        xmin, xmax = plt.xlim()
        
        __x_coord = xmax + 0.3
        for __traj, __name in traj_name.iteritems():
            plt.text(__x_coord, 
                     __traj, 
                     __name, 
                     EvaluationTest.Result._plotFont, 
                     horizontalalignment='left')
        
        # Allow more space on left side of the plot to prevent 
        # clipping of model names
        plt.subplots_adjust(left = 0.05,
                            right = 0.75,
                            bottom = 0.15)

        image_file = summary_path
        
        if output_dir is not None:
            image_file = os.path.join(output_dir,
                                      os.path.basename(summary_path))
            
        # Replace extension with '.svg' for the image file
        image_file = image_file.replace(CSEPFile.Extension.XML,
                                        CSEPFile.Extension.PNG)
        plt.savefig(image_file)
        plt.close()
        
        return [image_file]
        

    #----------------------------------------------------------------------------
    #
    # This method plots result data of RELM N evaluation test.
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

        dom, plot_obj = EvaluationTest.plot(result_file) 

        # Plot data specific to the test, and set up the labels
        observed_x_axes = cls.__plotData(dom)

        # abscissa tick formatting (no floating point numbers)
        xmin, xmax = xlim()
        xdiff = xmax - xmin
        if ( xdiff <= 5 ):
            abscissaTickLocDiff = 1
        elif ( xdiff <= 14 ):
            abscissaTickLocDiff = 2
        elif ( xdiff <= 39 ):
            abscissaTickLocDiff = 5
        else:
            abscissaTickLocDiff = 10
             
        abscissaLoc  = MultipleLocator( abscissaTickLocDiff )
        abscissaFmt  = FormatStrFormatter( '%d' )
        plot_obj.xaxis.set_major_formatter( abscissaFmt )
        plot_obj.xaxis.set_major_locator( abscissaLoc )


        # Return image filename
        return RELMTest._finishPlot(cls.MatPlotLib.XLabel, 
                                    observed_x_axes,
                                    result_file,
                                    output_dir)

            
    #-----------------------------------------------------------------------------
    #
    # __plotData
    # 
    # This method plots result data of RELM N evaluation test.
    #
    # Input: 
    #         doc - DOM element representing root element of test results.
    #
    # Output: None.
    # 
    @classmethod
    def __plotData(cls, doc):
       """ Plot data of RELM N evaluation test  ."""
         
       name = doc.elementValue(cls.xml.ModelName[0])
       name = re.sub(CSEP.Forecast.FromXMLPostfix,
                     '',
                     name)

       forecast = float(doc.elementValue(RELMNumberTest.Result.EventCountForecast))

       data_count = int(doc.elementValue(RELMNumberTest.Result.CDFCount))
                      
       data_str = doc.elementValue(RELMNumberTest.Result.CDFEventCount)
       data_array = data_str.split()
       abscissa = sorted(map(int, data_array))
      
       data_str = doc.elementValue(RELMNumberTest.Result.CDFValues)
       data_array = data_str.split()
       ordinate = sorted(map(float, data_array))

       if (len(abscissa) != data_count):
          error_msg = "%s: %s - abscissa data vector length mismatch" %(CSEPLogging.CSEPLogging.frame(cls),
                                                                        name)
    
          CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
          raise RuntimeError, error_msg
      
       elif (len(ordinate) != data_count):
          error_msg = "%s: %s - ordinate data vector length mismatch" %(CSEPLogging.CSEPLogging.frame(cls),
                                                                        name)
    
          CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
          raise RuntimeError, error_msg


       # Plot modification data if present
       RELMTest._plotModificationData(doc, name)


       # True event count for the test
       observed = float(doc.elementValue(cls.xml.TrueEvent))
    
       # plot observed no. of events      
       axvline(observed, color=RELMTest.Matplotlib._plotObserved['color'], 
               linewidth=RELMTest.Matplotlib._plotObserved['linewidth'], 
               zorder=EvaluationTest.Matplotlib.plotZOrder['vertical'], 
               label='_nolegend_' )
    
       # plot predicted no. of events
       axvline( forecast, 
                color=RELMTest.Matplotlib._plotPredicted['color'], 
                linestyle=RELMTest.Matplotlib._plotPredicted['linestyle'], 
                zorder=EvaluationTest.Matplotlib.plotZOrder['vertical'], 
                label='_nolegend_' )
    
       # plot N test curve
       plot( abscissa, 
             ordinate, 
             color=RELMTest.Matplotlib._plotCurve['colors'][0], 
             linestyle=RELMTest.Matplotlib._plotCurve['linestyle'][0], 
             zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
             label=name )
    
       # set x and y dimension of plot
       ylim( RELMTest.Matplotlib._plotAxes['ymin'], 
             RELMTest.Matplotlib._plotAxes['ymax'] )
       
       xmin, xmax = xlim()
    
       # get x axes coords of observed, required to split rejection bar
       observed_x_axes = ( observed - xmin ) / ( xmax - xmin )
    
       return observed_x_axes 

         
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


        test_name = RELMTest.evaluate(self,
                                      forecast_name)

        forecast_path = os.path.join(self.forecasts.dir(), 
                                     forecast_name)
        
        (scaled_forecast, covers_area) = RELMTest.prepareForecast(self,
                                                                  forecast_path)

        # Invoke N-test
        test_result = self.__invoke(scaled_forecast)
        
        
        # Write results to the file
        test_result.writeXML(test_name, 
                             forecast_name,
                             self.testDir,
                             self.filePrefix())                      
        

    #---------------------------------------------------------------------------
    #
    # Run N-test for the forecast
    #
    # Input: 
    #        forecast - numpy.array object that represents forecast data
    #
    def __invoke (self, 
                  forecast):
        """Computation of the N-test for the RELM framework.  Here, we have observed
 w events and the specified forecast has predicted l events.  We want to
 know if the observation is consistent with the prediction, assuming that
 the distribution of the number of events forecast is Poissonian.  To quantify this
 consistency, we assume that the forecast is true and compute the
 probability that we would observe fewer than w events (or at least w events).  This is the
 probability of observing 0, 1,..., or w-1 events, or w, w+1, ..., Inf events.
 in other words we're going to use the cdf.  We call these probabilities
 delta, and delta1 = poisscdf(w-eps, l), delta2 = poisscdf(w+eps, l), where eps
 is some small positive number << 1.  For plotting purposes, we also want to return
 the cdf, and the number of events in each modified catalog.  To show the
 complete cdf, we would need to compute it at 0, 1,..., Inf.  Rather than
 doing this, we find the point at which the cdf is very close to unity,
 and only return the cdf out to this point.  This point is given as x =
 poissinv(0.9999, l), so we return a vector with (x + 1) elements
 containing the cdf value at 0, 1,..., x."""
 

        # Number of events in the observed catalog: don't compute likelihood
        __likelihood = False
        number_quakes = RELMTest.numberEventsCatalog(forecast, 
                                                     self.catalogFile.npObject,
                                                     __likelihood)
    
        # Number of modified catalogs
        num_modifications = 0
        if self.catalogModificationsFile.npObject is not None:
            num_rows, num_modifications = self.catalogModificationsFile.npObject.shape
        
        # Compute the number of events in each modified catalog
        number_quakes_modifications = np.zeros(num_modifications)
        
        for index in xrange(0, num_modifications):
           number_quakes_modifications[index] = RELMTest.numberEventsCatalog(forecast,
                                                                             self.catalogModificationsFile.npObject[0, index],
                                                                             __likelihood)
    
        # Total number of events forecast
        number_quakes_forecast = ForecastHandlerFactory().CurrentHandler.numberEvents(forecast[:, CSEPGeneric.Forecast.Format.Rate])
    
        # Compute Delta's and store the important parameters
        result = RELMNumberTest.Result(number_quakes,
                                       number_quakes_forecast,
                                       number_quakes_modifications)
    
        return result

        