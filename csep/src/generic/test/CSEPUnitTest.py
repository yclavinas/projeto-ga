"""
Module CSEPUnitTest
"""

__version__ = "$Revision: 3779 $"
__revision__ = "$Id: CSEPUnitTest.py 3779 2012-08-01 22:33:08Z liukis $"

import unittest

#--------------------------------------------------------------------------------
#
# CSEPUnitTest.
#
# This module is designed as unit test suite for the CSEP system.
#
# It consists of:
    
# Unit tests for CSEP forecast evaluation tests (R)
from RTestAsymptoticResults import RTestAsymptoticResults
   
# Unit test for cutting catalog to the geographical area
from CutToAreaCatalog import CutToAreaCatalog
    
# Unit test for randomizing Independence Probability catalog data
from RandomizeIndependenceProbability import RandomizeIndependenceProbability
    
# Unit tests for the ForecastGroup class
from ForecastGroupTest import ForecastGroupTest
    
# Unit tests for the DispatcherInitFile class
from DispatcherInitFileTest import DispatcherInitFileTest
    
# Unit tests for the Dispatcher class
from DispatcherTest import DispatcherTest
    
# Unit test for evaluation tests cumulative results
from CumulativeResultsTest import CumulativeResultsTest
    
# Unit test for evaluation tests cumulative results
from IntermediateResultsTest import IntermediateResultsTest
    
# Unit test for the XML forecast master template
from ForecastXMLTemplateTest import ForecastXMLTemplateTest
    
# Unit test for plotting routines based on XML format result data
from PlotXMLResultsTest import PlotXMLResultsTest
    
# Unit test for publishing results by Dispatcher
from PublishResults import PublishResults
    
# Unit test for maps of scaled forecasts
from ForecastMapTest import ForecastMapTest
    
# Unit test for staging of archived files in the system
from CSEPStorageTest import CSEPStorageTest
    
# Unit test for BatchInitFile class
from BatchInitFileTest import BatchInitFileTest
    
# Unit test for CSEPEmail clas
from CSEPEmailTest import CSEPEmailTest
    
# Unit test for BatchProcessing class
from BatchProcessingTest import BatchProcessingTest
    
from GeoUtilsTest import GeoUtilsTest
    
# Unit test for staging of existing raw catalog data
from StageRawDataTest import StageRawDataTest
    
# Unit test for GeographicalRegionsInitFile class
from GeographicalRegionInitFileTest import GeographicalRegionInitFileTest
    
# Unit tests for "all-models' summary files (please see Trac ticket #185)
from AllModelsSummaryTest import AllModelsSummaryTest
    
from Trac230Test import Trac230Test
from Trac232Test import Trac232Test

# Unit tests for HybridForecast class
from HybridForecastTest import HybridForecastTest

# Invoke the module
if __name__ == '__main__':

   import logging
   
    
   # Invoke all tests
   unittest.main()

   # Shutdown logging
   logging.shutdown()
           
# end of main
