"""
Module CSEPPolygon
"""

__version__ = "$Revision$"
__revision__ = "$Id$"

import CSEPLogging
from CSEPInitFile import CSEPInitFile


#-------------------------------------------------------------------------------
#
# CSEPPolygon
#
# This module represents Polygon.
#
class CSEPPolygon (list):

    # Static data members
    
    # Structure-like to represent format of polygon's vertex
    class VertexFormat (object):
        Longitude = 0
        Latitude = 1
        IncludeVertex = 2
        IncludeSide = 3
        
        
    class IncludeInfo (object):
        
        def __init__ (self,
                      vertex_xml,
                      vertex,
                      side):
            """Initialize inclusion flags for the vertex."""
            
            self.xml = vertex_xml # XML element representing the vertex
            self.vertex = vertex # Flag to include vertex into polygon
            self.side = side     # Flag to include side into polygon


        def __repr__ (self):
            return repr(int(self.vertex)) + \
                   CSEPPolygon.XML.Separator + \
                   repr(int(self.side))
            

    # XML representation of polygon within CSEP
    class XML (object):
        
        # Name of Polygon element
        Element = 'polygon' 
        
        # Name of the OuterBoundaryIs element
        VertexElement = 'vertex'

        # Attributes to specify if vertex and corresponding side are included into
        # the polygon
        IncludeAttribute = 'include'
        IncludeSideAttribute = 'includeSide'
        
        Separator = ','

        
    # Logger for CSEPPolygon class
    __logger = None
    
    
    #----------------------------------------------------------------------------
    #
    # Initialization.
    #
    def __init__ (self,
                  xml_doc,
                  elem):
        """ Initialization for CSEPPolygon class based on ElementTree object."""
        
        if CSEPPolygon.__logger is None:
           CSEPPolygon.__logger = CSEPLogging.CSEPLogging.getLogger(CSEPPolygon.__name__)
           
        list.__init__(self, [])
        
        # Keep track of all vertexes coordinates
        self.ID = []
        
        # Extract polygon's vertexes
        for each_vertex in xml_doc.children(elem,
                                            CSEPPolygon.XML.VertexElement):
            
            # Extract coordinates
            x, y = each_vertex.text.strip().split()
            
            if (x, y) in self.ID:
                error_msg = "Vertex %s is provided multiple times within same polygon of %s file" %((x, y),
                                                                                                    xml_doc.name)
                CSEPPolygon.__logger.error(error_msg)
                raise RuntimeError, error_msg

            # Extract vertex and side "include" flags if any are provided
            include_vertex = True
            include_side = True
            
            if CSEPPolygon.XML.IncludeAttribute in each_vertex.attrib:
                # Attribute is provided
                include_vertex = bool(eval(each_vertex.attrib[CSEPPolygon.XML.IncludeAttribute]))

            if CSEPPolygon.XML.IncludeSideAttribute in each_vertex.attrib:
                # Attribute is provided
                include_side = bool(eval(each_vertex.attrib[CSEPPolygon.XML.IncludeSideAttribute]))
            
            self.ID.append((x,y))
            self.append(CSEPPolygon.IncludeInfo(each_vertex,
                                                include_vertex,
                                                include_side))

           
    #-----------------------------------------------------------------------
    #
    # Return string representation of polygon object 
    # 
    def __repr__ (self):
        """ String representation of polygon object"""
        
        result_str = ''
        
        for vertex, vertex_info in zip(self.ID,
                                       self):
            
            if len(result_str):
                result_str += CSEPPolygon.XML.Separator
                
            result_str += '['
            result_str += vertex[CSEPPolygon.VertexFormat.Longitude]
            result_str += CSEPPolygon.XML.Separator
            result_str += vertex[CSEPPolygon.VertexFormat.Latitude]
            result_str += CSEPPolygon.XML.Separator
            result_str += repr(vertex_info)
            result_str += ']'
        
        return result_str    


    #-----------------------------------------------------------------------
    #
    # Return string representation of polygon object for map generation.
    # 
    def toASCIIMap (self):
        """ String representation of polygon object"""
        
        result_str = ''
        
        for vertex in self.ID:
            
            if len(result_str):
                result_str += '\t'
                
            result_str += vertex[CSEPPolygon.VertexFormat.Longitude]
            result_str += CSEPPolygon.XML.Separator
            result_str += vertex[CSEPPolygon.VertexFormat.Latitude]
        
        return result_str    


    #-----------------------------------------------------------------------
    #
    # Verify provided CSEPPolygon XML definition against "self" definition
    # 
    def validate (self, 
                  model_polygon):
        """ Verify validity of XML representation for polygon against 
            provided template. """

        
        for each_coords, vertex in zip(self.ID,
                                       self):

#            print "COORDS:", each_coords
#            print "self:", self
#            print "model:", model_polygon
            model_index  = model_polygon.ID.index(each_coords)
            model_vertex = model_polygon[model_index]

            # Copy inclusion flags from model to the master template 
            vertex.xml.attrib[CSEPPolygon.XML.IncludeAttribute] = repr(model_vertex.vertex)
            vertex.xml.attrib[CSEPPolygon.XML.IncludeSideAttribute] = repr(model_vertex.side)
            
            # Copy values into CSEPPolygon.XML.IncludeInfo object
            vertex.vertex = model_vertex.vertex
            vertex.side = model_vertex.side
            
        return


