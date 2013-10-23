#!/bin/bash

# the file downloads earthquake catalogs from ftp://www.ncedc.org/pub/catalogs/anss. 
# example how to use the file:
# use: ./downlaod_anss.sh year month  for year enter a year between 1985 and the current year. for month enter a number between 1 and 12.
# the script will download all catalogs from 1985 up to the year and month you entered when you started the script. the downloaded files will be stored in the directory in which the script is executed (see log file). 


# Marc Rierola, riri@sed.ethz.ch  28.06.2006




year=$1
month=$2
#if [ -e download_anss.log ]
#then
#mv download_anss.log download_anss.log~
#fi
date +"%b %d %T" >> download_anss.log
echo ""script was started" " >> download_anss.log 

#date >> download_anss.log
date +"%b %d %T" >> download_anss.log
echo "the current directory is:" >> download_anss.log
pwd >> download_anss.log
#echo "Year that was choosen: $year" >> download_anss.log
#echo "Month that was choosen: $month" >> download_anss.log

if [ $year -lt 1985 ] || [ $month -lt 1 ] || [ $month -gt 12 ]
then
echo You entered either a wrong year \(older than 1985\) or a wrong month \(has to be between 1 and 12\)!! 
date +"%b %d %T" >> download_anss.log
echo "You entered either a wrong year (older than 1985) or a wrong month (has to be between 1 and 12)!! Try again!" >> download_anss.log
elif [ $year -ge 1985 ] && [ $month -ge 1 ] && [ $month -le 12 ]
then
 
#create start year 1985
diffyear=`expr $1 - 1985`
echo $1
echo $2
echo $diffyear
myyears=`expr $1 - $diffyear`
mymonth=`expr $2 - $2`
echo $myyears
start=$myyears
echo $start
stop=`expr $1 - 1`
echo $stop
allyears=$start
echo $allyears
#get 1985 start year
wget -r -nd ftp://www.ncedc.org/pub/catalogs/anss/$allyears
date +"%b %d %T" >> download_anss.log
echo "Download for year 1985 started" >> download_anss.log
# create each year between 1985 and $1 which is the input.
while [ $allyears -lt $stop ]
do
allyears=`expr $allyears + 1`
echo $allyears
#echo "Current Year": $allyears >> download_anss.log
#get all years between 1985 and input	
wget -r -nd ftp://www.ncedc.org/pub/catalogs/anss/$allyears
date +"%b %d %T" >> download_anss.log
echo "Getting catalog for the current ( $allyears ) year" >> download_anss.log
done
#create increments for the last year.
if [ $month == 1 ]
then
increment=( 01 )
elif [ $month == 2 ]
then
increment=( 01 02 )
elif [ $month == 3 ]
then
increment=( 01 02 03 )
elif [ $month == 4 ]
then
increment=( 01 02 03 04 )
elif [ $month == 5 ]
then
increment=( 01 02 03 04 05 )
elif [ $month == 6 ]
then
increment=( 01 02 03 04 05 06 )
elif [ $month == 7 ]
then
increment=( 01 02 03 04 05 06 07 )
elif [ $month == 8 ]
then
increment=( 01 02 03 04 05 06 07 08 )
elif [ $month == 9 ]
then
increment=( 01 02 03 04 05 06 07 08 09 )
elif [ $month == 10 ]
then
increment=( 01 02 03 04 05 06 07 08 09 10 )
elif [ $month == 11 ]
then
increment=( 01 02 03 04 05 06 07 08 09 10 11 )
elif [$month == 12 ]
then
increment=( 01 02 03 04 05 06 07 08 09 10 11 12 )
fi
for years in ${increment[*]}
do
years=$year.$years.cnss
#get last year with increments
wget -r -nd ftp://www.ncedc.org/pub/catalogs/anss/$year/$years
date +"%b %d %T" >> download_anss.log
echo "Downloading $years " >> download_anss.log
done
fi
