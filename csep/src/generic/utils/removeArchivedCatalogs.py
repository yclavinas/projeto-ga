"""
Utility to remove original raw catalogs that have been archived into SVN repository 

"""

import os

import CSEPFile
from CSEPLogging import CSEPLogging


# Class to remove existing raw catalog files that have been archived into SVN repository
class CatalogFiles:


   def __init__ (self,
                 filelist_name):

       # Open file to keep track of which raw catalogs need to be removed
       self.__filesToRemoveHandle = CSEPFile.openFile(filelist_name)

       
   def __del__ (self):
       self.__filesToRemoveHandle.close()
       
   
   def remove (self):
     """ Remove each file as specified in filelist."""

     runtime_dir = ''
     
     for each_file in self.__filesToRemoveHandle:

           # Remove newline at the end of each line
           each_file = each_file.strip()
           
           # Check if file really exists before removing it:
           if not os.path.exists(each_file):
              CSEPLogging.getLogger(__name__).warning("File '%s' does not exist." %each_file)
              
           else:
                  
               CSEPLogging.getLogger(__name__).info("Removing: %s" %each_file)
               os.remove(each_file)

           # Clean up intermediate products that exist since 200801* runtime
           # directories
           file_path, file_name = os.path.split(each_file)
     
           # New directory is specified
           if file_path != runtime_dir:
               runtime_dir = file_path
               
               for file_name in ['filtered_raw_data.txt', 
                                 'import_processed.dat']:
                   file_to_remove = os.path.join(file_path,
                                                 file_name)
                   
                   if not os.path.exists(file_to_remove):
                      CSEPLogging.getLogger(__name__).warning("File '%s' does not exist." %file_to_remove)
                      
                   else:
                          
                       CSEPLogging.getLogger(__name__).info("Removing: %s" %file_to_remove)
                       os.remove(file_to_remove)


if __name__ == "__main__":
    
    import optparse
    
    command_options = optparse.OptionParser()

    command_options.add_option('--filelist',
                               dest='list_file',
                               default=None,
                               help='Filename with list of files to remove. Default is None.')
    
    
    (values, args) = command_options.parse_args()

    
    c = CatalogFiles(values.list_file)
    c.remove()
    del c
