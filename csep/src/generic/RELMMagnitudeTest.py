"""
Module RELMMagnitudeTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import matplotlib, os, re
import numpy as np
from pylab import *

from RELMTest import RELMTest
from Forecast import Forecast
from EvaluationTest import EvaluationTest
from ForecastHandlerFactory import ForecastHandlerFactory
import CSEPLogging, CSEPUtils, CSEP, CSEPGeneric

Kappa = 'kappa'


#--------------------------------------------------------------------------------
#
# RELMMagnitudeTest.
#
# This class represents RELM M (magnitude) evaluation test for forecasts models.
#
class RELMMagnitudeTest (RELMTest):

    # Static data

    # Keyword identifying the class
    Type = "M"
    

    # Data structure to store test results    
    class Result (RELMTest.Result):

        # Names of result variables
        LogLikelihood = 'logLikelihood'
        
        #=======================================================================
        # Initialize results structure and compute result variables (kappa)
        # for the test
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
            
            # Normalized "true" result
            self[RELMMagnitudeTest.Result.LogLikelihood] = 0

            # Compute gamma
            self[Kappa] = CSEPUtils.frequencyOfOccurrence(self[RELMMagnitudeTest.Result.LogLikelihood],
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
            log_likelihood_node = xml.addElement(RELMMagnitudeTest.Result.LogLikelihood,
                                      test_node)
            log_likelihood_node.text = repr(self[RELMMagnitudeTest.Result.LogLikelihood])

            ### Create kappa elements
            kappa_node = xml.addElement(Kappa,
                                        test_node)
            kappa_node.text = '%.3f' %self[Kappa]
            
            # write XML format file
            xml.write()

    
    #===========================================================================
    # Definitions of XML elements used by the evaluation test.    
    #===========================================================================
    xml = RELMTest.XML('MTest',
                       Result.LogLikelihood,
                       [RELMTest.Result.Name],
                       {Kappa : RELMTest.Result.SimulationData},
                       {Kappa : CSEPUtils.frequencyOfOccurrence},
                       all_models_summary = {RELMTest.Result.LogLikelihoodTrue: None,
                                             RELMTest.Result.Simulation : None})
    
    #===========================================================================
    # matplotlib settings for the test     
    #===========================================================================
    MatPlotLib = RELMTest.Matplotlib('Log-Likelihood M',
                                     {Kappa : 'k-o'},
                                     {Kappa : RELMTest.Result.Name},
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
        """ Initialization for RELMMagnitudeTest class."""
        
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

        return RELMMagnitudeTest.Type


    #--------------------------------------------------------------------
    #
    # Invoke evaluation test for the forecast
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def evaluate (self, 
                  forecast_name):
        """ Computation of the M-test for the RELM framework.  For this computation,
