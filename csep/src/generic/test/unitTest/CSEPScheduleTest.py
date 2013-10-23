"""
Module CSEPScheduleTest
"""

__version__ = "$Revision: 3496 $"
__revision__ = "$Id: CSEPScheduleTest.py 3496 2011-11-10 20:22:41Z liukis $"


import sys, os, unittest, shutil, datetime

from CSEPTestCase import CSEPTestCase
from ForecastGroupInitFile import ForecastGroupInitFile


#--------------------------------------------------------------------
#
# Validate that ForecastGroup class properly parses 
# and initializes CSEPSchedule objects from the initialization file.
#
class CSEPScheduleTest (CSEPTestCase):

   # Static data of the class
   
   # Unit tests use sub-directory of global reference data directory
   __referenceDataDir = os.path.join(CSEPTestCase.ReferenceDataDir, 
                                     'unitTest', 'schedule')

   
   #-----------------------------------------------------------------------------
   #
   # This test verifies that CSEPSchedule class is creating dates according to
   # schedule as specified in configuration file.
   #
   def test(self):
      """ Confirm that CSEPSchedule class properly specifies dates according \
to the configuration file."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      # Copy reference init file to the test directory
      init_file = "forecast.init.xml"
      shutil.copyfile(os.path.join(CSEPScheduleTest.__referenceDataDir, init_file),
                      os.path.join(CSEPTestCase.TestDirPath, init_file))    

      # Use test directory as forecast group directory
      init_file = ForecastGroupInitFile(CSEPTestCase.TestDirPath)

      ### Validate results
      
      ### Models schedule
      element = ForecastGroupInitFile.ModelElement
      models_schedule = init_file.schedule(element)
      
      error = "Expected valid schedule element for '%s'." %(element)
      self.failIf(models_schedule is None, error)
      
      ### Test for specific dates
      # Year is specified as any
      test_date = datetime.datetime(2006, 1, 15)
      error = "Expected '%s' date to be found for '%s' schedule." \
              %(test_date.date(), element)
      self.failIf(models_schedule.has(test_date) == False, error)


      # Year is specified as any, month is provided by second 'month' element
      test_date = datetime.datetime(2005, 11, 10)
      error = "Expected '%s' date to be found for '%s' schedule." \
              %(test_date.date(), element)
      self.failIf(models_schedule.has(test_date) == False, error)


      # Year is explicit, month is any
      test_date = datetime.datetime(2007, 7, 21)
      error = "Expected '%s' date to be found for '%s' schedule." \
              %(test_date.date(), element)
      self.failIf(models_schedule.has(test_date) == False, error)


      # Year is explicit, month is explicit, day is any
      test_date = datetime.datetime(2007, 9, 28)
      error = "Expected '%s' date to be found for '%s' schedule." \
              %(test_date.date(), element)
      self.failIf(models_schedule.has(test_date) == False, error)


      # Date is explicit
      test_date = datetime.datetime(2006, 5, 1)
      error = "Expected '%s' date to be found for '%s' schedule." \
              %(test_date.date(), element)
      self.failIf(models_schedule.has(test_date) == False, error)


      # Date is not in the schedule
      test_date = datetime.datetime(2005, 8, 1)
      error = "Unexpected '%s' date is found for '%s' schedule." \
              %(test_date.date(), element)
      self.failIf(models_schedule.has(test_date) == True, error)

      
      # Test ranges
      for each_year in xrange(2009, 2012):
          for each_day in xrange(1, 16):
              test_date = datetime.datetime(each_year, 3, each_day)
              
              error = "Expected to find '%s' date for '%s' schedule." \
                      %(test_date.date(), element)
              self.failIf(models_schedule.has(test_date) == False, error)

      # Test ranges with increments
      for each_year in xrange(2000, 2007, 2):
          for each_month in xrange(4, 13, 4):
              for each_day in xrange(22, 29, 2):
                  test_date = datetime.datetime(each_year, each_month, each_day)
                  
                  error = "Expected to find '%s' date for '%s' schedule." \
                          %(test_date.date(), element)
                  self.failIf(models_schedule.has(test_date) == False, error)


      ### evaluationTests schedule
      element = ForecastGroupInitFile.EvaluationTestElement
      tests_schedule = init_file.schedule(element)
      error = "Expected valid schedule element for '%s'." %(element)
      self.failIf(tests_schedule is None, error)


      # Date is implicit: should match any date
      test_date = datetime.datetime(2007, 6, 19)
      error = "Expected '%s' date to be found for '%s' schedule." \
              %(test_date.date(), element)
      self.failIf(tests_schedule.has(test_date) == False, error)
      
      
   #-----------------------------------------------------------------------------
   #
   # This test verifies that CSEPSchedule class creates a complete set of dates
   # that represent the schedule.
   #
   def testBatchDates(self):
      """ Confirm that CSEPSchedule class creates complete list of dates that \
