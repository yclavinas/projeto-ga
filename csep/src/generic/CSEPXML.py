"""
CSEPXML module
"""

__version__ = "$Revision: 4150 $"
__revision__ = "$Id: CSEPXML.py 4150 2012-12-19 03:08:43Z liukis $"


#--------------------------------------------------------------------------------
#
# This module stores variables specific to the CSEP XML format.
#

# Namespace for the XML format documents
NAMESPACE = "http://www.scec.org/xml-ns/csep/0.1"

FORECAST_NAMESPACE = "http://www.scec.org/xml-ns/csep/forecast/0.1"

# Version
VERSION  = "1.0"

# Encoding
ENCODING = "utf-8"

# Key used to identify 'any' value (cronjob-like) for the XML element
ANY_VALUE = '*'


# Format string for floating point values in XML files:
# elements attributes only (element values, such as rates, are not affected)
FloatFormatStr = '%.2f'
FloatFormatStrZeroDigit = '%.0f'


from xml.etree.cElementTree import ElementTree, Element

#--------------------------------------------------------------------------------
#
# Indent ElementTree document. This function was "borrowed" from
# http://infix.se/2007/02/06/gentlemen-indent-your-xml as suggested by
# ElementTree maintainers.
#
# Input: 
#        elem - cElementTree.Element object to indent.
#        level - Level of indentation. Default is 0.
#
# Output:
#        Indented cElementTree.Element object
#
def indent(elem, level=0):
    """ Indent cElementTree.Element object in preparation for the 'pretty' print."""
    
    
    i = "\n" + level*3*" "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level+1)
            if not e.tail or not e.tail.strip():
                e.tail = i + "  "
        if not e.tail or not e.tail.strip():
            e.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            
    return elem
 