we re-normalize the forecast so that the total number of forecasted events
matches the total number of observed events, then we conduct the L-test
with the normalized forecast, considering only the distribution in 
magnitude space.  This means that all simulated catalogs should also 
have a fixed number of events rather than having Poisson distribution in 
the number of events.  For this functionality, we can use Schorlemmer's 
implementation of converting the forecast to an ECDF and then dropping 
events in."""

        test_name = RELMTest.evaluate(self,
                                      forecast_name)

        forecast_path = os.path.join(self.forecasts.dir(), 
                                     forecast_name)
        
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
                             self.catalogFile.intermediateObj,
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
    #
    def __invoke (self, 
                  forecast,
                  test_random_file_prefix):
        """Computation of the M-test for the RELM framework."""
 

        #----------------------------------------------------------------------- 
        # Reduce the forecast to a magnitude forecast only, by finding the unique
        # magnitude cells and summing the rates over the constituent bins
        # Find the number of unique magnitude cells
        # From numpy-discussion:
        # np.unique1d(a.view([('',a.dtype)]*a.shape[1])).view(a.dtype).reshape(-1,a.shape[1])
        # ATTN: had to create a deep copy of the magnitude cells, otherwise
        # view on view does not work!!!
        magn_cells = forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude:(CSEPGeneric.Forecast.Format.MaxMagnitude+1)].copy()
        num_cols = magn_cells.shape[1]        
        unique_magn_cells = np.unique(magn_cells.view([('',magn_cells.dtype)]*num_cols)).view(magn_cells.dtype).reshape(-1,num_cols)
                                      
        # Find the number of unique magnitude cells
        num_unique_magn_cells = unique_magn_cells.shape[0]
        
        # Make enough room for each magnitude cell
        magnitude_forecast = np.zeros((num_unique_magn_cells, 
                                       forecast.shape[1]))
        
        # Set the min/max magnitude for each cell
        magnitude_forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude:(CSEPGeneric.Forecast.Format.MaxMagnitude+1)] = unique_magn_cells
        magnitude_forecast[:, CSEPGeneric.Forecast.Format.MaskBit] = 1
        
        # Set the rate in each magnitude cell by summing over the relevant bins , set
        # the min/max lat/lon/depth for this cell
        for index in xrange(num_unique_magn_cells):
            # Find the bins that cover this cell
            sel_rows, = np.where(forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] == magnitude_forecast[index, 
                                                                                                 CSEPGeneric.Forecast.Format.MinMagnitude])
            selection = forecast[sel_rows, :]
            sel_rows, = np.where(selection[:, CSEPGeneric.Forecast.Format.MaxMagnitude] == magnitude_forecast[index, 
                                                                                                  CSEPGeneric.Forecast.Format.MaxMagnitude])
            selection = selection[sel_rows, :]

            # The magnitude rate is the sum over all constituent bins
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.Rate] = selection[:, CSEPGeneric.Forecast.Format.Rate].sum()
            
            # The min/max depth/lat/lon for this new bin should be set to the min/max
            # depth/mag over all the bins in this spatial cell
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.MinLongitude] = selection[:, 
                                                                                CSEPGeneric.Forecast.Format.MinLongitude].min()
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.MaxLongitude] = selection[:, 
                                                                                CSEPGeneric.Forecast.Format.MaxLongitude].max()
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.MinLatitude] = selection[:, 
                                                                               CSEPGeneric.Forecast.Format.MinLatitude].min()
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.MaxLatitude] = selection[:, 
                                                                               CSEPGeneric.Forecast.Format.MaxLatitude].max()    
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.DepthTop] = selection[:, 
                                                                            CSEPGeneric.Forecast.Format.DepthTop].min()
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.DepthBottom] = selection[:, 
                                                                               CSEPGeneric.Forecast.Format.DepthBottom].max()

        #print "Magn_forecast", magnitude_forecast


        # Normalize the forecast rates so that the total number of forecast events
        # matches the total number of observed events.  To do this, we divide each
        # rate by the total number of forecast events, then multiply each rate by
        # the total number of observed events.
        # Number of events in the observed catalog: don't compute likelihood
        __likelihood = False
        
        # Reduce catalog to masked forecast - only for M and S tests
        self.catalogFile.intermediateObj = RELMTest.filterObservations(forecast,
                                                                       self.catalogFile.npObject)
        
        number_quakes_observed = RELMTest.numberEventsCatalog(forecast, 
                                                              self.catalogFile.intermediateObj,
                                                              __likelihood)
        
        number_quakes_forecast = ForecastHandlerFactory().CurrentHandler.numberEvents(magnitude_forecast[:, CSEPGeneric.Forecast.Format.Rate])
        
        norm_forecast = magnitude_forecast.copy()
        norm_forecast[:, CSEPGeneric.Forecast.Format.Rate] /= (number_quakes_forecast/number_quakes_observed)
        
        # Pre-compute the log-likelihood for zero events per bin and add to the forecast model
        norm_forecast[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood] = CSEPUtils.logPoissonPDF(np.zeros_like(norm_forecast[:,CSEPGeneric.Forecast.Format.Rate]),
                                                                                              norm_forecast[:, CSEPGeneric.Forecast.Format.Rate]) 
        
        # Column to represent log-likelihood per each event 
        np_true_likelihood = np.array([np.nan] * self.catalogFile.intermediateObj.shape[0]) 
        
        # Compute the "true" result
        # Log-likelihood of the normalized forecast given the observation
        log_likelihood = RELMTest.numberEventsCatalog(norm_forecast, 
                                                      self.catalogFile.intermediateObj,
                                                      true_likelihood = np_true_likelihood)
        
        ### Compute the "results" of the modifications
        # Number of modified catalogs
        num_modifications = 0
        if self.catalogModificationsFile.npObject is not None:
            num_rows, num_modifications = self.catalogModificationsFile.npObject.shape
        
        # Compute the number of events in each modified catalog
        log_likelihood_modifications = np.zeros(num_modifications)

        for index in xrange(num_modifications):
            # Modified catalog, filtered by forecast's masking bit 
            mod_catalog = RELMTest.filterObservations(forecast,
                                                      self.catalogModificationsFile.npObject[0, index])
            
            # We want to renormalize the forecast so that the total number of
            # events forecast matches the total number of events in the
            # modification of interest
            temp_numberQuakesObserved = RELMTest.numberEventsCatalog(forecast, 
                                                                     mod_catalog, 
                                                                     __likelihood)
            temp_norm_forecast = magnitude_forecast.copy()
            temp_norm_forecast[:, CSEPGeneric.Forecast.Format.Rate] /= (number_quakes_forecast / temp_numberQuakesObserved)   
        
            # Pre-compute the log-likelihood for zero events per bin and add to the forecast model
            temp_norm_forecast[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood] = CSEPUtils.logPoissonPDF(np.zeros_like(temp_norm_forecast[:,CSEPGeneric.Forecast.Format.Rate]),
                                                                                                       temp_norm_forecast[:, CSEPGeneric.Forecast.Format.Rate]) 
        
            log_likelihood_modifications[index]  = RELMTest.numberEventsCatalog(temp_norm_forecast,
                                                                                mod_catalog) - log_likelihood

            # Free up temporary forecast memory
            del temp_norm_forecast
            
        
        # Compute the "results" of the simulations
        log_likelihoods_simulations = np.zeros(EvaluationTest.NumberSimulations)

        for index in xrange(EvaluationTest.NumberSimulations):
        
            # Compute the simulated number of events and sum them up
            ### ATTN: use (index+1) to format filename for random seed file 
            ###       to preserve Matlab's convention for the filename:
            ###       indexes start from 1
            log_likelihoods_simulations[index] = RELMTest._simulation(norm_forecast, 
                                                                      index + 1,
                                                                      test_random_file_prefix,
                                                                      number_quakes_observed) - \
                                                 log_likelihood

        
    
        # Compute Delta's and store the important parameters
        result = RELMMagnitudeTest.Result(log_likelihood,
                                          log_likelihoods_simulations,
                                          log_likelihood_modifications,
                                          np_true_likelihood)

        return result


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
    # This method plots result data of RELM S evaluation test.
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
    # This method plots result data of RELM M evaluation test.
    #
    # Input: 
    #         doc - DOM element representing root element of test results.
    #
    # Output: None.
    # 
    @classmethod
    def __plotData(cls, doc):
        """ Plot data of RELM M evaluation test."""


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


