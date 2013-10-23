#!/bin/tcsh

# dispatcher_one_year.tsh:
#
# Run daily Dispatcher for OceanicTransformFaults testing region 
# one day models generation and evaluation
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
set logdir=$CSEP/dispatcher/logs/Global/"$year"_"$month"
mkdir -p "$logdir"

set logfile="$logdir"/oceanic_transform_faults_daily_"$year-$month-$day-$hour$min$sec"


# Invoke Dispatcher for "today" (with 31 day delay for the testing date):
nohup python $CENTERCODE/src/generic/Dispatcher.py --year="$year" --month="$month" --day="$day" --forecastType=PolygonBased --configFile=/usr/local/csep/configuration/testing-regions/OceanicTransformFaults/cronjobs/dispatcher_daily.init.xml --waitingPeriod=31 --enableForecastXMLTemplate --enableForecastMap --publishServer=csep-usc@shear.usc.edu --publishDirectory=/home/scec-03/csep/us/results/data/us/usc/oceanic_transform_faults --logFile="$logfile" >& "$logfile" &

