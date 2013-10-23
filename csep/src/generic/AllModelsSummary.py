
"""
Module AllModelsSummary
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import re
#from xml.etree.cElementTree import ElementTree

import CSEPFile, CSEPInitFile, CSEPLogging
from Forecast import Forecast


#--------------------------------------------------------------------------------
#
# AllModelsEvaluationTestSummary
#
# This class is designed to create and update XML format summary file 
# for all participating in evaluation test forecasts models.
# For example, summary file for N-test invoked for models within forecast group
# will include N-test results for all models of the group.    
#
class AllModelsSummary (CSEPInitFile.CSEPInitFile):

    # Static data members
    
    # Prefix used for filename with test results
    Type = 'all.'
    
    # Root element of the document
    __rootElement = "CSEPAllModelsSummary"
    
    __logger = None
    
    # XML elements and attributes for dates
    __testDateElement = 'testDate'
    __startDateAttribute = 'forecastStartDate'
    __endDateAttribute = 'forecastEndDate'
    __creationDateTime = {'creationInfo' : 'creationTime'}
    __versionAttribute = 'CSEPVersion' 
        
    
    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #        summary_file - Path for the results summary file.
    #        test_class - Reference to the class that represents evaluation test
    #                     for produced results.  
    # 
    def __init__ (self, summary_file, 
                  test_class):    
        """ Initialization for AllModelsSummary class."""

        if AllModelsSummary.__logger is None:
           AllModelsSummary.__logger = CSEPLogging.CSEPLogging.getLogger(AllModelsSummary.__name__)
           
        # Initialization file
        CSEPInitFile.CSEPInitFile.__init__ (self, 
                                            summary_file)

        if self.exists() is False:
           
           # Create file with specified root element
           CSEPInitFile.CSEPInitFile.addElement(self, 
                                                AllModelsSummary.__rootElement)

        
        # Class type of evaluation test 
        self.__evalTestClass = test_class
        
        # CSEPInitFile object that represents results for a single test date
        # (to update summary file with)
        self.testDateResults = None
        

    #---------------------------------------------------------------------------
    #
    # Update results summary with test date results.
    #
    # Input: 
    #        result_file - File with test results for the date.
    #        test_date - datetime.date object that represents the test date
    #                    for the result file.   
    #        start_date - Start date for the forecast period. Default is None.
    #        end_date - End date for the forecast period. Default is None.
    # 
    def update (self, 
                result_file, 
                test_date, 
                start_date = None, 
                end_date = None):    
       """ Update summary file with test results for a particular date."""


       # Write new summary to the file:
       AllModelsSummary.__logger.info("Updating %s file with test results from %s" %(self.name,
                                                                                     result_file)) 

       # Instantiate result file object - check for existence
       self.testDateResults = CSEPInitFile.CSEPInitFile(result_file)

       if self.testDateResults.exists() is False:
          error_msg = "update(): Result file '%s' for %s does not exist." %(result_file,
                                                                            test_date.date())
          
          AllModelsSummary.__logger.error(error_msg)
          raise RuntimeError, error_msg
       

       # Will raise an exception if entry for models that correspond to the 
       # daily results is already in the summary file
       self.__checkExistence()

       # Insert entry for model(s) that correspond to the daily test result
       date_element = self.addNewTestResult()
      
       # Update dates
       date_element.text = '%s' %test_date.date()
        
       if start_date is not None:
           date_element.attrib[AllModelsSummary.__startDateAttribute] = '%s' %start_date
            
       if end_date is not None:            
           date_element.attrib[AllModelsSummary.__endDateAttribute] = '%s' %end_date
      
       # Propagate creation time of the test result
       for elem_name, attr_name in AllModelsSummary.__creationDateTime.iteritems():
           date_element.attrib[attr_name] = self.testDateResults.elements(elem_name)[0].attrib[attr_name]

           # Add CSEP version that generated result
           date_element.attrib[AllModelsSummary.__versionAttribute] = \
              self.testDateResults.elements(elem_name)[0].attrib[AllModelsSummary.__versionAttribute]
       
       fhandle = CSEPFile.openFile(self.name, 
                                   CSEPFile.Mode.WRITE)
       self.write(fhandle)
       fhandle.close()
       
   
    #----------------------------------------------------------------------------
    #
    # Add test result to the summary for all models.
    #
    # Input: None
    # 
    # Output: Date element for the daily test result
    #
    def addNewTestResult (self):    
       """ Add new test result to the summary file.""" 


       # All elements associated with the test 
       result_elem = self.addElement(self.__evalTestClass.xml.Root)


       # Names of participating models
       for each_name in self.__evalTestClass.xml.ModelName:
            
            # Model name from daily result 
            name_element = self.testDateResults.elements(each_name)[0]
            
            # Add element to the summary file
            summary_name_element = self.addElement(each_name,
                                                   result_elem)
            
            # Strip date from forecast name if any
            summary_name_element.text = re.sub(Forecast.NameSeparator.join(['',
                                                   '[0-9]+',
                                                   '[0-9]+',
                                                   '[0-9][0-9][0-9][0-9]']), 
                                               "", name_element.text.strip())
            
       ### Update 'true event'
       summary_true_event_element = self.addElement(self.__evalTestClass.xml.TrueEvent,
                                                    result_elem)
       summary_true_event_element.text = self.testDateResults.elements(self.__evalTestClass.xml.TrueEvent)[0].text.strip()
        
       # Update test result variable(s)
       for each_var in self.__evalTestClass.xml.TestVars.iterkeys():
           summary_var_element = self.addElement(each_var,
                                                 result_elem)
           summary_var_element.text = self.testDateResults.elements(each_var)[0].text.strip()


       for each_var in self.__evalTestClass.xml.AllModelsSummary.iterkeys():
            
           # Check if variable is not 'true event' - was added already
           if each_var != self.__evalTestClass.xml.TrueEvent: 

               # Share element between the trees - it's an element with lots of
               # children and attributes
               result_elem.append(self.testDateResults.elements(each_var)[0]) 

#               var_element = self.addElement(each_var,
#                                             result_elem)
#               var_element.text = self.testDateResults.elements(each_var)[0].text.strip()
                
       
       return self.addElement(AllModelsSummary.__testDateElement,
                              result_elem)
       
       
    #----------------------------------------------------------------------------
    #
    # Check if model(s) corresponding to the daily test result is already in the 
    # summary file.
    #
    # Input: None
    # 
    # Output: None
    #
    def __checkExistence (self):    
       """ Check if model(s) corresponding to the daily test result is already
           in the summary file."""


       # Poll already existing tests results in the summary file to check if 
       # result for a particular model(s) is already in the summary file
       for each_result in self.elements(self.__evalTestClass.xml.Root):
            
            # List of each model name associated with test result that is found in 
            # summary file
            found_names = []
            for each_name in self.__evalTestClass.xml.ModelName:
                
                # Model name from daily result 
                name_element = self.testDateResults.elements(each_name)[0]
                
                # Strip date from forecast name if any
                name_element = re.sub(Forecast.NameSeparator.join(['',
                                                                   '[0-9]+',
                                                                   '[0-9]+',
                                                                   '[0-9][0-9][0-9][0-9]']), 
                                      "", 
                                      name_element.text.strip())

                # Name elements from summary file
                summary_name_element = self.children(each_result,
                                                     each_name)[0]
                
                if name_element == summary_name_element.text.strip():
                    found_names.append(name_element)

            # Found summary entry that corresponds to the daily result                    
            if len(found_names) == len(self.__evalTestClass.xml.ModelName):
                
                ### Raise an error: summary file already contains results for
                ### specified models
                error_msg = "Result element exists for '%s' models, \
can not update existing record." %found_names

                AllModelsSummary.__logger.error(error_msg)
                raise RuntimeError, error_msg
                
                 
       return
    
