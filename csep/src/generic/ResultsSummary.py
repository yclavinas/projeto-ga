
"""
Module ResultsSummary
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import datetime, bisect
from xml.etree.cElementTree import ElementTree

import CSEPFile, CSEPInitFile, CSEPLogging


#--------------------------------------------------------------------------------
#
# ResultsSummary
#
# This class is designed to create and update XML format summary files 
# used by the CSEP software.
#
class ResultsSummary (CSEPInitFile.CSEPInitFile):

    # Static data members
    
    # Prefix used for filename with intermediate test results ("out of interest" 
    # results)
    Type = 'intermediate.'
    
    # Test date element tag: stores all processed test days
    TestDateElement = "testDate"
    
    __logger = None
    
    
    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        summary_file - Path for the results summary file.
    #        test_class - Reference to the class that represents evaluation test
    #                     for produced results.  
    # 
    def __init__ (self, 
                  summary_file, 
                  test_class,
                  root_element = "CSEPResultsSummary"):    
        """ Initialization for ResultsSummary class."""

        if ResultsSummary.__logger is None:
           ResultsSummary.__logger = CSEPLogging.CSEPLogging.getLogger(ResultsSummary.__name__)
           
        # Initialization file
        CSEPInitFile.CSEPInitFile.__init__ (self, 
                                            summary_file)

        if self.exists() is False:
           
           # Create file with specified root element
           CSEPInitFile.CSEPInitFile.addElement(self, 
                                                root_element)
        
        # Type of evaluation test 
        self.testClass = test_class 
        
        # CSEPInitFile object that represents results for a single test date
        self.testDateResults = None
        
        # Sorted list of all processed test dates (datetime.date objects) for the test
        self.processedDates = []

        self.testObj = None
        

    #---------------------------------------------------------------------------
    # Add evaluation test object required by cumulative summary (only if
    # evaluation test needs to be invoked to generate the summary - see
    # SuperThinnedResidualsTestingTest.py wrapper for one of diagnostics tests)
    #---------------------------------------------------------------------------
    def evaluationTest(self, test_obj):
        self.testObj = test_obj
        

    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def preserve(self):
        """ Flag if summaries should be preserved in daily tests results directory.
            Default is False, meaning not to preserve summary files on a daily basis."""
            
        return False
    

    #---------------------------------------------------------------------------
    #
    # Update results summary with test date results.
    #
    # Input: 
    #        result_file - File with test results for the date.
    #        test_date - datetime.date object that represents the test date
    #                    for the result files.   
    #        start_date - Start date for the forecast period. Default is None.
    #        end_date - End date for the forecast period. Default is None.
    # 
    def update (self, result_file, test_date, start_date = None, end_date = None):    
       """ Update summary file with test results for a particular date."""

       # 1. Check if test date is already in the cumulative:
       #    iterate through test dates
       processed_dates_elem = self.elements(ResultsSummary.TestDateElement)
       test_date_index = None

       # Instantiate result file object - check for existence
       self.testDateResults = CSEPInitFile.CSEPInitFile(result_file)
       if self.testDateResults.exists() is False:
          error_msg = "update(): Result file '%s' does not exist." %(result_file)
          
          ResultsSummary.__logger.error(error_msg)
          raise RuntimeError, error_msg
       
              
       if len(processed_dates_elem) != 0:

          # TestDate element exists: split string into datetime objects
          self.processedDates = [datetime.datetime.strptime(date_string, "%Y-%m-%d").date() for \
                                 date_string in processed_dates_elem[0].text.split()]
          
          # Search for test date
          if test_date in self.processedDates:
             test_date_index = self.processedDates.index(test_date)

          #=====================================================================
          # Fix for Trac ticket #164: Trac ticket #109 fix introduced 
          # incorrect forecast name parsing for R-test results
          #=====================================================================
          # Update name element for the test
          for each_name in self.testClass.xml.ModelName:
              name_elem = self.elements(each_name)[0]
              
              name_elem.text = self.getResultVariableValue(each_name)
       
       else:
          # There is no TestDate element in the summary file (empty file) -
          # construct all elements associated with test and 
          # insert TestDate element for evaluation test 
          self.buildNew()

      
       # TestDate is guaranteed to exist now
       all_test_dates = self.elements(ResultsSummary.TestDateElement)
       
       if len(all_test_dates):
           processed_dates_elem = all_test_dates[0]
          
                 
           if test_date_index is None:
              # Append test date, sort the date list, and get index of just inserted
              # test date ---> use that index to insert other variables values
              self.processedDates.append(test_date)
              self.processedDates.sort()
             
              # Acquire index to just added date
              test_date_index = self.processedDates.index(test_date)
           
           # Update test date tracker XML element with new date   
           processed_dates_elem.text = " ".join(str(token) for token in self.processedDates)    

       ###
       # Add intermediate values to the summary
       self.addTestResults(test_date, 
                           start_date, 
                           end_date)
       
       ###   
       # Update summary with new test results
       self.updateSummary(test_date_index)
       

       # Some cumulative summaries will be generated by invoking the evaluation test,
       # don't write the summary file then
       if len(all_test_dates):
      
           # Write new summary to the file: 
           with CSEPFile.openFile(self.name, CSEPFile.Mode.WRITE) as fhandle:
               self.write(fhandle)
       
   
    #----------------------------------------------------------------------------
    #
    # Populate empty result summary document with elements specific to the
    # evaluation test.
    #
    # Input: None
    # 
    # Output: Element representing the test.
    #
    def buildNew (self, 
                  empty_value = "0"):    
       """ Build new document structure with elements specific to the 
           evaluation test results."""


       # Construct all elements associated with test and 
       # insert TestDate element to track all processed dates for the test 
       test_elem = self.addElement(self.testClass.xml.Root)

       for var in self.testClass.xml.TestVars.keys():
           var_elem = self.addElement(var, test_elem)
           var_elem.text = empty_value


       # Add true test result variable   
       if self.testClass.xml.TrueEvent is not None:
           var_elem = self.addElement(self.testClass.xml.TrueEvent,
                                      test_elem)
           # Initialize empty true result test variable
           var_elem.text = empty_value

            
       # Add name element for the test
       for var in self.testClass.xml.ModelName:
          var_elem = self.addElement(var, test_elem)
          
          var_elem.text = self.getResultVariableValue(var)
          
          var_elem.attrib.update(self.testDateResults.elements(var)[0].attrib)
      
       # Add test date tracker
       self.addElement(ResultsSummary.TestDateElement,
                       test_elem)
       
       return test_elem
       
       
    #----------------------------------------------------------------------------
    #
    # Store intermediate test results within summary file. This method "registers"
    # intermediate values with corresponding cumulative variables.
    #
    # Input: 
    #        test_date - datetime.date object that represents the test date
    #                    for the result files.
    #        start_date - Start date for the forecast period
    #        end_date - End date for the forecast period
    # 
    # Output: None
    #
    def addTestResults (self, test_date, start_date, end_date):    
       """ Store intermediate test results within summary file."""

       test_date_index = self.processedDates.index(test_date)
       
       # Number of processed dates in summary file
       num_dates = len(self.processedDates)

       # Get a reference to the variable element
       var = self.testClass.xml.TrueEvent
       element = self.elements(var)[0]
       
       var_values = element.text.split()
       
       # Insert new value if new test date was added, overwrite existing one
       # if test date was already in summary file
       if len(var_values) != num_dates:
          var_values.insert(test_date_index, "")
       
       # Replace test date value with one from result file                   
       var_values[test_date_index] = self.getResultVariableValue(var)
       
       # Fix for Trac ticket #178: Add a sanity check for number of observed
       # events in intermediate summary result
       if len(self.testClass.xml.EvaluateSummary) != 0 and len(var_values) > 1:
           
           for each_type, each_operator in self.testClass.xml.EvaluateSummary.iteritems():
               eval_var_values = [eval("%s('%s')" %(each_type,
                                                    value)) for value in var_values] 
               
               # Evaluate values that correspond to current forecast period only
               start_date_index = bisect.bisect_left(self.processedDates,
                                                     start_date)

               # To allow re-processing of multiple dates that have incorrect
               # entries in the summary (i.e., '4 0 0 7') one at a time,
               # evaluate value up to the test date being processed
               end_date_index = min(test_date_index + 1,
                                    bisect.bisect_left(self.processedDates,
                                                       end_date))
               
               min_value = eval_var_values[start_date_index]
               
               # In case of an error, need to report which date failed value 
               # corresponds to
               date_index = start_date_index
               
               for each_value in eval_var_values[start_date_index:end_date_index]:
                   if each_operator(min_value, each_value) is False:
                       error_msg = "Inconsistent '%s %s' values are detected for the sequence of intermediate results %s (%s file: %s variable evaluated using '%s' type and '%s' operator). \
'%s' value corresponds to %s" %(min_value,
                              each_value,
                              eval_var_values,
                              self.name,
                              self.testClass.xml.TrueEvent,
                              each_type, each_operator,
                              each_value,
                              self.processedDates[date_index])
                                     
                       ResultsSummary.__logger.error(error_msg)
                       raise RuntimeError, error_msg 
                   
                   min_value = each_value
                   date_index += 1
             
       # Replace the whole 'text' string for the element
       element.text = " ".join(var_values)
    

    #----------------------------------------------------------------------------
    #
    # Extract value for given variable from the test result.
    #
    # Input: 
    #        var - Variable name. 
    # 
    # Output: String representation of the variable value.
    #
    def getResultVariableValue (self, var):    
       """ Extract value for the variable from the test result."""

       #print ElementTree.tostring(self.testDateResults.elements(var)[0])
       return self.testDateResults.elements(var)[0].text.strip()

    
    #----------------------------------------------------------------------------
    #
    # Update summary variables with test date results.
    #
    # Input: 
    #        test_date_index - Current position into the variable list to 
    #                          place current result value in.
    # 
    # Output: None.
    #
    def updateSummary (self, test_date_index):    
       """ Update summary variables with test date results."""

       num_dates = len(self.processedDates)
       
       # Replace corresponding result variables with new values if test date is
       # already in the summary results
       # Add new entry if test date is not registered with summary file
       for var in self.testClass.xml.TestVars.keys():
          
          # Get a reference to the variable element
          element = self.elements(var)[0]
          
          var_values = element.text.split()

          # Insert new value if new test date was added, overwrite existing one
          # if test date was already in summary file
          if len(var_values) != num_dates:
             var_values.insert(test_date_index, "")
                
          # Replace test date value with one from result file      
          var_values[test_date_index] = self.getResultVariableValue(var)
          
          # Replace the whole 'text' string for the element
          element.text = " ".join(var_values)

