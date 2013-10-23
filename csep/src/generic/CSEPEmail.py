"""
Module CSEPEmail
"""

__version__ = "$Revision: 3479 $"
__revision__ = "$Id: CSEPEmail.py 3479 2011-08-30 21:28:02Z liukis $"


import datetime, logging, smtplib, email, os
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import CSEPLogging


#--------------------------------------------------------------------------------
#
# CSEPEmail.
#
# Structure-like class that contains email information.
#
class CSEPEmail (object):

   # Static data of the class
   
   # Configuration file elements and attributes
   Element = 'email'
   HostAttribute = 'smtphost'
   UserAttribute = 'username'    
   PasswordAttribute = 'password'    
   FromAttribute = 'from'
   SubjectPrefixAttribute = 'subjectPrefix'
   SubjectFromAttribute = 'subjectFrom'

   __logger = None
    
   #-------------------------------------------------------------------------
   #
   # Initialization for EmailInfo.
   #
   # Input:
   #        init_file - ElementTree object representing Dispatcher 
   #                    initialization file.
   #
   def __init__(self, init_file):
      """ Initialization for EmailInfo."""
       
      if CSEPEmail.__logger is None:
         CSEPEmail.__logger = CSEPLogging.CSEPLogging.getLogger(CSEPEmail.__name__)
             
      # List of email addresses to send report to
      self.__toAddresses = None
      self.__fromAddress = None
      # Mailhost - defaults to localhost
      self.__host = '127.0.0.1'
      self.__user = None
      self.__password = None
      self.__subjectPrefix = ''
      self.__subjectFrom = 'CSEP'
      self.__attachResults = None
   
      # Extract 'to' addresses          
      value = init_file.elementValue(CSEPEmail.Element)
       
      # email element is present and has addresses specified
      if value is not None:
         self.__toAddresses = value.split()
          
         if len(self.__toAddresses) == 0:
            # email element is present but does not provide any addresses
            self.__toAddresses = None
         else:
             
            # Attributes dictionary for the email element
            attribs = init_file.elements(CSEPEmail.Element)[0].attrib
   
            # Extract hostname for the mail server
            if CSEPEmail.HostAttribute in attribs:
               self.__host = attribs[CSEPEmail.HostAttribute]
   
            else:
               error_msg = "%s file: %s element is missing '%s' attribute." \
                           %(init_file.name, 
                             CSEPEmail.Element,
                             CSEPEmail.HostAttribute)
                           
               CSEPEmail.__logger.error(error_msg) 
               raise RuntimeError, error_msg
   
            # Extract from address
            if CSEPEmail.FromAttribute in attribs:
               self.__fromAddress = attribs[CSEPEmail.FromAttribute]
   
            else:
               error_msg = "%s file: '%s' element is missing '%s' attribute." \
                           %(init_file.name,
                             CSEPEmail.Element,
                             CSEPEmail.FromAttribute)
                           
               CSEPEmail.__logger.error(error_msg) 
               raise RuntimeError, error_msg
             
            if CSEPEmail.UserAttribute in attribs:
               self.__user = attribs[CSEPEmail.UserAttribute]                   
                
               # if user name was provided, password must be present too:
               if CSEPEmail.PasswordAttribute in attribs:
                  self.__password = attribs[CSEPEmail.PasswordAttribute]     
   
               else:
                  error_msg = "%s file: '%' element is missing '%s' attribute." \
                              %(init_file.name, 
                                CSEPEmail.Element,
                                CSEPEmail.PasswordAttribute)
                              
                  CSEPEmail.__logger.error(error_msg) 
                  raise RuntimeError, error_msg

            if CSEPEmail.SubjectPrefixAttribute in attribs:
               self.__subjectPrefix = attribs[CSEPEmail.SubjectPrefixAttribute]                   

            if CSEPEmail.SubjectFromAttribute in attribs:
               self.__subjectFrom = attribs[CSEPEmail.SubjectFromAttribute]


   #-------------------------------------------------------------------------
   #
   # Send message.
   #
   # Input:
   #        msg - Body of the message
   #        subject - Subject for the message
   #        status - Status of the run
   #        hostname - Host where process, that sends e-mail, runs
   #
   def send(self, 
            msg, 
            subject, 
            status, 
            hostname,
            attach_files = []):
      """ Send provided message."""
   
      # e-mail addresses were provided
      if self.__toAddresses is not None:
       
         message = MIMEMultipart()
         message.attach(MIMEText(msg))
         
         message["From"] = self.__fromAddress
         message["To"] = ", ".join(self.__toAddresses)
         

         subject_info = self.__subjectPrefix
         
         if isinstance(subject, datetime.datetime):
            
            if len(subject_info) != 0 and subject_info[-1] != ' ':
               subject_info += ' '
               
            subject_info += "TestDate %s" %subject.date()


         message["Subject"] = "[%s@%s] %s %s" \
                              %(self.__subjectFrom,
                                hostname, 
                                subject_info,
                                status)
                              
         for each_file in attach_files:
             CSEPEmail.__logger.info("Attaching %s to status message" %each_file)
             
             fp = open(each_file, 'rb')
             img = MIMEImage(fp.read())
             fp.close()
             img.add_header('Content-Disposition', 
                            'attachment', 
                            filename=os.path.basename(each_file))
             message.attach(img)
            
         server = smtplib.SMTP(self.__host)
          
         if self.__user is not None:
            # User name and password are provided, login using that info
            server.login(self.__user, self.__password)
         
         CSEPEmail.__logger.info("Sending message to %s: \
subject=%s with %s status" %(self.__toAddresses, subject, status))    
         server.sendmail(self.__fromAddress,
                         self.__toAddresses,
                         message.as_string())                     
         server.quit()
       
      return
          
   
# Invoke the module
if __name__ == '__main__':

   import DispatcherInitFile, DispatcherOptionParser, Environment

   options = DispatcherOptionParser.DispatcherOptionParser().options()
   init_file = DispatcherInitFile.DispatcherInitFile(options.config_file)
   
   if init_file.exists():
      test_email = CSEPEmail(init_file)
      host_name = Environment.commandOutput('hostname').strip()
      test_email.send("Test message", 
                      datetime.datetime.now(), 
                      "TEST STATUS",
                      host_name,
                      attach_files = ['SystemInfrastructure.png.34456'])

   # Shutdown logging
   logging.shutdown()
   
# end of main

