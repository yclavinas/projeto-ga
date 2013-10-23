"""
   Forecast module
"""

__version__ = "$Revision: 4150 $"
__revision__ = "$Id: Forecast.py 4150 2012-12-19 03:08:43Z liukis $"


import os, re, copy, datetime, calendar, scipy.io
import numpy as np
import matplotlib.pyplot as plt

import CSEPFile, CSEP, Environment, CSEPLogging, CSEPPropertyFile, CSEPGeneric
from PostProcessFactory import PostProcessFactory
from CatalogDataSource import CatalogDataSource
from RELMCatalog import RELMCatalog
from ReproducibilityFiles import ReproducibilityFiles
from CSEPInputParams import CSEPInputParams
from CSEPStorage import CSEPStorage
from ForecastHandlerFactory import ForecastHandlerFactory


#--------------------------------------------------------------------------------
#
# Forecast.
#
# This class is designed to represent a forecast model.
# It invokes forecast model or sets up an environment to point to the file
# location of already generated forecasts.
#
class Forecast (ReproducibilityFiles, CSEPStorage):

    # Static data of the class
    # Root path for all available models source codes
    CodePath = os.path.join(Environment.Environment.Variable[Environment.CENTER_CODE_ENV],
                            'src', 'SCECModels')

    # Character used to separate forecast name fields 
    NameSeparator = '_'
    

    # Pattern for backup filenames created by editing programs
    __backupFilenamePattern = re.compile('.+[~]$')

    # File prefix for magnitude distribution plot of the forecast
    MagnitudeDistributionPrefix = 'MagnitudeDistribution_'


    # Logger object for the module
    Logger = CSEPLogging.CSEPLogging.getLogger(__name__)
 
      
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        dir_path - Directory to store forecast file to.
    #        template_file - Master template file for the forecast model.
    #        post_process_type - Keyword identifying post-processing for
    #                                     for the input catalog.
    #        start_date - Start date of the forecast. Default is None.    
    #        end_date - End date of the forecast. Default is None.
    # 
    def __init__ (self, dir_path,  
                        template_file,
                        post_process_type, 
                        start_date = None,
                        end_date = None):
        """ Initialization for Forecast class"""
        
        # Call base class constructors
        ReproducibilityFiles.__init__(self)
        CSEPStorage.__init__(self, dir_path)

        # Directory to store forecasts files to
        self.dir = dir_path
        
        # Instantiate post-processing object used to prepare input catalog
        self.__postProcess = post_process_type
        if self.__postProcess is not None:
            self.__postProcess = PostProcessFactory().object(post_process_type)

        # Forecast template file to be used by the model
        self.templateFile = template_file
        
        # Start date of the forecast (None for 1-day forecasts models)
        self.__startDate = start_date

        # Start date of the forecast (None for 1-day forecasts models)
        self.__endDate = end_date
        
        # Directory with catalog data
        self.catalogDir = None
        
        # Filename for forecast file to be generated
        self.__forecastFile = None
        
        # Control file for running the model
        self.parameterFile = None
        
        # Top-level forecasts archive directory to store
        # intermediate files if any required by forecast generation
        self.archive = None
        

    #--------------------------------------------------------------------
    #
    # Returns True if specified filename is a forecast model, False 
    # otherwise.
    # A filename is identified as a model file if:
    # 1. It is not a directory
    # 2. Is not a backup file
    # 3. Is not an 'ignore_name' file if such is provided
    #
    # Input: 
    #        file_path - Path to the file.
    #        ignore_name - Filename that should be ignored when classifying
    #                      entry for the forecast model. Default is None.
    #        ignore_extension - List of filename extensions that should be 
    #                           ignored when classifying directory entry for the 
    #                           forecast model. Default is None.
    #
    # Output:
    #         True if filename satisfies forecast model rules, False 
    #         otherwise.
    #
    @staticmethod
    def isFile (file_path, 
                ignore_name = None,
                ignore_extension = None):
        """ Returns True if specified filename is a forecast model, False 
            otherwise."""
        
        result = True
        
        if ignore_name is not None:
           result = (file_path != ignore_name)
           
        if ignore_extension is not None:
           
           for each_extension in ignore_extension:
               # Pattern for filenames with extensions that should be ignored
               # (metadata files)
               pattern_obj = re.compile('.+' + each_extension + '$')
               
               result = result and \
                        pattern_obj.match(file_path) is None
        
        return result and \
               os.path.isdir(file_path) is False and \
               Forecast.__backupFilenamePattern.match(file_path) is None
    
    
    #----------------------------------------------------------------------------
    #
    # Returns name of archive directory for the forecast file. Directory name is
    # based on the year and month that are part of the forecast file.
    #
    # Input: 
    #        filename - Name of the forecast file.
    #
    # Output:
    #        Archive directory to be used for the file, or None if filename 
    #        is not conforming to the CSEP forecast naming convention (was not
    #        generated by CSEP) 
    #
    @staticmethod
    def archiveDir (filename):
        """ Returns archive directory name for the specified forecast file.""" 
        
        # Get the base name of the specified file
        model = os.path.basename(filename)
        
        # Search for date formatted string in the name
        model_date = re.search(r'%s\d+%s\d+%s\d+' %(Forecast.NameSeparator,
                                                    Forecast.NameSeparator,
                                                    Forecast.NameSeparator),
                               model)
     
        # Found match
        if model_date is not None:
            model_date_str = model_date.group(0).strip(Forecast.NameSeparator)
            
            try:
                model_start_date = datetime.datetime.strptime(model_date_str,
                                                              Forecast.NameSeparator.join(['%m', 
                                                                                           '%d', 
                                                                                           '%Y']))
                # Return archive directory that would represent forecast based
                # on it's start date
                return Forecast.NameSeparator.join(['%s' %model_start_date.year,
                                                    '%s' %model_start_date.month])
                 
            except ValueError:
                # Failed to read date from the filename - does not conform to CSEP 
                # forecast naming convention
                return None
            
        else:
            
            return None
        

    #--------------------------------------------------------------------
    #
    # Return keyword identifying the model.
    # This method is implemented by children classes.
    #
    # Input: None.
    #
    # Output:
    #           String identifying the type
    #
    def type (self):
        """ Returns keyword identifying the forecast model type."""
        
        pass


    #----------------------------------------------------------------------------
    #
    # Return sub-type keyword (if any) identifying the model.
    #
    # Input: None.
    #
    # Output:
    #           String identifying the sub-type if exists, empty string otherwise.
    #
    def subtype (self):
        """ Returns keyword identifying the forecast model sub-type."""
        
        return ''


    #----------------------------------------------------------------------------
    #
    # Scale forecast by a factor relative to the test date 
    #
    # Input: 
    #        forecast - numpy.array object that represents forecast data
    #        scale_factor - Scale factor for the forecast
    #
    # Output:
    #          NumPy.array with scaled forecast data
    #
    @staticmethod
    def scale (forecast,
               scale_factor):
        """ Scale forecast by provided factor (relative to the test date 
            since forecast start date)."""
        
        if scale_factor is None:
            return forecast
        
        # Scale forecast rate
        forecast[:, CSEPGeneric.Forecast.Format.Rate] *= scale_factor
        
        return forecast
     

    #----------------------------------------------------------------------------
    #
    # Return filename for the input catalog data.
    #
    # Input: None.
    #
    # Output:
    #           String identifying the filename.
    #
    def inputCatalogFilename (self):
        """ Returns filename of input catalog data."""
        
        return self.__postProcess.files.catalog


    #----------------------------------------------------------------------------
    #
    # Set start date for the forecast period.
    #
    # Input: 
    #        test_date - Forecast period start date
    # 
    # Output:
    #         None.
    # 
    def __setStartDate (self, test_date):
        """ Set start date for the forecast period."""

        self.__startDate = test_date
        return
     

    #----------------------------------------------------------------------------
    #
    # Set end date for the forecast period.
    #
    # Input: 
    #        test_date - Forecast period end date
    # 
    # Output:
    #         None.
    # 
    def __setEndDate (self, test_date):
        """ Set end date for the forecast period."""

        self.__endDate = test_date
        return

     
    #----------------------------------------------------------------------------
    #
    # Get start date for the forecast period.
    #
    # Input: None.
    # 
    # Output:
    #         datetime object.
    # 
    def __getStartDate (self):
        """ Get start date for the forecast period."""

        return self.__startDate

    start_date = property(__getStartDate, __setStartDate, 
                          doc = "Start date for the forecast period.")    


    #--------------------------------------------------------------------
    #
    # Get end date for the testing period used by the post-processing.
    #
    # Input: None.
    # 
    # Output:
    #         datetime object.
    # 
    def __getEndDate (self):
        """ Get end date for the forecast period."""

        return self.__endDate

    end_date = property(__getEndDate, __setEndDate, 
                        doc = "End date for the forecast period.")    


    #--------------------------------------------------------------------
    #
    # Return full path for the result forecast file.
    #
    # Input: None.
    #
    # Output:
    #           String identifying the filename.
    #
    def filename (self):
        """ Returns filename of generated forecast."""
        
        return self.rawFilename()
     

    #----------------------------------------------------------------------------
    #
    # Return full path for the original forecast file as it was created by
    # the forecast model code. CSEP populates master ForecastML XML-based 
    # template with forecast rates converted to (EQ per day per degree**2) units.
    #
    # Input: None.
    #
    # Output:
    #           String identifying the filename.
    #
    def rawFilename (self):
        """ Returns filename of original forecast as generated by the model."""
        
        return self.__forecastFile
     

    #--------------------------------------------------------------------
    #
    # Invoke forecast model.
    # This method is implemented by children classes.
    #
    # Input: None.
    #
    # Output: None.
    #
    def run (self):
        """ Invokes forecast model."""
        
        pass


    #---------------------------------------------------------------------------
    #
    # Returns flag if model is required to generate result file 
    # (forecast/detection/etc.) each time the model is invoked.
     
    # This method is overwritten by children classes if forecast file is optional
    #
    # Input: None.
    #
    # Output: True if model is required to generate forecast/detection/etc. file
    #         on each run of the model, False otherwise 
    #
    def resultIsRequired (self):
        """ Returns flag if model is required to generate result file 
            (forecast/detection/etc.) each time the model is invoked."""
        
        return True


    #----------------------------------------------------------------------------
    #
    # Set start and end date for the forecast period. This method should be
    # implemented by derived classes to calculate end date for the forecast.
    #
    # Input: 
    #        start_date - Forecast period start date.
    #        num_years - Forecast duration in years. Default is None.
    #        num_months - Forecast duration in months. Default is None.
    #        num_days - Forecast duration in days. Default is None.
    # 
    # Output:
    #         None.
    # 
    def setPeriod (self, 
                   start_date, 
                   num_years=None, 
                   num_months=None, 
                   num_days=None):
        """ Set start and end date for the forecast period."""

        self.__startDate = start_date
        self.__endDate = start_date
        
        if num_days is not None:
           self.__endDate += datetime.timedelta(days=num_days)

        end_year = self.__endDate.year
        end_month = self.__endDate.month
        
        if num_months is not None:
           end_month += num_months
           
           if end_month > 12:
              # Roll over into the next year
              end_month = end_month % 12
              end_year += 1

        if num_years is not None:
           end_year += num_years

           
        # Make sure day is within the month range    
        end_day = self.__endDate.day
        end_date_calendar = calendar.Calendar()
        month_days = [d for d in end_date_calendar.itermonthdays(end_year, 
                                                                 end_month) if d != 0]
        
        while end_day not in month_days:
           end_day -= 1
           
        self.__endDate = datetime.datetime(end_year,
                                           end_month,
                                           end_day,
                                           self.__endDate.hour,
                                           self.__endDate.minute,
                                           self.__endDate.second)
           
        return
     

    #----------------------------------------------------------------------------
    #
    # Compute number of days between given start and end date for the forecast 
    # period.
    #
    # Input: 
    #        start_date - Forecast period start date.
    #        end_date - Forecast period end date. 
    # 
    # Output:
    #         Number of days for the forecast period.
    # 
    def numDays (start_date, end_date):
        """ Compute number of days between given start and end date for the 
            forecast period."""

        from dateutil import rrule
        
        # End date is exclusive
        num_days = rrule.rrule(rrule.DAILY, 
                               dtstart=start_date, 
                               until=end_date).count()
        num_days -= 1
        return float(num_days)

    numDays = staticmethod(numDays)
     

    #--------------------------------------------------------------------
    #
    # Write input parameter file for the model.
    #
    # Input: 
    #        filename - Optional name of parameter file. Default is None,
    #                   meaning to use name of the parameter file as it is
    #                   formatted by the 'writeParameterFile' method.
    # 
    # Output:
    #          fhandle - Handle to generated parameter file.
    #        
    def writeParameterFile (self, 
                            filename = None):
        """ Format input parameter file for the model.
            Created file will be used by a forecast model to invoke the
            forecast generation."""

        self.parameterFile = self.type() + self.subtype() + "_control" + \
                             CSEPFile.Extension.ASCII

        if filename is not None:
            self.parameterFile = filename
      
        # Register input parameters file for reproducibility
        info_msg = "Input parameters file used by %s model to generate \
'%s' forecast file for %s." %(self.type(), 
                              self.rawFilename(), 
                              self.__startDate.date())

        # Record parameter file with reproducibility registry
        ReproducibilityFiles.add(self,
                                 self.parameterFile, 
                                 info_msg, 
                                 CSEPFile.Extension.ASCII)
        
        fhandle = file(self.parameterFile, 
                       CSEPFile.Mode.WRITE)
        
        return fhandle


    #---------------------------------------------------------------------------
    # Return flag that indicates if forecast model requires input catalog. 
    # Defauls is True meaning that forecast model requires input catalog 
    # from authorized data source.
    # 
    def requiresInputCatalog (self):
        """ Flag if forecast model requires input catalog. Default is True meaning  
            that forecast model requires input catalog from authorized data source."""
            
        return True


    #---------------------------------------------------------------------------
    # Set all metadata before creating forecast file.
    # 
    def setMetadata (self,
                     test_date, 
                     catalog_dir, 
                     archive_dir = None):
        """ Set all metadata before creating forecast file."""
            
        self.catalogDir = catalog_dir
        
        # Set forecast start and end date - derived model class will set this up
        self.setPeriod(test_date)
        
        # Create forecast file name
        filename = self.type() + self.subtype()

        filename = Forecast.NameSeparator.join([filename,
                                                "%s" %self.__startDate.month, 
                                                "%s" %self.__startDate.day, 
                                                "%s" %self.__startDate.year]) + \
                   CSEPFile.Extension.ASCII
                   
        self.__forecastFile = os.path.join(self.dir, filename)
        
        # Set top-level archive directory to the one provided (if any)
        self.archive = archive_dir


    #----------------------------------------------------------------------------
    #
    # Create forecast.
    # This method is implemented by children classes.
    #
    # Input: 
    #       test_date - datetime object that represents testing date.
    #       catalog_dir - Directory with catalog data
    #       archive_dir - Directory to store intermediate model results if any.
    #                     Default is None.
    #        data_source - Optional catalog data source. Default is None.
    #                      In a case when raw data download is disabled, need
    #                      to stage existing raw catalog data based on metadata
    #                      of existing data product. 
    #        
    # Output:
    #        List of names for created forecast files.
    #
    def create (self, 
                test_date, 
                catalog_dir, 
                archive_dir = None,
                data_source = CatalogDataSource()):
        """ Generate forecast."""

        # To support hybrid forecasts, have to have it as a separate method
        self.setMetadata(test_date, 
                         catalog_dir, 
                         archive_dir)

        # Check if forecast file already exists - generated by other 
        # ForecastGroup or if reprocessing:
        if os.path.exists(self.filename()) is False:

           Forecast.Logger.info("Creating forecast: %s" %self.filename())
           
           # Check if forecast file is archived 
           if archive_dir is not None:
               
              archive_forecast_dir = os.path.join(archive_dir,
                                                  Forecast.archiveDir(self.filename()))
              
              # Stage -fromXML format of the forecast if it's available
              staged_forecasts = []
              
              if CSEP.Forecast.UseXMLMasterTemplate:

                  from_xml_filename = CSEP.Forecast.fromXMLTemplateFilename(self.filename())
                  
                  Forecast.Logger.info("Checking for existence of %s forecast" %from_xml_filename)
                  
                  if CSEPStorage.stage(self, 
                                       [os.path.basename(from_xml_filename)],
                                       archive_forecast_dir) is True:
                          
                      # File has been staged
                      staged_forecasts.append(os.path.basename(from_xml_filename))
              
                  
              if CSEPStorage.stage(self, 
                                   [os.path.basename(self.filename())],
                                   archive_forecast_dir) is True:
              
                  # File has been staged
                  staged_forecasts.append(os.path.basename(self.filename()))
             
              else:
                  # Set search criteria for the file of interest  - in a case when
                  # raw catalog file should be staged based on metadata of existing
                  # forecast file
                  data_source.dirSearchCriteria(self.filename(),
                                                archive_forecast_dir)

              if len(staged_forecasts):
                  return staged_forecasts
                   
           
           # Prepare input catalog file and store it in specified directory
           self.__prepareCatalog(data_source)
           
           # Write parameter file
           self.writeParameterFile()
           
           # Invoke the model
           self.run()
           
           if os.path.exists(self.filename()) is True:
           
               # Create metadata file for the forecast 
               comment = "%s forecast file with start date '%s' and end date '%s'" \
                         %(self.type(), self.__startDate, self.__endDate)
                         
               Forecast.metadata(self.filename(), 
                                 comment, 
                                 archive_dir)
               
               
               # Generate unique copies of files required for forecast reproducibility
               ReproducibilityFiles.copyAndCleanup(self,
                                                   self.type())

           # Return empty list only if forecast file is optional for the model run
           elif self.resultIsRequired() is False:
                
               # Forecast file is not generated
               return [] 
        
        return [os.path.basename(self.filename())]
     
     
    #---------------------------------------------------------------------------
    #
    # Prepare input catalog for the model.
    #
    # Input: data_source - Catalog data source. This object is used only if
    #                      download of raw catalog data is disabled, and
    #                      existing raw catalog file needs to be staged for
    #                      processing. 
    #        
    def __prepareCatalog (self,
                          data_source):
        """ Process already downloaded pre-processed catalog data for 
            the input to the forecast model, or stage already existing raw
            catalog file based on metadata of existing forecast file if it's
            a re-processing."""
    
   
        # Some forecasts don't require input catalog
        if self.requiresInputCatalog() is False:
            return
        
        
        # Generate input catalog if it doesn't exist - all models of the
        # same test group will use the same input catalog
        catalog = RELMCatalog(self.catalogDir, 
                              data_source, 
                              self.__postProcess)
        
        # Re-use downloaded raw data that is already pre-processed, or
        # stage existing raw data traced down through metadata of existing
        # forecast file
        catalog.create(self.__startDate,
                       self.catalogDir)


    #----------------------------------------------------------------------------
    #
    # Create metadata file for the forecast file and store it in the 'archive'
    # directory.
    #
    # Input:
    #        filepath - Path to the forecast file
    #        comment - Comment for the forecast file
    #        archive_dir - Archive directory
    #
    # Output:
    #         List of existing forecasts files.
    #
    @staticmethod
    def metadata (filepath, comment, archive_dir = None):
       """ Create metadata file for the forecast file and store it in the 'archive'
directory."""
        
       # Create metadata file for the forecast 
       metafile = CSEPPropertyFile.CSEPPropertyFile.metaFilename(filepath)
        
       CSEPPropertyFile.CSEPPropertyFile.createMetafile(metafile, 
                                                        os.path.basename(filepath),
                                                        CSEPFile.Extension.toFormat(filepath),
                                                        comment)
        
       # Move metadata file to the archive directory - the forecast file
       # will be moved there later
       if archive_dir is not None:
          new_path = os.path.join(archive_dir, 
                                  os.path.basename(metafile))
          os.renames(metafile, new_path)
          
       return
    

    #===========================================================================
    # createMagnitudeDistributionPlot
    # 
    # This method creates magnitude distribution plot for the forecast model.
    #
    # Inputs:
    #         forecast_path - Path of the forecast file in ASCII format.
    #         result_dir - Directory to store result image file to. Default is
    #                      '.' (current runtime directory)
    # 
    #===========================================================================
    @staticmethod
    def createMagnitudeDistributionPlot(forecast_path,
                                        result_dir = '.'):
        """ Create magnitude distribution plot for the forecast model"""
        
        # Full forecast path
        forecast_file = os.path.basename(forecast_path)
        
        np_forecast = ForecastHandlerFactory().CurrentHandler.load(forecast_path)
                    
        # Load forecast 
        forecast = np_forecast

        # Reduce forecast to the valid locations if weights flag is enabled
        if CSEP.Forecast.UseWeights is True:
            weights = np_forecast[:, CSEPGeneric.Forecast.Format.MaskBit].astype(int)
                  
            # Select the rows to be used
            selected_rows = weights > 0
            forecast = np_forecast[selected_rows, :]

        
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
            res = np.where(forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] == magnitude_forecast[index, 
                                                                                                 CSEPGeneric.Forecast.Format.MinMagnitude])
            sel_rows, = np.where(forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude] == magnitude_forecast[index, 
                                                                                                 CSEPGeneric.Forecast.Format.MinMagnitude])
            selection = forecast[sel_rows, :]
            sel_rows, = np.where(selection[:, CSEPGeneric.Forecast.Format.MaxMagnitude] == magnitude_forecast[index, 
                                                                                                  CSEPGeneric.Forecast.Format.MaxMagnitude])
            selection = selection[sel_rows, :]

            # The magnitude rate is the sum over all constituent bins
            magnitude_forecast[index, CSEPGeneric.Forecast.Format.Rate] = selection[:, CSEPGeneric.Forecast.Format.Rate].sum()
        
        num_quakes_forecast = ForecastHandlerFactory().CurrentHandler.numberEvents(magnitude_forecast[:, CSEPGeneric.Forecast.Format.Rate])

        # Normalize forecast
        magnitude_forecast[:, CSEPGeneric.Forecast.Format.Rate] /= num_quakes_forecast

        # Plot magnitude
        __width = 0.05       # the width of the bars
        
        fig = plt.figure()
        ax1 = fig.add_subplot(111)

        rect1 = ax1.bar(magnitude_forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude], 
                        magnitude_forecast[:, CSEPGeneric.Forecast.Format.Rate], 
                        __width, 
                        color='b')
        #print "Rate=", magnitude_forecast[:, CSEPGeneric.Forecast.Format.Rate]
        
        ax1.set_title(CSEPFile.Name.extension(forecast_file))
        ax1.set_ylabel('Pr (Magnitude)', color='b')
        ax1.set_xlabel('Magnitude')
        for tick in ax1.get_yticklabels():
            tick.set_color('b')

        ax1.set_ylim(0, 
                     magnitude_forecast[:, CSEPGeneric.Forecast.Format.Rate].max() + 0.1)
            
        #ax = fig.add_subplot(212)
        ax2 = ax1.twinx()
        rect2 = ax2.bar(magnitude_forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude], 
                        np.log10(magnitude_forecast[:, CSEPGeneric.Forecast.Format.Rate]),
                        __width, 
                        color='g')
        
        ax2.set_ylabel(r'$\log_{10}$' + '(Pr (Magnitude))', color='g')
        for tick in ax2.get_yticklabels():
            tick.set_color('g')

        ax2.set_xlim(magnitude_forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude].min() - 1.0, 
                     magnitude_forecast[:, CSEPGeneric.Forecast.Format.MinMagnitude].max() + 1.0)

        #plt.show()
        
        # Create result directory if it doesn't exist (when maps are generated
        # in stand-alone mode)
        if os.path.exists(result_dir) is False:
            os.makedirs(result_dir)
        
        # Replace extension with '.svg' for the image file
        image_file = Forecast.MagnitudeDistributionPrefix + \
                     os.path.basename(forecast_file).replace(CSEPFile.Extension.replace(CSEPFile.Extension.SVG,
                                                                                        forecast_file),
                                                             CSEPFile.Extension.SVG)
        
        image_path = os.path.join(result_dir,
                                  image_file)
        plt.savefig(image_path)
        
        return image_path
        

