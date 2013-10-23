"""
Module SVNRepository
"""

__version__ = "$Revision$"
__revision__ = "$Id$"


import os, glob, pysvn, time

import CSEPLogging, CSEPLock


#-------------------------------------------------------------------------------
#
# SVNRepository.
#
# This class represents an interface for data repository using SVN
# 
class SVNRepository (object):

    # Static data of the class
    
    # Logger for the class
    __logger = None
    
    # main branch of SVN
    __trunkBranch = 'trunk'

    # tags branch of SVN
    __tagsBranch = 'tags'

    __logMessage = None
    

    # Number of seconds to sleep b/w re-tries to commit files to SVN (if it's 
    # locked by another process)
    __sleepSeconds = 2
    

    #---------------------------------------------------------------------------
    #
    # Initialization.
    #
    # Input: 
    #
    #        svn_working_dir - Directory with working copy of SVN. Default is None.
    #        start_date - Optional start date for raw data being archived.
    #                     Default is None
    # 
    def __init__ (self, 
                  svn_working_dir = None,
                  start_date = None):
        """ Initialization for SVNRepository class"""

        if SVNRepository.__logger is None:
           SVNRepository.__logger = CSEPLogging.CSEPLogging.getLogger(SVNRepository.__name__)
           
        self.__dir = svn_working_dir
        self.__dataStartDate = start_date
        
        if self.__dir is not None and start_date is not None:
            # Append start_date to the directory path of working copy 
            self.__dir = os.path.join(self.__dir,
                                      "StartDate_%s" %start_date.strftime("%Y_%m_%d"))

        self.__url = None
        self.__isWorkingCopy = False
        
        if self.__dir is not None:
            # Determine URL for SVN        
            client = pysvn.Client()
            
            try:
                entry = client.info(self.__dir)
                self.__url = entry.url
                self.__isWorkingCopy = True
            except:
                # It's not a working copy of SVN
                SVNRepository.__logger.info('%s directory is not a working copy of SVN' 
                                            %self.__dir)
                
        # Flag that working copy of repository has been modified and committed to 
        # the repository
        self.__isChanged = False
        
        self.__tag = None
        self.__tagComment = None
        self.__mainBranch = SVNRepository.__trunkBranch
        
        # Directory lock for working copy of SVN - seems more appropriate to use
        # instead of SVN-type of lock because:
        # 1) the whole directory should be locked - SVN operates on a single file
        # 2) the whole directory should be locked before download takes place, 
        #    not at a time of commit 
        self.__lock = None
     

    #----------------------------------------------------------------------------
    #
    # Object cleanup.
    #
    # Input: None
    # 
    def __del__ (self):
       """ Cleanup for SVNRepository class. Removes locks (if any) created by 
           the object."""
         
       self.unlock()
        

    #----------------------------------------------------------------------------
    #
    # Lock working copy of SVN (usually before download of new data)
    #
    def lock (self):
       """ Lock working copy of SVN."""
       
       if self.__dir is not None:  
           self.__lock = CSEPLock.DirLock(self.workingCopyDir())


    #----------------------------------------------------------------------------
    #
    # Allow to set main branch of SVN (to support import of already existing
    # raw catalogs into SVN: $SVN/data/import should be used to store each
    # iteration of new data, and $SVN/data/tags should be used to tag it with
    # process runtime information)
    #
    def mainBranch (self,
                    branch_name):
       """ Set main brunch of SVN."""
       
       self.__mainBranch = branch_name


    #----------------------------------------------------------------------------
    #
    # Unlock working copy of SVN
    #
    def unlock (self):
       """ Unlock working copy of SVN."""
         
       if self.__lock is not None:
           self.__lock.release()
           
           # Re-set the lock object to None once it's released
           self.__lock = None
       

    #===========================================================================
    # Return path to working copy of SVN.
    #===========================================================================
    def workingCopyDir (self):
        """ Return path to working copy of SVN."""

        return self.__dir
        

    #---------------------------------------------------------------------------
    #
    # Return flag to indicate if working copy of repository has been changed
    #
    # Input: None.
    #
    # Output: True if data has been changed, False otherwise
    #
    def __getModificationStatus (self):
        """ Return flag to indicate if working copy of repository has been changed."""

        return self.__isChanged
    
    Changed = property(__getModificationStatus, 
                       doc = "Flag to indicate if working copy of repository has been changed")
        

    #---------------------------------------------------------------------------
    @staticmethod
    def workingCopy (data_path):
        """ Return flag to indicate if entry is a working copy of SVN repository."""

        if data_path is not None:
            try:
                client = pysvn.Client()
                entry = client.info(data_path)
                return True

            except:
                # It's not a working copy of SVN
                SVNRepository.__logger.info('%s is not a working copy of SVN' 
                                            %data_path)
                return False


    #---------------------------------------------------------------------------
    #
    # Return flag to indicate if directory is a working copy of SVN repository
    #
    # Input: None.
    #
    # Output: True if directory is a working copy, False otherwise
    #
    def __getWorkingCopyStatus (self, data_path = None):
        """ Return flag to indicate if directory is a working copy of SVN repository."""

        # Filepath is not provided, just return status of directory that was
        # provided to instantiate object        
        return self.__isWorkingCopy
    
    isWorkingCopy = property(__getWorkingCopyStatus, 
                             doc = "Flag to indicate if entry is a working copy of SVN repository")


    #---------------------------------------------------------------------------
    #
    # Callback required by repository tagging
    #
    @staticmethod
    def __getLogMessage():
        return True, SVNRepository.__logMessage


    #---------------------------------------------------------------------------
    #
    # Commit changes if any to the repository
    #
    # Input: None 
    # 
    def commit (self, 
                comment = None,
                types = []): 
        """ Commit changes within working copy to SVN repository """

        # It is not a working copy of SVN, return
        if self.__dir is None:
            return self.__isChanged
        
        
        client = pysvn.Client()

        try:
            # Check if self.__dir is a working copy of SVN repository
            status = client.status(self.__dir)
            
            # If directory does not exist, status will be an empty list
            if len(status) == 0:
                return self.__isChanged
            
            # Check if there are new files of specified type
            new_files = []
            for each_type in types: 
                new_files.extend([each_file.path for each_file in status 
                                  if (each_file.text_status == pysvn.wc_status_kind.unversioned and
                                      each_file.path.endswith(each_type))])
        
            if len(new_files) != 0:
                
                # There are updated files, commit them to repository
                SVNRepository.__logger.info("Adding %s files to repository from %s: %s"
                                            %(len(new_files),
                                              self.__dir,
                                              new_files))
                client.add(new_files)
                

            # Check which existing files in SVN have been updated
            updated_files = [each_file.path for each_file in status 
                             if each_file.text_status == pysvn.wc_status_kind.modified]
        
            if len(new_files) != 0 or \
               len(updated_files) != 0:
                
                commit_successful = False
                    
                while commit_successful is False:
                    
                    try:
                    
                        # There are updated files, commit them to repository
                        SVNRepository.__logger.info("Committing files to repository from %s: %s updated files(%s), %s new files (%s)"
                                                    %(self.__dir,
                                                      len(updated_files),
                                                      updated_files,
                                                      len(new_files),
                                                      new_files))
                        client.checkin([self.__dir], 
                                       comment)
                        self.__isChanged = True
                        commit_successful = True
                        
                    except pysvn.ClientError, error:
                        
                        # Other than "SVN locked" exception has occurred
                        if 'locked' not in str(error):
                            raise
                        
                        else:
                            
                            SVNRepository.__logger.warning('SVN client exception has occurred: %s, will retry in %s seconds' %(error,
                                                                                                                               SVNRepository.__sleepSeconds))
                            # Repository is locked by another commit
                            time.sleep(SVNRepository.__sleepSeconds)
                
            else:
                # There is no change in working copy, report it in logging
                SVNRepository.__logger.info("There are no new or updated files in %s"
                                            %self.__dir)

            # If tag is provided, tag data in repository
            if self.__tag is not None and len(self.__tag) != 0:
                
                msg = "Setting SVN tag %s for %s" %(self.tagURL(),
                                                    self.__url)
                if comment is not None:
                    msg += ' (%s)' %comment
                
                if self.__tagComment is not None:
                    msg += ' (%s)' %self.__tagComment
                    
                SVNRepository.__logger.info(msg)

                try:
                    SVNRepository.__logMessage = msg
                    client.callback_get_log_message = SVNRepository.__getLogMessage
                    client.copy(self.__url,
                                self.tagURL())
                except pysvn.ClientError, error:
                    
                    # SVN tag already exists (generated by other process with
                    # exactly the same tag based on date and time stamp of runtime
                    # directory
                    error_str = str(error)
                    if 'exists'  in error_str and self.__tag in error_str:
                        # Generate an error if there are changes to the working copy
                        # that could not be committed
                        if len(new_files) != 0 or \
                           len(updated_files) != 0:
                            
                            error_msg = "Could not tag modified files in SVN: %s" %error
                            SVNRepository.__logger.error(error_msg)
                            raise RuntimeError, error_msg
                        else:
                            # Just generate a warning 
                            SVNRepository.__logger.warning(error_str)
                            
                    else:
                        # Some other exception has occurred, re-throw
                        raise
            
        except pysvn.ClientError, error:
            
            SVNRepository.__logger.error('SVN client exception has occurred: %s' %error)
        
        
        return self.__isChanged
   

    #---------------------------------------------------------------------------
    #
    # Set tag for data in repository
    #
    def setTag (self,
                tag_name,
                tag_comment = None):
        """Set tag for data in repository"""
        
        SVNRepository.__logger.info("Tag is provided: %s (comment='%s')" %(tag_name,
                                                                           tag_comment))
        self.__tag = tag_name
        self.__tagComment = tag_comment
        

    #---------------------------------------------------------------------------
    #
    # Get current tag for data in repository
    #
    def tagURL (self):
        """Get current tag for data in repository"""
        
        if self.__tag is None:
            return None
            
        tag_url = self.__url.replace(self.__mainBranch,
                                     SVNRepository.__tagsBranch)
        return os.path.join(tag_url, 
                            self.__tag)
        
        
# Invoke the module
if __name__ == '__main__':

   import EvaluationTestOptionParser
   import CSEPOptionParser

   parser = EvaluationTestOptionParser.EvaluationTestOptionParser()
        
   # List of requred options
   options = parser.options()
   
   storage = SVNRepository(options.test_dir)
   storage.commit()

   