"""
Module CSEPTest
"""

__version__ = "$Revision: 3339 $"
__revision__ = "$Id: CSEPTest.py 3339 2011-06-02 23:23:32Z  $"

#--------------------------------------------------------------------------------
#
# CSEPTest.
#
# This module is designed as an acceptance test suite for the CSEP system.
#
# It consists of:
#
# Catalog download
from CatalogRetrieval import CatalogRetrieval
    
# Catalog pre-processing - reformatting of the catalog data into the ZMAP format
from CatalogPreProcessing import CatalogPreProcessing
    
# Catalog post-processing for:
#    - longterm forecasts evaluations (generate observations for the longterm forecasts).
#    - shortterm forecasts evaluations (generate observations for the shortterm forecasts).
#    - shortterm forecasts models (generate input catalog for the shortterm
#     forecast generation).
#    - TBD: for longterm forecasts models.
from CatalogPostProcessing import CatalogPostProcessing
    
# Forecast evaluation tests (RELM N, L, R tests) - test results reproducibility
from EvaluationTests import EvaluationTests
    
# Forecast evaluation tests (RELM N, L, R tests) - test "production" mode of
# tests (draw random numbers by the system)
from RandomEvaluationTests import RandomEvaluationTests
    
# Forecast alarm-based evaluation tests (MASS, ROC tests) - test results reproducibility
from AlarmBasedEvaluationTests import AlarmBasedEvaluationTests
    
# Forecast alarm-based evaluation tests (MASS, ROC tests) with masking bit on -
# test results reproducibility
from AlarmBasedWithMaskEvaluationTests import AlarmBasedWithMaskEvaluationTests
    
# Forecast alarm-based evaluation tests (MASS, ROC tests) - test "production" mode
# of tests (create seed file for random number generator by the system)
from RandomAlarmBasedEvaluationTests import RandomAlarmBasedEvaluationTests
    
# Diagnostics evaluation tests introduced to the CSEP testing framework by
# Robert Clements et al from UCLA, Los Angeles
from DiagnosticEvaluationTests import DiagnosticsEvaluationTests

# Statistical evaluation tests introduced to the CSEP testing framework by
# David Rhoades et al from GNS Science, Lower Hutt, New Zealand
from StatisticalEvaluationTests import StatisticalEvaluationTests


# Invoke the module
if __name__ == '__main__':

    import logging, unittest
    
    
    # Invoke all tests
    unittest.main()
        
    # Shutdown logging
    logging.shutdown()
        
# end of main
