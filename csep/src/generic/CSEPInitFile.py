"""
Module CSEPInitFile
"""

__version__ = "$Revision: 3769 $"
__revision__ = "$Id: CSEPInitFile.py 3769 2012-07-24 20:37:27Z liukis $"


import os
from xml.etree.cElementTree import parse, ElementTree, Element, tostring, fromstring

import CSEPXML, CSEPLogging, CSEPSchedule, CSEPFile, Environment


#--------------------------------------------------------------------------------
#
# CSEPInitFile
#
# This module is designed to open and parse XML format initialization files 
# used by the CSEP software.
# It parses specified initialization file for a defined list of elements, and stores
# found nodes in the dictionary. The document tree is preserved after the initial
# parsing, and can be searched for elements that were not specified for the
# initial parsing.
#
class CSEPInitFile (object):

    # Static data members
    
    # Token for runtime test date that would need to be replaced with actual 
    # value of test date if appears in any XML format initialization file
    # within CSEP testing framework
    TestDateToken = '$TESTDATE$'

    # Name of schedule element
    __scheduleElement = 'schedule' 
    
    # Name of the year element
    __yearElement = 'year'
    
    # Name of the month element
    __monthElement = 'month'

    # Name of the day element
    __dayElement = 'day'
    
    # Name of error handler element - used to expand a set of expressions to be
    # excluded from triggering a failure condition within running process
    __errorHandlerElement = "ignoreErrorStrings"
    __errorStringSeparator = '|'

    __logger = None
    

    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #           file_path - Path for the initialization file. Default is None.
    #           element_list - List of required top-level XML elements 
    #                          for the file. Default is an empty list.
    #           namespace - Namespace defined within the document. Default
    #                       is CSEPXML.NAMESPACE.
    # 
    def __init__ (self, 
                  file_path = None, 
                  element_list = [], 
                  namespace = CSEPXML.NAMESPACE):
        """ Initialization for CSEPInitFile class."""

        if CSEPInitFile.__logger is None:
           CSEPInitFile.__logger = CSEPLogging.CSEPLogging.getLogger(CSEPInitFile.__name__)
           
        # Initialization file
        self.__file = file_path
        
        # Namespace for the document
        self.__namespace = namespace
        
        # Dictionary of elements names and corresponding nodes
        self.__foundElements = {}
        
        # Tree element of the document
        self.__tree = None
        
        # Check for file existence
        if file_path is not None and os.path.exists(file_path):

           CSEPInitFile.__logger.info("Parsing file '%s'" %file_path)
                      
           self.__tree = parse(self.__file).getroot()

           # Extract top level elements from the XML document
           for xml_token in element_list:
              
              self.__foundElements[xml_token] = self.__findNodes(xml_token)
              
              if len(self.__foundElements[xml_token]) == 0:
                 
                 # Required element is missing
                 error_msg = "'%s' element is missing in '%s' configuration file: %s" \
                             %(xml_token, self.__file, self.name)
                 
