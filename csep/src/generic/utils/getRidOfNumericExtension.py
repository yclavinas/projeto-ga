import os, glob, re

import Environment

#===============================================================================
# Utility class to get rid of numerical file extensions in files
#===============================================================================
class DirFiles (object):
    
    #===========================================================================
    # dir_path - Path to the directory with files to be renamed 
    #===========================================================================
    def rename(self, dir_path):
        
        
#        files = glob.glob('%s' %os.path.join(dir_path,
#                                             '*[0-9]'))

        files = glob.glob('%s' %os.path.join(dir_path,
                                             '*.svg'))
        
        for each_path in files:
            
            new_name = re.sub(r'svg$', 'png', each_path)
            print "Replacing", each_path, "by", new_name
            
            Environment.invokeCommand('convert -density 300 %s %s' %(each_path,
                                                                     new_name))
             
                
if __name__ == "__main__":
    
    files = DirFiles()
    
    all_subdirs = os.listdir('.')
    for each_dir in all_subdirs:
        if os.path.isdir(each_dir):
            files.rename(each_dir)
                    