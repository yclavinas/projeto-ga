#!/bin/tcsh

# batch_reprocess.tcsh:
#
# Run re-processing of test dates for one-day models in batch mode
#

source ~/.tcshrc

set year=`date '+%Y'`
# Don't pad integer values with zero's
set month=`date '+%_m'`
set day=`date '+%_d'`

# Pad time values with zero's
set hour=`date '+%H'`
set min=`date '+%M'`
set sec=`date '+%S'`

# Capture all output produced by Dispatcher into the daily log file
set logfile=$CSEP/batchProcessing/logs/batch_"$year-$month-$day-$hour$min$sec"


# Invoke BatchProcessing for "today":
nohup python $CENTERCODE/src/generic/BatchProcessing.py --configFile=$CSEP/cronjobs/reprocess/batch.init.xml --logFile="$logfile" >& "$logfile" &


