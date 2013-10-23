"""
Module TStatisticalTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import os, re
import numpy as np
import matplotlib.pyplot as plt
#from pylab import *
import matplotlib.font_manager as font_manager

from StatisticalTest import StatisticalTest
from EvaluationTest import EvaluationTest
import CSEPLogging, CSEPUtils, CSEP, CSEPFile


#-------------------------------------------------------------------------------
#
# T statistical test for evaluation of rate-based forecasts. 
#
# This class represents T statistical evaluation test for forecasts models.
#
class TStatisticalTest (StatisticalTest):

    # Static data

    # Keyword identifying the class
    Type = "T"
    
    __logger = None

    __table = [12.71, 4.30, 3.18, 2.78, 2.57,
               2.45, 2.36, 2.31, 2.26, 2.23,
               2.20, 2.18, 2.16, 2.14, 2.13,
               2.12, 2.11, 2.10, 2.09, 2.09,
               2.08, 2.07, 2.07, 2.06, 2.06,
               2.05, 2.05, 2.05, 2.04, 2.04] + \
               [2.03] * 5 + [2.02] * 5 + \
               [2.01] * 10 + [2.0] * 20 + \
               [1.99] * 20 + [1.98] * 30 + [1.97] * 40

    # XML elements to store test results 
    __meanInformationGain = 'meanInformationGain'
    __lowerConfidenceLimits = 'lowerConfidenceLimits'
    __upperConfidenceLimits = 'upperConfidenceLimits'
    __numberEvents = 'numberEvents'

    InfoGainTitle = 'Information gain per earthquake'
    InfoGainPostfix = 'InformationGain'

    ProbGainTitle = 'Probability gain per earthquake'
    ProbGainPostfix = 'ProbabilityGain'
    

    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    # 
    def __init__ (self, group):
        """ Initialization for TStatisticalTest class."""

        if TStatisticalTest.__logger is None:
           TStatisticalTest.__logger = CSEPLogging.CSEPLogging.getLogger(TStatisticalTest.__name__)
        
        StatisticalTest.__init__(self, group)


    def initializeData (self, forecasts_files):
        """ Initialization of internal data for TStatisticalTest object."""
        
        TStatisticalTest.__logger.info("Initializing T-Test with %s models" %forecasts_files)
        StatisticalTest.initializeData(self,
                                       forecasts_files)

        # Number of models participating in the test
        num_models = len(forecasts_files)
    
        if num_models != 0:
            
            # These arrays are shared by each model evaluation since T-Test is
            # a cumulative test for all models included into forecast group 
            self.np_mnmat = np.zeros((num_models, num_models), dtype = np.float)
            self.np_lower = np.zeros((num_models, num_models), dtype = np.float)
            self.np_upper = np.zeros((num_models, num_models), dtype = np.float)
            self.np_Nmat = np.zeros((num_models, num_models), dtype = np.float)
    
            # For WTest
            # wsigmat = np.array((num_models, num_models), dtype = np.float)
            # wmat = np.array((num_models, num_models), dtype = np.float)

        else:
            self.np_mnmat = None
            self.np_lower = None
            self.np_upper = None
            self.np_Nmat = None


    #===========================================================================
    # Is internal data initialized?
    #===========================================================================
    def isInitialized (self):
        """ Returns a flag is internal data of the class was initialized (True)
            or not (False)."""
            
        return (self.np_mnmat is not None)
            

    #---------------------------------------------------------------------------
    #
    # Returns keyword identifying the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: String representation of the test type.
    #
    def type (self):
        """ Returns test type."""

        return TStatisticalTest.Type

            
    #---------------------------------------------------------------------------
    #
    # Invoke evaluation test for the forecast
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def evaluate (self, 
                  forecast_name):
        """ Invoke evaluation test for the forecast."""


        test_name = StatisticalTest.evaluate(self, forecast_name)
        
        # Evaluation test should not be invoked (observation catalog is invalid)
        if test_name is None:
            return
        
        # Invoke T-test
        test_result = self.__invoke(forecast_name)
        
        # Write results to the file if very last forecast is evaluated within
        # the group
        all_models = StatisticalTest.rates(self.forecasts).all_models
        if all_models.index(forecast_name) == (len(all_models) - 1):
            
            test_results = {TStatisticalTest.__meanInformationGain: self.np_mnmat,
                            TStatisticalTest.__lowerConfidenceLimits: self.np_lower,
                            TStatisticalTest.__upperConfidenceLimits: self.np_upper,
                            TStatisticalTest.__numberEvents: self.np_Nmat}
            
            results = StatisticalTest.Result(test_results)
            results.writeXML(test_name,
                             tuple(StatisticalTest.rates(self.forecasts).all_models),
                             self.testDir,
                             self.filePrefix())                      
        

    #---------------------------------------------------------------------------
    #
    # Run T-test for the forecast
    #
    # Input: 
    #        forecast - numpy.array object that represents forecast data
    #
    def __invoke (self, 
                  forecast):
        """Computation of the T-statistics test. This test is introduced by 