represent specified schedule."""

      # Setup test name
      CSEPTestCase.setTestName(self, 
                               self.id())

      try:
         
         # Configuration file for the test directory
         config_file = "forecast.init.xml"
   
         # Use test directory as forecast group directory
         init_file = ForecastGroupInitFile(CSEPScheduleTest.__referenceDataDir,
                                           config_file)
         
         ### Models schedule
         element = ForecastGroupInitFile.ModelElement
         models_schedule = init_file.schedule(element)         
         
         for d in models_schedule.dates():
            pass

         self.fail("Failed to raise an exception for an ambiguous start date")

      except RuntimeError, error:

         self.failIf(error.args[0].find("dates(): Start date is ambiguous") < 0, 
            "Failed to raise exception of expected content.")
      
         
      # Configuration file for the test directory
      config_file = "forecast_dates.init.xml"

      # Use test directory as forecast group directory
      init_file = ForecastGroupInitFile(CSEPScheduleTest.__referenceDataDir,
                                        config_file)

      element = ForecastGroupInitFile.EvaluationTestElement
      tests_schedule = init_file.schedule(element)

      ### Validate results
      all_dates = []
      
      for each_date in tests_schedule.dates():
         all_dates.append(each_date)
         
      # Expected results
      reference_value = [datetime.datetime(2007, 11, 5, 0, 0),
                         datetime.datetime(2007, 11, 6, 0, 0),
                         datetime.datetime(2007, 11, 7, 0, 0),
                         datetime.datetime(2007, 12, 1, 0, 0),
                         datetime.datetime(2007, 12, 2, 0, 0),
                         datetime.datetime(2007, 12, 3, 0, 0),
                         datetime.datetime(2007, 12, 5, 0, 0),
                         datetime.datetime(2007, 12, 6, 0, 0),
                         datetime.datetime(2007, 12, 7, 0, 0),
                         datetime.datetime(2007, 12, 31, 0, 0),
                         datetime.datetime(2008, 1, 1, 0, 0), 
                         datetime.datetime(2008, 1, 15, 0, 0), 
                         datetime.datetime(2008, 1, 30, 0, 0), 
                         datetime.datetime(2008, 2, 1, 0, 0), 
                         datetime.datetime(2008, 2, 2, 0, 0), 
                         datetime.datetime(2008, 2, 3, 0, 0), 
                         datetime.datetime(2008, 2, 4, 0, 0), 
                         datetime.datetime(2008, 2, 5, 0, 0), 
                         datetime.datetime(2008, 2, 6, 0, 0), 
                         datetime.datetime(2008, 2, 7, 0, 0), 
                         datetime.datetime(2008, 2, 8, 0, 0), 
                         datetime.datetime(2008, 2, 9, 0, 0), 
                         datetime.datetime(2008, 2, 10, 0, 0), 
                         datetime.datetime(2008, 2, 11, 0, 0), 
                         datetime.datetime(2008, 2, 12, 0, 0), 
                         datetime.datetime(2008, 2, 13, 0, 0), 
                         datetime.datetime(2008, 2, 14, 0, 0), 
                         datetime.datetime(2008, 2, 15, 0, 0), 
                         datetime.datetime(2008, 2, 16, 0, 0), 
                         datetime.datetime(2008, 2, 17, 0, 0), 
                         datetime.datetime(2008, 2, 18, 0, 0), 
                         datetime.datetime(2008, 2, 19, 0, 0), 
                         datetime.datetime(2008, 2, 20, 0, 0), 
                         datetime.datetime(2008, 2, 21, 0, 0), 
                         datetime.datetime(2008, 2, 22, 0, 0), 
                         datetime.datetime(2008, 2, 23, 0, 0), 
                         datetime.datetime(2008, 2, 24, 0, 0), 
                         datetime.datetime(2008, 2, 25, 0, 0), 
                         datetime.datetime(2008, 2, 26, 0, 0), 
                         datetime.datetime(2008, 2, 27, 0, 0), 
                         datetime.datetime(2008, 2, 28, 0, 0), 
                         datetime.datetime(2008, 2, 29, 0, 0),
                         datetime.datetime(2008, 3, 1, 0, 0), 
                         datetime.datetime(2008, 3, 2, 0, 0), 
                         datetime.datetime(2008, 3, 3, 0, 0)]
      
      self.failIf(reference_value != all_dates,
                  "Failed to get all schedule dates: expected %s, got %s"
                  %(reference_value, all_dates))
      
      

# Invoke the module
if __name__ == '__main__':
   
   # Invoke all tests
   unittest.main()
        
# end of main
