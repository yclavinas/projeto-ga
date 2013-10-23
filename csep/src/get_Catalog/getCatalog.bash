#!/bin/bash

# $1 : Year
# $2 : Month
# $3 : Day
# $4 : Catalog filename

mkdir catalog
cd catalog

# Download raw data
$CENTERCODEPATH/getCatalog_Download.bash $1 $2 $3
cat *.cnss > import_raw.dat

# Pre-processing
awk -f $CENTERCODEPATH/getCatalog_PreProcess.Mag.awk import_raw.dat > temp1.dat
awk -f $CENTERCODEPATH/getCatalog_PreProcess.Loc.awk temp1.dat > temp2.dat
sed -f $CENTERCODEPATH/getCatalog_PreProcess.sed temp2.dat > import_processed.dat

# Prepare Script for Matlab
echo "addpath('`echo $CENTERCODEPATH`');" > invoke.m
echo "addpath('`echo $CENTERCODEPATH`getCatalog_Decluster');" >> invoke.m
echo "addpath('`echo $CENTERCODE`/LongtermForecast');" >> invoke.m;
echo "initialize;" >> invoke.m
echo "getCatalog_PostProcess(`echo $1`, `echo $2`, `echo $3`, '`echo $4`');" \
     >> invoke.m
echo "quit;" >> invoke.m

# Post-processing
matlab -nojvm -nodisplay -r invoke

# Garbage Collection
rm -f *.cnss
rm -f temp1.dat
rm -f temp2.dat
rm -f invoke.m

cd ..
