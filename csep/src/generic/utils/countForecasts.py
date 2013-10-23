import os, glob
from ForecastGroupInitFile import ForecastGroupInitFile


#===============================================================================
# Utility class to collect available forecasts within testing region
#===============================================================================
class TestingRegion (object):
    
    #===========================================================================
    # region_path - Path to the testing region top-level directory 
    #===========================================================================
    def countForecasts(self, region_path):
        
        
        print 'REGION: %s' %region_path
        
        group_dirs = os.listdir(region_path)
        
        cwd = os.getcwd()
         
        for each_path in group_dirs:
            
            dir_path = os.path.join(region_path, each_path)
            if os.path.isdir(dir_path) is True and each_path != 'cronjobs' and \
               each_path != '.svn' and (each_path.find('optimized') < 0):
         
                init_file = ForecastGroupInitFile(dir_path)
                __tests = init_file.elementValue(ForecastGroupInitFile.EvaluationTestElement)
                os.chdir(dir_path)
               
                print "ForecastGroup: %s" %dir_path
                print '---> EvaluationTests: %s' %__tests  
                self.__findForecasts()
                
                print '\n\n'
                os.chdir(cwd)
                
                
    def __findForecasts(self):
        
        found_files = glob.glob('forecasts/*-fromXML.mat')
        
        if len(found_files) == 0:
            
            # For file-based forecasts which are placed directly under forecast group
            # top-level directory
            found_files = glob.glob('*-fromXML.mat')
            
        
        if len(found_files) == 0:
                
            # Check out archive directory
            if os.path.exists('forecasts/archive') is True:
                found_dirs = glob.glob('forecasts/archive/20*')
                found_dirs.sort()

                # There are archived files, check for content of only one archive
                # for filenames 
                if len(found_dirs) != 0:
                    print "Forecasts archives: ", found_dirs  
                    found_files = glob.glob('%s/*-fromXML.mat' %found_dirs[0])
 
        print "===>num=%s" %len(found_files)
        
        for each_file in found_files:
            print "--->forecast: ", each_file
                
                
if __name__ == "__main__":
    
    all_regions = TestingRegion()
    
    center_code_env = os.environ["CSEP"]
    
    all_regions.countForecasts(os.path.join(center_code_env,
                                            'SCEC-natural-laboratory'))
    
    all_regions.countForecasts(os.path.join(center_code_env,
                                            'testing-regions/SWPacific'))

    all_regions.countForecasts(os.path.join(center_code_env,
                                            'testing-regions/NWPacific'))

    all_regions.countForecasts(os.path.join(center_code_env,
                                            'testing-regions/Global'))
                    