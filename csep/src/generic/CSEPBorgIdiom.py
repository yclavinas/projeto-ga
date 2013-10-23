"""
Module CSEPBorgIdiom
"""

__version__ = "$Revision$"
__revision__ = "$Id$"



#-------------------------------------------------------------------------------
#
# CSEPBorgIdiom.
#
# This class implements Borg Idiom (also known as Monostate pattern) used by 
# CSEPFactory class. All objects of the class share the same state information 
# and behavior.
# 
class CSEPBorgIdiom (object):

    # Static data of the class
    _shared_state = {}
      
    #===========================================================================
    # ATTN:
    # 1. If child class is to overwrite __new__ method, just use CSEPBorgIdiom.__new__
    # instead of object.__new__.
    # 2. If instances of the same derived class to share the state among themselves,
    # but not with instances of other subclasses of Borg, make sure that derived
    # class has at it's own class scope the "state": _shared_state = {}    
    #===========================================================================
    def __new__ (cls, *args, **kwargs):
        obj = object.__new__(cls, *args, **kwargs)
        obj.__dict__ = cls._shared_state
        return obj
        
