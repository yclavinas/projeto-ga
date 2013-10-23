"""
CSEPXMLGeneric module
"""

__version__ = "$Revision: 2680 $"
__revision__ = "$Id: CSEPXMLGeneric.py 2680 2009-11-30 20:11:55Z liukis $"


import os, re, datetime, string, time

import CSEPFile, MatlabLogical, CSEPXML, CSEP, CSEPLogging, CSEPInitFile, \
       CSEPGeneric
from CSEPPropertyFile import CSEPPropertyFile
from Forecast import Forecast as ForecastBaseClass
from CSEPPolygon import CSEPPolygon


        