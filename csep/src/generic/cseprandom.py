#!/usr/bin/env python

import random, datetime, sys, os

import CSEPFile
from Environment import *


class CSEPRandom(object):

    # Flag to retrieve the seed value to stdout: force seed generation if specified
    # file doesn't exist, or read seed from the file.
    ReadSeedFromFile = False
      
    # Buffer to store random numbers - to use to write it to the file
    __bufferSize = 1024
   
   
    #===========================================================================
    # Inputs:
    #         seed_filename - Filename to store/write random seed value to/from.
    #                         Default is None.
    #         seed_value - Seed value to use. Default is None.
    #===========================================================================
    def __init__ (self,
                  seed_filename = None,
                  seed_value = None):
        """ Initialize CSEPRandom object"""
        
        self.__lSeed = seed_value
        
        # If seed value is not explicitly provided, check if file with seed is 
        # provided (if CSEPRandom.ReadSeedFromFile is True), 
        # or need to generate one by the system (if CSEPRandom.ReadSeedFromFile 
        # is False)
        if self.__lSeed is None:
            self.seed(seed_filename)
        
        
    #===========================================================================
    # Create and store seed value to the file if CSEPRandom.ReadSeedFromFile
    # is set to False, or read seed value from specified file.
    #===========================================================================
    def seed(self, seed_filename):
       """Create seed value for random number generator and store it to the 
          specified file or read it from provided file if 
          'CSEPRandom.ReadSeedFromFile' is enabled (disabled by default)."""

           
       if CSEPRandom.ReadSeedFromFile is True:
          
          if seed_filename is None or \
             os.path.exists(seed_filename) is False:
             
             error_msg = "Seed filename must be provided: %s" %seed_filename
             raise RuntimeError, error_msg

          # Read seed value from existing file
          self.__lSeed = [long(val) for val in open(seed_filename)][0]
          
       else:
          
          self.__lSeed = CSEPRandom.createSeed() 
         
          # Write seed to the file if requested
          self.__writeSeed(seed_filename)
        
       return
   
    
    #===========================================================================
    #  Create seed value.
    # 
    # Output: seed value
    #===========================================================================
    @staticmethod
    def createSeed():
        """ Create seed value"""
        
        return hash(datetime.datetime.utcnow())


    def createNumbers(self, nNumber, sOutputFilename = None):
        """ Create nNumber number of random files. The method creates a seed value
        if it is not provided as input argument.""" 
        

        # Set Python's random seed
        random.seed(self.__lSeed)

        # Local variable optimization:
        new_random = random.random
    
        random_numbers = []
    
        # Open file output
        if sOutputFilename is not None:
            ftOutput = file(sOutputFilename, "w")
      
    
            left_to_write = nNumber
            now_to_write = CSEPRandom.__bufferSize  
            
            # Local variable optimization:
            output_write = ftOutput.write
            
            while left_to_write > 0:
                
               # Account for remainder of the the requested number of random values
               if now_to_write > left_to_write:
                  now_to_write = left_to_write
                   
               # Write buffer to the file
               output_write(' '.join(str(new_random()) for i in xrange(0, now_to_write)))         
               output_write(' ')
                
               # Update remaining number of random numbers to write
               left_to_write -= now_to_write
                
            ftOutput.close()
            
        else:
            # Return random numbers as a list
            # ATTN: cast nNumber to int type to get rid of warning message -
            #       sometimes it's specified by a caller as float  number
            random_numbers = [new_random() for i in xrange(int(nNumber))]

        return random_numbers
    

    def __writeSeed(self,
                    filename):
        """ Write seed used by random number generator to the file if output file
            is specified. """

        if filename is None:
        
            error_msg = "Seed filename must be provided to save new value: %s" \
                        %self.__lSeed
            raise RuntimeError, error_msg

        # Check if specified nested directory exists:
        seed_dir = os.path.dirname(filename)
        if len(seed_dir) != 0 and os.path.exists(seed_dir) is False:
            os.makedirs(seed_dir)
            
        fhandle = CSEPFile.openFile(filename, 
                                     CSEPFile.Mode.WRITE)
        fhandle.write("%s\n" %self.__lSeed)
        fhandle.close()



if __name__ == '__main__':

  import getopt


  # Read commandline arguments
  sCmdParams = sys.argv[1:]
  opts, args = getopt.gnu_getopt(sCmdParams, 
                                 'n:o:s:f:r:', 
                                 ['number=', 
                                  'output=', 
                                  'seed=', 
                                  'file=', 
                                  'readSeed='])

  # Set defaults
  number_values = 1
  output_filename = None
  seed_value = None
  seed_filename = None
  
  for option, parameter in opts:
    if option == '-n' or option == '--number':
      number_values = long(parameter)
      
    if option == '-o' or option == '--output':
      output_filename = parameter
      
    if option == '-s' or option == '--seed':
      seed = long(parameter)
      
    # Capture seed to specified ASCII file, or read seed from the specified
    # file if '--read' option is set to true
    if option == '-f' or option == '--file':
      seed_filename = parameter
      
    # Read seed value from specified ASCII file  
    if option == '-r' or option == '--readSeed':
      CSEPRandom.ReadSeedFromFile = bool(parameter)
      

  generator = CSEPRandom(seed_filename, 
                         seed_value)
  numbers = generator.createNumbers(number_values, 
                                    output_filename)

