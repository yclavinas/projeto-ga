
"""
Module DiagnosticsSummary
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import datetime, ast

import CSEPFile, CSEPInitFile, CSEPLogging
from ResultsSummary import ResultsSummary
from ResultsCumulativeSummary import ResultsCumulativeSummary


#--------------------------------------------------------------------------------
#
# DiagnosticsSummary
#
# This class is designed to create and update XML format summary files 
# by diagnostics evaluation tests.
#
class DiagnosticsSummary (ResultsCumulativeSummary):

    # Static data members
    
    # Prefix used for filename with intermediate test results ("out of interest" 
    # results)
    
    Type = 'diagnosticsSummary.'
    
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
                  test_class):    
        """ Initialization for DiagnosticsSummary class."""

        if DiagnosticsSummary.__logger is None:
           DiagnosticsSummary.__logger = CSEPLogging.CSEPLogging.getLogger(DiagnosticsSummary.__name__)
           
        ResultsCumulativeSummary.__init__(self, 
                                          summary_file, 
                                          test_class)
        
        # RTT summaries are created from scratch every time update is requested
        self.__testDate = None


    #----------------------------------------------------------------------------
    #
    # Populate empty result summary document with elements specific to the
    # evaluation test.
    #
    # Input: None
    # 
    # Output: Element representing the test.
    #
    def buildNew (self):    
       """ Build new document structure with elements specific to the 
           evaluation test results."""

       # If evaluation test needs to be invoked to generate summary, there
       # won't be daily results within cumulative summary XML file
       if self.testClass.xml.InvokeTest is True:
           return
       
       
       test_elem = ResultsSummary.buildNew(self,
                                           '')
       
       # Initialize 'true' result of the test to zeros
       for var in self.testClass.xml.TestVars.keys():
           # Element was added by ResultsSummary.buildNew() above
           var_elem = self.elements(var)[0]
         
           # Identify number of elements for the test result (residual column):
           num_vals = None
           result_val = self.testDateResults.elementValue(var)
             
           if result_val is not None:
                num_vals = len(result_val.split())
         
           # Initialize cumulative simulation values
           if num_vals is not None:
               var_elem.text = " ".join(["0"] * num_vals)
               #print "buildNew:", ElementTree.tostring(test_elem)
               
       # Add extra variables that might be used by the cumulative summaries
       for each_var in self.testClass.xml.PlotVars:
            
           var_elem = self.addElement(each_var,
                                      test_elem)
           # Initialize empty true result test variable
           var_elem.text = self.getResultVariableValue(each_var)
           
       # If there are any values that should be stacked up for the cumulative
       # summary, preserve these values in daily results element of the summary
       for each_var in self.testClass.xml.StackVars:
            var_elem = self.addElement(each_var, test_elem)
            var_elem.text = self.getResultVariableValue(each_var)
        
      
       return test_elem
       
       
    #----------------------------------------------------------------------------
    #
    # Store daily test results within summary file. This method "registers"
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
    def addTestResults (self, 
                        test_date, 
                        start_date, 
                        end_date):    
       """ Store daily test results within summary file."""

       # If evaluation test needs to be invoked to generate summary, there
       # won't be daily results within cumulative summary XML file
       if self.testClass.xml.InvokeTest is True:
           self.__testDate = test_date
           return


       test_elem, reprocess_of_test_date = self.addTestElements(test_date, 
                                                                start_date, 
                                                                end_date)

       # Update filename with current forecast that is contributing to the summary
       for var in self.testClass.xml.ModelName:
          var_elem = self.elements(var)[0]
          var_elem.attrib.clear()
          var_elem.attrib.update(self.testDateResults.elements(var)[0].attrib)

       # If there are any values that should be stacked up for the cumulative
       # summary, preserve these values in daily results element of the summary
       for each_var in self.testClass.xml.StackVars:
            var_elem = self.children(test_elem, each_var)
            if reprocess_of_test_date:
                # Element already exists, update the value with new result
                var_elem = var_elem[0]
                
            else:
                var_elem = self.addElement(each_var, test_elem)
                
            var_elem.text = self.getResultVariableValue(each_var)
       
       ###
       # Populate element with result data: overwrite old data if any
              
       # Test element for the summary file       
       cumulative_test_elem = self.elements(self.testClass.xml.Root)[0]   

       # Populate result vector for the test and corresponding cumulative
       # result vector (residual)
       for var in self.testClass.xml.TestVars.values():

          new_elems = self.testDateResults.elements(var)
          if len(new_elems) == 0:
              # Test date does not provide such result vector
              continue
          
          new_values_elem = new_elems[0]
          new_values = [float(token) for token in new_values_elem.text.split()]

          # Access cumulative variables for the test
          cumulative_var = self.children(cumulative_test_elem, var)[0]
          cumulative_values = [float(token) for token in cumulative_var.text.split()]
          
          # Access result vector for the test date within cumulative file
          var_elem = self.children(test_elem, var)[0]
          
          # Initialize list of existing values of result variable (if any) to all zero's
          old_values = [0] * len(new_values)
          
          if reprocess_of_test_date is True:
             old_values = [float(token) for token in var_elem.text.split()]
          
          # Populate with result vector from daily result file for the test date

          # Populate vector that represents daily result within cumulative summary
          var_elem.text = new_values_elem.text
          
          # Add results to the cumulative variable for the test:
          
          # Check if cumulative vector has been initialized to the same number of
          # vector elements as result vector in daily test result 
          if len(new_values) > len(cumulative_values) and len(cumulative_values) == 0:
             warning_msg = "Number of cumulative values is reset for \
'%s' variable in '%s' file (%s) based on '%s' file (%s)." \
                         %(var, 
                           self.name, len(cumulative_values),
                           self.testDateResults.name, len(new_values))
             CSEPLogging.CSEPLogging.getLogger(DiagnosticsSummary.__name__).warning(warning_msg)
             
             # This is very first time cumulative is set for the vector,
             # increase number of elements to the same number as in daily result vector
             cumulative_values = ["0"] * new_values

          
          sum_values = [ci + ni - oi for ci, ni, oi in 
                        zip(cumulative_values, new_values, old_values)]   
             
          cumulative_var.text = " ".join(repr(token) for token in sum_values)
          
       #print "After addTestResult", self.tostring()
       return   


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

       # If evaluation test needs to be invoked to generate summary, there
       # won't be daily results within cumulative summary XML file
       if self.testClass.xml.InvokeTest is False:

           cumulative_test_elem = self.elements(self.testClass.xml.Root)[0]
           from xml.etree.cElementTree import tostring
           
           # Stack up variables from all testing dates to create a summary
           for each_var in self.testClass.xml.StackVars:
               
               # Step through all tests dates for cumulative summary
               cum_values = ''
               all_results = self._getAllResults()
           
               for each_date in self.processedDates:
                    
                    # Results for a particular date
                    test_date_elem = all_results[each_date]
                    
                    cum_values += self.children(test_date_elem,
                                                each_var)[0].text
                    cum_values += ' '
    
               # Reset cumulative variable
               var_elem = self.children(cumulative_test_elem, each_var)[0]
               var_elem.text = cum_values       
               
       else:
            
           self.testObj.updateSummary(self.name,
                                      self.__testDate)

