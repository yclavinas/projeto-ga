"""
Module WStatisticalTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import matplotlib, os, scipy.stats, glob, re
from pylab import *
import matplotlib.font_manager as font_manager

from StatisticalTest import StatisticalTest
from EvaluationTest import EvaluationTest
from TStatisticalTest import TStatisticalTest
import CSEPLogging, CSEPUtils, CSEP, CSEPFile


#-------------------------------------------------------------------------------
#
# W statistical test for evaluation of rate-based forecasts. 
#
# This class represents W statistical evaluation test for forecasts models.
#
class WStatisticalTest (StatisticalTest):

    # Static data

    # Keyword identifying the class
    Type = "W"
    
    __logger = None

    __table = [-1] * 5 + [0, 2, 4, 6, 8, 11, 14,
                          17, 21, 25, 30, 35, 40,
                          46, 52, 59, 66, 73, 81, 89]

    __WilcoxonSignificance = 'WilcoxonSignificance'
    

    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    # 
    def __init__ (self, group):
        """ Initialization for WStatisticalTest class."""

        if WStatisticalTest.__logger is None:
           WStatisticalTest.__logger = CSEPLogging.CSEPLogging.getLogger(WStatisticalTest.__name__)
        
        StatisticalTest.__init__(self, group)


    def initializeData (self, forecasts_files):
        """ Initialization of internal data for WStatisticalTest object."""
        
        WStatisticalTest.__logger.info("Initializing W-Test with %s models" %forecasts_files)
        StatisticalTest.initializeData(self,
                                       forecasts_files)

        # Number of models participating in the test
        num_models = len(forecasts_files)
    
        if num_models != 0:
            
            # These arrays are shared by each model evaluation since W-Test is
            # a cumulative test for all models included into forecast group
            self.np_wmat = np.zeros((num_models, num_models), dtype = np.float)
            self.np_wsigmat = np.zeros((num_models, num_models), dtype = np.float)
    

        else:
            self.np_wmat = None
            self.np_wsigmat = None
            

    #===========================================================================
    # Is internal data initialized?
    #===========================================================================
    def isInitialized (self):
        """ Returns a flag is internal data of the class was initialized (True)
            or not (False)."""
            
        return (self.np_wsigmat is not None)
            

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

        return WStatisticalTest.Type

            
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
        
        
        # Invoke W-test
        test_result = self.__invoke(forecast_name)
        
        # Write results to the file if very last forecast is evaluated within
        # the group
        all_models = StatisticalTest.rates(self.forecasts).all_models
        if all_models.index(forecast_name) == (len(all_models) - 1):
            
            test_results = {WStatisticalTest.__WilcoxonSignificance: self.np_wsigmat}
            
            results = StatisticalTest.Result(test_results)
            results.writeXML(test_name,
                             tuple(StatisticalTest.rates(self.forecasts).all_models),
                             self.testDir,
                             self.filePrefix())                      
        

    #---------------------------------------------------------------------------
    #
    # Run W-test for the forecast
    #
    # Input: 
    #        forecast - numpy.array object that represents forecast data
    #
    def __invoke (self, 
                  forecast):
        """Computation of the W-statistics test. This test is introduced by 
