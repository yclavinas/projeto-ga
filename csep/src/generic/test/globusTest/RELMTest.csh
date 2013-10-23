#!/bin/csh

# This script is invoked by 'globus_job_run' or 'globus_job_submit' commands.
# To run the script, type on a command line:
# globus_job_run motion -s CSEP/src/LongtermForecast/test/RELMTest.csh


setenv CENTERCODE /home/mliukis/globusStage/src/
setenv CENTERCODEPATH /home/mliukis/globusStage/src/
setenv PYTHONPATH /home/mliukis/globusStage/src/LongtermForecast:/home/mliukis/globusStage/src/generic


/usr/bin/python /home/mliukis/globusStage/src/LongtermForecast/test/RELMTest.py --year=2006 --month=11 --day=1 --catalog=catalog.decl.mat --forecasts=/home/mliukis/globusStage/test_forecast --test="N"
