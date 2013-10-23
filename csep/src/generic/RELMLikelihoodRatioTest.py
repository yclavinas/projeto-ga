"""
Module RELMLikelihoodRatioTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import matplotlib, os, scipy.stats
import numpy as np
from pylab import *
from copy import deepcopy

from RELMTest import RELMTest
from Forecast import Forecast
from cseprandom import CSEPRandom
from EvaluationTest import EvaluationTest
from ForecastHandlerFactory import ForecastHandlerFactory
import CSEPGeneric, CSEPLogging, CSEPUtils, CSEPFile


Alpha = 'alpha'
Beta = 'beta'

#--------------------------------------------------------------------------------
#
# RELMTest.
#
# This class is designed to evaluate available models with RELM tests.
#
class RELMLikelihoodRatioTest (RELMTest):

    # Static data

    # Keyword identifying the class
    Type = "R"
    
    # Data structure to store test results    
    class Result (RELMTest.Result):

        # Names of result variables
        LogLikelihoodRatio = 'logLikelihoodRatio'
        LogLikelihoodRatioTrue = 'logLikelihoodRatioTrue'
        SimulationData1 = 'modelSimulationData1' # top-level element for simulation data #1
        SimulationData2 = 'modelSimulationData2' # top-level element for simulation data #2
        
        
        #=======================================================================
        # Initialize results structure and compute result variables (delta1,
        # delta2) for the test
        # 
        # Inputs:
        #   log_likelihood_ratio - Log-likelihood ratio
        #   log_likelihoods_simulations_1 - Log-likelihood for simulations based
        #                                   on 1st model for the test  
        #   log_likelihoods_simulations_2 - Log-likelihood for simulations based
        #                                   on 2nd model for the test  
        #   log_likelihood_modifications - Log-likelihood based on modified
        #                                  catalogs
        #
        def __init__ (self, 
                      log_likelihood_ratio,
                      log_likelihoods_simulations_1,
                      log_likelihoods_simulations_2,
                      log_likelihood_modifications):
            
            # Call base class constructor
            RELMTest.Result.__init__(self, 
                                     log_likelihood_modifications)
            
            # Normalized "true" result
            self[RELMLikelihoodRatioTest.Result.LogLikelihoodRatio] = 0
            # Non-normalized "true" result
            self[RELMLikelihoodRatioTest.Result.LogLikelihoodRatioTrue] = log_likelihood_ratio

            self[RELMLikelihoodRatioTest.Result.SimulationData1] = log_likelihoods_simulations_1
            self[RELMLikelihoodRatioTest.Result.SimulationData2] = log_likelihoods_simulations_2

            # Compute gamma
            self[Alpha] = CSEPUtils.frequencyOfOccurrence(self[RELMLikelihoodRatioTest.Result.LogLikelihoodRatio],
                                                          log_likelihoods_simulations_2.tolist())

            self[Beta] = CSEPUtils.frequencyOfOccurrence(self[RELMLikelihoodRatioTest.Result.LogLikelihoodRatio],
                                                          log_likelihoods_simulations_1.tolist())


        #=======================================================================
        # writeXML
        # 
        # Write test results to XML format file
        #
        # Inputs:
        #         test_name - Name of evaluation test
        #         model_name - List of model filenames for the test
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

            for counter in xrange(1, len(model_file) + 1):
                
                name_node = xml.addElement('modelName%s' %counter,
                                           test_node)
                name_node.text = CSEPFile.Name.extension(model_file[counter-1])

            # Create logLikelihoodRatio element
            log_likelihood_node = xml.addElement(RELMLikelihoodRatioTest.Result.LogLikelihoodRatio,
                                      test_node)
            log_likelihood_node.text = repr(self[RELMLikelihoodRatioTest.Result.LogLikelihoodRatio])

            # Create logLikelihoodTrue (not normalized) element
            log_likelihood_node = xml.addElement(RELMLikelihoodRatioTest.Result.LogLikelihoodRatioTrue,
                                      test_node)
            log_likelihood_node.text = '%.5f' %self[RELMLikelihoodRatioTest.Result.LogLikelihoodRatioTrue]
            
            
            ###  Create top-level simulationData element
            xml_test_name = test_name.replace('-', '')
            simulation_node = xml.addElement(RELMLikelihoodRatioTest.Result.SimulationData1,
                                               test_node)
            simulation_node.attrib[RELMTest.Result.PublicID] = 'smi://local/simulationdata/%s/1/1' %xml_test_name.lower()
            
            ### Create count element for simulationData
            count_node = xml.addElement(RELMTest.Result.SimulationCount,
                                        simulation_node)
            count_node.text = repr(self[RELMLikelihoodRatioTest.Result.SimulationData1].size)
            
            ### Create values element
            values_node = xml.addElement(RELMTest.Result.Simulation,
                                         simulation_node)
            if self[RELMLikelihoodRatioTest.Result.SimulationData1].size != 0:
                values_node.text = ' '.join(repr(i) for i in self[RELMLikelihoodRatioTest.Result.SimulationData1])
            else:
                values_node.text = ' '

            simulation_node = xml.addElement(RELMLikelihoodRatioTest.Result.SimulationData2,
                                               test_node)
            simulation_node.attrib[RELMTest.Result.PublicID] = 'smi://local/simulationdata/%s/1/2' %xml_test_name.lower()
            
            ### Create count element for simulationData
            count_node = xml.addElement(RELMTest.Result.SimulationCount,
                                        simulation_node)
            count_node.text = repr(self[RELMLikelihoodRatioTest.Result.SimulationData2].size)
            
            ### Create values element
            values_node = xml.addElement(RELMTest.Result.Simulation,
                                         simulation_node)
            if self[RELMLikelihoodRatioTest.Result.SimulationData2].size != 0:
                values_node.text = ' '.join(repr(i) for i in self[RELMLikelihoodRatioTest.Result.SimulationData2])
            else:
                values_node.text = ' '
            
            ### Create alpha and beta elements
            node = xml.addElement(Alpha, test_node)
            node.text = '%.3f' %self[Alpha]

            node = xml.addElement(Beta, test_node)
            node.text = '%.3f' %self[Beta]
            
            # write XML format file
            xml.write()


    #===========================================================================
    # Nested class with definitions of XML elements used by the evaluation test.    
    #===========================================================================
    xml = RELMTest.XML('RTest',
                       Result.LogLikelihoodRatio,
                       ['modelName1', 'modelName2'],
                       {Alpha : Result.SimulationData2,
                        Beta : Result.SimulationData1},
                       {Alpha : CSEPUtils.frequencyOfOccurrence,
                        Beta : CSEPUtils.frequencyOfOccurrence},
                        all_models_summary = {Result.LogLikelihoodRatioTrue: None})    
                                       

    #===========================================================================
    # matplotlib settings for the test     
    #===========================================================================
    MatPlotLib = RELMTest.Matplotlib('Log-Likelihood Ratio R',
                                     {Alpha : 'b-o',  # R-test, alpha - blue circles
                                      Beta :'g-s'},  # R-test, beta  - green squares
                                     {Alpha : 'modelName1',
                                      Beta : 'modelName2'}) 

    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    # 
    def __init__ (self, group):
        """ Initialization for RELMLikelihoodRatioTest class."""
        
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

        return RELMLikelihoodRatioTest.Type


    #--------------------------------------------------------------------
    #
    # Compose and invoke Matlab script for the test.
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def evaluate (self, 
                  forecast_name):
        """ Run evaluation test for all possible combinations of the forecast
            with other available forecasts models."""

        test_name = RELMTest.evaluate(self,
                                      forecast_name)

        # Skip all models up to and including the model passed to the script,
        all_models = deepcopy(self.forecasts.files())
        
        while len(all_models) != 0:
                       
            # Pop first element off
            pop_model = all_models.pop(0)
            
            if (forecast_name == pop_model):
                break
        
                  
        # Iterate through remaining models
        for model in all_models:
            
            self.__evaluateModels(forecast_name, 
                                  model,
                                  test_name)
                

    #===========================================================================
    # numberEventsCatalog
    #
    # This method computes the number of events in the catalog.    
    #
    # Input:
    #         forecast1 - numpy.array object which represents forecast #1 data
    #         forecast2 - numpy.array object which represents forecast #2 data    
    #         catalog - numpy.array object which represents catalog data
    #         compute_likelihood - Flag if zero likelihood should be computed.
    #                              If flag is set to True (default), then
    #                              forecast column with computed zero likelihood
    #                              is returned.  
    #         
    # Output: Number of events in catalog
    #
    #===========================================================================
    @classmethod
    def numberEventsCatalog(cls,
                            forecast1,
                            forecast2, 
                            catalog):
        """ Computes the number of events in the catalog."""

        num1 = RELMTest.numberEventsCatalog(forecast1, 
                                            catalog)
        
        num2 = RELMTest.numberEventsCatalog(forecast2, 
                                            catalog)
        
        # Get the number of events
        return (num1 - num2)


    #--------------------------------------------------------------------
    #
    # Invoke evaluation test for the forecast
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def __evaluateModels (self, 
                          forecast_name1,
                          forecast_name2,
                          test_name):
        """ Invoke evaluation test for two specified forecasts."""


        models_list = [forecast_name1,
                       forecast_name2]
        
        CSEPLogging.CSEPLogging.getLogger(RELMLikelihoodRatioTest.__name__).info('%s for %s'
                                                                                 %(test_name,
                                                                                   models_list))

        forecast_path1 = os.path.join(self.forecasts.dir(), 
                                      forecast_name1)
        forecast_path2 = os.path.join(self.forecasts.dir(), 
                                      forecast_name2)

        
        # Scale forecast #1 taking into account weights of forecast #2
        forecast2_mask = ForecastHandlerFactory().CurrentHandler.load(forecast_path2)
        
        (scaled_forecast1, covers_area_forecast1) = RELMTest.prepareForecast(self,
                                                                             forecast_path1,
                                                                             forecast2_mask[:, CSEPGeneric.Forecast.Format.MaskBit])

        forecast1_mask = ForecastHandlerFactory().CurrentHandler.load(forecast_path1)
        
        (scaled_forecast2, covers_area_forecast2) = RELMTest.prepareForecast(self,
                                                                             forecast_path2,
                                                                             forecast1_mask[:, CSEPGeneric.Forecast.Format.MaskBit])

        # Top-level directory to store random number seed for each simulation
        test_random = RELMTest.randomSeedDir(self,
                                             models_list)
        
        # Invoke N-test
        test_result = self._invoke(scaled_forecast1,
                                   scaled_forecast2, 
                                   test_random)
        
        
        # Write results to the file
        test_result.writeXML(test_name, 
                             models_list,
                             self.testDir,
                             self.filePrefix())                      


    #---------------------------------------------------------------------------
    #
    # Run R-test for the forecasts
    #
    # Input: 
    #        forecast1 - numpy.array object that represents forecast #1 data
    #        forecast2 - numpy.array object that represents forecast #2 data    
    #        test_random_file_prefix - Full path to the file prefix used to store
    #                                  random seed value used by each simulation.
    #                                  Simulation count and file extension are
    #                                  appended to this prefix by each iteration
    #
    def _invoke (self, 
                 forecast1,
                 forecast2,
                 test_random_file_prefix):
        """Computation of the R-test for the RELM framework."""
 

        # Pre-compute the log-likelihood for zero events per bin and 
        # add to the forecast model
        forecast1[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood] = CSEPUtils.logPoissonPDF(np.zeros_like(forecast1[:,CSEPGeneric.Forecast.Format.Rate]), 
                                                                                          forecast1[:,CSEPGeneric.Forecast.Format.Rate])
        forecast2[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood] = CSEPUtils.logPoissonPDF(np.zeros_like(forecast2[:,CSEPGeneric.Forecast.Format.Rate]), 
                                                                                          forecast2[:,CSEPGeneric.Forecast.Format.Rate])

        
        #CSEPLogging.CSEPLogging.getLogger(__name__).info('ZeroLikelihood index=%s' %log_likelihood)

        # Compute the "true" result
        # Log-likelihood of the forecast given the observation
        log_likelihood_ratio = RELMLikelihoodRatioTest.numberEventsCatalog(forecast1, 
                                                                           forecast2, 
                                                                           self.catalogFile.npObject)

        ### Compute the "results" of the modifications
        # Number of modified catalogs
        num_modifications = 0
        if self.catalogModificationsFile.npObject is not None:
            num_rows, num_modifications = self.catalogModificationsFile.npObject.shape
        
        # Compute the number of events in each modified catalog
        log_likelihood_ratio_modifications = np.zeros(num_modifications)
        
        for index in xrange(0, num_modifications):
           log_likelihood_ratio_modifications[index] = RELMLikelihoodRatioTest.numberEventsCatalog(forecast1,
                                                                                                   forecast2,
                                                                                                   self.catalogModificationsFile.npObject[0, index]) - \
                                                       log_likelihood_ratio
        

        # Compute the "results" of the simulations
        log_likelihoods_simulations1 = np.zeros(EvaluationTest.NumberSimulations)
        log_likelihoods_simulations2 = np.zeros(EvaluationTest.NumberSimulations)        

        for index in xrange(EvaluationTest.NumberSimulations):
        
            # Compute the simulated number of events and sum them up
            ### ATTN: use (index+1) to format filename for random seed file 
            ###       to preserve Matlab's convention for the filename:
            ###       indexes start from 1

            sim_forecast = 1
            log_likelihoods_simulations2[index] = RELMLikelihoodRatioTest.__simulation(forecast1,
                                                                                       forecast2,
                                                                                       sim_forecast, 
                                                                                       index + 1,
                                                                                       test_random_file_prefix) - \
                                                 log_likelihood_ratio

            sim_forecast = 2
            log_likelihoods_simulations1[index] = -1.0 * RELMLikelihoodRatioTest.__simulation(forecast1,
                                                                                              forecast2,
                                                                                              sim_forecast, 
                                                                                              index + 1,
                                                                                              test_random_file_prefix) + \
                                                 log_likelihood_ratio
        
    
        # Compute Delta's and store the important parameters
        result = RELMLikelihoodRatioTest.Result(log_likelihood_ratio,
                                                log_likelihoods_simulations1,
                                                log_likelihoods_simulations2,
                                                log_likelihood_ratio_modifications)

        return result


    #===========================================================================
    # Compute simulation results
    #
    # Inputs:
    #         forecast1 - numpy.array object that represents forecast #1 data
    #         forecast2 - numpy.array object that represents forecast #2 data
    #         sim_forecast - Simulation forecast
    #         index - Simulation index
    #         test_random_file_prefix - Full path to the file prefix used to store
    #                                   random seed value used by each simulation.
    #                                   Simulation count and file extension are
    #                                   appended to this prefix by each iteration
    # 
    # Output:
    #         Likelihood ratio
    #===========================================================================
    @staticmethod
    def __simulation(forecast1,
                     forecast2,
                     sim_forecast, 
                     sim_index,
                     test_random_file_prefix):
        """ Compute simulation results"""

        # Delete any observation in forecast
        forecast1[:, CSEPGeneric.Forecast.Format.Observations] = 0
        forecast2[:, CSEPGeneric.Forecast.Format.Observations] = 0        

        # Create filename for simulation random seed file
        iteration = 1
        forecast = forecast1
        if sim_forecast == 2:
            iteration = 3
            forecast = forecast2

        total_forecast_rate = forecast[:, CSEPGeneric.Forecast.Format.Rate].sum()
            
        seed_file = RELMTest.randomSeedFile(test_random_file_prefix,
                                            sim_index, 
                                            iteration)
    
        # Random numbers used by simulations
        generator = CSEPRandom(seed_file)
        num = 1 # Number of random numbers to generate
        number_events = int(scipy.stats.poisson.ppf(generator.createNumbers(num)[0], 
                                                    total_forecast_rate))
    
        # Create filename for simulation random seed file
        iteration += 1
        seed_file = RELMTest.randomSeedFile(test_random_file_prefix,
                                            sim_index, 
                                            iteration)
        
        # Random numbers used by simulations
        generator = CSEPRandom(seed_file)
        random_numbers = np.array(generator.createNumbers(number_events))
        
        rates_CDF = np.cumsum(forecast[:, CSEPGeneric.Forecast.Format.Rate]/total_forecast_rate)

        # Create a deep copy of pre-computed log-likelihood to avoid modifying 
        # the vector between simulations
        log_likelihood1 = forecast1[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood].copy()
        log_likelihood2 = forecast2[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood].copy()        
        
        for index in xrange(number_events):
             
             # Check if any indices exist: length of returned tuple
             indices = np.nonzero(rates_CDF > random_numbers[index])
             if len(indices):
                 found_index = indices[0].min()
                 
                 bin_of_interest = forecast[found_index,:]
                 
                 RELMLikelihoodRatioTest.__updateSimulationBin(forecast1,
                                                               bin_of_interest,
                                                               log_likelihood1)

                 RELMLikelihoodRatioTest.__updateSimulationBin(forecast2,
                                                               bin_of_interest,
                                                               log_likelihood2)

        # Return likelihood
        return np.nansum(log_likelihood1) - np.nansum(log_likelihood2) 


    #===========================================================================
    # Update forecast's observed events and log-likelihood with simulated event 
    #===========================================================================
    @staticmethod
    def __updateSimulationBin(forecast,
                              bin_of_interest,
                              log_likelihood):
         """ Update forecast's observed events and log-likelihood with 
            simulated event"""


         select = (forecast[:, CSEPGeneric.Forecast.Format.MinLongitude] == \
                   bin_of_interest[CSEPGeneric.Forecast.Format.MinLongitude])
         total_select = (forecast[:, CSEPGeneric.Forecast.Format.MinLatitude] == \
                         bin_of_interest[CSEPGeneric.Forecast.Format.MinLatitude])
         total_select = np.logical_and(total_select, select)

         select = (forecast[:, CSEPGeneric.Forecast.Format.DepthTop] == \
                   bin_of_interest[CSEPGeneric.Forecast.Format.DepthTop])
         total_select = np.logical_and(total_select, select)
                          
         select = (forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] == \
                   bin_of_interest[CSEPGeneric.Forecast.Format.MinMagnitude])
         total_select = np.logical_and(total_select, select)
         
         # Tuple of indices
         indices = total_select.nonzero()

         if len(indices):
             found_index = indices[0]

             forecast[found_index, CSEPGeneric.Forecast.Format.Observations] += 1
          
             observations = forecast[found_index, CSEPGeneric.Forecast.Format.Observations]
             rate = forecast[found_index, CSEPGeneric.Forecast.Format.Rate]
             
             log_likelihood[found_index] = CSEPUtils.logPoissonPDF(observations, 
                                                                   rate)
        

    #----------------------------------------------------------------------------
    #
    # This method plots result data of RELM R evaluation test.
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

        dom, ax = EvaluationTest.plot(result_file) 

        # Plot data specific to the test, and set up the labels
        observed_x_axes = cls.__plotData(dom)

        # Return image filename
        __legend_ncols = 2
        return RELMTest._finishPlot(cls.MatPlotLib.XLabel, 
                                    observed_x_axes,
                                    result_file,
                                    output_dir,
                                    __legend_ncols)


    #-----------------------------------------------------------------------------
    #
    # __plotData
    # 
    # This method plots result data of RELM R evaluation test.
    #
    # Input: 
    #         doc - DOM element representing root element of test results.
    #
    # Output: None.
    # 
    @classmethod
    def __plotData(cls, doc):
        """ Plot data of RELM R evaluation test."""

        logger = CSEPLogging.CSEPLogging.getLogger(__name__)


        # Extract names of forecasts models
        names = []
        abscissas = []
        data_count = int(doc.elementValue("simulationCount"))

        # Fix for Trac ticket #125: forecast #1 corresponds to simulationData2,
        # and forecast #2 corresponds to simulationData1:
        # iterate through resultVariable<->modelName dictionary
        for var, var_model in cls.MatPlotLib.ResultVarModel.iteritems():
     
            name = doc.elementValue(var_model)
            names.append(name)

            # Simulation vector for the variable
            data_array = doc.elementValue("simulation", 
                                          cls.xml.TestVars[var]).split()
            node_abscissa = sorted(map(float, data_array))

            # Check consistensy of metadata about simulation vector
            if (len(node_abscissa) != data_count):
               error_msg = "%s: %s - metadata vs. data vector length mismatch in simulation for %s (got %s, expected %s)" \
                           %(CSEPLogging.CSEPLogging.frame(cls), 
                             names, 
                             cls.xml.TestVars[var],
                             len(node_abscissa), data_count)
               logger.error(error_msg)
             
               raise RuntimeError, error_msg

            abscissas.append(node_abscissa)
        

        step = 1.0 / float(data_count)
        ordinate = np.linspace(step, 1.0, num=data_count)

        # Plot modification data if present
        name = '/'.join(names)
        RELMTest._plotModificationData(doc, name)
      
        # True event count for the test
        observed = float(doc.elementValue(cls.xml.TrueEvent))
      
        # plot observed log-likelihood ratio
        axvline(observed, 
                color=RELMTest.Matplotlib._plotObserved['color'], 
                linewidth=RELMTest.Matplotlib._plotObserved['linewidth'], 
                zorder=EvaluationTest.Matplotlib.plotZOrder['vertical'], 
                label='_nolegend_' )

        # plot the two R test curves
        for index, each_abscissa in enumerate(abscissas):
            plot(each_abscissa, 
                 ordinate, 
                 color=RELMTest.Matplotlib._plotCurve['colors'][index], 
                 linestyle=RELMTest.Matplotlib._plotCurve['linestyle'][2], 
                 zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
                 label=names[index])
        

        # set x and y dimension of plot
        ylim(RELMTest.Matplotlib._plotAxes['ymin'],  
             RELMTest.Matplotlib._plotAxes['ymax'])
        xmin, xmax = xlim()

        # get x axes coords of observed, required to split rejection bar
        observed_x_axes = ( observed - xmin ) / ( xmax - xmin )

        return observed_x_axes
 