David Rhoades which implements the Wilcoxon signed-rank test. "... If the normal
distribution assumption seems to be violated, non-parametric alternative to the
paired t-test... may be applied to test whether the median of (Xi - Yi) is equal
to (Nhat_A - Nhat_B)/N." 
For full description of the test please refer to the
"A first-order test to compare regional earthquake likelihood models" by 
D.A. Rhoades, M.C. Gerstenberger, and A. Christophersen, GNS Science, Lower Hutt,
New Zealand."""
 

        # Forecast's index into list of available forecasts for the test
        group_rates = StatisticalTest.rates(self.forecasts)
        index = group_rates.all_models.index(forecast)
        
        for j in xrange(0, len(group_rates.all_models)):
            
            diff = np.log(group_rates.np_event_rates[index][:, StatisticalTest.EventInfo.Format.Rate]) - \
                   np.log(group_rates.np_event_rates[j][:, StatisticalTest.EventInfo.Format.Rate])

            # How many common events forecasts provide rates for
            N = (~np.isnan(diff)).sum()

            Nhat1 = group_rates.np_sum_rates[index, j]
            Nhat2 = group_rates.np_sum_rates[j, index]

            diff -= (Nhat1 - Nhat2)/N

            nan_diff = diff[~np.isnan(diff)]
            absdiff = np.abs(nan_diff)
            abs_diff_sum = (absdiff==0).sum()
            
            rankdiff = scipy.stats.rankdata(absdiff)
            rankdiff -= abs_diff_sum
            
            N -= abs_diff_sum
            ranktest = np.zeros(rankdiff.size)
            
            for i in xrange(0, rankdiff.size):
                ranktest[i] = rankdiff[absdiff==absdiff[i]].mean()

            Splus = ranktest[nan_diff>0].sum()
            Sminus = ranktest[nan_diff<0].sum()
            self.np_wmat[index,j] = min(Splus,Sminus)
            
            if index!=j:
                # self.np_wsigmat[index,j] is set to zero by default,
                # non-diagonal elements should be one of 0 or 1:
                # According to David's email from 2011/06/02:
                # "wsigmat' is the matrix of significance-test results for the
                # Wilcoxon (W) test. A value of 1 in the [i,j] position 
                # indicates a significant difference (with 95% confidence) 
                # between model i and model j. A value of 0 indicates 
                # no significant difference"
                if N<=25:
                    if self.np_wmat[index,j] <= WStatisticalTest.__table[N-1]:
                        self.np_wsigmat[index,j] = 1
                        
                else:
                    expw = 0.25*N*(N+1)
                    sdw = np.sqrt(N*(N+1)*(2*N+1)/24)
                    
                    if self.np_wmat[index,j] < (expw-1.96*sdw):
                        self.np_wsigmat[index,j] = 1
            else:
                # Set diagonal elements of wsigmat to nan (just like David's code)
                self.np_wsigmat[index, j] = np.nan
            
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
    def plot (cls, result_file, output_dir = None):
        """ Plot test results."""
 
        # Extract directory path
        path_str, file_str = os.path.split(result_file) 
         
        ### Create plot per each forecast within result file: W-test results are
        ### plotted on top of T-test results
        
        # Check for existence of T-test result file
        file_pattern = "%s_%s-%s%s" %(cls.filePrefix(),
                                      TStatisticalTest.Type,
                                      EvaluationTest.FilePrefix,
                                      CSEPFile.Extension.XML)
        
        t_test_result_file = glob.glob(os.path.join(path_str,
                                                    file_pattern))

        if len(t_test_result_file) == 0:
            t_test_result_file = glob.glob(os.path.join(path_str,
                                                        "*%s*[1-9]" %file_pattern))
        
        if len(t_test_result_file) == 0:
            error_msg = "%s-test result file is required to generate %s-test plot" %(TStatisticalTest.Type,
                                                                                     WStatisticalTest.Type) 
            WStatisticalTest.__logger.error(error_msg)
            raise RuntimeError, error_msg

        # Get DOM object for the result
        doc = StatisticalTest.plot(result_file)

        # Get rid of internal CSEP 'fromXML' keyword from all model names
        models = [re.sub(CSEP.Forecast.FromXMLPostfix,
                         '',
                         each_name) for each_name in doc.elementValue(EvaluationTest.Result.Name).split()]
     
        num_models = len(models)
        
        # Re-store numpy arrays to represent test results
        w_sign_str = doc.elementValue(WStatisticalTest.__WilcoxonSignificance)
        w_sign = [float(each_val) for each_val in w_sign_str.split()]
        np_w_sign = np.array([w_sign])
        np_w_sign.shape = (num_models, num_models)
        
        # Information gain plot
        plots = TStatisticalTest.plot(t_test_result_file[0],
                                      output_dir,
                                      np_w_sign,
                                      result_file)
        
        return plots
    

