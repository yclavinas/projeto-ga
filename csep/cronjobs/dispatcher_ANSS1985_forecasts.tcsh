#!/bin/tcsh

# dispatcher_ANSS1985_forecasts.tcsh:
#
# Run daily Dispatcher to generate one-day forecasts.
# All groups use ANSS catalog with start date of 1985-01-01 and Magnitude>=3.0.
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
set logdir=$CSEP/dispatcher/logs/"$year"_"$month"
mkdir -p "$logdir"

set logfile="$logdir"/dailyANSS1985_"$year-$month-$day-$hour$min$sec"


# Invoke Dispatcher for "today" (with 31 day delay for the testing date):
nohup python $CENTERCODE/src/generic/Dispatcher.py --year="$year" --month="$month" --day="$day" --configFile=/usr/local/csep/cronjobs/dispatcher_ANSS1985_forecasts.init.xml --waitingPeriod=31 --enableForecastXMLTemplate --enableForecastMap --tests=" " --publishServer=csep-usc@shear.usc.edu --publishDirectory=/home/scec-03/csep/us/results/data/us/usc/california --logFile="$logfile" >& "$logfile" &


