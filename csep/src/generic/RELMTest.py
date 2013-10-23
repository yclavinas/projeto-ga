"""
Module RELMTest
"""

__version__ = "$Revision: 4150 $"
__revision__ = "$Id: RELMTest.py 4150 2012-12-19 03:08:43Z liukis $"


import os, shutil, glob, datetime, scipy.stats, re, matplotlib
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.dates import MO, YearLocator, MonthLocator, DayLocator, \
                             WeekdayLocator, DateFormatter

import CSEP, Environment, CSEPPropertyFile, CSEPLogging, \
       CSEPGeneric, CSEPFile, CSEPInitFile, CSEPUtils
from EvaluationTest import EvaluationTest
from Forecast import Forecast
from RELMCatalog import RELMCatalog
from ResultsSummary import ResultsSummary
from ResultsCumulativeSummary import ResultsCumulativeSummary
from ResultsSummaryFactory import ResultsSummaryFactory
from ForecastHandlerFactory import ForecastHandlerFactory     
from cseprandom import CSEPRandom


#--------------------------------------------------------------------------------
#
# RELMTest.
#
# This class is designed to evaluate available models with RELM tests.
#
class RELMTest (EvaluationTest):

    #===========================================================================
    # Nested class that represents RELMTest result data as dictionary type.
    # Derived classes should derive from the class to provide specifics of the
    # test results.    
    #===========================================================================
    class Result (EvaluationTest.Result):
        
        # Names of results variables
        ModificationData = 'modificationData'
        ModificationCount = 'modificationCount'
        Modification = 'modification'
        
        SimulationData = 'simulationData' # top-level element for simulation data
        Simulation = 'simulation'
        SimulationCount = 'simulationCount'

        # True log-likelihood elements and attributes
        LogLikelihoodTrue = 'logLikelihoodTrue'
        LogLikelihoodSumAttribute = 'sum'
        LogLikelihoodSumIsValidAttribute = 'sumIsValid'
        LogLikelihoodEvent = 'event'
        EventLongitude = 'longitude'
        EventLatitude = 'latitude'
        EventDate = 'date'
        EventMagnitude = 'magnitude'
        EventDepth = 'depth'
        
        # Names of attributes
        PublicID = 'publicID'
        
        
        def __init__ (self,
                      modification_events,
                      simulation_data = None,
                      event_likelihood = None,
                      sum_log_likelihood = None):
            """ Initialize method for RELMTest.Result object"""
            
            EvaluationTest.Result.__init__(self)

            num = 0
            if modification_events.ndim != 0:
                num, = modification_events.shape
                
            self[RELMTest.Result.ModificationCount] = num
            self[RELMTest.Result.Modification] = modification_events
            
            if simulation_data is not None:
                self[RELMTest.Result.Simulation] = simulation_data
                self[RELMTest.Result.SimulationCount] = simulation_data.size

            if event_likelihood is not None:

                # "True" logL per each observed event (per each forecast bin)
                self[RELMTest.Result.LogLikelihoodTrue] = event_likelihood

                # Non-normalized "true" result (sum of logL for all observed events)
                self[RELMTest.Result.LogLikelihoodSumAttribute] = sum_log_likelihood

        
        #=======================================================================
        # Generate confidence interval for given vector of simulations
        #
        # Inputs: 
        #         simulations - String representation of the simulation vector
        #         norm_factor - Normalization factor that was applied to the
        #                       simulation vector. If normalization value is 
        #                       provided, add it to the simulation vector to 
        #                       "de-normalize" it. Default is None.
        #
        # Outputs:
        #         list of lower and upper range values
        #=======================================================================
        @staticmethod
        def confidenceRange (simulations,
                             norm_factor = None):
            """ Generate [2.5; 97.5]% confidence range for given vector of 
                simulations"""
            

            # Confidence limits (%)
            __lower_confidence = 0.025
            __upper_confidence = 0.975
            

            __simulations_vals = [float(each) for each in simulations.split(' ')]
            __sorted_sims = np.array(__simulations_vals)

            __num_elements, = __sorted_sims.shape
                        
            # If normalization value is provided, de-normalize simulations
            if norm_factor is not None:
                __sorted_sims += norm_factor
                
            __sorted_sims.sort()
            
            
            return [__sorted_sims[int(__lower_confidence * __num_elements)],
                    __sorted_sims[int(__upper_confidence * __num_elements)]]
            

        #=======================================================================
        # writeXML
        # 
        # Write test results to XML format file
        #
        # Inputs:
        #         test_name - Name of evaluation test
        #         model_filename - Filename of the model for the test
        #         dirpath - Directory to write XML format file to
        #         file_prefix - Prefix to use for XML format filename
        #         catalog - numpy.array representing observation catalog for
        #                   the test. Default is None.  
        #         forecast_covers_area - Flag if forecast covers the whole testing
        #                                area. If True, sum of true log-likelihoods
        #                                is a valid measure, if False - sum of true
        #                                log-likelihoods is not a valid measure for
        #                                for the test. Default is True.
        #
        # Output: Tuple of test_node and xml document objects
        #  
        #=======================================================================
        def writeXML (self, 
                      test_name, 
                      model_filename, 
                      dirpath,
                      file_prefix,
                      catalog = None,
                      forecast_covers_area = True):
            """Write test results to XML format file"""
          
          
            test_node, xml = EvaluationTest.Result.writeXML(self,
                                                            test_name,
                                                            model_filename,
                                                            dirpath,
                                                            file_prefix)
      
            # Convert test results based on catalog uncertainties to the XML format    
            ###  Create top-level modificationData element
            modification_node = xml.addElement(RELMTest.Result.ModificationData,
                                               test_node)
            modification_node.attrib[RELMTest.Result.PublicID] = 'smi://local/modificationdata/1'
            
            ### Create count element for modificationData
            count_node = xml.addElement(RELMTest.Result.ModificationCount,
                                        modification_node)
            count_node.text = repr(self[RELMTest.Result.ModificationCount]);
            
            ### Create modifications values element
            values_node = xml.addElement(RELMTest.Result.Modification,
                                         modification_node)
            if self[RELMTest.Result.ModificationCount] != 0:
                values_node.text = ' '.join(repr(i) for i in self[RELMTest.Result.Modification])
            else:
                values_node.text = ' '
                
                
            # Write simulation data if it's present
            if RELMTest.Result.Simulation in self:
                ###  Create top-level simulationData element
                simulation_node = xml.addElement(RELMTest.Result.SimulationData,
                                                   test_node)
                simulation_node.attrib[RELMTest.Result.PublicID] = 'smi://local/simulationdata/1'
                
                ### Create count element for simulationData
                count_node = xml.addElement(RELMTest.Result.SimulationCount,
                                            simulation_node)
                count_node.text = repr(self[RELMTest.Result.SimulationCount]);
                
                ### Create values element
                values_node = xml.addElement(RELMTest.Result.Simulation,
                                             simulation_node)
                if self[RELMTest.Result.SimulationCount] != 0:
                    values_node.text = ' '.join(repr(i) for i in self[RELMTest.Result.Simulation])
                else:
                    values_node.text = ' '


            if RELMTest.Result.LogLikelihoodTrue in self:
                
                log_likelihood_node = xml.addElement(RELMTest.Result.LogLikelihoodTrue,
                                                     test_node)
                log_likelihood_node.attrib[RELMTest.Result.LogLikelihoodSumAttribute] = \
                   '%.5f' %self[RELMTest.Result.LogLikelihoodSumAttribute]
                
                log_likelihood_node.attrib[RELMTest.Result.LogLikelihoodSumIsValidAttribute] = \
                   repr(forecast_covers_area)
                
                for index, each_event in enumerate(catalog):
                    
                    # Add event and corresponding logL
                    event_node = xml.addElement(RELMTest.Result.LogLikelihoodEvent,
                                                log_likelihood_node)
    
                    event_node.text = '%.5f' %self[RELMTest.Result.LogLikelihoodTrue][index]
                    event_node.attrib[RELMTest.Result.EventLongitude] = '%.6f' %each_event[CSEPGeneric.Catalog.ZMAPFormat.Longitude]
                    event_node.attrib[RELMTest.Result.EventLatitude] = '%.6f' %each_event[CSEPGeneric.Catalog.ZMAPFormat.Latitude]
                    event_node.attrib[RELMTest.Result.EventMagnitude] = '%.4f' %each_event[CSEPGeneric.Catalog.ZMAPFormat.Magnitude]
                    event_node.attrib[RELMTest.Result.EventDepth] = '%.4f' %each_event[CSEPGeneric.Catalog.ZMAPFormat.Depth]
                    
                    event_date = datetime.datetime(int(each_event[CSEPGeneric.Catalog.ZMAPFormat.DecimalYear]),
                                                   int(each_event[CSEPGeneric.Catalog.ZMAPFormat.Month]),
                                                   int(each_event[CSEPGeneric.Catalog.ZMAPFormat.Day]),
                                                   int(each_event[CSEPGeneric.Catalog.ZMAPFormat.Hour]),
                                                   int(each_event[CSEPGeneric.Catalog.ZMAPFormat.Minute]),
                                                   int(each_event[CSEPGeneric.Catalog.ZMAPFormat.Second]),
                                                   CSEP.Time.microseconds(each_event[CSEPGeneric.Catalog.ZMAPFormat.Second]))
                     
                    event_node.attrib[RELMTest.Result.EventDate] = event_date.strftime(CSEP.Time.ISO8601Format) 

                
            return (test_node, xml)


        #----------------------------------------------------------------------------
        #
        # Create plot of evaluation test summary for all participating model of 
        # the forecast group. This method plots true logL as computed by the test
        # with [2.5; 97.5]% uncertainty interval based on test simulations. 
        #
        # Input: 
        #        test_class - Reference to the class for evaluation test
        #        summary_path - Path to the summary file for the test
        #        output_dir - Directory to place plot file to. Default is None.    
        #
        # Output: List of plot files
        #
        @staticmethod
        def plotAllModelsSummary(test_class,
                                 summary_path,
                                 output_dir = None):
            """ Create a plot of forecasted number of events against
                observed interval of events (interval limits are defined by 
                observed catalog with applied uncertainties). """
                
            ### Check for existence of the summary file - in case there are no
            # models in the group are available yet
            if summary_path is None or os.path.exists(summary_path) is False:
                return []
                
                
            __forecasted_marker = 'k-|'
            __observed_marker = 's'
            
            __rejected_color = 'r'
            __accepted_color = 'g' 
            
            __line_width = 1.5
            __y_coord_delta = 0.1
            
            xml_obj, plot_obj = EvaluationTest.plot(summary_path,
                                                    fig_size_num_tags = test_class.xml.Root)
            
            # Dictionary of trajectory index and corresponding model name
            traj_name = {}
            __y_coord = 0

            traj_zorder = EvaluationTest.Matplotlib.plotZOrder['trajectory']

            # Test result for each model
            for traj_index, each_model_xml in enumerate(xml_obj.elements(test_class.xml.Root)):
                                        
                # Extract true logL values
                true_logL = xml_obj.children(each_model_xml,
                                             RELMTest.Result.LogLikelihoodTrue)[0]
                true_logL_val = float(true_logL.attrib[RELMTest.Result.LogLikelihoodSumAttribute])
                
                marker_format = __forecasted_marker
                    
                # Collect confidence limits
                simulations_str = xml_obj.children(each_model_xml,
                                                   RELMTest.Result.Simulation)[0].text
    
                
                # Get 2.5 and 97.5 percentile of confidence limits for true logL
                var_values = RELMTest.Result.confidenceRange(simulations_str,
                                                             true_logL_val)

                marker_format = __observed_marker
    
                # Determine color to use for trueLogL
                if true_logL_val < min(var_values):
                    # Model is rejected
                    marker_format += __rejected_color
                    
                else:
                    # Model is accepted
                    marker_format += __accepted_color
                    
                __y_coord += __y_coord_delta
                
                plt.plot([true_logL_val],
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
                                                               test_class.xml.ModelName[0])[0].text)
            
    
            # Disable y-axis ticks and their labels
            y_ticks_vals = traj_name.keys()
            y_ticks_vals.sort()
            plt.yticks(y_ticks_vals, [])
                
            plt.xlabel(test_class.MatPlotLib.XLabel)   
            plt.ylim(0, __y_coord + __y_coord_delta) 
            
            # Allow more space on left side of the plot to prevent
            # clipping of model names
            plt.subplots_adjust(left = 0.05,
                                right = 0.75,
                                bottom = 0.15)

            xmin, xmax = plt.xlim()
            
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
                         horizontalalignment='left')
            
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
            
    
    #===========================================================================
    # Nested class that defines attributes of XML format result data specific
    # to the RELM evaluation test.
    # Each of the derived classes must define an object of the class that sets
    # each of the data attributes.
    #===========================================================================
    class XML (object):

        def __init__(self, 
                     root, 
                     true_event, 
                     model_name, 
                     test_vars, 
                     func, 
                     eval_dict = {},
                     all_models_summary = {}):
            # Root element for the test. Corresponding matlab script to invoke the 
            # test uses the same name
            self.Root = root
            
            # True event for the test 
            self.TrueEvent = true_event
    
            # XML elements that represent names of forecast models involved in test
            self.ModelName = model_name
            
            # XML elements that represent result variables for the evaluation test
            # and corresponding simulation data used to compute result variable values
            self.TestVars = test_vars
            
            # Function to calculate result variable (used to calculate cumulative
            # variable also)
            self.ResultVarFunc = func
            
            # Variable type and an operator to evaluate intermediate summary results 
            # (see Trac ticket #178: Add a sanity check for number of observed
            # events in cumulative result)
            self.EvaluateSummary = eval_dict
            
            self.AllModelsSummary = all_models_summary
        
    
    # Static data

    # Prefix for the test generated files    
    __filePrefix = 'r' + EvaluationTest.FilePrefix

    # Pattern used to match result files in Matlab format
    __matlabResultPattern = '%s*%s' %(__filePrefix, 
                                      CSEPFile.Extension.MATLAB)
    
    # Pattern used to match result files in ASCII format
    __asciiResultPattern = '%s*%s' %(__filePrefix, 
                                     CSEPFile.Extension.ASCII)

    # Pattern used to match result files in XML format
    __xmlResultPattern = '%s*%s' %(__filePrefix, 
                                   CSEPFile.Extension.XML)

    # Pattern used to match directory with random seed files in ASCII format
    __randomSeedPostfix = 'randomSeed'
    __randomSeedPattern = '*%s' %__randomSeedPostfix

    # Keyword identifying the class
    __type = "RELMTest"
    
    # Common directory for RELM evaluation tests and related files
    _scriptsPath = [os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV], 
                                 'src', 'RELMTests')]

    __logger = None


    #===========================================================================
    # Nested class with matplotlib settings for the test     
    #===========================================================================
    class Matplotlib (object):

        # Static data
        _plotObserved = { 'color'     : 'k',
                          'linestyle' : '-',
                          'linewidth' : 2 }
        
        _plotPredicted = { 'color'     : 'k',
                           'linestyle' : '--',
                           'linewidth' : 1 }
        
        _plotCurve = { 'markersize' : None,
                        'colors': ( 'g', 'b' ),
                        'linestyle' : ( 'steps', '-', '-' ),
                        'linewidth' : None }
        
        _plotAxes = { 'ymin' : 0.0, 
                      'ymax' : 1.0 } 

        _plotRejectionBar = {'facecolor' : '0.65', 
                             'significance_level' : 0.05 }
    
        _plotLabels = {'ylabel_size'     : 14,
                       'ylabel_rotation' : 30 }
        

        def __init__ (self, x_label, line_style, var_model, plot_upper = True):
            
            # X-axis label for the plot
            self.XLabel = x_label
            
            # Matplotlib line style
            self.LineStyle = line_style
            
            # Result variable and corresponding model name for the plotted data
            self.ResultVarModel = var_model
            
            # Flag if upper significance area should be plotted for the 
            # cumulative test results plot
            self.PlotUpperSignificance = plot_upper
            
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be invoked.
    # 
    def __init__ (self, group):
        """ Initialization for RELMTest class."""
        
        EvaluationTest.__init__(self, group)
        
        if RELMTest.__logger is None:
           RELMTest.__logger = CSEPLogging.CSEPLogging.getLogger(RELMTest.__name__)
        
        
    #----------------------------------------------------------------------------
    #
    # Returns file prefix for test result file.
    #
    # Input: None
    #
    # Output: File prefix used by test results.
    @classmethod
    def filePrefix (cls):
        """ Returns file prefix for test result file."""
        
        return RELMTest.__filePrefix 


    #-----------------------------------------------------------------------------
    #
    # Returns description word for the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: Description of the test (such RELMTest, AlarmTest, etc.)
    #
    def typeDescriptor (self):
        """ Returns test type descriptor."""

        return RELMTest.__type
        

    #----------------------------------------------------------------------------
    #
    # Formats a name for top-level directory to store random seed values
    #
    # Input: 
    #        forecast_name - Filename for the forecast model, or list of
    #                        forecasts models for the test
    #
    # Output: Name of the top-level directory to store random seed values to 
    #
    def randomSeedDir(self,
                      forecast_name):
        """Formats a name for top-level directory to store random seed values."""
     
        models = None
        if isinstance(forecast_name, list) is True:
            models = '_'.join([CSEPFile.Name.extension(name) for name in forecast_name])
        else:
            models = CSEPFile.Name.extension(forecast_name)
        
        test_model_name = '%s-%s_%s' %(self.type(),
                                       EvaluationTest.FilePrefix,
                                       models)
        
        return os.path.join(self.testDir,
                            '%s-%s' %(test_model_name, RELMTest.__randomSeedPostfix),
                            test_model_name)


    #----------------------------------------------------------------------------
    #
    # Formats a name for top-level directory to store random seed values
    #
    # Input: 
    #        prefix - Filename prefix to store random seed file to
    #        sim_index - Simulation counter.
    #        sim_iter - Simulation iteration counter.
    #
    # Output: Name of random seed file for the simulation 
    #
    @staticmethod
    def randomSeedFile(prefix,
                       sim_index,
                       sim_iter):
        """Formats a filename for to store random seed value to."""
     
        seed_filepath = "%s-simulation%s_%s-%s%s" %(prefix, 
                                                    sim_index, 
                                                    sim_iter, 
                                                    RELMTest.__randomSeedPostfix,
                                                    CSEPFile.Extension.TEXT)
        
        return seed_filepath
        

    #--------------------------------------------------------------------
    #
    # Invoke test for the model
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def evaluate (self, 
                  forecast_name):
        """ Invoke the test. This method is implemented by derived children classes."""
        
        self.prepareCatalog()

        test_name = '%s-%s' %(self.type(),
                              EvaluationTest.FilePrefix)

        CSEPLogging.CSEPLogging.getLogger(RELMTest.__name__).info('%s for %s'
                                                                  %(test_name,
                                                                    forecast_name))
        
        return test_name


    
    #--------------------------------------------------------------------
    #
    # prepareCatalog
    #
    # This method prepares observation catalog for evaluation test:
    # * Filter observation catalog based on forecast group parameters: magnitude,
    #   depth, beginning of the forecast 
    #
    # Since all forecasts models share the same observation catalog, it should
    # be prepared once per test within the group
    #
    # Input: None
    #
    # Output:
    #        Tuple of (filtered catalog, 
    #                  catalog modifications) as numpy.array objects
    #
    def prepareCatalog(self):
        """ Prepare observation catalog for evaluation test"""

        # Numpy object for observation catalog has not been initialized yet
        if self.catalogFile.npObject is None:
            
            # Load declustered catalog ('mCatalogDecl' variable) or 
            # undeclustered catalog ('mCatalog' variable)
            catalog = RELMCatalog.load(self.catalogFile.name)
    
            # Filter catalog data based on forecast group parameters: 
            # 1. Beginning of forecast (in case the same observation catalog is re-used by
            #    multiple forecast groups with different starting date)
            # 2. Catalog is already filtered by test area, magnitude and depth  
            #    by PostProcess module defined for the forecast group
            self.catalogFile.npObject = RELMCatalog.cutToTime(catalog,
                                                              self.forecasts.postProcess().start_date)
    
            # Load catalog modifications if any: 3-dimensional numpy.array 
            # that represents catalogs with applied uncertainties 
            self.catalogModificationsFile.npObject = RELMCatalog.load(self.catalogModificationsFile.name)
          
            if self.catalogModificationsFile.npObject is not None:
    
                # Fix for Trac ticket #230: Row-order iteration is used on 
                # column-order cell array of modification catalogs generated in Python
                num_rows, num_columns = self.catalogModificationsFile.npObject.shape
                num_catalogs = num_columns
                
                # In a case of re-processing, Matlab generated modification catalogs 
                # might be used --> need to use row-order notation of the array 
                if (num_rows > 1 and num_columns == 1):
                    
                    num_catalogs = num_rows
                    self.catalogModificationsFile.npObject = self.catalogModificationsFile.npObject.transpose()
                    
                
                # Filter each of the catalogs by start date (in case the same catalog
                # is re-used by related forecasts groups with different start date)
                for index in xrange(0, num_catalogs):
                  self.catalogModificationsFile.npObject[0, index] = RELMCatalog.cutToTime(self.catalogModificationsFile.npObject[0, index],
                                                                                           self.forecasts.postProcess().start_date)
        
        
    #-----------------------------------------------------------------------------
    #
    # prepareForecast
    # 
    # This method prepares forecast and observation catalog for evaluation test:
    # * Scales forecast to the test date (since forecast's start date)
    # * Reduce forecast to the valid locations if weights flag is enabled
    # * Filter observation catalog based on forecast group parameters: magnitude,
    #   depth, beginning of the forecast 
    #
    # Input: 
    #        forecast_file - Path to the forecast file.
    #        weights - Optional weights for other forecast file (if two forecasts
    #                  are required by evaluation test)
    #
    # Output: 
    #         Tuple of scaled (and reduced if weights are enabled) forecast as 
    #         numpy.array object and flag if forecast covers the whole testing
    #         area
    #
    def prepareForecast(self,
                        forecast_file,
                        weights = None): 
      """ Prepare forecast for evaluation test."""

      # Prepare forecast: scale to the test date
      forecast = ForecastHandlerFactory().CurrentHandler.load(forecast_file)
      
      scaled_forecast = Forecast.scale(forecast,
                                       self.scaleFactor)

      np_forecast = None
      
      # Flag if forecast covers the whole test area
      covers_whole_area = True
      
      # Reduce forecast to the valid locations if weights flag is enabled
      if CSEP.Forecast.UseWeights is True:
          combined_weight = scaled_forecast[:, CSEPGeneric.Forecast.Format.MaskBit].astype(int)
              
          if weights is not None:
              combined_weight *= weights.astype(int)
              
          # Select the rows to be used
          selected_rows = combined_weight > 0
          np_forecast = scaled_forecast[selected_rows, :]
          
          if np.nansum(combined_weight) != forecast.shape[0]:
               covers_whole_area = False

      else:
          np_forecast = scaled_forecast
          

      return (np_forecast, covers_whole_area)
  

    #===========================================================================
    # numberEventsCatalog
    #
    # This method computes the number of events in the catalog.    
    #
    # Input:
    #         forecast - numpy.array object which represents forecast data
    #         catalog - numpy.array object which represents catalog data
    #         compute_likelihood - Flag if zero likelihood should be computed.
    #                              If flag is set to True (default), then
    #                              forecast column with computed zero likelihood
    #                              is returned.
    #         true_likelihood - numpy.array object with additional column to
    #                           capture true log-likelihood of each observed event
    #                           Default is None meaning that true log-likelihood
    #                           should not be calculated per each event.
    #         
    # Output: Number of events in catalog
    #
    #===========================================================================
    @classmethod
    def numberEventsCatalog(cls,
                            forecast, 
                            catalog,
                            compute_likelihood = True,
                            true_likelihood = None):
        """ Computes the number of events in the catalog."""

        # Combine observations with forecast
        binned_catalog = ForecastHandlerFactory().CurrentHandler.addObservations(forecast, 
                                                               catalog,
                                                               compute_likelihood,
                                                               true_likelihood)
        
        # Get the number of events
        sum_binned_catalog = ForecastHandlerFactory().CurrentHandler.numberEvents(binned_catalog)
        #print "SUM=", sum_binned_catalog
        del binned_catalog
        
        return sum_binned_catalog


    #===========================================================================
    # Filter observation catalog against masked forecast
    #
    # This method is used by M- and S- evaluation tests to filter observed 
    # catalog against masking bit of forecast. This is to avoid non-observed 
    # events outside of forecast's masking bit coverage to appear 
    # as "observed" events when matched against space collapsed/normalized
    # forecast.
    #===========================================================================
    @staticmethod
    def filterObservations(forecast,
                           catalog):
        """ Filter observation catalog against masked forecast""" 


        # Get the number of earthquakes in catalog
        catalog_num_rows, catalog_num_cols = catalog.shape
        
        filter_index = np.array([True] * catalog_num_rows) 
        
        # print "Filtering OBSERVATIONS:", catalog.shape
        if catalog_num_cols > 1:
            
            for index in xrange(0, catalog_num_rows):
                __x = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Longitude]
                __y = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Latitude]
                __z = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Depth]
                __m = catalog[index, CSEPGeneric.Catalog.ZMAPFormat.Magnitude]
                
                # print 'x=', __x, 'y=', __y, "z=", __z, "__m=", __m
                selection, = np.where((forecast[:, CSEPGeneric.Forecast.Format.MinLongitude] <= __x) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MaxLongitude] > __x) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MinLatitude] <= __y) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MaxLatitude] > __y) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.DepthTop] <= __z) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.DepthBottom] > __z) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] <= __m) & \
                                      (forecast[:, CSEPGeneric.Forecast.Format.MaxMagnitude] > __m))
                
                #print "Selection=", selection, selection.shape
                if selection.size == 0:
                    # print "Event is outside of forecast coverage"
                    filter_index[index] = False
                    
        # print "After filtering OBSERVATIONS: ", catalog.shape
        filtered_catalog = catalog
         
        if catalog_num_rows != 0:
            filtered_catalog = catalog[filter_index, :]
        
        return filtered_catalog 


    #===========================================================================
    # Compute simulation results
    #
    # Inputs:
    #         forecast - numpy.array object that represents forecast data
    #         index - Simulation index
    #         test_random_file_prefix - Full path to the file prefix used to store
    #                                   random seed value used by each simulation.
    #                                   Simulation count and file extension are
    #                                   appended to this prefix by each iteration
    # 
    # Output:
    #         Likelihood
    #===========================================================================
    @staticmethod
    def _simulation(forecast, 
                    sim_index,
                    test_random_file_prefix,
                    num_events = None):
        """ Compute simulation results"""

        total_forecast_rate = forecast[:, CSEPGeneric.Forecast.Format.Rate].sum()
    
        # Delete any observation in forecast
        forecast[:, CSEPGeneric.Forecast.Format.Observations] = 0

        # Create filename for simulation random seed file
        iteration = 1
        number_events = num_events
        
        if num_events is None:
            # Number of events were not provided for the simulation
            
            seed_file = RELMTest.randomSeedFile(test_random_file_prefix,
                                                sim_index, 
                                                iteration)
        
            # Random numbers used by simulations
            generator = CSEPRandom(seed_file)
            num = 1 # Number of random numbers to generate
            number_events = int(scipy.stats.poisson.ppf(generator.createNumbers(num)[0], 
                                                        total_forecast_rate))
            iteration += 1
    
        # Create filename for simulation random seed file
        seed_file = RELMTest.randomSeedFile(test_random_file_prefix,
                                            sim_index, 
                                            iteration)
        
        # Random numbers used by simulations
        generator = CSEPRandom(seed_file)
        random_numbers = np.array(generator.createNumbers(number_events))
        
        rates_CDF = np.cumsum(forecast[:, CSEPGeneric.Forecast.Format.Rate]/total_forecast_rate)

        # Create a deep copy of pre-computed log-likelihood to avoid modifying 
        # the vector between simulations
        log_likelihood = forecast[:, CSEPGeneric.Forecast.Format.PrecomputedZeroLikelihood].copy()
        
        for index in xrange(int(number_events)):
             
             # Check if any indices exist: length of returned tuple
             indices = np.nonzero(rates_CDF > random_numbers[index])
             if len(indices):
                 found_index = indices[0].min()
                 forecast[found_index, CSEPGeneric.Forecast.Format.Observations] += 1
                  
                 # Create numpy.arrays out of one value to pass to logPoissonPDF 
                 # (expects numpy arrays)
                 next_index = found_index + 1
                 observations = forecast[found_index:next_index, 
                                         CSEPGeneric.Forecast.Format.Observations].astype(np.float)
                 rate = forecast[found_index:next_index, 
                                 CSEPGeneric.Forecast.Format.Rate].astype(np.float)
                 
                 log_likelihood[found_index] = CSEPUtils.logPoissonPDF(observations, 
                                                                       rate)

        #print "Sim logL", log_likelihood
        # Cumulative likelihood to return
        sum_log_likelihood = ForecastHandlerFactory().CurrentHandler.numberEvents(log_likelihood)
        
        # Free up memory
        del log_likelihood
        
        return sum_log_likelihood

        
    #----------------------------------------------------------------------------
    #
    # Create copies of test results files with unique filenames 
    # and generate corresponding metadata files. New files are generated
    # under the same directory as original result files.
    #
    # Input: None.
    #
    # Output: 
    #        True if result data is available, False - otherwise.
    #
    def resultData (self):
        """ Copy test result and related data to files with unique names, 
            and generate corresponding metadata files."""

        # Base class implementation of the method takes care of XML format
        # test results, and forecast maps in PNG format
        if EvaluationTest.resultData(self) is False:
            return False
        
        
        # There are more formats of result data: Matlab, ASCII
        comment = "Evaluation test result file "

        # Matlab results files 
        EvaluationTest._storeResultData(self,
                                        RELMTest.__type,
                                        RELMTest.__matlabResultPattern,
                                        CSEPFile.Format.MATLAB,
                                        comment)

        EvaluationTest._storeResultData(self,
                                        RELMTest.__type,
                                        RELMTest.__asciiResultPattern,
                                        CSEPFile.Format.ASCII,
                                        comment)
              
        comment = "Directory with random seed files used by evaluation test "
        __archive_dir = True
        EvaluationTest._storeResultData(self,
                                        RELMTest.__type,
                                        RELMTest.__randomSeedPattern,
                                        CSEPFile.Format.TARGZ,
                                        comment,
                                        __archive_dir)

        return True


    #----------------------------------------------------------------------------
    #
    # Finish test specific plot. This method displays legend, rejection bars 
    # based on modification data, and axis labels.
    #
    # Input: 
    #        x_axis_label - Label for the x-axis
    #        observed_x_axes - x-axis values based on modification data for the
    #                          test. 
    #        result_file - Path to the result file in XML format
    #        output_dir - Directory to place plot file to.
    #
    # Output: List of generated plot files.
    #
    @classmethod
    def _finishPlot (cls, 
                     x_axis_label, 
                     observed_x_axes, 
                     result_file,
                     output_dir,
                     legend_ncols = 1):
        """ Finish test specific plot: legend, axis labels, and rejection bars
            for already plotted test result data."""
      
        # plot legend
        l = plt.legend(bbox_to_anchor = EvaluationTest.Matplotlib._plotLegend['bbox_to_anchor'], 
                       loc = EvaluationTest.Matplotlib._plotLegend['loc'],
                       mode = EvaluationTest.Matplotlib._plotLegend['mode'], 
                       ncol=legend_ncols,
                       columnspacing = EvaluationTest.Matplotlib._plotLegend['columnspacing'],
                       prop=EvaluationTest.Matplotlib._plotLegend['prop'])

        l.set_zorder(EvaluationTest.Matplotlib.plotZOrder['legend'])

        ### plot "patches" = rejection bars

        # upper patch
        plt.axhspan((1.0-0.5*RELMTest.Matplotlib._plotRejectionBar['significance_level']), 
                    1.0, 
                    0.0, 
                    observed_x_axes,
                    facecolor=RELMTest.Matplotlib._plotRejectionBar['facecolor'], 
                    zorder=EvaluationTest.Matplotlib.plotZOrder['rejection'],
                    label='_nolegend_' )

        # lower patch
        plt.axhspan(0.0, 
                    0.5*RELMTest.Matplotlib._plotRejectionBar['significance_level'], 
                    observed_x_axes,
                    1.0,
                    facecolor=RELMTest.Matplotlib._plotRejectionBar['facecolor'], 
                    zorder=EvaluationTest.Matplotlib.plotZOrder['rejection'], 
                    label='_nolegend_' )

        # --------------------------------------------------------------------------------------------------
        plt.xlabel(x_axis_label, 
                   EvaluationTest.Matplotlib._plotLabelsFont)
        plt.ylabel('Fraction of Cases', 
                   EvaluationTest.Matplotlib._plotLabelsFont)

        a = plt.gca()
        a.set_zorder(EvaluationTest.Matplotlib.plotZOrder['axes'])
      
        # Use provided output directory if any
        image_file = result_file
        
        if output_dir is not None:
            image_file = os.path.join(output_dir,
                                      os.path.basename(result_file))
    
        # Replace extension with '.svg' for the image file
        image_file = image_file.replace(CSEPFile.Extension.XML, '')
        image_file += CSEPFile.Extension.SVG
      
        plt.savefig(image_file)
        plt.close()
      
        # Return name of generated plot file
        return [image_file]
      

    #-----------------------------------------------------------------------------
    #
    # __plotModificationData
    # 
    # This method plots modification data of the evaluation test.
    #
    # Input: 
    #         doc - ElementTree object representing root element of test results.
    #         name - Name of the model for the test.
    #
    # Output: None.
    # 
    @classmethod
    def _plotModificationData (cls, doc, name):
        """ Plot modification data of evaluation test."""
   
        # check if modifications are given
        count_elem = doc.elementValue("modificationCount")
        data_elem = doc.elementValue("modification")
          
        logger = CSEPLogging.CSEPLogging.getLogger( __name__ )
        no_modification_data = False
       
        if ((count_elem is not None) and (data_elem is not None)):
            modification_count = int(count_elem)
            modification_array = data_elem.split()
            modifications = sorted(map(float, modification_array))
         
            # check if no. of modifications and simulations match
            if (len(modifications) == modification_count):
           
               if modification_count == 0:
                  # There is no modification data available:
                  no_modification_data = True
                   
               else:
                  # get 5% and 95% values
                  lower_idx = int(np.floor(0.025 * (modification_count - 1)))
                  upper_idx = int(np.ceil(0.975 * (modification_count - 1)))
                   
                  #logger.debug("lower_idx=%s upper_idx=%s" %(lower_idx, upper_idx))
    
                  # plot grey box for modifications - y range is full axis range
                  plt.axvspan(modifications[lower_idx],
                              modifications[upper_idx],
                              facecolor='0.90',
                              edgecolor='0.90' ,
                              zorder=EvaluationTest.Matplotlib.plotZOrder['modification'],
                              label='_nolegend_')
    
            else:
               error_msg = "%s: %s - mismatch in modification dimensions" %(CSEPLogging.CSEPLogging.frame(cls),
                                                                            name)
               logger.error(error_msg)
                
               raise RuntimeError, error_msg
        else:
            no_modification_data = True
         
         
        if no_modification_data is True:
           logger.info("%s: %s - no modification data available" %(CSEPLogging.CSEPLogging.frame(cls),
                                                                   name))


    #-----------------------------------------------------------------------------
    #
    # plotSummary
    # 
    # This method plots test results summary.
    #
    # Input: 
    #         summary_file - Filename for test results in XML format.
    #         test_class - Reference to the class that represents evaluation 
    #                      test that produced the result.
    #         output_dir - Directory to place plot file to. Default is None.    
    #
    # Output: 
    #         Filename for generated plot.
    #
    @classmethod 
    def plotSummary(cls, 
                    summary_file,
                    output_dir = None):
      """ Plot summary test result file in XML format. This method generates
         so-called alpha-tracker (beta, delta, gamma)."""
      
      # Read the whole file in
      doc = CSEPInitFile.CSEPInitFile(summary_file)
      
      # set figsize, clear figure
      matplotlib.rcParams['figure.figsize'] = (12, 9)
      #clf()

      ### process abscissa data - is the same for N-, L-, and R-test
    
      # get abscissa (= ISO date) data array, convert to ASCII before
      abscissa_str = doc.elementValue(ResultsSummary.TestDateElement)
      abscissa_array = abscissa_str.encode("ascii").split()
    
      # convert abscissa array to datetime structure
      abscissa = []
      for absc in abscissa_array:
         absc_parts = absc.split('-')
         abscissa_date = datetime.date(int(absc_parts[0]), 
                                       int(absc_parts[1]), 
                                       int(absc_parts[2]) )
         abscissa.append(matplotlib.dates.date2num(abscissa_date))
        
      # abscissa (date axis) formatting / define tick locators and formatters
      # NOTE: we expect the dates in <testDate> to be in ascending order
        
      # get difference in years
      startyear = int(matplotlib.dates.num2date(abscissa[0]).strftime('%Y'))
      endyear   = int(matplotlib.dates.num2date(abscissa[len(abscissa)-1]).strftime('%Y'))
      yeardiff  = endyear - startyear
        
      if ( yeardiff >= 3 ):
         abscissaFmt  = DateFormatter( '%Y' )
         abscMajorLoc = YearLocator()
         abscMinorLoc = MonthLocator( (1, 4, 7, 10) )
      elif ( yeardiff >= 1 ):
         abscissaFmt  = DateFormatter( '%b %Y' )
         abscMajorLoc = MonthLocator( (1, 4, 7, 10) )
         abscMinorLoc = MonthLocator()
      else:
         # get month difference
         startmonth = int(matplotlib.dates.num2date(abscissa[0]).strftime('%m'))
         endmonth   = int(matplotlib.dates.num2date(abscissa[len(abscissa)-1]).strftime('%m'))
         monthdiff  = endmonth - startmonth
         if ( monthdiff >= 6 ):
            abscissaFmt  = DateFormatter( '%b %Y' )
            abscMajorLoc = MonthLocator( (1, 3, 5, 7, 9, 11) )
            abscMinorLoc = MonthLocator()
         elif ( monthdiff >= 2 ):
            abscissaFmt  = DateFormatter( '%b %Y' )
            abscMajorLoc = MonthLocator()
            abscMinorLoc = WeekdayLocator( MO )
         elif ( monthdiff > 1 ):
            abscissaFmt  = DateFormatter( '%b %d' )
            abscMajorLoc = WeekdayLocator( MO )
            abscMinorLoc = DayLocator()
         else:
            # all dates in the same month, or over 2-months period
            
            # get difference of days
            daydiff  = len(abscissa)
            if ( daydiff > 10 ):
                abscissaFmt  = DateFormatter( '%b %d' )
                abscMajorLoc = WeekdayLocator( MO )
                abscMinorLoc = DayLocator()
            else:
                # range is smaller than 10 days, major tick every day
                abscissaFmt  = DateFormatter( '%b %d' )
                abscMajorLoc = DayLocator()
                abscMinorLoc = matplotlib.ticker.NullLocator()

         
      # use AUTO for ordinate formatting      
      # ordinateFmt = FormatStrFormatter( '%0.3f' )
      # ax.yaxis.set_major_formatter( ordinateFmt )
      ax = plt.subplot(111)
      
      # Plot variables specific to the test
      for var, var_model in cls.MatPlotLib.ResultVarModel.iteritems():

         ordinate_str = doc.elementValue(var)

         # get model name (for legend)
         label_str = doc.elementValue(var_model)
         
         # Append result variable to the model name - to make more obvious which 
         # result variable represents which model
         # Check if there is subscript for the variable name:
         var_tokens = re.split('[0-9]', var)
         var_subscript = var.replace(var_tokens[0], '')

         if len(var_subscript) != 0:
             label_str += r' ($\%s_%s$)' %(var_tokens[0], var_subscript)
         else:
             label_str += r' ($\%s$)' %var_tokens[0]  
         
         # get ordinate data array
         ordinate_array = ordinate_str.split()
         ordinate = map( float, ordinate_array )
         
         # check for equal array dimension
         if (len(abscissa_array) != len(ordinate)):
            error_msg = "%s: %s - %s data vector and date vector length mismatch" \
                        %(CSEPLogging.CSEPLogging.frame(cls), 
                          summary_file, 
                          var)
                        
            CSEPLogging.CSEPLogging.getLogger(__name__).error(error_msg)
            raise RuntimeError, error_msg

         plt.plot_date(abscissa, ordinate, 
                       cls.MatPlotLib.LineStyle[var], 
                       markersize = 8.0, 
                       zorder=EvaluationTest.Matplotlib.plotZOrder['trajectory'], 
                       label=label_str)


      # Display Y-axis label and legend for lines
      y_labels = cls.xml.TestVars.keys()
      y_labels.sort()
      
      math_y_labels = []
      for each_y in y_labels:
         var_tokens = re.split('[0-9]', each_y)
         var_subscript = each_y.replace(var_tokens[0], '')
         label_str = ''

         if len(var_subscript) != 0:
             label_str += r'$\%s_%s$' %(var_tokens[0], var_subscript)
         else:
             label_str += r'$\%s$' %var_tokens[0]  
          
         math_y_labels.append(label_str)
          
      plt.ylabel(' / '.join(math_y_labels), 
                 EvaluationTest.Matplotlib._plotLabelsFont)  

      # check if abscissa has only one data point: set x axis range explicitly
      # (plus / minus one day)
      if (len(abscissa) == 1 ):
         plt.xlim(abscissa[0]-1, abscissa[0]+1)
         
      plt.ylim(RELMTest.Matplotlib._plotAxes['ymin'], 
               RELMTest.Matplotlib._plotAxes['ymax'])
      

      # plot legend
      legend_ncols = len(cls.MatPlotLib.ResultVarModel) % 3

      l = plt.legend(loc=EvaluationTest.Matplotlib._plotLegend['loc'],
                     bbox_to_anchor=EvaluationTest.Matplotlib._plotLegend['bbox_to_anchor'],
                     mode=EvaluationTest.Matplotlib._plotLegend['mode'],
                     ncol=legend_ncols,
                     columnspacing=EvaluationTest.Matplotlib._plotLegend['columnspacing'],
                     prop=EvaluationTest.Matplotlib._plotLegend['prop'])
      
      l.set_zorder(EvaluationTest.Matplotlib.plotZOrder['legend'])

      #=========================================================================
      #      plot "patches" = rejection bars
      #=========================================================================

      # upper patch - not all plots need that patch
      if cls.MatPlotLib.PlotUpperSignificance is True:
          plt.axhspan( (1.0-0.5*RELMTest.Matplotlib._plotRejectionBar['significance_level']), 
                       1.0,
                       facecolor=RELMTest.Matplotlib._plotRejectionBar['facecolor'], 
                       zorder=EvaluationTest.Matplotlib.plotZOrder['rejection'], 
                       label='_nolegend_' )

      # lower patch
      plt.axhspan(0.0, 
                  0.5*RELMTest.Matplotlib._plotRejectionBar['significance_level'],
                  facecolor=RELMTest.Matplotlib._plotRejectionBar['facecolor'], 
                  zorder=EvaluationTest.Matplotlib.plotZOrder['rejection'], 
                  label='_nolegend_' )
      
         
      # formatting of abscissa (date) axis
      ax.xaxis.set_major_formatter(abscissaFmt)
      ax.xaxis.set_major_locator(abscMajorLoc)
      ax.xaxis.set_minor_locator(abscMinorLoc)
        
      # not required!
      # ax.autoscale_view()
        
      labels = ax.get_xticklabels()
      plt.setp(labels, 
               'rotation', 
               RELMTest.Matplotlib._plotLabels['ylabel_rotation'], 
               fontsize=RELMTest.Matplotlib._plotLabels['ylabel_size'])
      
      show_grid = True
      plt.grid(show_grid, 
               zorder=EvaluationTest.Matplotlib.plotZOrder['grid'] )

      a = plt.gca()
      a.set_zorder(EvaluationTest.Matplotlib.plotZOrder['axes'] )
      #show()
      
      # Replace extension with '.svg' for the image file
      image_file = summary_file
      if output_dir is not None:
          image_file = os.path.join(output_dir,
                                    os.path.basename(summary_file))
          
      image_file = image_file.replace(CSEPFile.Extension.XML,
                                      CSEPFile.Extension.SVG)
      plt.savefig(image_file)
      plt.close()

      # Return name of generated plot file
      return image_file


