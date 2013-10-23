"""
Module DevianceResidualsTest
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os
from copy import deepcopy
from mpl_toolkits.basemap import Basemap
import matplotlib.mpl as mpl
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm as mpl_cm


import EvaluationTest, CSEPLogging, ReproducibilityFiles, CSEPFile, \
       Environment, GeographicalRegions
from DiagnosticsTest import DiagnosticsTest


#-------------------------------------------------------------------------------
#
# DevianceResidualsTest
#
# This class is designed to invoke deviance residuals evaluation test
# which is introduced to the CSEP Testing Framework by Robert Clements et al.
#
class DevianceResidualsTest (DiagnosticsTest):

    #===========================================================================
    # Nested class that represents DiagnosticsTest result data as 
    # dictionary type.
    # Derived classes should derive from the class to provide specifics of the
    # test results.    
    #===========================================================================
    class Result (DiagnosticsTest.Result):
        
        ModelNames = ['modelName1', 
                      'modelName2']
        
        
        #=======================================================================
        #        
        #=======================================================================
        def __init__ (self,
                      ascii_result_file, 
                      xml_elements,
                      test_args):
            """ Initialize method for DevianceResidualsTest.Result object"""
            
            DiagnosticsTest.Result.__init__(self,
                                            ascii_result_file, 
                                            xml_elements,
                                            test_args)
            
        
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
                      file_prefix):
            """Write test results to XML format file"""
          
          
            test_node, xml = DiagnosticsTest.Result.writeXML(self,
                                                             test_name,
                                                             model_filename,
                                                             dirpath,
                                                             file_prefix,
                                                             write_file = False)
            
            # Add model names to XML format file
            for __index in xrange(1, len(model_filename) + 1):
                name_node = xml.addElement(DevianceResidualsTest.Result.ModelNames[__index - 1],
                                           test_node)
                name_node.text = CSEPFile.Name.extension(model_filename[__index-1])
                
            xml.write()
            

    # Static data

    # Keyword identifying the class
    Type = "RD"

    __logger = None

    __minLongitude = 'minlon'
    __maxLongitude = 'maxlon'
    __minLatitude = 'minlat'
    __maxLatitude = 'maxlat'
    __mask1 = 'mask1'
    __mask2 = 'mask2'
    __deviance = 'deviance'

    __figureSize = (9, 9)


    xml = DiagnosticsTest.Result.XML(Type + EvaluationTest.EvaluationTest.FilePrefix,
                                     Result.ModelNames,
                                     __deviance,
                                     [__minLongitude, __minLatitude])


    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        group - ForecastGroup object. This object identifies forecast
    #                models to be invoked.
    #        args - Optional input arguments for the test. Default is None.    
    # 
    def __init__ (self, group, args = None):
        """ Initialization for DevianceResidualsTest class."""
        
        DiagnosticsTest.__init__(self, group, args)

        if DevianceResidualsTest.__logger is None:
           DevianceResidualsTest.__logger = CSEPLogging.CSEPLogging.getLogger(DevianceResidualsTest.__name__)


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

        # Prepare catalog
        DiagnosticsTest.prepareCatalog(self)

        test_name = '%s-%s' %(self.type(),
                              EvaluationTest.EvaluationTest.FilePrefix)

        # Skip all models up to and including the model passed to the script,
        all_models = deepcopy(self.forecasts.files())
        
        while len(all_models) != 0:
                       
            # Pop first element off
            pop_model = all_models.pop(0)
            
            if (forecast_name == pop_model):
                break
        

        # R package reports library load messages to stderr, ignore them 
        ignore_stdout_messages = True
            
                  
        # Iterate through remaining models
        for model in all_models:
            
            __forecasts = [forecast_name,
                           model]
            
            DevianceResidualsTest.__logger.info('%s for %s' %(test_name,
                                                              __forecasts))
            # Create parameter file for the run
            __script_file, __result_file = self.createParameterFile(__forecasts)
    
            # Record original ASCII result file as generated by evaluation code
            # with reproducibility registry
            info_msg = "Result file as generated by R code %s \
for %s diagnostics test for '%s' in '%s' directory." %(os.path.join(DiagnosticsTest._scriptsPath,
                                                                    self.execFunction()),
                                                       self.type(),
                                                       __forecasts,
                                                       self.forecasts.dir())
            
            ReproducibilityFiles.ReproducibilityFiles.add(self,
                                                          os.path.basename(__result_file),
                                                          info_msg,
                                                          CSEPFile.Format.ASCII)
    
            # Invoke test
            # Set executable permissions on the file
            os.chmod(__script_file, 0755)
            
            Environment.invokeCommand(__script_file,
                                      ignore_stdout_messages)
            
            # Convert ASCII results as generated by original R code to XML format
            test_result = DevianceResidualsTest.Result(__result_file,
                                                       self.xmlElements(),
                                                       self._getArgs())
            test_result.writeXML(test_name, 
                                 __forecasts, 
                                 self.testDir,
                                 self.filePrefix()) 


    #-----------------------------------------------------------------------------
    #
    # Returns description word for the test. Implemented by derived classes.
    #
    # Input: None
    #
    # Output: Description of the test (such RELMTest, AlarmTest, etc.)
    #
    def type (self):
        """ Returns test type identifier."""

        return DevianceResidualsTest.Type


    #===========================================================================
    # Write alpha to the parameter file for the test
    #===========================================================================
    def writeAlphaInfo(self, fhandle):
        """Write alpha for the test."""
        
        return fhandle


    #===========================================================================
    # Write R function to invoke for the test
    #===========================================================================
    def execFunction(self):
        """Return R source function for the test."""
        
        return 'deviance_residuals.R'


    #===========================================================================
    # Return list of XML elements that represent test results
    #===========================================================================
    @classmethod
    def xmlElements(cls):
        """Return list of XML elements that represent test results"""
        
        return [DevianceResidualsTest.__minLongitude,
                DevianceResidualsTest.__maxLongitude,
                DevianceResidualsTest.__minLatitude,
                DevianceResidualsTest.__maxLatitude,
                DevianceResidualsTest.__mask1,
                DevianceResidualsTest.__mask2,
                DevianceResidualsTest.__deviance]
    

    #----------------------------------------------------------------------------
    #
    # This method plots result data of evaluation test.
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

        
        doc, ax = EvaluationTest.EvaluationTest.plot(result_file) 

        # Extract region min/max longitude and latitude
        region = GeographicalRegions.Region.info()
        
        min_lat, max_lat, min_lon, max_lon = region.areaCoordinates(is_for_map = True)

        # Values from result file
        parent_name = cls.xml.Root
        min_lon_values_str = doc.elementValue(DevianceResidualsTest.__minLongitude,
                                              parent_name).split()
        min_lon_values = map(float, min_lon_values_str)

        min_lat_values_str = doc.elementValue(DevianceResidualsTest.__minLatitude,
                                              parent_name).split()
        min_lat_values = map(float, min_lat_values_str)

        if isinstance(min_lat, list) is False:
            # Values are provided for the region
            min_lon -= 1.0
            max_lon += 1.0
            min_lat -= 1.0
            max_lat += 1.0
            
        else:
            # Values are not provided, learn from result file
            min_lon = min(min_lon_values)
            if min_lon > -179.0:
                min_lon -= 1.0

            max_lon = max(min_lon_values)
            if max_lon < 179.0:
                max_lon += 1.0
                            
            min_lat = min(min_lat_values)
            if min_lat > -89.0:
                min_lat -= 1.0

            max_lat = max(min_lat_values)
            if max_lat < 89.0:
                max_lat += 1.0

        grid_meridians, grid_parallels = region.grid(coords=(min_lat, max_lat, min_lon, max_lon))
        
        fig = plt.figure(figsize = DevianceResidualsTest.__figureSize)        

        ### Generate map of the observed seismicity using ANSS catalog and
        ### specified magnitude threshold
        __map = Basemap(llcrnrlon=min_lon, urcrnrlon=max_lon, 
                        llcrnrlat=min_lat, urcrnrlat=max_lat, 
                        resolution='f')
        
#        # Load area coordinates for the testing region
#        area = np.loadtxt(CSEPFile.openFile(CSEPFile.Name.ascii(region.testArea)))
#        x, y = anss_map(area[:, 0], area[:,1])
#        anss_map.plot(x, y, 'y.', alpha = 0.1, zorder=100)
#        
        __map.fillcontinents(color = '0.95',
                             zorder = 10)
        __map.drawrivers(zorder=20, 
                         color = 'b', 
                         linewidth = 0.3)
        __map.drawstates(zorder=30, 
                         linewidth = 0.3)
        
        #map.fillcontinents(zorder=30)
        __map.drawcoastlines(zorder=40)

        # Draw longitude on the map 
        __map.drawmeridians(grid_meridians, 
                            labelstyle='+/-', 
                            labels=[1,1,0,1],
                            zorder=50)

        # Draw latitude on the map
        __map.drawparallels(grid_parallels,
                            labelstyle='+/-', 
                            labels=[1,1,1,1],
                            zorder=60)

        residual_values_str = doc.elementValue(DevianceResidualsTest.__deviance,
                                               parent_name).split()
        residual_values = map(float, residual_values_str)

        models_names = []
        for each_elem in DevianceResidualsTest.Result.ModelNames:
            models_names.append(doc.elementValue(each_elem))
        
        # Use pcolor with min(residuals)-1 value for not provided bins
        unique_min_lon_values = sorted(set(min_lon_values))
        unique_min_lat_values = sorted(set(min_lat_values))
        
        __xnum = len(unique_min_lon_values)
        __ynum = len(unique_min_lat_values)
        
        __datain = np.array([np.nan] * __xnum*__ynum)
        __datain.shape = (__ynum, __xnum)
        
        for each_lon, each_lat, each_residual in zip(min_lon_values, 
                                                     min_lat_values, 
                                                     residual_values):
            
            __lon_index = unique_min_lon_values.index(each_lon)
            __lat_index = unique_min_lat_values.index(each_lat)
            
            __datain[__lat_index, __lon_index] = each_residual

        # Create masked array to isolate testing region
        __datain_masked = np.ma.masked_where(np.isnan(__datain), __datain)

        unique_min_lon_values = np.array(unique_min_lon_values)
        unique_min_lat_values = np.array(unique_min_lat_values)
        
        __x, __y = __map(unique_min_lon_values, 
                         unique_min_lat_values)

        __cmap = mpl.cm.cool

        __map.pcolor(__x, __y, 
                     __datain_masked, 
                     cmap = __cmap,
                     zorder = 70, 
                     alpha = 0.3)
        
        cax = fig.add_axes([0.2, 0.05, 0.6, 0.02])

        colorbar = mpl.colorbar.ColorbarBase(cax, 
                                             cmap=__cmap,
                                             format='%2.1f',
                                             orientation='horizontal')
        
        # Return image filename
        return DiagnosticsTest._finishPlot(result_file,
                                           output_dir,
                                           "Deviance residuals (%s)" %(' vs. '.join(models_names)))
 
 
    #----------------------------------------------------------------------------
    #
    # This method plots summary result data of evaluation test.
    #
    # Input: 
    #         result_file - File with cumulative test results.
    #         output_dir - Directory to place plot file to. Default is None.     
    #
    @classmethod
    def plotSummary (cls, 
                     result_file, 
                     output_dir = None):
        """ Plot test results in XML format."""
 
        
        return cls.plot(result_file, 
                        output_dir)

