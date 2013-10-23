"""
   CSEPInputParams module
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import copy
import CSEPLogging


#--------------------------------------------------------------------------------
#
# CSEPInputParams
#
# This class is designed to represent input parameters that might be passed
# to forecast models, data source for catalog retrieval. 
#
class CSEPInputParams:

    # Static data of the class

    # Character used to separate input arguments for different objects
    InputSeparator = '|'

    # Character used to separate input arguments for the same object
    __inputFieldSeparator = ','

    # Character used to separate input key and value
    __keyValueSeparator = '='

      
    #----------------------------------------------------------------------------
    #
    # Parse input arguments if any.
    #
    # Input:
    #        input_dictionary - Dictionary of supported input arguments 
    #                           with their default values.
    #        args - String representation of user provided dictionary of 
    #               input arguments.
    #
    # Output:
    #        deep copy of 'input_dictionary' if 'args' is None, updated deep copy 
    #        of dictionary if 'args' is not None.
    #
    @staticmethod
    def parse (input_dictionary, args):
        """ Parse input arguments if any and return updated dictionary
            of arguments."""

        # Create new object from default dictionary and return it to the caller
        # with modified values as specified by 'args'
        return_dictionary = copy.deepcopy(input_dictionary)
        
        # Input arguments were provided:
        if args is not None:
           args_pairs = args.split(CSEPInputParams.__inputFieldSeparator)
           
           for each_pair in args_pairs:
              # Strip whitespaces from key and value
              key, value = [token.strip() for token in \
                            each_pair.split(CSEPInputParams.__keyValueSeparator)]
              
              if return_dictionary.has_key(key):
                 return_dictionary[key] = value
              else:
                 error_msg = "Unknown input argument '%s' is specified. \
Supported arguments are %s." \
                             %(key, input_dictionary.keys())
                             
                 CSEPLogging.CSEPLogging.getLogger(CSEPInputParams.__name__).error(error_msg)
                 raise RuntimeError, error_msg

        
        return return_dictionary

