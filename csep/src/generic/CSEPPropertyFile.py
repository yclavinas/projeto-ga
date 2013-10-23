"""
Module CSEPPropertyFile
"""

__version__ = "$Revision: 4218 $"
__revision__ = "$Id: CSEPPropertyFile.py 4218 2013-03-04 21:01:48Z liukis $"

import os, sys, string, time, re, datetime
import CSEPFile, CSEP, CSEPLogging


# Enumeration of allowable datatypes for the 'type' field of the property file
class TypeField (object):
   STRING = "string"
   INTEGER = "int"
   FLOAT = "float"
   TIME = "time"
         

#-------------------------------------------------------------------------------
#
# CSEPPropertyFile
#
# This module is designed to generate and manipulate CSEP property files that 
# describe captured information in key/value/type format.
#
class CSEPPropertyFile (object):

    # Static data members

    # Field separator
    Separator = "="
    
    # Filename separator
    NameSeparator ="."

    # Comment identifier
    Comment = "#"
    
    # Map of current sequence per datatype in the format:
    # datatype <--> currrent sequence number OR 
    # if datatype description is provided:
    # datatype.description <--> currrent sequence number 
    DatatypeSequence = {}

    
    # Structure-like class that represents content of the metadata file
    class Metadata (object):

       # Extension for metadata files.
       Extension = ".meta"
    
      
       # Line indeces into the file
       __commentLineIndex = 0 
      
       # Keywords and corresponding indeces used by metadata file
       DateKeyword = 'CreationDateTime'
       DataFileKeyword = 'DataFilename'
       DataLinkKeyword = 'DataFileIsLink'
       ProducedByKeyword = 'ProducedBy'
       FileDescriptionKeyword = 'FileDescription'
       RuntimeDirectoryKeyword = 'runtimeDirectory'
       SVNKeyword = 'SVNTag'       
       
       __tokenIndex = 0
       __valueIndex = 1
       
     
       #----------------------------------------------------------------------------
       #
       # Initialization.
       #
       # Input: 
       #        filename - Name of the metadata file
       #
       def __init__ (self, filename):
          """Constructor for the Metadata class."""
         
          # Store name for metadata file
          self.file = filename
          
          # File content  
          self.info = {CSEPPropertyFile.Metadata.DateKeyword : None,
                       CSEPPropertyFile.Metadata.DataFileKeyword : None,
                       CSEPPropertyFile.Metadata.DataLinkKeyword : None,
                       CSEPPropertyFile.Metadata.SVNKeyword : None}

          self.originalDataFilename = None
          self.dispatcherRuntimeDir = None          

          
          fhandle = CSEPFile.openFile(self.file)
         
          try:
   
             lines = fhandle.readlines()         
   
   
             # Very first line is a comment with original data filename that 
             # corresponds to the metadata file
             tokens = lines[CSEPPropertyFile.Metadata.__commentLineIndex].split(CSEPPropertyFile.Comment)
             self.originalDataFilename = tokens[CSEPPropertyFile.Metadata.__valueIndex].strip()
            
             for line in lines[1:]:
   
                tokens = [key.strip() for key in line.split(CSEPPropertyFile.Separator)]

                # Each line is in 'key=value' format, extract keyword from line of file
                keyword = tokens[CSEPPropertyFile.Metadata.__tokenIndex]
                 
                # Extract date information
                if keyword == CSEPPropertyFile.Metadata.DateKeyword:
                   
                   self.info[CSEPPropertyFile.Metadata.DateKeyword] = \
                       datetime.datetime.strptime(tokens[CSEPPropertyFile.Metadata.__valueIndex], 
                                                  CSEP.Time.ISO8601Format)

                # Extract data file information   
                if keyword in [CSEPPropertyFile.Metadata.DataFileKeyword, 
                               CSEPPropertyFile.Metadata.DataLinkKeyword,
                               CSEPPropertyFile.Metadata.SVNKeyword]:
                   
                   self.info[keyword] = tokens[CSEPPropertyFile.Metadata.__valueIndex]

                #---------------------------------------------------------------     
                # Extract dispatcher run-time directory from the line that captures
                # options used by Dispatcher instance
                # ProducedBy = ['/usr/local/cruise/projects/CSEP/checkout/src/generic/Dispatcher.py',
                #               '--year=2008', '--month=2', '--day=24', 
                #               '--configFile=/home/csep/operations/cronjobs/dispatcher_daily.init.xml', 
                #               '--waitingPeriod=31', '--disableMatlabDisplay', 
                #               '--enableForecastXMLTemplate', '--enableForecastMap',
                #               '--publishServer=csep-usc@intensity.usc.edu', 
                #               '--publishDirectory=/var/www/html/csep/data/us/usc', 
                #               '--logFile=/home/csep/operations/dispatcher/logs/daily_2008-2-24', 
                #               'runtimeDirectory=/home/csep/operations/dispatcher/runs/csep/20080224000501',
                #               'runtimeTestDate=2008-01-24'] = string
                if keyword == CSEPPropertyFile.Metadata.ProducedByKeyword:
                   
                   # Join value of the token using the same separator 
                   # it was used to split it
                   options = CSEPPropertyFile.Separator.join(tokens[CSEPPropertyFile.Metadata.__valueIndex:])
                   
                   # Extract runtimeDirectory value
                   for each_pair in options.split(','):
                      
                      # If there key=value pair
                      if each_pair.find(CSEPPropertyFile.Separator) >= 0:
                         
                         # Get rid of single quotes
                         each_pair = string.replace(each_pair, '\'', '')
                         values = each_pair.split(CSEPPropertyFile.Separator)
                         
                         key = values[CSEPPropertyFile.Metadata.__tokenIndex]
                         value = values[CSEPPropertyFile.Metadata.__valueIndex]
                         
                         if key.strip() == CSEPPropertyFile.Metadata.RuntimeDirectoryKeyword:
                            self.dispatcherRuntimeDir = value.strip()
                            break
   
          finally:
            
             fhandle.close()


       #----------------------------------------------------------------------------
       #
       # Display object content.
       #
       # Input: None
       #
       def print_info (self):
          """Display content for the Metadata object."""
         
          print CSEPPropertyFile.Metadata.DateKeyword, "=", self.info[CSEPPropertyFile.Metadata.DateKeyword], "\n",\
                CSEPPropertyFile.Metadata.DataFileKeyword, "=", self.info[CSEPPropertyFile.Metadata.DataFileKeyword], "\n",\
                CSEPPropertyFile.Metadata.DataLinkKeyword, "=", self.info[CSEPPropertyFile.Metadata.DataLinkKeyword], "\n",\
                "OriginalFilename = ", self.originalDataFilename, "\n",\
                CSEPPropertyFile.Metadata.ProducedByKeyword, "=", self.dispatcherRuntimeDir, "\n"

    # End of Metadata class
   

    #---------------------------------------------------------------------------
    #
    # Generate unique filename for the datatype and corresponding metadata filename.
    # 
    # Input: 
    #         datatype - Datatype to be stored in the file.
    #         description - Optional description for the datatype, such as forecast model
    #                       name, for example.  Default is None.
    #
    # Output:
    #         A tuple of data and metadata filenames.      
    #
    @staticmethod 
    def filenamePair (datatype, description = None):
        """ Generate a pair of unique data and metadata filenames."""

        key = datatype
        __dir = None
        
        if description != None:

            if os.path.basename(description) != description:
                # Generate unique name based on the basename
                __dir = os.path.dirname(description)
                 
            key = CSEPPropertyFile.NameSeparator.join([datatype, 
                                                       os.path.basename(description)])

        CSEPPropertyFile.__incrementSequence(key)
                
        datafile = CSEPPropertyFile.__dataFilename(key)
        metafile = CSEPPropertyFile.metaFilename(datafile)
        
        if __dir is not None:
            datafile = os.path.join(__dir,
                                    datafile)
            metafile = os.path.join(__dir,
                                    metafile)
        
        return (datafile, metafile)
     
     
    #--------------------------------------------------------------------
    #
    # Write line of information to the file.
    # 
    # Input: 
    #         fhandle - Handle to the open file.
    #         key - Key for the information.
    #         value - Value for the information.
    #         type - Datatype for the information. Default is "string".
    #         units - Units for the value. Default is None.
    #
    # Output: None.
    #
    @staticmethod 
    def write (fhandle, key, value, type = TypeField.STRING, units=None):
        """ Write line of information to the data file."""
        
        # Iinsert line continuation character if new line is encountered as part
        #            of the 'value' string
        if isinstance(value, str):
            value = string.replace(value, "\n", "\\\n")
            
            # Escape 'Separator' characters if found in the 'value' string
            value = string.replace(value, 
                                   CSEPPropertyFile.Separator,
                                   "\\" + CSEPPropertyFile.Separator)
        
        line = "%s %s %s %s %s"  %(key, 
                                   CSEPPropertyFile.Separator, 
                                   value, 
                                   CSEPPropertyFile.Separator, 
                                   type)
        
        if units != None:
           line = "%s %s %s" %(line, CSEPPropertyFile.Separator, units)
           
        line = line + "\n\n"
        fhandle.write(line)
    
        
    #--------------------------------------------------------------------
    #
    # Write line of comment to the file.
    # 
    # Input: 
    #         fhandle - Handle to the open file.
    #         comment_line - Comment to write to the file.
    #
    # Output: None.
    #
    @staticmethod 
    def writeComment (fhandle, comment_line):
        """ Write comment line to the data file."""
        
        line = "%s %s\n"  %(CSEPPropertyFile.Comment, comment_line)
        fhandle.write(line)
    

    #--------------------------------------------------------------------
    #
    # Create metadata file.
    #
    # Input: 
    #         filename - Name of the file.
    #         comment - Comment for the file.
    #         format - File format for the data file.
    #         descripition - Description for the data.
    #         datafile_path - Optional path to the data file (to be checked for 
    #                         soft links). Default is None.
    #         args_list - List of command-line arguments for the program that
    #                     generated the metafile. Default is None.
    #         svn_tag - SVN tag for existing data file in SVN repository. Default
    #                   is None meaning that data does not exist in repository.
    #         preserve_data - Flag if data file should be preserved 
    #                         (generate copy with unique filename). Introduced during
    #                         Trac ticket ##306: Don't preserve OneDayModelInputCatalog 
    #                         data products within testing framework 
    #
    # Output: None.
    #
    @staticmethod 
    def createMetafile (filename, 
                        comment, 
                        format, 
                        description,
                        datafile_path = None,
                        args_list = None,
                        in_svn = False,
                        svn_tag = None,
                        preserve_data = True):
        """ Generate metadata file."""

        # Extract data filename from corresponding metadata filename.
        datafile = re.split(CSEPPropertyFile.Metadata.Extension, filename)[0]
          
        if preserve_data:   
            if os.path.exists(datafile) is False:
                # No original data file is provided,
                # or original data file is not a link
                if (datafile_path is None or os.path.islink(datafile_path) is False) and \
                   in_svn is False and svn_tag is None:
                    
                   # Data file does not exist, raise an exception to prevent the 
                   # creation of corresponding metadata file
                   error_msg = "createMetafile(): Data file doesn't exist '%s'" %datafile
                   CSEPLogging.CSEPLogging.getLogger(CSEPPropertyFile.__name__).error(error_msg)
                   
                   raise RuntimeError, error_msg
                 
                else:
                    # Data file does not exist, set to point to original file 
                    datafile = datafile_path
                    
        else:
            # Original data filename is passed as a comment field for corresponding
            # metadata file
            datafile = comment
        
              
        # Open file for writing
        fhandle = CSEPFile.openFile(filename, 
                                    CSEPFile.Mode.WRITE)
        
        # Write comment
        CSEPPropertyFile.writeComment(fhandle, comment)
        
        CSEPPropertyFile.write(fhandle, 
                               CSEPPropertyFile.Metadata.DataFileKeyword, 
                               datafile)
        
        # If original data file is a soft link to other existing file, capture it
        if datafile_path is not None:
           
           if os.path.islink(datafile_path):
              
              CSEPPropertyFile.write(fhandle, 
                                     CSEPPropertyFile.Metadata.DataLinkKeyword, 
                                     os.path.realpath(datafile_path))
        
     
        # Record program and options that generated the file
        command_args = args_list
        if command_args is None:
            command_args = sys.argv
             
        CSEPPropertyFile.write(fhandle, 
                               CSEPPropertyFile.Metadata.ProducedByKeyword, 
                               command_args)
        
        # Creation date and time
        CSEPPropertyFile.write(fhandle, 
                               CSEPPropertyFile.Metadata.DateKeyword, 
                               CSEPPropertyFile.creationTime(datafile), 
                               TypeField.TIME)
        
        # Data file format
        CSEPPropertyFile.write(fhandle, 
                               "FileFormat", 
                               format)
        
        # Data description
        CSEPPropertyFile.write(fhandle, 
                               CSEPPropertyFile.Metadata.FileDescriptionKeyword, 
                               description)
        
        if svn_tag is not None:
            CSEPPropertyFile.write(fhandle, 
                                   CSEPPropertyFile.Metadata.SVNKeyword, 
                                   svn_tag)
        
        fhandle.close()


    #---------------------------------------------------------------------------
    #
    # Copy metadata file.
    #
    # Input: 
    #         filename - Name of original metadata file.
    #         dest_filename - Name of destination metadata file.    
    #         add_info - Dictionary of new information to be added to the copy
    #
    # Output: None.
    #
    @staticmethod 
    def copyMetafile (filename, 
                      dest_filename, 
                      add_info,
                      add_comment = None): 
        """ Copy metadata file to new destination and add new information if available."""
    
        fhandle = open(filename, 
                       CSEPFile.Mode.READ)
        fhandle_out = open(dest_filename, 
                           CSEPFile.Mode.WRITE)
       
        for line in fhandle.xreadlines():
            if len(line) and line[0] == CSEPPropertyFile.Comment and add_comment is not None:
                line = line.strip() # Strip newline at the end
                line += add_comment
                line += '\n'
                 
            elif len(line):
                tokens = [t.strip() for t in line.split(CSEPPropertyFile.Separator)]
                
                # Need to update the field
                if tokens[0] in add_info:
                    tokens[1] += add_info[tokens[0]]
                    
                    line = (" %s " %CSEPPropertyFile.Separator).join(tokens)
            fhandle_out.write(line)
                
        fhandle.close()
        fhandle_out.close()        
        
             
    #--------------------------------------------------------------------
    #
    # Generate unique data filename.
    #
    # Input: 
    #         datatype - Datatype (and optional description) to be stored in the file.
    #
    # Output:
    #         filename - Generated filename.       
    #
    @staticmethod 
    def __dataFilename (datatype):
        """ Generate unique filename given datatype to be stored in that file and 
            current sequence number for it."""
              
        # Generated filename has format "namespace.datatype.date.sequence"
        # Acquire current time - as the number of seconds since the epoch in UTC
        current_time = time.time()
          
        filename = "%s.%s.%f.%s" %(CSEP.NAMESPACE,
                                   datatype, 
                                   current_time, 
                                   CSEPPropertyFile.DatatypeSequence[datatype])

        return filename
    

    #--------------------------------------------------------------------
    #
    # Generate a name of the metadata file.
    #
    # Input: 
    #         filename - Name of the data file.
    #
    # Output:
    #         metafile - Generated filename.       
    #
    @staticmethod 
    def metaFilename (filename):
        """ Generate filename for the metadata given the name of the corresponding 
            data file."""
           
        # Generate metadata filename that corresponds to the data filename.
        metafile = filename + CSEPPropertyFile.Metadata.Extension
        
        return metafile
    
            
    #--------------------------------------------------------------------
    #
    # Increment current sequence if data and metadata files were generated for the
    # current sequence number.
    # This method is called every time new filename is generated.
    #
    # Input: 
    #          datatype - Datatype (and optional description) for which filenames
    #                          were generated.
    #
    # Output: None.
    #
    @staticmethod            
    def __incrementSequence (datatype):
        """ Update datatype counter and increment current sequence number if 
            expected number of files has been generated for the sequence."""
        
        if CSEPPropertyFile.DatatypeSequence.has_key(datatype) is False:
            # Set initial value if datatype is not registered with the dictionary
            CSEPPropertyFile.DatatypeSequence[datatype] = 1
        else:
            # Increment the sequence number
            CSEPPropertyFile.DatatypeSequence[datatype] += 1
    
            
    #----------------------------------------------------------------------------
    #
    # Get creation time of the file.
    # This is a static method of the class.
    #
    # Input:
    #          filename - Name of the file.
    #
    # Output:
    #          String representation of ISO8601 format creation time for the file.
    #
    @staticmethod 
    def creationTime (filename):
        """ Get creation time of the file."""
        
        local_time = time.localtime(os.stat(filename).st_ctime)
        CSEPLogging.CSEPLogging.getLogger(CSEPPropertyFile.__name__).debug("Creation time for %s is %s" \
                                                                           %(filename, local_time))
        
        iso_8601 = time.strftime(CSEP.Time.ISO8601Format, 
                                 local_time)
        CSEPLogging.CSEPLogging.getLogger(CSEPPropertyFile.__name__).debug("iso time = %s" %iso_8601)
        
        return iso_8601
    
                