#                 error_msg = "'%s' element is missing in '%s' configuration file: %s" \
#                             %(xml_token, self.__file, self.tostring())
                 
                 CSEPInitFile.__logger.error(error_msg)
                 raise RuntimeError, error_msg
              
              CSEPInitFile.__logger.debug("%s: Found %s nodes for %s" \
                                          %(self.__file, 
                                            len(self.__foundElements[xml_token]), 
                                            xml_token))

           # Check if error strings to ignore are provided for CSEP error handler
           __error_strings = self.elementValue(CSEPInitFile.__errorHandlerElement)
           if __error_strings is not None:
               for each_str in __error_strings.split(CSEPInitFile.__errorStringSeparator):
                   Environment.ErrorHandler.addIgnoreString(each_str)
              
           #print tostring(CSEPXML.indent(self.__tree))
           

    #----------------------------------------------------------------------------
    #
    # Does initialization file exist?
    # 
    # Input: None.
    #
    # Output:
    #         True if initialization file exists, False otherwise.
    #
    def exists (self):
        """ Check existence of the file."""

        return (self.__tree is not None)


    #----------------------------------------------------------------------------
    #
    # Return root element of the document.
    # 
    # Input: None.
    #
    # Output:
    #         Object representing root element of the document
    #
    def root (self):
        """ Return 'root' element of the document."""

        return self.__tree


    #---------------------------------------------------------------------------
    #
    # Generator method that iterates over elements with specified tag within
    # the file
    #
    # Input: 
    #       model_files - List of current forecasts files for the group
    # 
    def next (self, tag_name): 
        """ Generator method that iterates over elements with specified tag within 
            the file."""

        for each_event in self.elements(tag_name):
            yield each_event


    #--------------------------------------------------------------------
    #
    # Get values of specified XML elements.
    # 
    # Input: 
    #         node - Element to be searched for children.
    #         child_tag - Tag of children to be searched for.
    #
    # Output:
    #         A list of children nodes.
    #
    def nextChild (self, node, child_tag):
       """ Acquire values of specified XML children elements by tags."""

       for each_child in self.children(node, child_tag):
           yield each_child


    #----------------------------------------------------------------------------
    #
    # Returns namespace used by the file.
    # 
    # Input: None.
    #
    # Output:
    #         Namespace
    #
    def __getNamespace (self):
        """ Returns namespace of the file."""

        return self.__namespace
     
    namespace = property(__getNamespace, doc = "XML namespace of the file.")


    #--------------------------------------------------------------------
    #
    # Create new document tree with specified root element tag.
    # 
    # Input:
    #         element_tag - Tag for new element.
    #
    # Output: 
    #         New element object.
    #
    def addElement (self, 
                    element_tag = None, 
                    parent_element = None,
                    xml_string = None):
        """ Create new document tree."""

        # If parent is not provided, append new element to the root element
        parent = parent_element
        
        if parent is None:
           parent = self.__tree
        
        new_element = None
        
        if element_tag is not None:
            ns = ''
            if self.__namespace is not None and len(self.__namespace) != 0:
                ns = "{%s}" %self.__namespace
            
            new_element = Element("%s%s" %(ns, element_tag))
            
        else:
            # List of xml formated data is provided
            new_element = fromstring(xml_string)
        
        
        if parent is not None:
           # If parent exists, append new child
           parent.append(new_element)
        else:
           # Initialize root element of the document
           self.__tree = new_element
           
        return new_element


    #--------------------------------------------------------------------
    #
    # Returns name of the file.
    # 
    # Input: None.
    #
    # Output:
    #         Filename.
    #
    def __getFilename (self):
        """ Returns path of the file."""

        return self.__file
     
    name = property(__getFilename, doc = "Full path of the file.")


    #--------------------------------------------------------------------
    #
    # Get list of XML elements.
    # 
    # Input: 
    #         element_name - Element name.
    #
    # Output:
    #         A list of elements by specified name.
    #
    def elements (self, element_name):
        """ Get all XML elements by name."""


        if self.exists() is False:
            # Elements are requested for non-existent file: report frame information 
            # for the caller
            error_msg = "%s: Elements of '%s' tag are requested for non-existent '%s' file" \
                        %(CSEPLogging.CSEPLogging.frame(self.__class__,
                                                        level=2),
                          element_name,
                          self.name)
            CSEPInitFile.__logger.error(error_msg)
            
            raise RuntimeError, error_msg
         
            
        # Element node is registered with internal dictionary if
        # constructor was asked to search for such element.
        if self.__foundElements.has_key(element_name):
           return self.__foundElements[element_name]
        # Element is not registered with internal dictionary,
        # search the tree:
        else:
           return self.__findNodes(element_name)

   
    #--------------------------------------------------------------------
    #
    # Get value of specified XML element.
    # 
    # Input: 
    #         element_name - Element name.
    #         parent_name - Optional name of the parent element. Default is None.
    #         index - Element index into the list. Default is zero.
    #
    # Output:
    #         A value of the element if it exists or None.
    #
    def elementValue (self, element_name, parent_name = None, index = 0):
        """ Acquire a value of specified XML element by tag."""

        # List of found nodes
        nodes = []
        
        if parent_name is not None:
           parent = self.elements(parent_name)
           
           if len(parent) == 0:
              return None
           
           else:
              nodes = self.children(parent[0], element_name)
              
        else:      
           nodes  = self.elements(element_name)
           

        # Return None if no elements exist
        if len(nodes) == 0:
           return None
        
        if (index + 1) > len(nodes):
           message = "Index %s exceeds the length of node list (%s) for '%s' \
XML element stored in %s file." %(index, len(nodes), element_name, self.__file) 

           CSEPInitFile.__logger.error(message)
           raise RuntimeError, message
           
        # Return stripped of preceeding and trailing spaces and new-lines string
        text = nodes[index].text
        
        if text is not None:
           return text.strip()
        else:
           return text


    #--------------------------------------------------------------------
    #
    # Get attributes of specified XML element.
    # 
    # Input: 
    #         element_name - Element name.
    #         parent_name - Optional name of the parent element. Default is None.
    #         index - Element index into the list. Default is zero.
    #
    # Output:
    #         A dictionary of element attributes.
    #
    def elementAttribs (self, element_name, parent_name = None, index = 0):
        """ Acquire a value of specified XML element by tag."""

        # List of found nodes
        nodes = []
        
        if parent_name is not None:
           parent = self.elements(parent_name)
           
           if len(parent) == 0:
              return {}
           
           else:
              nodes = self.children(parent[0], element_name)
              
        else:      
           nodes  = self.elements(element_name)
           

        # Return None if no elements exist
        if len(nodes) == 0:
           return {}
        
        if (index + 1) > len(nodes):
           message = "Index %s exceeds the length of node list (%s) for '%s' \
XML element stored in %s file." %(index, len(nodes), element_name, self.__file) 

           CSEPInitFile.__logger.error(message)
           raise RuntimeError, message
           
        # Return node attributes
        __node_attribs = nodes[index].attrib
        
        for each_attr, each_value in __node_attribs.iteritems():
            
            __node_attribs[each_attr] = Environment.replaceVariableReference(Environment.CENTER_CODE_ENV,
                                                                             each_value)
        
        return __node_attribs


    #--------------------------------------------------------------------
    #
    # Get values of specified XML elements.
    # 
    # Input: 
    #         element_list - List of element names.
    #         index - Element index into the list. Default is zero.
    #
    # Output:
    #         A tuple of elements values.
    #
    def elementsValues (self, element_list, index = 0):
        """ Acquire values of specified XML elements by tags."""

        values = []
        
        # Iterate through the list
        for name in element_list:
           
           # List of found nodes
           values.append(self.elementValue(name, index))

        return tuple(values)


    #--------------------------------------------------------------------
    #
    # Get values of specified XML elements.
    # 
    # Input: 
    #         node - Element to be searched for children.
    #         child_tag - Tag of children to be searched for.
    #
    # Output:
    #         A list of children nodes.
    #
    def children (self, node, child_tag):
       """ Acquire values of specified XML elements by tags."""

       return node.findall(self.__xpath(child_tag))
    
    
    #---------------------------------------------------------------------------
    #
    # Write document to the file.
    # 
    # Input: 
    #         fhandle - Optional handle to the open file. Default is None. If no
    #                   file handler is provided, document content is written to 
    #                   the file provided at initialization time (self.__file) 
    #
    # Output:
    #         None.
    #
    def write (self, fhandle = None):
       """ Writes ElementTree object to the file."""

       __file_handler = fhandle
       if __file_handler is None:
           __file_handler = CSEPFile.openFile(self.__file,
                                              CSEPFile.Mode.WRITE)
           
       ElementTree(CSEPXML.indent(self.__tree)).write(__file_handler)
       
       # File handler was not provided, close locally opened file
       if fhandle is None:
           __file_handler.close()
           
       return

        
    #--------------------------------------------------------------------
    #
    # Write document to the string
    # 
    # Input: 
    #         fhandle - Handle to the open file.
    #
    # Output:
    #         None.
    #
    def tostring (self):
       """ Converts ElementTree object to string."""

       return tostring(self.__tree)


    #----------------------------------------------------------------------------
    #
    # Get 'schedule' for specified XML element.
    # 
    # Input: 
    #         xml_element - Element name, or object representing the XML element
    #
    # Output:
    #         A CSEPSchedule object if schedule element exists, or
    #         a schedule object that represents any day of the year otherwise.
    #         In a case if specified 'element_name' does not exist, None is
    #         returned. 
    #
    def schedule (self, xml_element):
        """ Acquire a schedule of specified XML element by tag."""

        # XML element object
        elem = xml_element
        
        # Name of the element is provided
        if isinstance(xml_element, str):
           # List of found nodes
           nodes  = self.elements(xml_element)
   
           # Return None if no elements exist
           if len(nodes) == 0:
              return None
           elif len(nodes) > 1:
              error_msg = "More than one '%s' elements specified by '%s' file." \
                          %(xml_element, self.name)
                          
              CSEPInitFile.__logger.error(error_msg) 
              raise RuntimeError, error_msg

           elem = nodes[0]
           
           
        # Schedule object that defaults to any day of any year
        result_schedule = CSEPSchedule.CSEPSchedule()

        # Get schedule element for the node
        schedule = self.children(elem, 
                                 CSEPInitFile.__scheduleElement)
        if len(schedule) == 0:
           return result_schedule
        elif len(schedule) > 1:
           error_msg = "There are more than one '%s' elements detected for \
the '%s' element in '%s' file." %(CSEPInitFile.__scheduleElement,
                                  elem.tag, self.name)

           CSEPInitFile.__logger.error(error_msg) 
           raise RuntimeError, error_msg
        
        
        # Extract values for year, month, day
        for year in self.children(schedule[0], 
                                  CSEPInitFile.__yearElement):
            
           # Get all month elements and corresponding days
           for month in self.children(year, 
                                      CSEPInitFile.__monthElement):
               
              for day in self.children(month,
                                       CSEPInitFile.__dayElement):

                 result_schedule.add(year.text, month.text, day.text)
                 
        return result_schedule
      

    #--------------------------------------------------------------------
    #
    # Find tree nodes by name.
    # 
    # Input: 
    #         name - Element name.
    #
    # Output:
    #         A list of tree nodes.
    #
    def __findNodes(self, name):
       """ Find tree nodes by name."""

       # Return an empty list if initialization file doesn't exist
       if self.__tree is None:
          return []
       
       
       return self.__tree.findall(self.__xpath(name))
                

    #--------------------------------------------------------------------
    #
    # Create xpath for the specified tag.
    # 
    # Input: 
    #         name - Element name.
    #
    # Output:
    #         XPath for the tag.
    #
    def __xpath(self, name):
       """ Create xpath for the tag."""

       element_xpath = './/{%s}%s' %(self.__namespace, name)
       
       if self.__namespace is None or len(self.__namespace) == 0:
           element_xpath = './/%s' %(name)
       
       return element_xpath
   