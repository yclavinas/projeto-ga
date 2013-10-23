"""
Module RELMLikelihoodTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import matplotlib, scipy.stats, os, re
import numpy as np
from pylab import *

from RELMTest import RELMTest
from Forecast import Forecast
from EvaluationTest import EvaluationTest
import CSEPLogging, CSEPUtils, CSEP, CSEPGeneric


Xi = 'xi'

#--------------------------------------------------------------------------------
#
# RELMLikelihoodTest.
#
# This class represents RELM L (log likelihood) evaluation test for forecasts models.
#
class RELMConditionalLikelihoodTest (RELMTest):

    # Static data

    # Keyword identifying the class
    Type = "CL"
    
    
    # Data structure to store test results    
    class Result (RELMTest.Result):

        # Names of result variables
        LogLikelihood = 'logLikelihood'  
        
        
        #=======================================================================
        # Initialize results structure and compute result variables (delta1,
        # delta2) for the test
        # 
        # Inputs:
        #   log_likelihood - Log-likelihood
        #   log_likelihoods_simulations - Log-likelihood for simulations
        #   log_likelihood_modifications - Log-likelihood based on modified
        #                                  catalogs
        #   event_likelihood - Vector of true likelihoods per each observed event
        #
        def __init__ (self, 
                      log_likelihood,
                      log_likelihoods_simulations,
                      log_likelihood_modifications,
                      event_likelihood):
            
            # Call base class constructor
            RELMTest.Result.__init__(self, 
                                     log_likelihood_modifications,
                                     log_likelihoods_simulations,
                                     event_likelihood,
                                     log_likelihood)
            
            # Normalized (by logLikelihoodSum) "true" result - always set to zero
            self[RELMConditionalLikelihoodTest.Result.LogLikelihood] = 0

            # Compute gamma
            self[Xi] = CSEPUtils.frequencyOfOccurrence(self[RELMConditionalLikelihoodTest.Result.LogLikelihood],
                                                       log_likelihoods_simulations.tolist())


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
        #         np_catalog - numpy.array representing observation catalog for
        #                      the test  
        #         forecast_covers_area - Flag if forecast covers the whole testing
        #                                area. If True, sum of true log-likelihoods
        #                                is a valid measure, if False - sum of true
        #                                log-likelihoods is not a valid measure for
        #                                for the test 
        #=======================================================================
        def writeXML (self, 
                      test_name, 
                      model_file, 
                      dir_path, 
                      file_prefix,
                      np_catalog,
                      forecast_covers_area):
            """Write test results to XML format file"""

            test_node, xml = RELMTest.Result.writeXML(self, 
                                                      test_name, 
                                                      model_file,
                                                      dir_path,
                                                      file_prefix,
                                                      np_catalog,
                                                      forecast_covers_area)

            # Create logLikelihood element
            log_likelihood_node = xml.addElement(RELMConditionalLikelihoodTest.Result.LogLikelihood,
                                                 test_node)
            log_likelihood_node.text = repr(self[RELMConditionalLikelihoodTest.Result.LogLikelihood])

            ### Create gamma elements
            xi_node = xml.addElement(Xi,
                                     test_node)
            xi_node.text = '%.3f' %self[Xi]
            
            # write XML format file
            xml.write()

    
    
    #===========================================================================
    # Definitions of XML elements used by the evaluation test.    
    #===========================================================================
    xml = RELMTest.XML('CLTest', 
                       Result.LogLikelihood,
                       [RELMTest.Result.Name],
                       {Xi : RELMTest.Result.SimulationData},
                       {Xi : CSEPUtils.frequencyOfOccurrence},
                       all_models_summary = {RELMTest.Result.LogLikelihoodTrue: None,
                                             RELMTest.Result.Simulation : None})
    

    #===========================================================================
    # matplotlib settings for the test     
    #===========================================================================
    MatPlotLib = RELMTest.Matplotlib('Log-Likelihood L',
                                     {Xi : 'k-o'},
                                     {Xi : RELMTest.Result.Name},
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
        """ Initialization for RELMConditionalLikelihoodTest class."""
        
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

        return RELMConditionalLikelihoodTest.Type


    #----------------------------------------------------------------------------
    #
    # Create plot of evaluation test summary for all participating model of 
    # the forecast group. This method plots true logL as computed by the test
    # with [2.5; 97.5]% uncertainty interval based on test simulations. 
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
        """ Create a plot of true logLikelihood within [2.5; 97.5]% confidence
            bounds for all models as specified by summary file."""
            
        return RELMTest.Result.plotAllModelsSummary(cls,
                                                    summary_path,
                                                    output_dir)
    

    #----------------------------------------------------------------------------
    #
    # This method plots result data of RELM L evaluation test.
    #
    # Input: 
    #         observed - Observed number of events for the test.
    #         output_dir - Directory to place plot file to. Default is None.     
    #
    @classmethod
    def plot (cls, 
              result_file, 
              output_dir = None):
        """ Plot test results in XML format."""

        dom, ax = EvaluationTest.plot(result_file) 

        # Plot data specific to the test, and set up the labels
        observed_x_axes = cls.__plotData(dom)

        # Return image filename
        return RELMTest._finishPlot(cls.MatPlotLib.XLabel, 
                                    observed_x_axes,
                                    result_file,
                                    output_dir)


    #-----------------------------------------------------------------------------
    #
    # __plotData
    # 
    # This method plots result data of RELM L evaluation test.
    #
    # Input: 
    #         doc - DOM element representing root element of test results.
    #
    # Output: None.
    # 
    @classmethod
    def __plotData(cls, doc):
        """ Plot data of RELM L evaluation test."""

        name = doc.elementValue(cls.xml.ModelName[0])
        name = re.sub(CSEP.Forecast.FromXMLPostfix,
                      '',
                      name)
        
        data_count = int(doc.elementValue("simulationCount"))

        data_str = doc.elementValue("simulation")
        data_array = data_str.split()
        abscissa = sorted(map(float, data_array))
         
        if (len(abscissa) != data_count):
            error_msg = "%s: %s - data vector length mismatch" %(CSEPLogging.CSEPLogging.frame(cls),
                                                                 name)
            CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
             
            raise RuntimeError, error_msg
     
        step = 1.0 / float(data_count)
        ordinate = np.linspace(step, 1.0, num=data_count)

        # Plot modification data if present
        RELMTest._plotModificationData(doc, name)
     
        # True event count for the test
        observed = float(doc.elementValue(cls.xml.TrueEvent))
 
        # plot observed log-likelihood
        axvline (observed, 
                 color=RELMTest.Matplotlib._plotObserved['color'], 
                 linewidth=RELMTest.Matplotlib._plotObserved['linewidth'],
                 zorder=EvaluationTest.Matplotlib.plotZOrder['vertical'], 
                 label='_nolegend_' )

        # plot L test curve
        plot (abscissa, 
              ordinate, 
              color=RELMTest.Matplotlib._plotCurve['colors'][0], 
              linestyle=RELMTest.Matplotlib._plotCurve['linestyle'][1], 
              zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
              label=name )

        # set x and y dimension of plot
        ylim(RELMTest.Matplotlib._plotAxes['ymin'], 
             RELMTest.Matplotlib._plotAxes['ymax'])
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
        
        # Scaled to the test date forecast and flag if forecast covers the whole
        # testing area
        (scaled_forecast, forecast_covers_area) = RELMTest.prepareForecast(self,
                                                                           forecast_path)

        # Top-level directory to store random number seed for each simulation
        test_random = RELMTest.randomSeedDir(self,
                                             forecast_name)
        
        # Invoke N-test
        test_result = self.__invoke(scaled_forecast, 
                                    test_random)
        
        # Write results to the file
        test_result.writeXML(test_name, 
                             forecast_name,
                             self.testDir,
                             self.filePrefix(),
                             self.catalogFile.npObject,
                             forecast_covers_area)                      
        

    #---------------------------------------------------------------------------
    #
    # Run L-test for the forecast
    #
    # Input: 
    #        forecast - numpy.array object that represents forecast data
    #        test_random_file_prefix - Full path to the file prefix used to store
    #                                  random seed value used by each simulation.
    #                                  Simulation count and file extension are
    #                                  appended to this prefix by each iteration
    #        covers_area - Flag set to True if forecast covers the whole testing
    #                      area, False otherwise.
    #
    def __invoke (self, 
                  forecast,
                  test_random_file_prefix):
        """Computation of the L-test for the RELM framework."""
 

        # Pre-compute the log-likelihood for zero events per bin and 
        # add to the forecast model
        forecast_rate = forecast[:,CSEPGeneric.Forecast.Format.Rate].astype(np.float)
        forecast[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood] = CSEPUtils.logPoissonPDF(np.zeros_like(forecast_rate), 
                                                                                              forecast_rate)
        
        #CSEPLogging.CSEPLogging.getLogger(__name__).info('ZeroLikelihood index=%s' %log_likelihood)

        # Column to represent log-likelihood per each event 
        np_true_likelihood = np.array([np.nan] * self.catalogFile.npObject.shape[0]) 
                                             
        
        # Compute the "true" result
        # Log-likelihood of the forecast given the observation
        log_likelihood = RELMTest.numberEventsCatalog(forecast, 
                                                      self.catalogFile.npObject,
                                                      true_likelihood = np_true_likelihood)

        __likelihood = False
        number_quakes_observed = RELMTest.numberEventsCatalog(forecast, 
                                                              self.catalogFile.npObject,
                                                              __likelihood)

        ### Compute the "results" of the modifications
        # Number of modified catalogs
        num_modifications = 0
        if self.catalogModificationsFile.npObject is not None:
            num_rows, num_modifications = self.catalogModificationsFile.npObject.shape
        
        # Compute the number of events in each modified catalog
        log_likelihood_modifications = np.zeros(num_modifications)
        
        for index in xrange(0, num_modifications):
           log_likelihood_modifications[index] = RELMTest.numberEventsCatalog(forecast,
                                                                              self.catalogModificationsFile.npObject[0, index]) - \
                                                 log_likelihood
    
        
        # Compute the "results" of the simulations
        log_likelihoods_simulations = np.zeros(EvaluationTest.NumberSimulations)

        for index in xrange(EvaluationTest.NumberSimulations):
        
            # Compute the simulated number of events and sum them up
            ### ATTN: use (index+1) to format filename for random seed file 
            ###       to preserve Matlab's convention for the filename:
            ###       indexes start from 1

            log_likelihoods_simulations[index] = RELMTest._simulation(forecast, 
                                                                      index + 1,
                                                                      test_random_file_prefix,
                                                                      number_quakes_observed) - \
                                                 log_likelihood

        
    
        # Compute Delta's and store the important parameters
        result = RELMConditionalLikelihoodTest.Result(log_likelihood,
                                                      log_likelihoods_simulations,
                                                      log_likelihood_modifications,
                                                      np_true_likelihood)

        return result

