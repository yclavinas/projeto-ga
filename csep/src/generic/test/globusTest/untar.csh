#!/bin/csh

# Untar source files required to run the job

# This script untars the previously copied with globus-url-copy command an archive of 
# source code and data file that are required to run the RELMTest. Tar file is copied to the
# stage area instead of actual files in order to preserve the file permissions.
tar xvf $1

