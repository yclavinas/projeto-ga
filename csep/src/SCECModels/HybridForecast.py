"""
HybridForecast module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os, datetime, ast, glob
import numpy as np

import CSEPLogging, CSEP, CSEPFile, CSEPGeneric
from ForecastHandlerFactory import ForecastHandlerFactory
from Forecast import Forecast


#-------------------------------------------------------------------------------
#
# HybridForecast forecast model.
#
# This class is designed to automate hybrid forecast generation based
# on existing forecasts models installed within testing center. Hybrid model
# can use file-based forecasts or dynamically created forecasts (with installed
# codes) within the testing center.
#
class HybridForecast (Forecast):

    # Static data of the class 

    # Master XML template file to populate with forecast rates (should be set
    # through configuration file to the desired template)
    TemplateFile = None

    __logger = None
    
    class XML (object):
        
        # Runtime ID for the model
        NameAttribute = 'name'
        
        # Operator to apply to contributing components (for example, 
        # max() for AVMAX model)
        OperatorAttribute = 'operator'
        
        # Files attribute if contributing models are file-based within testing
        # framework (no code is available to invoke the model, aka "black-box" model)
        FilesAttribute = 'files'

        # Files attribute if contributing models are identified by provided tokens 
        # (models generated intermediate forecasts files such as TimeVariant (TV) component of the forecast)
        TokensAttribute = 'tokens'
        
        DirAttribute = 'dir'
        WeightsAttribute = 'weights'
        # Keyword to introduce variable value into configuration file:
        # to be replaced by provided value in the attribute
        NAttribute = "N" 
        
        # Name of component element for the hybrid (to apply operator to)
        ComponentElement = 'component'
        
        # Name of one of component's group element 
        # (to sum up rates to get total component rate) 
        GroupElement = 'group'

    # Forecast group with weights and requested models or files for the contribution
    class GroupInfo (object):
        
        def __init__ (self,
                      weights,
                      files,
                      models_types=None,
                      files_tokens=None):
            self.weights = weights
            self.files = files
            self.models = models_types
            self.tokens = files_tokens
            

    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        hybrid_elem - XML element of the DOM tree to represent hybrid model
    #        init_file - XML element representing the model
    #        forecast_group - Forecast group for the hybrid model
    # 
    def __init__ (self,
                  hybrid_elem = None,
                  init_file = None, 
                  forecast_group = None):
         """ Initialization for HybridForecast class"""

         from ForecastGroup import ForecastGroup
         
             
         # Initialize logger for the class
         if HybridForecast.__logger is None:
             HybridForecast.__logger = CSEPLogging.CSEPLogging.getLogger(HybridForecast.__name__)
         
         group_dir = forecast_group
         if not isinstance(forecast_group, str):
             group_dir = forecast_group.dir()
             
         Forecast.__init__(self, 
                           group_dir, 
                           HybridForecast.TemplateFile,
                           None) # No post-processing is necessary???
         
         # Dictionary of {'forecast group': [models]} contributing to the hybrid
         # Each component is a dictionary of groups
         self.components = {}
         
         self.Type = None
         self.operator = None

         # Initialization of the forecast is done through XML 
         # configuration file
         if hybrid_elem is not None:
          
             # Index into model's components
             index = 0
             
             # Parse out components from XML init file that contribute to the model
             for each_component in init_file.nextChild(hybrid_elem,
                                                       HybridForecast.XML.ComponentElement):
                 
                 self.components[index] = {}
    
                 # Check if variable is provided for the group (to be replaced by
                 # it's value in weights)
                 Nvar = ""
                 if HybridForecast.XML.NAttribute in each_component.attrib:
                     Nvar = eval(each_component.attrib[HybridForecast.XML.NAttribute],
                                 {}, {})
                     # Replace with string representation
                     Nvar = repr(Nvar)
    
                 # Parse each component
                 for each_group in init_file.nextChild(each_component,
                                                       HybridForecast.XML.GroupElement):
    
                     # Check if forecast group directory is provided, then 
                     # forecast group for provided directory should be created
                     group_dir = forecast_group.dir
                     if HybridForecast.XML.DirAttribute in each_group.attrib:
                         group_dir = each_group.attrib[HybridForecast.XML.DirAttribute]
    
                     # Extract weights for each model
                     print "Nvar=", Nvar, "weights=", each_group.attrib[HybridForecast.XML.WeightsAttribute]
                     
                     weights_txt = each_group.attrib[HybridForecast.XML.WeightsAttribute].replace(HybridForecast.XML.NAttribute,
                                                                                                  Nvar)
                     models_weights = eval(weights_txt,
                                           {}, {})
                    
                     # Check if specific models are requested within the group
                     group_models = None
                     if each_group.text is not None:
                         models_types = each_group.text.strip()
                         if len(models_types):
                             group_models = models_types.split()
                 
                     # If forecast group includes file-based models, then
                     # specific filenames should be requested by the component
                     group_files = None
                     if HybridForecast.XML.FilesAttribute in each_group.attrib:
                         group_files = each_group.attrib[HybridForecast.XML.FilesAttribute].split() 
    
                     # If model produces intermediate forecasts (such as time-variant component)
                     # that are to be included into the group, then
                     # specific filename tokens should be provided
                     group_tokens = None
                     if HybridForecast.XML.TokensAttribute in each_group.attrib:
                         group_tokens = each_group.attrib[HybridForecast.XML.TokensAttribute].split() 
    
                     # Can't specify file-based and dynamic models within the same
                     # group
                     if group_models is not None and \
                        group_files is not None:
                         error_msg = "Can not provide file-based %s and dynamic models %s within the same forecast group %s" \
                                     %(group_files,
                                       group_models,
                                       group_dir)
                                     
                         HybridForecast.__logger.error(error_msg)
                         raise RuntimeError, error_msg
    
                     # Either models or file-based forecasts must be specified
                     if group_models is None and \
                        group_files is None and \
                        group_tokens is None:
                         error_msg = "%s configuration file: file-based or dynamic models or file tokens for dynamic models should be specified for the group representing %s directory" \
                                     %(init_file.name,
                                       group_dir)
                                     
                         HybridForecast.__logger.error(error_msg)
                         raise RuntimeError, error_msg
                      
                     # Instantiate forecast group if it's different than the one for
                     # the hybrid model
                     group = forecast_group
                     if group_dir != forecast_group.dir:
                         group = ForecastGroup(group_dir,
                                               model_list = group_models)
                         
                     # Add group with corresponding meta data into components dictionary
                     if group in self.components[index]:
                         error_msg = "%s configuration file: the same forecast group can't be included more than once per component: %s" \
                                     %(init_file.name,
                                       group.dir)
    
                         HybridForecast.__logger.error(error_msg)
                         raise RuntimeError, error_msg
                                      
                     self.components[index][group] = HybridForecast.GroupInfo(models_weights,
                                                                              group_files,
                                                                              group_models,
                                                                              group_tokens)
                 
                 if len(self.components[index]) == 0:
                     error_msg = "At least one <%s> element is expected within model's component (%s configuratin file)" \
                                 %(HybridForecast.XML.GroupElement,
                                   init_file.name)
    
                     HybridForecast.__logger.error(error_msg)
                     raise RuntimeError, error_msg
                     
                 # Increment component index            
                 index += 1
                 
                     
             # Check if name is provided
             if HybridForecast.XML.NameAttribute in hybrid_elem.attrib:
                 self.Type = hybrid_elem.attrib[HybridForecast.XML.NameAttribute]
                 
             else: 
                 error_msg = "Hybrid model name should be provided in '%s[%s]' element attribute of %s file" \
                             %(hybrid_elem.tag,
                               HybridForecast.XML.NameAttribute,
                               init_file.name)
                              
                 HybridForecast.__logger.error(error_msg)
                 raise RuntimeError, error_msg
    
    
             # Check if name is provided
             if HybridForecast.XML.OperatorAttribute in hybrid_elem.attrib:
                 self.operator = hybrid_elem.attrib[HybridForecast.XML.OperatorAttribute]
                 
             elif len(self.components) != 1: 
                 error_msg = "Operator for the hybrid model should be provided in '%s[%s]' element attribute of %s file" \
                             %(hybrid_elem.tag,
                               HybridForecast.XML.OperatorAttribute,
                               init_file.name) 
    
                 HybridForecast.__logger.error(error_msg)
                 raise RuntimeError, error_msg


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
        
        return self.Type


    #--------------------------------------------------------------------
    #
    # Write input parameter file for the model.
    #
    # Input: None
    #        
    def writeParameterFile (self, 
                            filename = None):
        """ Format input parameter file for the model."""

        # There is no parameter file for the hybrid model
        pass
    

    #---------------------------------------------------------------------------
    # Return flag that indicates if forecast model requires input catalog. 
    # Defauls is True meaning that forecast model requires input catalog 
    # from authorized data source.
    # 
    def requiresInputCatalog (self):
        """ Flag if forecast model requires input catalog. Default is True meaning  
            that forecast model requires input catalog from authorized data source."""
            
        return False


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
 
        if CSEP.Forecast.UseXMLMasterTemplate:
            return CSEP.Forecast.fromXMLTemplateFilename(self.rawFilename())

        return self.rawFilename()
    
    
    #--------------------------------------------------------------------
    #
    # Generate hybrid forecast
    #
    # Input: None
    #        
    def run (self):
        """ Generate hybrid forecast."""
        
        
        # Step through all components of the model, load each forecast and
        # apply corresponding weight to the rate, store result in list of numpy.array's
        np_rates = []
        
        forecast_file = None
        
        for comp_index in xrange(0, len(self.components)):
            
            for each_group, each_meta in self.components[comp_index].iteritems():
                 
                # Load file of the group
                HybridForecast.__logger.info("Component[%s] meta: files=%s models=%s tokens=%s" %(comp_index,
                                                                                                  each_meta.files, 
                                                                                                  each_meta.models,
                                                                                                  each_meta.tokens))
                if each_meta.files is not None:
                    
                    group_files = each_group.files()
                    HybridForecast.__logger.info("Group files %s vs. requested files %s" %(group_files,
                                                                                           each_meta.files))

                    # Load requested files, apply weights
                    for each_index, each_file in enumerate(each_meta.files):
                        # If XML template is enabled, make sure to use "from XML template"
                        # naming convention of the file
                        from_xml_filename = os.path.join(each_group.dir(),
                                                         each_file)
                        HybridForecast.__logger.info("Group %s file: %s" %(each_group.dir(),
                                                                           from_xml_filename))
                        
                        if CSEP.Forecast.UseXMLMasterTemplate:
                            from_xml_filename = CSEP.Forecast.fromXMLTemplateFilename(from_xml_filename)

                        forecast_file = self.__addWeightedForecast(from_xml_filename,
                                                                   each_index,
                                                                   forecast_file,
                                                                   comp_index,
                                                                   each_meta,
                                                                   np_rates)

                elif each_meta.tokens is not None:
                    
                    group_files = each_group.files()
                    HybridForecast.__logger.info("Group files %s vs. requested tokens %s" %(group_files,
                                                                                            each_meta.tokens))

                    # Load requested files, apply weights
                    for each_index, each_token in enumerate(each_meta.tokens):
                        # If XML template is enabled, make sure to use "from XML template"
                        # naming convention of the file
                        
                        from_xml = CSEPFile.Extension.ASCII
                        if CSEP.Forecast.UseXMLMasterTemplate:
                            from_xml = CSEP.Forecast.FromXMLPostfix + CSEPFile.Extension.ASCII 

                        found_files = glob.glob(os.path.join(each_group.dir(),
                                                             '%s*%s' %(each_token,
                                                                       from_xml)))
                        
                        if len(found_files) == 0:
                            error_msg = "No files exist for %s token under %s group directory" %(each_token,
                                                                                                 each_group.dir())
                            HybridForecast.__logger.error(error_msg)
                            raise RuntimeError, error_msg
                        
                        elif len(found_files) > 1:
                            error_msg = "More than one file exists for %s token under %s group directory: %s" %(each_token,
                                                                                                                each_group.dir(),
                                                                                                                found_files)
                            HybridForecast.__logger.error(error_msg)
                            raise RuntimeError, error_msg
                            
                        forecast_file = self.__addWeightedForecast(found_files[0],
                                                                   each_index,
                                                                   forecast_file,
                                                                   comp_index,
                                                                   each_meta,
                                                                   np_rates)
                    
                elif each_meta.models is not None:
            
                    group_models = each_group.models
                    HybridForecast.__logger.info("Group models %s vs. requested models %s" %(group_models,
                                                                                             each_meta.models))
                    
                    for each_index, each_model in enumerate(each_group.models):
                        
                        if each_model.type() in each_meta.models:
                            # Index into 'models types' requested by hybrid 
                            # (the same index should be used to access weights)
                            model_index = each_meta.models.index(each_model.type())
                            
                            # Model should've already generated it's forecast
                            model_file = each_model.filename()
                            
                            if CSEP.Forecast.UseXMLMasterTemplate:
                                model_file = CSEP.Forecast.fromXMLTemplateFilename(model_file)

                            forecast_file = self.__addWeightedForecast(model_file,
                                                                       model_index,
                                                                       forecast_file,
                                                                       comp_index,
                                                                       each_meta,
                                                                       np_rates)
                            #print "np_rates after", each_model.Type, np_rates
                    

        # Apply hybrid operator to the components to get final forecast
        if self.operator is not None:
            for each_index in xrange(0, np_rates[0].size):
                index_rates = [rates[each_index] for rates in np_rates]
                 
                forecast_file[each_index, CSEPGeneric.Forecast.Format.Rate] = eval('%s(%s)' %(self.operator,
                                                                                       index_rates))
                
        else:
            # No operator is provided, just use component cumulative rate as
            # hybrid forecast rate
            forecast_file[:, CSEPGeneric.Forecast.Format.Rate] = np_rates[0]
    
        # Write forecast to the file
        np.savetxt(self.filename(), 
                   forecast_file)
        
    
    #---------------------------------------------------------------------------
    #
    # Add weighted forecast to the hybrid forecast
    #
    # Input:
    #        
    def __addWeightedForecast (self, 
                               forecast,
                               forecast_index,
                               hybrid_forecast,
                               component_index,
                               meta,
                               np_rates):
        """ Add weighted forecast to the hybrid forecast."""

        np_forecast = ForecastHandlerFactory().CurrentHandler.load(forecast)
        
        if hybrid_forecast is None:
            # Create deep copy of very first loaded forecast to
            # prevent overwrite by sequencial loads
            hybrid_forecast = np_forecast.copy()
            
        else:
            
            # Validate that forecasts grids are consistent:
            if np.array_equal(np_forecast[:, CSEPGeneric.Forecast.Format.MinLongitude:CSEPGeneric.Forecast.Format.MaxMagnitude],
                              hybrid_forecast[:, CSEPGeneric.Forecast.Format.MinLongitude:CSEPGeneric.Forecast.Format.MaxMagnitude]) is False:
                
                error_msg = "%s HybridForecast: inconsistent grid is detected within %s forecast file" \
                            %(self.type(),
                              forecast)
                            
                HybridForecast.__logger.error(error_msg)
                raise RuntimeError, error_msg

        HybridForecast.__logger.info("Adding forecast %s to %s.component[%s] with weight %s" 
                                     %(forecast,
                                       self.Type,
                                       component_index,
                                       meta.weights[forecast_index]))
            
        
        # Take forecast's masking bit into consideration
        combined_mask = hybrid_forecast[:, CSEPGeneric.Forecast.Format.MaskBit].astype(int)
        combined_mask *= np_forecast[:, CSEPGeneric.Forecast.Format.MaskBit].astype(int)
              
        # Select the rows that have masking bit set - should be identical to
        # hybrid forecast
        rows_with_masking_bit = combined_mask > 0
        
        # Reset rates in bins that are masked out to zero not to contribute to the
        # hybrid
        np_forecast[~rows_with_masking_bit, CSEPGeneric.Forecast.Format.Rate] = 0.0
        
        # Reset any of already accumulated rates in bins that are masked out 
        # after processing current component to zero - should be excluded from
        # hybrid
        hybrid_forecast[~rows_with_masking_bit, CSEPGeneric.Forecast.Format.Rate] = 0.0
        
        # Set masking bit to new combined mask
        hybrid_forecast[:, CSEPGeneric.Forecast.Format.MaskBit] = combined_mask

        weighted_rate = np_forecast[:, CSEPGeneric.Forecast.Format.Rate]*meta.weights[forecast_index]
        
        if len(np_rates) <= component_index:
            np_rates.append(weighted_rate)
            
        else:
            
            # Step through all accumulated rates to reset rates in masked out bins
            # to zero to exclude from hybrid forecast
            for each_comp_index in xrange(0, len(np_rates)):
                np_rates[each_comp_index][~rows_with_masking_bit] = 0.0
                
            np_rates[component_index] += weighted_rate
    
    
        return hybrid_forecast
    