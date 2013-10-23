import os, glob

"""
utility to rename files that match specified pattern by replacing search pattern 
with target pattern 

"""


class RenameFiles:

   __dryRun = True
   
   def rename (self, 
               search_pattern,  # search pattern for glob
               target_pattern,  # target pattern to replace search pattern
               search_subdirs,  # search sub-directories
               dry_run):        # dry run: don't actually rename files 
     """ Rename file that match search pattern by replacing search pattern with 
         target pattern."""

     self.__dryRun = dry_run
     
     self.__findFiles(search_pattern,
                      target_pattern)

          
     if search_subdirs is True:
         
         entries = os.listdir('.')
         cwd = os.getcwd()
         
         for dir_path in entries:
             if os.path.isdir(dir_path) is True:
         
                 os.chdir(dir_path)
                 
                 self.__findFiles(search_pattern,
                                  target_pattern)
                     
                 os.chdir(cwd)


   def __findFiles (self, 
                    search_pattern,  # search pattern for glob
                    target_pattern):  # target pattern to replace search pattern
     """ Rename file that match search pattern by replacing search pattern with 
         target pattern."""

     found_files = glob.glob('*%s*' %search_pattern)

     for each_file in found_files:
         new_filename = each_file.replace(search_pattern,
                                          target_pattern)
         print "Renaming", each_file, "with", new_filename
         
         if self.__dryRun is False:
             os.rename(each_file, new_filename)
             


if __name__ == "__main__":
    
    import optparse
    
    
    command_options = optparse.OptionParser()
    
    command_options.add_option('--searchPattern',
                               dest='search',
                               default=None,
                               help='Search pattern for filenames in current directory')

    command_options.add_option('--targetPattern',
                               dest='target',
                               default=None,
                               help='Replacement pattern for new filename')

    command_options.add_option('--disableRecursive',
                               dest='subdirs',
                               default=True,
                               action='store_false',
                               help='Search sub-directories. Default is True.')

    command_options.add_option('--disableDryRun',
                               dest='dry_run',
                               default=True,
                               action='store_false',
                               help='Invoke dry run of the program. Default is True.')
    
    
    (values, args) = command_options.parse_args()
    
    c = RenameFiles()
    c.rename(values.search,
              values.target,
              values.subdirs,
              values.dry_run)
    
