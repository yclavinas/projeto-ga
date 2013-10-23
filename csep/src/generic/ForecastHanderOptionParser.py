"""
Module ForecastHandlerOptionParser
"""

__version__ = "$Revision"
__revision__ = "$Id$"


import optparse
import CSEP


#===============================================================================
# Command-line options supported by the ForecastHandlerFactory.py module
#===============================================================================
class ForecastHandlerOptionParser (optparse.OptionParser):
    
    ForecastOption = "--forecast"
    StartDateOption = "--startDate"
    EndDateOption = "--endDate"
    TemplateOption = "--xmlTemplate"
    ConvertToXMLOption = '--toXML'
    ConvertToASCIIOption = '--toASCII'        
    
            
    #-----------------------------------------------------------------------
    # Initialization.
    #        
    def __init__ (self):
        """ Initialization for ForecastHandlerOptionParser class"""
        
        # Report CSEP version on request (--version option)        
        optparse.OptionParser.__init__(self, version = CSEP.Version)
        
        # Define options
        self.add_option(ForecastHandlerOptionParser.ForecastOption, 
                        dest="forecast",
                        default=None,
                        help="Filename of input forecast. Default is None.") 
 
        self.add_option(ForecastHandlerOptionParser.StartDateOption, 
                        dest="start_date", 
                        default=None,
                        help="Start date of the forecast in YYYY-MM-DDTHH:MM:SS format. Default is None.") 

        self.add_option(ForecastHandlerOptionParser.EndDateOption, 
                        dest="end_date", 
                        default=None,
                        help="End date of the forecast in YYYY-MM-DDTHH:MM:SS format. Default is None.") 

        self.add_option(ForecastHandlerOptionParser.TemplateOption, 
                        dest="xml_template", 
                        default=None,
                        help="Master XML template to populate with forecast information.") 

        self.add_option(ForecastHandlerOptionParser.ConvertToXMLOption, 
                        dest="convert_to_xml",
                        action='callback',
                        callback=ForecastHandlerOptionParser.__setConvertFormat,
                        help="Set conversion of the forecast to XML format.")

        self.add_option(ForecastHandlerOptionParser.ConvertToASCIIOption, 
                        dest="convert_to_ascii",
                        action='callback',
                        callback=ForecastHandlerOptionParser.__setConvertFormat,
                        help="Set conversion of the forecast to ASCII format.")


    #=======================================================================
    # Sanity check for dependent options when conversion is requested
    #=======================================================================
    @staticmethod
    def __setConvertFormat(option, opt_str, value, parser):
        """ Sanity check for dependent options when conversion is requested"""
        
        
        setattr(parser.values, option.dest, True)
        
        if opt_str == ForecastHandlerOptionParser.ConvertToXMLOption:
            # Check for required options
            if parser.values.forecast is None or \
               parser.values.start_date is None or \
               parser.values.end_date is None or \
               parser.values.xml_template is None:
                
               raise optparse.OptionConflictError("requires %s, %s, %s and %s options to be specified before %s" \
                                                  %(ForecastHandlerOptionParser.ForecastOption,
                                                    ForecastHandlerOptionParser.StartDateOption,
                                                    ForecastHandlerOptionParser.EndDateOption,
                                                    ForecastHandlerOptionParser.TemplateOption,
                                                    opt_str),
                                                   option)
                
        elif opt_str == ForecastHandlerOptionParser.ConvertToASCIIOption and \
             parser.values.forecast is None:
            
            raise optparse.OptionConflictError("requires %s option to be specified before %s"
                                               %(ForecastHandlerOptionParser.ForecastOption,
                                                 opt_str),
                                                 option)


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

