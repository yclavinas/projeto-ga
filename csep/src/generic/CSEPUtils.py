"""
CSEPUtils module

Stores utilities used by the CSEP computing framework.
 
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import scipy.stats, scipy.special, calendar
import numpy as np


#-----------------------------------------------------------------------------
#
# Detects indices of list elements that have values less than 
# given value.
#
# Input: 
#        simulations - List of simulations results
#        value - Maximum element value for search criteria.
#    
# Output:
#        List of indices.
#
def __lessValueIndices(simulations, value):
    """Detects indices of list elements that have values less than
       specified value."""
         
    sims_len = len(simulations)

    # Return list of indeces for found simulations values
    return [i for i in xrange(sims_len) if simulations[i] <= value]
   
   
#-----------------------------------------------------------------------------
#
# Calculate probability of the event: frequency of event occurrence within
# given number of simulations.  
#
# Input: 
#        event_count - True event count for the simulations.
#        simulations - List of simulations results
#    
# Output:
#        Frequency of 'event_count' occurrence.
#
def frequencyOfOccurrence(event_count, simulations):
    """ Calculate frequency of less than event value occurrences within
        givin number of simulations."""
          
    return len(__lessValueIndices(simulations,
                                  event_count)) / float(len(simulations))
   

#-----------------------------------------------------------------------------
#
# Poisson cumulative distribution function.
#
# P = poissonCDF(x, lambda_param) computes the Poisson cumulative
# distribution function with parameter lambda_param at the values in x.   
#
# Input: 
#        x - List of values
#        lambda_param - Scalar or list containing lambda parameter for distribution.
#    
# Output:
#        Poisson CDF value
#
def poissonCDF(x, lambda_param):
    """ P = poissonCDF(x, lambda_param) computes the Poisson cumulative
        distribution function with parameter lambda_param at the values in x"""

    param = lambda_param
    
    if isinstance(lambda_param, list) is True:
        param = lambda_param[0]
        
    return float(scipy.stats.poisson.cdf(x, param))


#-----------------------------------------------------------------------------
#
# Generate normally distributed random errors.
#
# Inputs:
#         error - numpy array object with errors to randomize
#         random_num - numpy array object with of random numbers
#    
# Output:
#        Vector of normally distributed random values
#
def normalRandom(error, random_num):
    """ Generate normally distributed random errors """
    
    # mu is zero, sigma is error
    __MU = 0.0
    
    # Sigma is equal to 'error'
    return np.array([scipy.stats.norm.ppf(__r, __MU, __e) for __r, __e in zip(random_num, error)])


#===============================================================================
# Calculates the natural logarithm of the Poisson probability density function.
# Function returns the log of the Poisson probability density function with 
# parameter LAMBDA at the values in X.
#
# Input:
#        x - Parameter x (see help for Matlab's 'poisspdf')
#        lambda_param - Parameter lambda (see help for Matlab's 'poisspdf')
#
# Output: Natural logarithm of the Poisson probability density 
#        
#===============================================================================
def logPoissonPDF(x, lambda_param):
    """Calculates natural logarithm of the Poisson probability density function."""
    
    
    # Create emtpy matrix for results
    result = np.zeros_like(x)
    if result.size != 0:

        sel = lambda_param < 0
        result[sel] = np.NaN
        
        # Select all computable elements
        sel = (x >= 0)
        total_sel = (x == np.round(x))
        
        total_sel = np.logical_and(sel,
                                   total_sel)
        
        sel = (lambda_param >= 0)
        total_sel = np.logical_and(sel,
                                   total_sel)

        # Smallest positive double precision floating point number
        __real_min_float =  np.finfo(np.double).tiny.item()
        
        # Adding of realmin to 0 cases is to get the effect of 0^0 = 1.
        lambda_zero = (lambda_param[total_sel]==0).astype(float)

        # ATTN: np.any() returns
        # >>> type(np.any(a))
        # <type 'numpy.bool_'>
        # which is not Python's True, therefore can't use 'result is True' evaluation 
        if np.any(total_sel) == True:

            result[total_sel] = -lambda_param[total_sel] + \
                                x[total_sel] * (np.log(lambda_param[total_sel] + __real_min_float*lambda_zero)) - \
                                scipy.special.gammaln(x[total_sel] + 1)
                    
    return result
    

#===============================================================================
# Swap key:value of dictionary.
#
# Input:
#        exist_dict - Existing dictionary
#
# Output: new dictionary with values as keys, and keys as values 
#   
#===============================================================================
def swapDictionary(exist_dict):
    """Create new dictionary by swapping key and value of existing dictionary"""
    
    new_dict = {}
    
    for key, value in exist_dict.iteritems():
        new_dict.setdefault(value, []).append(key)
    
    return new_dict


#===============================================================================
# Convert given test date to the decimal year representation 
#
# Input:
#        test_date - Date to convert to decimal year notation
#
# Output:
#        Decimal year representation of the date.
#
#===============================================================================
def decimalYear(test_date):
    """ Convert given test date to the decimal year representation."""
    
    if test_date is None:
        return None
    
    
    # This implementation is based on the Matlab version of the 'decyear' 
    # function that was inherited from RELM project
    __hours_per_day = 24.0
    __mins_per_day = __hours_per_day * 60.0
    __secs_per_day = __mins_per_day * 60.0
    
    # Get number of days in the year of specified test date
    num_days_per_year = 365.0
    if calendar.isleap(test_date.year) is True:
        num_days_per_year = 366.0
    
    # Compute number of days in months preceding the test date 
    # (excluding the month of the test date)
    num_days = sum([calendar.monthrange(test_date.year, i)[1] for i in xrange(1, test_date.month)])
    
    dec_year = test_date.year + (num_days + (test_date.day - 1) + \
                                 test_date.hour/__hours_per_day + \
                                 test_date.minute/__mins_per_day + \
                                 # test_date.second/__secs_per_day)/num_days_per_year
                                 (test_date.second + test_date.microsecond * 1e-6)/__secs_per_day)/num_days_per_year
    return dec_year
    
    