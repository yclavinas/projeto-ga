"""
Module CSEPSchedule
"""

__version__ = "$Revision: 3498 $"
__revision__ = "$Id: CSEPSchedule.py 3498 2011-11-10 20:29:19Z liukis $"

import datetime
import CSEPXML, CSEPLogging


#--------------------------------------------------------------------------------
#
# CSEPSchedule
#
# This module represents a schedule for the forecast groups:
# to invoke forecast models
# to invoke evaluation tests for existing forecast models.
#
class CSEPSchedule (object):

    # Static data members

    __logger = None

    # Value separator for range format:
    # 1985:1990   - values from 1985 up to 1990 inclusive with default increment of 1
    # 1985:1990:2 - values from 1985 up to 1990 inclusive with specified increment of 2
    __rangeSeparator = ':'
    
    # Default value for range increment if not provided by configuration file
    __defaultRangeIncrement = 1
    
    
    #--------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #       any_value - Character that represents 'any' value. Default is
    #                   CSEPXML.ANY_VALUE. 
    # 
    def __init__ (self, any_value = CSEPXML.ANY_VALUE):    
        """ Initialization for CSEPSchedule class."""
    
        if CSEPSchedule.__logger is None:
           CSEPSchedule.__logger = CSEPLogging.CSEPLogging.getLogger(CSEPSchedule.__name__)
           
        # Remember 'any' value
        self.__anyValue = any_value 
        
        # Flag to indicate that dictionary was set to the default state
        self.__initialized = True
        
        # Schedule dictionary of dictionaries in the format:
        # year : {month : [days]} 
        self.__dict = {any_value: {any_value: [any_value]}}


    #--------------------------------------------------------------------
    #
    # Add element to the dictionary.
    # 
    # Input: 
    #        year - Years.
    #        month - Months within the year.
    #        days - Days for specified months.
    #
    # Output: None.
    #
    def add (self, years, months, days):
        """ Add an entry to the schedule."""


        if self.isDefault() is True:
           # This is the first time entry is added to the dictionary,
           # remove default setting
           self.__dict = {}
           self.__initialized = False
        
        
        year_list = years.split()
        month_list = months.split()

        for each_year in year_list:
           CSEPSchedule.__logger.debug("Adding year=%s with month=%s days=%s" \
                                       %(each_year, months, days))
           
           # Support range of years if any is provided
           for year in CSEPSchedule.__rangeValues(each_year):

               # Support range of months if any is provided
               for each_month in month_list:
                   
                   for month in CSEPSchedule.__rangeValues(each_month):
                       
                       # Append specified days to the month:
                       for each_day in days.split():
                           self.__dict.setdefault(year, {}).setdefault(month, []).extend(CSEPSchedule.__rangeValues(each_day))
                           
        # print "DICT: ", self.__dict

    #--------------------------------------------------------------------
    #
    # Return values that correspond to specified range, or return original
    # value as a list if it does not represent range of values.
    # 
    # Input: 
    #        value - Value as provided in configuration file
    #
    # Output: None.
    #
    @staticmethod
    def __rangeValues(value):
        """ Return values that correspond to specified range, or return original
            value as Python's list if it does not represent range of values."""
            
        return_values = [value]
        
        # Range is provided, iterate over specified values
        if CSEPSchedule.__rangeSeparator in value:
            value_str = value.split(CSEPSchedule.__rangeSeparator)
               
            increment = CSEPSchedule.__defaultRangeIncrement
            if len(value_str) == 3:
                increment = int(value_str[-1])
        
            return_values = range(int(value_str[0]),
                                  int(value_str[1])+1,
                                  increment)
        
        return [str(each_value) for each_value in return_values]
        

    #--------------------------------------------------------------------
    #
    # Checks if specified date is within the schedule.
    # 
    # Input: 
    #        test_date - datetime object that represents test date.
    #
    # Output: True if date is within the schedule, False otherwise.
    #
    def has (self, test_date):
        """ Checks if specified date is within the schedule."""
      
        # If schedule was set as a default, then any date is within the schedule.
        if self.isDefault() is True:
           return True

        
        # Dictionary of matching years
        found_years = {}
        
        # Convert year to string: dictionary stores info in string format
        year_string = str(test_date.year)
        
        if year_string in self.__dict:
           found_years[year_string] = self.__dict[year_string]
           
        if self.__anyValue in self.__dict:
           found_years[self.__anyValue] = self.__dict[self.__anyValue]
        
        # Did not find matching or "any" year 
        if len(found_years) == 0:
           return False
        
        
        # Dictionary of matching months        
        found_months = {}

        # Convert month to string: dictionary stores info in string format
        month_string = str(test_date.month)

        # Search month dictionaries
        for month_dict in found_years.values():
           
           if month_string in month_dict:
              found_months.setdefault(month_string, []).extend(month_dict[month_string])
              
           if self.__anyValue in month_dict:
              found_months.setdefault(self.__anyValue, []).extend(month_dict[self.__anyValue])

        # Did not find matching or "any" month 
        if len(found_months) == 0:
           return False

        
        for day_list in found_months.values():
           
           # Has any day set
           if self.__anyValue in day_list:
              return True
           
           # Has requested day set (check for string representation of day)
           found_day = [s for s in day_list if s == str(test_date.day)]
           if len(found_day) >= 1:
              return True
        
           
        # Have not found day for specific year and month
        return False


    #---------------------------------------------------------------------------
    #
    # Flag if schedule is set to default: any date of any year.
    # 
    # Input: None
    #
    # Output: True if schedule is set to the default one (any date of any year).
    #
    def isDefault (self):
        """ Generator to return each date from the schedule in chronological order."""
      
        return self.__initialized is True 


    #----------------------------------------------------------------------------
    #
    # Generator method that iterates through all dates of the schedule.
    # 
    # Input: None
    #
    # Output: Next date in the schedule
    #
    def dates (self, 
               start_date = None, 
               stop_date = None):
        """ Generator to return each date from the schedule in chronological order."""
      
        import calendar
        
        
        schedule_calendar = calendar.Calendar()
        
        all_years = None
        
        # ATTN: the only condition is the start date must be explicitly set
        #       for the schedule - to know where to start iteration from
        if self.isDefault() is True or \
           self.__anyValue in self.__dict:
      
           # Check if start date is provided
           if start_date is not None:
               
               # Issue a warning that start_date.year is used as starting point,
               # and 10 years since that start date is assumed to be end year
               # for the schedule
               stop_year = start_date.year + 10
               if stop_date is not None:
                   stop_year = stop_date.year + 1
                   
               all_years = range(start_date.year, stop_year)
               
               msg = "%s: Year of provided start date (%s) is used since schedule provides ambiguous \
start date ('%s' value is specified for the year) within generator method" %(CSEPLogging.CSEPLogging.frame(CSEPSchedule),
                                                                             start_date,
                                                                             self.__anyValue)
        
               CSEPSchedule.__logger.warning(msg)
               
           else: 
               error_msg = "dates(): Start date is ambiguous for schedule \
(has '%s' value for the year) within generator method" %self.__anyValue
    
               CSEPSchedule.__logger.error(error_msg)
               raise RuntimeError, error_msg
           
        else:
            # Sort years of the schedule
            all_years = [int(year) for year in self.__dict.keys()]
            all_years.sort()

        
        for each_year in all_years:

           all_months = []
            
           # "Any" year is specified in the schedule
           if self.__anyValue in self.__dict:
               all_months = self.__dict[self.__anyValue]
               
           else:
               # Dictionary of months for the year
               all_months = self.__dict[str(each_year)]
                
           # Sort months and days
           months = []
           
           # "Any" month is specified
           if self.__anyValue in all_months:
              months = [i for i in xrange(1, 13)]
              
           else:
              months = [int(month) for month in all_months.keys()]
              months.sort()
              
           # Step through "day" list for each month
           for each_month in months:
              
              all_days = []

              # "Any" month was specified for the year
              if self.__anyValue in all_months:
                 all_days = all_months[self.__anyValue]
                 
              else:
                 all_days = all_months[str(each_month)]

              # Any day is specified for the month
              any_day = [s for s in all_days if s == self.__anyValue]

              if len(any_day) >= 1:
                 
                 # Find all valid days within a month: "0" is returned for day
                 # outside of the month but that is part of month week
                 all_days = [d for d in schedule_calendar.itermonthdays(each_year, 
                                                                        each_month) if d != 0]
              else:
                 all_days = [int(d) for d in all_days] 
              
              all_days.sort()
              
              for each_day in all_days:
                 
                 # Return current date within the schedule
                 next_date = datetime.datetime(each_year,
                                               each_month,
                                               each_day)
                 if (start_date is not None) and (next_date < start_date):
                     continue
                  
                 if (stop_date is not None) and (next_date > stop_date):
                     # Stop generator
                     return
                 
                 else:
                     yield next_date
              
        # Stop generator
        return


# Can't invoke the module - expects Python objects as inputs
