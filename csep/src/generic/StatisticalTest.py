"""
Module StatisticalTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import datetime, os
import numpy as np

from EvaluationTest import EvaluationTest
from RELMCatalog import RELMCatalog
from ForecastHandlerFactory import ForecastHandlerFactory
import CSEPLogging, CSEPUtils, CSEPFile, CSEPGeneric, CSEPInitFile


#-------------------------------------------------------------------------------
#
# StatisticalTest.
#
# This class represents statistical evaluation test for forecasts models.
#
class StatisticalTest (EvaluationTest):

    class EventInfo (object):
        """ Catalog event information """
        
        class Format (object):
            
            Longitude = 0
            Latitude = 1
            Magnitude = 2
            Rate = 3
            
        def __init__(self, long, lat, depth, magn):
            self.x = long
            self.y = lat
            self.z = depth
            self.m = magn
            
        #----------------------------------------------------------------------- 
        def __str__ (self):
            """ String representation of EventInfo object."""
            
            return "longitude=%s latitude=%s depth=%s magnitude=%s" %(self.x,
                                                                      self.y,
                                                                      self.z,
                                                                      self.m)

        #----------------------------------------------------------------------- 
        def toList (self):
            """ List representation of EventInfo object."""
            
            return [self.x, self.y, self.m]
            

    class EventSummary (object):
        """ Structure-like class to store observed event information."""
        
        def __init__(self):
            """ Initialize StatisticalTest.EventSummary object"""
            
            # Dictionary {date: [EventInfo]} to store information of observed events
            # by date of occurrence
            self.info = {}


    # Data structure to store test results    
    class Result (EvaluationTest.Result):
        
        #=======================================================================
        # Initialize results structure for the test
        # 
        # Inputs:
        #
        def __init__ (self, 
                      results_dict):
            """ Initialize results structure with tests results"""
            
            # Call base class constructor
            EvaluationTest.Result.__init__(self)
            
            for key, value in results_dict.iteritems():
                self[key] = value
        

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
                      models_files, 
                      dir_path, 
                      file_prefix):
            """Write test results to XML format file"""

            test_node, xml = EvaluationTest.Result.writeXML(self,
                                                            test_name,
                                                            models_files,
                                                            dir_path,
                                                            file_prefix)

            # Create elements that represent test results:
            for key, value in self.iteritems():
                node = xml.addElement(key,
                                      test_node)
                # numpy arrays should be "flattened" and reshaped back into
                # original matrix 
                node.text = ' '.join([repr(i) for i in self[key].flatten()])

            # write XML format file
            xml.write()
            
            
    # Static data and internal classes
    
    class RatesInfo (object):
        """ Class to store cumulative and per observed event forecasts rates."""
        
        def __init__(self,
                     group):
            """ Initialize RateInfo object."""
    
            self.initialize(group.files())


        def initialize(self,
                       forecasts_files):
            """ Initialize rates arrays for forecast group: cumulative forecasts
                rates and rates for observed events for the test period."""
            
            need_to_initialize = True
            
            # Check if 'all_models' already exists for the object
            if hasattr(self, 'all_models') is True and \
               self.all_models == forecasts_files:
                
                # Different than self.all_models forecasts list is 
                # provided: re-initialize internal data attributes, otherwise
                # keep originally initialize data attributes
                need_to_initialize = False
                    

            if need_to_initialize is True:

                # David's code modelnm
                self.all_models = forecasts_files
                num_models = len(self.all_models)

                # Numpy array to store total forecasts rates for the testing period
                # based on common masking bit for any two given forecasts
                # David's code: en.mat 
                self.np_sum_rates = np.zeros((num_models, num_models),
                                             dtype = np.float)
            
                # Forecasts rates for observed events
                # David's code: lambda.mat
                self.np_event_rates = None
                
            
    # Since cumulative rate collection is a very expensive operation (for example,
    # to step through all existing one-day models within SCEC Testing Center since
    # beginning of operations on 2007-09-01), and used
    # by both T and W tests for the same forecast group, rates information 
    # should be stored per forecast group object (NOT a directory - multiple 
    # groups might share forecast directory)
    __rates = {}
    
    # Prefix for the test generated files
    __filePrefix = 's' + EvaluationTest.FilePrefix
    
    # Pattern used to match result files in XML format
    __xmlResultPattern = '%s*%s' %(__filePrefix,
                                   CSEPFile.Extension.XML)

    # Keyword identifying the class
    __type = "StatisticalTest"
    
    __logger = None

   
    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be evaluated.
    # 
    def __init__ (self, group):
        """ Initialization for StatisticalTest class."""
        
        EvaluationTest.__init__(self, group)

        if StatisticalTest.__logger is None:
           StatisticalTest.__logger = CSEPLogging.CSEPLogging.getLogger(StatisticalTest.__name__)

        self.initializeData(self.forecasts.files())


    #===========================================================================
    # Return rates information for ForecastGroup 
    #===========================================================================
    @staticmethod
    def rates (forecast_group):
        """Return rates for forecast_group"""
        
        return StatisticalTest.__rates.setdefault(forecast_group,
                                                  StatisticalTest.RatesInfo(forecast_group))

    
    def initializeData (self, forecasts_files):
        """ Initialization of internal data for StatisticalTest object."""
        
        StatisticalTest.rates(self.forecasts).initialize(forecasts_files)


    #===========================================================================
    # Is internal data initialized?
    #===========================================================================
    def isInitialized (self):
        """ Returns a flag if internal data of the class was initialized (True)
            or not (False). This method is implemented by derived children
            classes."""
            
        pass


    #---------------------------------------------------------------------------
    #
    # Invoke evaluation test for the forecast
    #
    # Input: 
    #        forecast_name - Forecast model to test
    #
    def evaluate (self, 
                  forecast_name):
        """ Run evaluation test for all possible combinations of the forecast
            with other available forecasts models."""


        # Observation catalog is not valid for the test
        if self.prepareCatalog() is False:
            return None
        
        # If number of forecasts files have changed, re-initialize internal data to
        # correspond to current number of forecasts files for evaluation
        num_models = len(self.forecasts.files())
        group_rates = StatisticalTest.rates(self.forecasts)
        
        if len(group_rates.all_models) != num_models or \
           self.isInitialized() is False:
            
            # Number of forecasts files has changed since object creation time
            self.initializeData(self.forecasts.files())
        
        # Prepare forecasts data for the test
        self.prepareForecasts()
        
        test_name = '%s-%s' %(self.type(),
                              EvaluationTest.FilePrefix)

        StatisticalTest.__logger.info('%s for %s' %(test_name,
                                                    forecast_name))

        return test_name
    

    #---------------------------------------------------------------------------
    #
    # prepareCatalog
    #
    # This method prepares observation catalog for evaluation test:
    # * Filter observation catalog based on forecast group parameters: start
    #   date for the forecast group within testing center
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


        # Numpy object for cumulative catalog has not been initialized yet
        if self.cumulativeCatalogFile.npObject is None:
            
            # Statistical tests use cumulative catalog for the whole time period
            # of forecast group existence within Testing Center
            # (ever since forecast group was introduced to the testing center):
            # use the same filters to prepare input catalog for the test, except
            # for start date which is:
            # * is entry date of the forecast group into the Testing Center
            post_process = self.forecasts.postProcess()
            
            # Load catalog
            catalog = RELMCatalog.load(self.cumulativeCatalogFile.name)
    
            # Filter catalog data based on forecast group parameters: 
            # 1. Entry date of forecast into testing center (in case the same 
            #    observation catalog is re-used by multiple forecast groups 
            #    with different entry date)
            # 2. Catalog is already filtered by test area, magnitude and depth  
            #    by PostProcess module defined for the forecast group
            self.cumulativeCatalogFile.npObject = RELMCatalog.cutToTime(catalog,
                                                                        self.forecasts.postProcess().cumulative_start_date)
    
            #-------------------------------------------------------------------
            # Create dictionary of observed events to simplify navigation of
            # observed events when collecting forecasts rates 
            self.cumulativeCatalogFile.intermediateObj = StatisticalTest.EventSummary()
            
            # Dictionary of test year: {month: [days]}
            for each_row in self.cumulativeCatalogFile.npObject:

                year = int(each_row[CSEPGeneric.Catalog.ZMAPFormat.DecimalYear])
                month = int(each_row[CSEPGeneric.Catalog.ZMAPFormat.Month])
                day = int(each_row[CSEPGeneric.Catalog.ZMAPFormat.Day])

                self.cumulativeCatalogFile.intermediateObj.info.setdefault(datetime.datetime(year, 
                                                                                             month, 
                                                                                             day), 
                                                                           []).append(StatisticalTest.EventInfo(each_row[CSEPGeneric.Catalog.ZMAPFormat.Longitude],
                                                                                                                each_row[CSEPGeneric.Catalog.ZMAPFormat.Latitude],
                                                                                                                each_row[CSEPGeneric.Catalog.ZMAPFormat.Depth],
                                                                                                                each_row[CSEPGeneric.Catalog.ZMAPFormat.Magnitude]))
                
        # Return flag that catalog satisfies test criteria
        continue_test = True

        # Valid for the test catalog criteria: must have at least 2 events
        min_num_events_required = 2
        
        # Don't run the test if observation catalog consists of less that 2 events
        num_rows, num_cols = self.cumulativeCatalogFile.npObject.shape
        
        if num_rows < min_num_events_required:
            
            StatisticalTest.__logger.info("Observation catalog contains %s event (%s required), skipping %s evaluation test." %(num_rows,
                                                                                                                                 min_num_events_required,
                                                                                                                                 self.type()))
            continue_test = False
                    
        # Return flag that catalog satisfies test criteria
        return continue_test
        

    #-----------------------------------------------------------------------------
    #
    # prepareForecast
    # 
    def prepareForecasts(self): 
      """ Prepare forecasts for evaluation test.
      
          This method collects cumulative rate of each forecast for the test
          time period in cells common to each pair of tested forecasts. Due
          to expensive FileIO by Python, create 2-dim matrix of forecasts 
          cumulative rates given mask of each forecast - this matrix would be
          constructed once and used to invoke evaluation test for each forecast.
          
          Input arguments: None
      """
      
      # Forecasts are prepared once for all statistical test runs: per each model
      group_rates = StatisticalTest.rates(self.forecasts)
      if group_rates.np_event_rates is not None:
          return
      
      num_forecasts = len(group_rates.all_models)    
      group_rates.np_event_rates = np.zeros((num_forecasts,),
                                            dtype = np.object)
      
      # Determine if forecast is static (file-based) or dynamic (model code is
      # installed within testing center and multiple forecast periods exist for
      # the model) :
      # 1. In case of static forecast:
      #    * Load forecast
      #    * Extract rate that correspond to the observed event (forecast rate
      #      for the whole testing period scaled down to one day) 
      #    * Sum up forecast rate for the whole testing period (up to the test
      #      date)
      # 2. In case of dynamic forecast: 
      #    beginning with entry date into the testing center for each testing period
      #    up to the test date:
      #    * Load forecast
      #    * Extract rate that correspond to the observed event (forecast rate
      #      for the whole testing period scaled down to one day)
      #    * Sum up forecast rate for the whole testing period (up to the test
      #      date)
      use_static_forecast = False
      
      # Number of days in forecast period: used to get daily forecast rates
      num_scale_days = 0 
      
      # Cumulative start date is later or the same as current forecast's start
      # date - it's file-based forecasts or very first forecast is generated since
      # model entry into the testing center 
      if self.forecasts.postProcess().cumulative_start_date >= \
         self.forecasts.postProcess().start_date:

          # Cumulative test period is the same as current test period, use
          # only current forecasts for the test (covers file-based forecasts, and
          # forecasts groups for which <entryDate> value is not provided)
          use_static_forecast = True

      current_start_date = self.forecasts.postProcess().start_date
      current_end_date = self.forecasts.postProcess().end_date
      
      if current_end_date is None:
          # One-day models don't have end_date set up
          current_end_date = self.forecasts.postProcess().start_date + datetime.timedelta(days=1)

      # Number of days within current forecast period
      num_scale_days = (current_end_date - current_start_date).days
    
      StatisticalTest.__logger.info("Current forecast period is set to %s days (start date=%s, end date=%s)" \
                                    %(num_scale_days,
                                      current_start_date,
                                      current_end_date))

      # Matrix of forecasts masks
      np_mask = None

      current_forecasts = np.zeros((num_forecasts,),
                                   dtype = np.object)

      # Load masking bit vector of each forecast file participating in test
      for index, each_forecast in enumerate(group_rates.all_models):
          
          np_forecast = ForecastHandlerFactory().CurrentHandler.load(os.path.join(self.forecasts.dir(),
                                                                each_forecast))
          
          if np_mask is None:
              num_rows, num_cols = np_forecast.shape
              np_mask = np.zeros((num_forecasts, num_rows),
                                 dtype = np.float)
          
          np_mask[index] = np_forecast[:, CSEPGeneric.Forecast.Format.MaskBit].astype(int)
          
          StatisticalTest.__logger.info("%s forecast's masking bit is set for %s bins" \
                                        %(each_forecast,
                                          np_mask[index].sum()))

          if use_static_forecast is True:
              
              # Scale down forecast rate for the whole testing period to one day rate
              np_forecast[:, CSEPGeneric.Forecast.Format.Rate] /= num_scale_days
              current_forecasts[index] = np_forecast


      # Number of days in testing period: up to the testDate
      num_test_days = 0 
      
      # Iterate through each day of testing period
      test_date = self.forecasts.postProcess().cumulative_start_date

      events_dates = self.cumulativeCatalogFile.intermediateObj.info.keys()
      events_dates.sort()

                  
      # Collect forecasts total rates and per each observed event
      while test_date <= self.testDate:
          
          num_test_days += 1

#          print "use_static=%s" %use_static_forecast, "hasModels(%s) = %s" %(test_date,
#                                                                             self.forecasts.hasModels(test_date))
          if (use_static_forecast is False) and \
             (self.forecasts.hasModels(test_date) is True):
              # Load forecasts that correspond to the test date 
              # into local dictionary 'current_forecasts' or 
              # use previously loaded forecasts

              # Extract start and end dates for test period that covers 'test_date'
              schedule_generator = self.forecasts.models.schedule.dates(test_date)
              current_start_date = schedule_generator.next()
              current_end_date = schedule_generator.next()

              # Number of days within current forecast period
              num_scale_days = (current_end_date - current_start_date).days

              StatisticalTest.__logger.info("Current forecast period is set to %s days (start date=%s, end date=%s)" \
                                            %(num_scale_days,
                                              current_start_date,
                                              current_end_date))
                  
              # Load all forecasts into 'current_forecasts' that
              # represent 'test_date'
              for index, each_forecast in enumerate(group_rates.all_models):
                  # Filename for forecast with start date of 'test_date'
                  current_model_name = self.forecasts.archivedName(each_forecast,
                                                                   test_date)
          
                  # Check if current_model_name is not last available forecast: 
                  # it would not appear under 'forecasts/archive' sub-directory yet,
                  # current forecasts are located under 'forecasts' directory
                  current_path, current_file = os.path.split(current_model_name)
                  if current_file == each_forecast:
                      # Current forecast is under 'GROUP/forecasts' directory
                      current_model_name = os.path.join(self.forecasts.dir(),
                                                        each_forecast) 
                   
                  StatisticalTest.__logger.info("Loading %s forecast that correspond to %s start date" \
                                                %(current_model_name,
                                                  test_date))
                  
                  np_forecast = ForecastHandlerFactory().CurrentHandler.load(current_model_name)
    
                  # Scale down forecast rate for the whole testing period to one day rate
                  np_forecast[:, CSEPGeneric.Forecast.Format.Rate] /= num_scale_days
                  current_forecasts[index] = np_forecast
              

          # Prepare forecasts rates: cumulative and per each observed event
          # in common bins for any pair of forecasts
          for index, each_forecast in enumerate(group_rates.all_models):
                  
              # Collect total rate based on masking bit for each pair of 
              # forecasts
              for each_other_forecast in group_rates.all_models:
                  
                  other_forecast_index = group_rates.all_models.index(each_other_forecast)
                  selection = (np_mask[index] * np_mask[other_forecast_index]) > 0 
#                  print "Sum of rates for %s bins (index=%s, other_index=%s)=%s" %(selection.sum(),
#                                                                                   index, 
#                                                                                   other_forecast_index,
#                                                                                   current_forecasts[index][selection, CSEPGeneric.Forecast.Format.Rate].sum()) 
#                  print "Forecast index=%s, other_forecast_index=%s" %(index,
#                                                                       other_forecast_index)
#                  print "GroupRates.np_sum_rates.shape=", group_rates.np_sum_rates.shape
                  
                  group_rates.np_sum_rates[index,
                                           other_forecast_index] += current_forecasts[index][selection, CSEPGeneric.Forecast.Format.Rate].sum()

          # Collect rate per observed event that falls within forecast period or
          # if file-based forecasts are used for evaluation
          if test_date in events_dates: 
              if (test_date < current_end_date and \
                  test_date >= current_start_date) or \
                  use_static_forecast is True:
                  
                  # Iterate through all events for the date
                  for each_event in self.cumulativeCatalogFile.intermediateObj.info[test_date]:
                      
                      # Iterate through all forecasts to update event information 
                      for forecast_index, forecast in enumerate(current_forecasts):
                      
                          # Have to create new event info list per each forecast
                          # since rate information is appended to it 
                          event_info = each_event.toList()
                              
                          selection, = np.where((forecast[:, CSEPGeneric.Forecast.Format.MinLongitude] <= each_event.x) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.MaxLongitude] > each_event.x) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.MinLatitude] <= each_event.y) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.MaxLatitude] > each_event.y) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.DepthTop] <= each_event.z) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.DepthBottom] >= each_event.z) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] <= each_event.m) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.MaxMagnitude] > each_event.m) & \
                                                (forecast[:, CSEPGeneric.Forecast.Format.MaskBit] == 1.0))
                
                          if selection.size != 0:

                              event_rate = forecast[selection, CSEPGeneric.Forecast.Format.Rate].tolist()
                              
                              StatisticalTest.__logger.info("Forecast %s rate for %s (%s): %s" \
                                                             %(group_rates.all_models[forecast_index],
                                                               test_date,
                                                               each_event,
                                                               forecast[selection, :]))
                              
                              # Fix for Trac ticket #286: 'inf' value is 
                              # introduced into T statistical test result if 
                              # forecast is providing rate of zero for observed event
                              event_rate = [np.nan if x==0.0 else x for x in event_rate]
                              
                              if np.nan in event_rate:
                                  StatisticalTest.__logger.warning("Zero rate was replaced by NaN in model %s for %s event (%s): %s" \
                                                                   %(group_rates.all_models[forecast_index],
                                                                     test_date,
                                                                     each_event,
                                                                     forecast[selection, :]))
                                  
                              
                              event_info.extend(event_rate)
                              
                          else:
                              StatisticalTest.__logger.info("No rate is provided by forecast %s for %s (%s)" \
                                                             %(group_rates.all_models[forecast_index],
                                                               test_date,
                                                               each_event))
                              
                              event_info.append(np.nan)
                                     
                              
                          if isinstance(group_rates.np_event_rates[forecast_index], 
                                        int) is True:
                              # Array element was not initialized yet
                              # ATTN: specifying 'np.float' as datatype converts
                              # any None values to nan
                              group_rates.np_event_rates[forecast_index] = np.array([event_info],
                                                                                    dtype = np.float)
                              #print "Setting event info to np_event_rates: %s", event_info
                                      
                          else:
                              # Add new event info
                              group_rates.np_event_rates[forecast_index] = np.append(group_rates.np_event_rates[forecast_index],
                                                                                     np.array([event_info], dtype = np.float),
                                                                                     axis = 0)
                              #print "Appending event info to np_event_rates:", event_info
                              
                               
          # Increment test date
          test_date += datetime.timedelta(days=1)
      
#      print 'event_rates:', group_rates.np_event_rates
#      print 'sum_rates:', group_rates.np_sum_rates


    #---------------------------------------------------------------------------
    #
    # Returns file prefix for test result file.
    #
    # Input: None
    #
    # Output: File prefix used by test results.
    #
    @classmethod
    def filePrefix (cls):
        """ Returns file prefix for test result file."""
        
        return StatisticalTest.__filePrefix
        
        
    #---------------------------------------------------------------------------
    #
    # Formats filename for the evaluation test summary of all models in the 
    # forecast group. This method overwrites base-class implementation of the
    # method since there are no summary files for all models for now.
    #
    # Input: None
    #
    # Output: Filename for all-models summary file
    #
    def allModelsSummaryFile (self):
        """ Formats filename for the evaluation test summary of all models in the 
            forecast group."""

        # Path to the all models summary file - None
        return None
        
        
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

        return StatisticalTest.__type
        

    #-----------------------------------------------------------------------------
    #
    # Update cumulative test result data with daily result. This method can
    # be overwritten by derived classes. Statistical evaluation tests don't have
    # cumulative test results (evaluation test is a cumulative test), 
    # therefore the class overwrites the method not to update the cumulative 
    # results.
    #
    # Input: 
    #        result_file - Daily result file to be used to update 
    #                      corresponding cumulative result file.
    #
    # Output: None.
    #
    def updateCumulativeResultData (self, result_file):
        """ Update cumulative test result data with daily result."""

        pass


    #----------------------------------------------------------------------------
    #
    # This method plots result data of statistical evaluation test.
    #
    # Input: 
    #         result_file - Test results file in XML format 
    #         output_dir - Directory to place plot file to. Default is None.    
    #
    @classmethod
    def plot (cls, 
              result_file,
              output_dir = None):
        """ Plot test results in XML format."""

        # Read the whole file in
        return CSEPInitFile.CSEPInitFile(result_file)