if __name__ == '__main__':
    
    ### Stand-alone functionality to be used by miniCSEP distribution
    import optparse
    from CSEPOptions import CommandLineOptions
    
    
    #===========================================================================
    # Command-line options for the module when invoked in stand-alone mode
    #===========================================================================
    class ForecastOptions (optparse.OptionParser):
        
        ForecastOption = "--forecast"
        MagnitudeDistributionOption = "--enableMagnitudeDistributionPlot"
                
        
        #-----------------------------------------------------------------------
        # Initialization.
        #        
        def __init__ (self):
            """ Initialization for CSEPOptionParser class"""
            
            # Report CSEP version on request (--version option)        
            optparse.OptionParser.__init__(self, version = CSEP.Version)
            
            # Define options
            self.add_option(ForecastOptions.ForecastOption, 
                            dest="forecast",
                            default=None,
                            help="Filename of input forecast. Default is None.") 

            self.add_option(ForecastOptions.MagnitudeDistributionOption, 
                            action="store_true", 
                            dest="magnitude_plot", 
                            default=False, 
                            help="Create magnitude distribution plot for the forecast. \
Default is not to generate magnitude distribution plot.")

            # To be used if spawned by BatchProcessing module            
            self.add_option(CommandLineOptions.LOG_FILE, 
                            dest="log_file", 
                            type="string",
                            help="Log file used to capture progress and error \
messages to. This option is used only to make the software aware of the file \
where it's output was redirected to. Caller has to explicitly redirect output \
and error streams to the specified file. Default is stdout stream handler.", 
                            metavar="FILE",
                            default=None)
            
            self.add_option(CommandLineOptions.TEST_DIR,
                            dest="test_dir", 
                            type="string",
                            default=".",
                            help="Directory to store results files to. \
Default is '.' (current run-time directory).", 
                            metavar="DIR") 
            

        #--------------------------------------------------------------------
        #
        # Get command line options values.
        #
        # Input: None
        # 
        # Output:
        #        Map of command line options and their values.
        #
        def options (self):
            """Get command line options and their values."""
    
            # Parse command line arguments
            (values, args) = self.parse_args()
            
            return values
        
    # End of Forecast class


    parser = ForecastOptions()
    options = parser.options()
    
    
    ### Create magnitude distribution
    if options.magnitude_plot is True:
        
        result_file = Forecast.createMagnitudeDistributionPlot(options.forecast, 
                                                               options.test_dir)
        Forecast.Logger.info('Magnitude distribution of the %s forecast is stored in %s file.' %(options.forecast,
                                                                                          result_file)) 

