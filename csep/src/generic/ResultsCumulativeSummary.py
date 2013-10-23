

"""
Module ResultsCumulativeSummary
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import datetime, re
#from xml.etree.cElementTree import ElementTree

from ResultsSummary import ResultsSummary
import CSEPLogging, CSEPUtils, CSEP, CSEPFile
from Forecast import Forecast


#--------------------------------------------------------------------------------
#
# ResultsCummulativeSummary
#
# This class is designed to create and update XML format intermediate summary files 
# used by the CSEP software.
#
class ResultsCumulativeSummary (ResultsSummary):

    # Static data members
    
    # Prefix used for filename with intermediate test results ("out of interest" 
    # results)
    Type = 'cumulative.'

    # Test date results element and attributes
    TestResultsElement = "testResults"
    TestDateAttribute = "date"
    __simulationElement = "simulation"

    
    #--------------------------------------------------------------------
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
        """ Initialization for ResultsCummulativeSummary class."""

        # Initialization file
        ResultsSummary.__init__(self, 
                                summary_file,
                                test_class,
                                root_element)

        # Dictionary of all test results as cElementTree.Element objects with
        # date as the key:  {test_date : __testResultElement}
        self.__allResults = {}

        # Number of simulations for the test
        self.__numSimulations = None


    def _getAllResults (self):    
        """ Return dictionary of all daily results."""
        
        return self.__allResults
        

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

        # Call parent's method to construct general elements
        test_elem = ResultsSummary.buildNew(self)
       
        # Construct elements associated with cumulative results - simulation values.
        # ATTN: make sure there is only one element per each specified simulation element:
        # some of the variables can depend on the same simulation element
        for var in set(self.testClass.xml.TestVars.values()):
            var_elem = self.addElement(var, test_elem)
         
            # Identify number of simulations for the test:
            # 1. Check if there is simulation vector for the variable: tests
            #    that use random numbers will produce simulation vector of
            #    results based on these random numbers
            num_sims = 1
            simulation_val = self.testDateResults.elementValue(ResultsCumulativeSummary.__simulationElement)
             
            if simulation_val is not None:
                num_sims = len(simulation_val.split())
         
            # Initialize cumulative simulation values
            var_elem.text = " ".join(["0"] * num_sims)
            #print "buildNew:", ElementTree.tostring(test_elem)
      
        return test_elem


    #---------------------------------------------------------------------------
    # 
    #---------------------------------------------------------------------------
    def addTestElements(self, 
                        test_date, 
                        start_date, 
                        end_date):
       """Add a new element or acquire existing element from the summary file
          that represents daily result"""
           
       #========================================================================
       #  Fix for Trac ticket #162: Date XX-XX-XXXX-fromXML pattern should be 
       #  stripped in cumulative plot label
       #========================================================================
       # Strip forecast date from the model name(s) if any - name is used by 
       # the cumulative plot label 
       for var in self.testClass.xml.ModelName:
           
           # Fix for Trac ticket #
           model_name_elem = self.elements(var)[0]
           model_name_elem.text = re.sub(Forecast.NameSeparator.join(['',
                                                                      '[0-9]+',
                                                                      '[0-9]+',
                                                                      '[0-9][0-9][0-9][0-9]']) +
                                         CSEP.Forecast.FromXMLPostfix, 
                                         "", model_name_elem.text)


       # Check if summary file already contains simulation data for the test date
       # (old data)
       all_test_results = self.elements(ResultsCumulativeSummary.TestResultsElement)
       
       ###
       # Populate dictionary of test results (if any) with date object as the key
       for elem in all_test_results:
          
          # Date for the result is stored as element attribute
          date_string = elem.attrib[ResultsCumulativeSummary.TestDateAttribute].strip()
          
          elem_date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
          self.__allResults[elem_date] = elem
          
       
       ###       
       # If summary file does not contain test_date results, insert one:
       test_elem = None
       
       # Flag to indicate that test date is being re-processed: summary file
       # already contains the result data for the test date 
       reprocess_of_test_date = False
       
       if test_date not in self.__allResults:
                
          # Add XML element that represents data for the test date:
          test_elem = self.addElement(ResultsCumulativeSummary.TestResultsElement)
          test_elem.attrib[ResultsCumulativeSummary.TestDateAttribute] = \
             "%s" %(test_date)
          
          # Register new element with dictionary of test results   
          self.__allResults[test_date] = test_elem
          
          # Append empty elements for test specific true result variable to the 
          # testResult element
          if self.testClass.xml.TrueEvent is not None:
              var_elem = self.addElement(self.testClass.xml.TrueEvent, 
                                         test_elem)
                
          # Append empty elements for the test specific simulation or 
          # forecast data variable to the testResult element
          # ATTN: make sure there is only one element per each specified simulation element:
          # some of the variables can depend on the same simulation element
          for var in set(self.testClass.xml.TestVars.values()):
             # Access simulation variable within each model 
             var_elem = self.addElement(var, test_elem)
             #var_elem.text = " ".join("0" for i in xrange(0, self.__numSimulations))
             
       else:
          
          reprocess_of_test_date = True
          # Acquire existing object for the test date (old test results)
          test_elem = self.__allResults[test_date]


       return (test_elem, reprocess_of_test_date) 


    #----------------------------------------------------------------------------
    #
    # Store final test results within summary file. This is done
    # for cumulative summary since summation of simulation data is used to 
    # calculate new result variables. If old data for the test date is already 
    # present in the file, replace it.
    # This method also populates a dictionary of single test results with test
    # date as the key into the dictionary.
    #
    # Input: 
    #        test_date - date object that represents the test date
    #                    for the result files.
    #        Inherited from base class method signature and not used by class
    #        implementation:  
    #        start_date - Start date for the forecast period
    #        end_date - End date for the forecast period
    # 
    # Output: None
    #
    def addTestResults (self, test_date, start_date, end_date):    
       """ Store final test results (such as simulation values and intermediate
           varibles values) within summary file since evaluation test result 
           variables are computed based on the summation of test results for 
           processed test dates."""

       
       test_elem, reprocess_of_test_date = self.addTestElements(test_date, 
                                                                start_date, 
                                                                end_date)

       ###
       # Populate element with result data: overwrite old data if any
              
       # Test element for the summary file       
       cumulative_test_elem = self.elements(self.testClass.xml.Root)[0]   

       # Update true test result variable, and corresponding cumulative
       # variable
       var = self.testClass.xml.TrueEvent
       var_elem = self.children(test_elem, var)[0]
       
       # If test date is being re-processed, subtract old value from cumulative
       # first
       old_value = 0
       if reprocess_of_test_date is True:
          old_value = float(var_elem.text.strip())
          
       # Set value for test date variable   
       var_elem.text = self.getResultVariableValue(var)
       
       # Add variable value to the cumulative variable value for the test
       cumulative_var = self.children(cumulative_test_elem, var)[0]
       new_value = float(cumulative_var.text)
       new_value -= old_value
       new_value += float(var_elem.text)
       cumulative_var.text = repr(new_value)
           
       
       # Populate simulation variables for the test and corresponding cumulative
       # simulation variables
       # ATTN: make sure there is only one element per each specified simulation element:
       # some of the variables can depend on the same simulation element
       for var in set(self.testClass.xml.TestVars.values()):
          
          # Access cumulative variables for the test
          cumulative_var = self.children(cumulative_test_elem, var)[0]
          cumulative_values = [float(token) for token in cumulative_var.text.split()]
          
          # Access simulation variable for the test within cumulative file
          var_elem = self.children(test_elem, var)[0]
          
          # Initialize list of existing values of result variable (if any) to all zero's
          old_values = [0] * len(cumulative_values)
          
          if reprocess_of_test_date is True:
             old_values = [float(token) for token in var_elem.text.split()]
          
          # Populate with value of underlying 'simulation' element from 
          # result file for the test date
          new_values_elem = self.testDateResults.elements(var)[0]

          # Check if variable has simulation vector 
          sim_elems = self.testDateResults.children(new_values_elem,
                                                    ResultsCumulativeSummary.__simulationElement)
          if len(sim_elems) != 0:
              # Use values of the underlying element - simulation
              new_values_elem = sim_elems[0]

          var_elem.text = new_values_elem.text
          new_values = [float(token) for token in var_elem.text.split()]
          
          # Add results to the cumulative variable for the test:
          
          # Check consistensy of simulation values
          if len(new_values) != len(cumulative_values):
             error_msg = "Inconsistent number of summation values is detected for \
'%s' variable in '%s' file (%s) vs. '%s' file (%s)." \
                         %(var, self.testDateResults.name, len(new_values),
                           self.name, len(cumulative_values))
             CSEPLogging.CSEPLogging.getLogger(ResultsCumulativeSummary.__name__).error(error_msg)
             
             raise RuntimeError, error_msg

          
          sum_values = [ci + ni - oi for ci, ni, oi in 
                        zip(cumulative_values, new_values, old_values)]
             
          cumulative_var.text = " ".join(repr(token) for token in sum_values)
          
          # Set number of simulations for the test
          self.__numSimulations = len(new_values)          
       
       #print "After addTestResult", self.tostring()
       return   
          
       
    #----------------------------------------------------------------------------
    #
    # Update summary variables with test date results. This method checks if
    # test date is the last entry in registered processed test dates for the test.
    # If it's last entry, it will calculate new result variables based on already
    # updated cumulative simulation values for the test. If the results are
    # product of test date re-processing, it will compute simulation summary for 
    # that test date, and re-calculate result variables for the dates that follow
    # the re-processed date.
    #
    # Input: 
    #        test_date_index - Current position into the variable list to 
    #                          place current result value in.
    # 
    # Output: None.
    #
    def updateSummary (self, test_date_index):    
       """ Update summary variables with test date results."""
       
       # If test date is the last entry in registered processed dates, use 
       # already updated cumulative simulation values to calculate result variables
       last_index = len(self.processedDates) - 1
       last_entry = (test_date_index == last_index)
       num_dates = len(self.processedDates)

       test_elem = self.elements(self.testClass.xml.Root)[0]

       # Use cumulative simulation values for the test if it's last entry in
       # processed test dates list
       if last_entry is True:
          
          for var, sim in self.testClass.xml.TestVars.items():

             # Find cumulative simulation element that corresponds to 
             # the result variable
             sim_elem = self.children(test_elem, sim)[0]

             # Extract numerical values for simulation
             sim_values = [float(token) for token in sim_elem.text.split()]

             # Cumulative "observed" variable for the test
             # (eventCount, logLikelihood, or logLikelihoodRatio)
             true_result_elem = self.children(test_elem,
                                              self.testClass.xml.TrueEvent)[0]
             
             # Get a reference to the cumulative variable element
             var_element = self.children(test_elem, var)[0]
             
             var_values = var_element.text.split()
   
             # Insert new value if new test date was added, overwrite existing one
             # if test date was already in summary file
             if len(var_values) != num_dates:
                var_values.insert(test_date_index, "")
                   
             # Replace test date value with one from result file
             var_values[test_date_index] = repr(self.testClass.xml.ResultVarFunc[var](float(true_result_elem.text),
                                                                                      sim_values))
             
             # Replace the whole 'text' string for the element
             var_element.text = " ".join(var_values)
          
       else:
           
          ### RE-calculate cumulative for true result and simulation vector:
          #   some of the result variables are dependent on the same simulation
          #   vector, so make sure simulation vector is re-calculated only once
          simulation_dict = CSEPUtils.swapDictionary(self.testClass.xml.TestVars)

          # Replace corresponding result variables with new values if test date is
          # already in the summary results
          #for var, sim_var in self.testClass.xml.TestVars.items():
          for sim_var, var_list in simulation_dict.iteritems():

             # Sum up true result and simulation values up to and including 
             # test date if it's re-processing of some sort for the test date
             index = 0
             cum_sim_values = [0] * self.__numSimulations
             true_result_value = 0
             
             while index < test_date_index:
                
                # Results for a particular date
                test_date_elem = self.__allResults[self.processedDates[index]]
                
                cum_sim_values, true_result_value = self.__updateCumulative(test_date_elem, 
                                                                            sim_var, 
                                                                            cum_sim_values, 
                                                                            true_result_value)
                #print "update: for ", index, "cum_sim_values=", cum_sim_values
                #print "update: true value=", true_result_value
                index += 1

       
             # Get a reference to the test cumulative variable element that is 
             # dependent on simulation vector
             #var_elem = self.children(test_elem, var)[0]             
             var_elements = [self.children(test_elem, var)[0] for var in var_list]

             #var_values = var_elem.text.split()
             var_values = [each_var.text.split() for each_var in var_elements]
             for each_var_values in var_values:
                 # Insert new value if new test date was added, overwrite exising one
                 # if test date was already in summary file
                 if len(each_var_values) != num_dates:
                    each_var_values.insert(test_date_index, "")


             # Iterate through all remaining test dates in the registry of 
             # processed dates - they need to be recalculated if test_date is not 
             # last entry in the registry
             # 'index' is already set to test_date_index by previous 'while' loop
             while index <= last_index:

                # Results for a particular date
                test_date_elem = self.__allResults[self.processedDates[index]]

                cum_sim_values, true_result_value = self.__updateCumulative(test_date_elem, 
                                                                            sim_var,
                                                                            cum_sim_values, 
                                                                            true_result_value)
                
      
                      
                # Replace test date value with one from result file
                for each_var_values, each_var in zip(var_values, var_list):
                    each_var_values[index] = repr(self.testClass.xml.ResultVarFunc[each_var](true_result_value,
                                                                                             cum_sim_values))
                
                # Replace the whole 'text' string for the element
                for each_var, each_var_values in zip(var_elements, var_values):
                    each_var.text = " ".join(each_var_values)

                index += 1
                

    #----------------------------------------------------------------------------                
    #
    # Add single test date results to cumulative to be able to calculate new
    # cumulative test variables.
    #
    # Input: 
    #        test_date_elem - cElementTree.Element object that represents test 
    #                         results for a single test date
    #        sim_var - Name of variable with simulation values for the test 
    #        sim_values - Cumulative simulation values up to the test date that
    #                     represented by 'test_elem' input argument
    #        true_result_value - Cumulative true test result value for the test
    #                            up to the test date that represented by 
    #                            'test_elem' input argument
    # 
    # Output: A tuple of updated cumulative simulation values and true test result
    #
    def __updateCumulative (self, 
                            test_date_elem, 
                            sim_var,
                            sim_values, 
                            true_result_value):    
       """ Update cumulative variables with test date results."""
       
       # Update cumulative true result value
       true_result_elem = self.children(test_date_elem,
                                        self.testClass.xml.TrueEvent)[0]
       true_result_value += float(true_result_elem.text)                                
       
       # Accumulate simulation values corresponding to the result variable
       sim_elem = self.children(test_date_elem, sim_var)[0]
       
       # Extract numerical values for simulation
       test_sim_values = [float(token) for token in sim_elem.text.split()]
       
       # Sum up simulation values
       new_sim_values = []
       for cum_val, sim_val in zip(sim_values, test_sim_values):
          new_sim_values.append(cum_val + sim_val)
       
        
       return (new_sim_values, true_result_value)
                 

    #---------------------------------------------------------------------------
    #
    # Re-compute results summary
    #
    # Input: None 
    # 
    def recompute (self):    
       """ Re-compute summary file based on daily results stored internally."""

       # 1. Check if test date is already in the cumulative:
       #    iterate through test dates
       processed_dates_elem = self.elements(ResultsSummary.TestDateElement)

       if len(processed_dates_elem) != 0:

          # TestDate element exists: split string into datetime objects
          self.processedDates = [datetime.datetime.strptime(date_string, "%Y-%m-%d").date() for \
                                 date_string in processed_dates_elem[0].text.split()]


       # Collect daily tests results from the file
       all_test_results = self.elements(ResultsCumulativeSummary.TestResultsElement)
       
       # Populate dictionary of test results (if any) with date object as the key
       for elem in all_test_results:
          
          # Date for the result is stored as element attribute
          date_string = elem.attrib[ResultsCumulativeSummary.TestDateAttribute].strip()
          
          elem_date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
          self.__allResults[elem_date] = elem


       # Top-level test element
       test_elem = self.elements(self.testClass.xml.Root)[0]
      
       
       ### RE-calculate cumulative for true result and simulation vector:
       #   some of the result variables are dependent on the same simulation
       #   vector, so make sure simulation vector is re-calculated only once
       simulation_dict = CSEPUtils.swapDictionary(self.testClass.xml.TestVars)


       # Replace corresponding result variables with new values if test date is
       # already in the summary results
       #for var, sim_var in self.testClass.xml.TestVars.items():
       for sim_var, var_list in simulation_dict.iteritems():

           # Determine number of simulation values for the test
           if self.__numSimulations is None:

               sim_elem = self.children(test_elem, sim_var)[0]

               # Determine number of values for simulation
               self.__numSimulations = len([float(token) for token in sim_elem.text.split()])
       

           # Sum up true result and simulation values up to and including 
           cum_sim_values = [0] * self.__numSimulations
           true_result_value = 0

           # Get a reference to the test cumulative variable element that is 
           # dependent on simulation vector
           var_elements = [self.children(test_elem, var)[0] for var in var_list]
           var_values = [each_var.text.split() for each_var in var_elements]


           # Iterate through all test dates in the registry of 
           # processed dates, and recalculate cumulative result variable
           for index in xrange(len(self.processedDates)):

               # Results for a particular date
               test_date_elem = self.__allResults[self.processedDates[index]]

               cum_sim_values, true_result_value = self.__updateCumulative(test_date_elem, 
                                                                           sim_var,
                                                                           cum_sim_values, 
                                                                           true_result_value)
                  
               # Replace test date value with one from result file
               for each_var_values, each_var in zip(var_values, var_list):
                   each_var_values[index] = repr(self.testClass.xml.ResultVarFunc[each_var](true_result_value,
                                                                                            cum_sim_values))
            
               # Replace the whole 'text' string for the element
               for each_var, each_var_values in zip(var_elements, var_values):
                   each_var.text = " ".join(each_var_values)
            
           ### Sanity check for test cumulatives 
           # Make sure cumulative for the simulation vector is the same as recorded in the file
           CSEPLogging.CSEPLogging.getLogger(ResultsCumulativeSummary.__name__).info("Verifying re-computed cumulative vs. cumulative stored in the file for '%s'"
                                                                                      %sim_var)
           if CSEPFile.compareLines(self.children(test_elem, sim_var)[0].text,
                                    ' '.join([repr(value) for value in cum_sim_values]),
                                    1E-12) is True:
               
               CSEPLogging.CSEPLogging.getLogger(ResultsCumulativeSummary.__name__).info("...consistent")

            
       # Write new summary to the file: 
       fhandle = CSEPFile.openFile(self.name, 
                                   CSEPFile.Mode.WRITE)
       self.write(fhandle)
       fhandle.close()
       
   

# Invoke the module in stand-alone mode
if __name__ == '__main__':

    import glob, os
    import CSEPOptionParser
    from EvaluationTestFactory import EvaluationTestFactory
    from EvaluationTest import EvaluationTest
    from CSEPOptions import CommandLineOptions
    
    
    parser = CSEPOptionParser.CSEPOptionParser()
        
    # List of requred options to recompute cumulative summary files
    required_options = [CommandLineOptions.FORECASTS,
                        CommandLineOptions.TESTS]
    options = parser.options(required_options)
    
    if os.path.exists(options.forecast_dir) is False:
        CSEPLogging.CSEPLogging.getLogger(ResultsCumulativeSummary.__name__).error("Forecast directory '%s' does not exist"
                                                                                   %options.forecast_dir)
    
    test_list = options.test_list.split()
    
    for each_test in test_list:
        
        # EvaluationTest class reference
        test_class_ref = EvaluationTestFactory().classReference(each_test)
        
        # Find cumulative tests for the forecast group
        command = '%s/results/%s*%s-%s*%s' %(options.forecast_dir,
                                             ResultsCumulativeSummary.Type,
                                             each_test,
                                             EvaluationTest.FilePrefix,
                                             CSEPFile.Extension.XML)
        found_cumulative_files = glob.glob(command) 
        print "Found files (%s)" %command, found_cumulative_files
    
        # Re-compute test variables for each of found cumulative files
        for each_file in found_cumulative_files:
            
            CSEPLogging.CSEPLogging.getLogger(ResultsCumulativeSummary.__name__).info("Re-computing cumulative %s"
                                                                                      %each_file)            
            cum_file = ResultsCumulativeSummary(each_file,
                                                test_class_ref)
            cum_file.recompute()
            
            