David Rhoades which "...implements the classical paired t-test, found in any standard
statistical text...". For full description of the test please refer to the
"A first-order test to compare regional earthquake likelihood models" by 
D.A. Rhoades, M.C. Gerstenberger, and A. Christophersen, GNS Science, Lower Hutt,
New Zealand."""
 

        # Forecast's index into list of available forecasts for the test
        group_rates = StatisticalTest.rates(self.forecasts)
        index = group_rates.all_models.index(forecast)
        
        for j in xrange(0, len(group_rates.all_models)):
            
            diff = np.log(group_rates.np_event_rates[index][:, StatisticalTest.EventInfo.Format.Rate]) - \
                   np.log(group_rates.np_event_rates[j][:, StatisticalTest.EventInfo.Format.Rate])
            
            nan_diff = diff[~np.isnan(diff)]
            
            tmn = nan_diff.mean()
            
            # numpy.cov returns value in array
            tvar = np.cov(nan_diff)
            
            # How many common events forecasts provide rates for
            N = (~np.isnan(diff)).sum()
            
            Nhat1 = group_rates.np_sum_rates[index, j]
            Nhat2 = group_rates.np_sum_rates[j, index]
            
            tmn = tmn-(Nhat1-Nhat2)/N

            # All hard-coded values are inherited from original R code submitted
            # by David
            tval = 1.96
            if N <= 160.0:
                tval = TStatisticalTest.__table[N-2]
                
            smn = np.sqrt(tvar/N)
            self.np_mnmat[index,j] = tmn
            self.np_lower[index,j] = tmn - smn*tval
            self.np_upper[index,j] = tmn + smn*tval
            self.np_Nmat[index,j] = N
            
        return
        
        
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
    def plot (cls, 
              result_file, 
              output_dir = None, 
              np_wilcoxon_sign = None,
              image_file = None):
        """ Plot test results."""
 
        # Get DOM object for the result
        doc = StatisticalTest.plot(result_file)
         
        ### Create 2 plots per each forecast within result file: 
        ### probability gain and information gain 
        plots = []
        
        # Get rid of the extension
        name = CSEPFile.Name.extension(result_file)

        # Information gain plot
        plots = cls.__plotData(doc, 
                               name,
                               TStatisticalTest.InfoGainTitle,
                               TStatisticalTest.InfoGainPostfix,
                               output_dir,
                               image_file,
                               wilcoxon_sign = np_wilcoxon_sign)
        
        # Probability gain plot
        plots.extend(cls.__plotData(doc, 
                                    name,
                                    TStatisticalTest.ProbGainTitle,
                                    TStatisticalTest.ProbGainPostfix,
                                    output_dir,
                                    image_file,
                                    np.exp,
                                    np_wilcoxon_sign))
        
        return plots
    

    #-----------------------------------------------------------------------------
    #
    # __plotData
    # 
    # This method plots result data of RELM S evaluation test.
    #
    # Input: 
    #         doc - DOM element representing root element of test results.
    #
    # Output: None.
    # 
    @classmethod
    def __plotData(cls, 
                   doc,
                   result_name,
                   x_label,
                   file_keyword,
                   output_dir,
                   image_name = None,
                   function_op = None,
                   wilcoxon_sign = None):
        """ Plot data of T evaluation test."""

        __marker = 'k-|'
        __line_width = 1.5
        __y_coord_delta = 0.1
        
        traj_zorder = EvaluationTest.Matplotlib.plotZOrder['trajectory']

        # Get rid of internal CSEP 'fromXML' keyword from all model names
        models = [re.sub(CSEP.Forecast.FromXMLPostfix,
                         '',
                         each_name) for each_name in doc.elementValue(EvaluationTest.Result.Name).split()]
     
        num_models = len(models)
        plt.rcParams['figure.figsize'] = (9, num_models)
        
        result_plots = []
        
        # Re-store numpy arrays to represent test results
        mean_info_gain_str = doc.elementValue(TStatisticalTest.__meanInformationGain)
        mean_info_gain = [float(each_val) for each_val in mean_info_gain_str.split()]
        np_mean_info_gain = np.array([mean_info_gain])
        np_mean_info_gain.shape = (num_models, num_models)

        lower_conf_str = doc.elementValue(TStatisticalTest.__lowerConfidenceLimits)
        lower_conf = [float(each_val) for each_val in lower_conf_str.split()]
        np_lower_conf = np.array([lower_conf])
        np_lower_conf.shape = (num_models, num_models)

        upper_conf_str = doc.elementValue(TStatisticalTest.__upperConfidenceLimits)
        upper_conf = [float(each_val) for each_val in upper_conf_str.split()]
        np_upper_conf = np.array([upper_conf])
        np_upper_conf.shape = (num_models, num_models)

        num_events_str = doc.elementValue(TStatisticalTest.__numberEvents)
        num_events = [float(each_val) for each_val in num_events_str.split()]
        np_num_events = np.array([num_events])
        np_num_events.shape = (num_models, num_models)
        
        for index, each_model in enumerate(models):

            traj_index = 0
            traj_name = {}
            
            # Format filename for image file
            image_file = result_name
            if image_name is not None:
                image_file = image_name
                
            if output_dir is not None:
                image_file = os.path.join(output_dir,
                                          os.path.basename(result_name))
                
            image_file += "_%s_%s%s" %(each_model,
                                       file_keyword,
                                       CSEPFile.Extension.SVG)

            # clear figure
            fig = plt.figure()
            plot_obj = fig.add_subplot(111)
            plt.clf()
            
            plt.title(each_model,
                      EvaluationTest.Matplotlib._titleFont)
            
            for other_model_index, other_model in enumerate(models):
            
                if index != other_model_index:
                    x = np_mean_info_gain[index, other_model_index]
                    data_points = [np_lower_conf[index, other_model_index],
                                   #x, 
                                   np_upper_conf[index, other_model_index]]
                    
                    if function_op is not None:
                        data_points = function_op(data_points)
                        x = function_op(x)
                    
                    traj_index += __y_coord_delta
                    __y_coord = traj_index
                    traj_name[__y_coord] = other_model
                    
                    plt.plot(data_points,
                             [__y_coord]*len(data_points), # y coordinate for the interval
                             __marker,
                             markersize = 15.0,
                             linewidth = __line_width,
                             zorder = traj_zorder)

                    plt.plot(x,
                             __y_coord, # y coordinate for the interval
                             'ko',
                             markersize = 10.0,
                             markeredgecolor='k',
                             markerfacecolor='w',
                             markeredgewidth=1.5,
                             zorder = traj_zorder - 1)
                    
                    # Plot number of events
                    plt.text(x,
                             __y_coord + __y_coord_delta/2.0,
                             '%d' %int(np_num_events[index, 
                                                     other_model_index]),
                             ha='center', 
                             va='bottom',
                             zorder= traj_zorder + 1,
                             fontdict=EvaluationTest.Result._plotFont)
                    
                    # Plot Wilcoxon significance if it's provided
                    if wilcoxon_sign is not None:
                        wilcoxon_char = 'ns'
                        if wilcoxon_sign[index, other_model_index] == 1:
                            wilcoxon_char = '*'
                            
                        plt.text(x,
                                 __y_coord - __y_coord_delta/2.0,
                                 wilcoxon_char,
                                 ha='center', 
                                 va='bottom',
                                 zorder= traj_zorder + 1,
                                 fontdict=EvaluationTest.Result._plotFont)
            
            # Plot vertical line at x=0
            vertical_x = 0.0
            if function_op is not None:
                vertical_x = function_op(vertical_x)
                
            plt.axvline(vertical_x,
                        color = 'k',
                        linestyle = '--',
                        linewidth=2.0,
                        zorder=EvaluationTest.Matplotlib.plotZOrder['vertical'], 
                        label='_nolegend_')
                        
            # Allow more space on left side of the plot to prevent
            # clipping of model names
            fig.subplots_adjust(left = 0.05,
                                right = 0.75,
                                bottom = 0.15)

            #plot_obj.yaxis.
            xmin, xmax = plt.xlim()
            
            if xmax == 0.0:
                xmax = 1.0
            if xmin == 0.0:
                xmin = -1.0
            
            xmin = np_lower_conf[index, :].min() - 1.0
            xmax = np_upper_conf[index, :].max() + 1.0
            
            if function_op is not None:
                xmin = function_op(xmin)
                xmax = function_op(xmax)
                plt.xscale('log')
            
            # Place models names on x-axis proportional to the [min;max] range
            # displayed
            __x_delta = abs(xmax-xmin)/10.0
            if __x_delta > 10.0:
                __x_delta = 5.0
            elif __x_delta > 1.0:
                __x_delta = 1.0
                
            __x_coord = xmax + __x_delta
            for __traj, __name in traj_name.iteritems():
                plt.text(__x_coord, 
                         __traj, 
                         __name, 
                         EvaluationTest.Result._plotFont, 
                         ha='left')

                
            plt.xlabel(x_label)   
            plt.ylim(0, traj_index + __y_coord_delta)
            plt.xlim(xmin, xmax)
            

            # Disable y-axis ticks and their labels
            y_ticks_vals = traj_name.keys()
            y_ticks_vals.sort()
            plt.yticks(y_ticks_vals, [])

            plt.savefig(image_file)
            plt.close()
            
            result_plots.append(image_file)

        return result_plots
    
        