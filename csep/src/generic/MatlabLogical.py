"""
Module MatlabLogical
"""

__version__ = "$Revision: 2950 $"
__revision__ = "$Id: MatlabLogical.py 2950 2010-05-27 02:27:42Z liukis $"


# Map of Python to Matlab logical values
Boolean = {True: "1",
           False : "0",
           "True": "1",
           "False": "0",
           "0": "0",
           "1" : "1"}

# Matlab variables to use for catalog data
class CatalogVar (object):
    
    # Name of undeclustered catalog
    Undeclustered = "mCatalogNoDecl"
    
    # Name of declustered catalog
    Declustered = "mCatalogDecl"
    
    # Name of variable for cell matrix to store all catalog uncertainties
    Uncertainties = 'mModifications'
   