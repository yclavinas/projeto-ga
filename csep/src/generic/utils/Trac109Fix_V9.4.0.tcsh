#!/bin/tcsh

# Script to rename existing cumulative filenames that are affected by the fix
# for Trac ticket #109 for CSEP V9.4.0:
#
# Unnecessary replacement of '_' with '-' for RELM test results (required by
# Matlab plotting which was replaced by matplotlib) is removed. 
#

pushd /var/www/html/csep/us/results/data/us/usc/california/five-year-rate-models/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=Triple-S-FiveYearCalifornia-RateBased --targetPattern=Triple_S_FiveYearCalifornia_RateBased --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/california/five-year-rate-models-V9.1/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=Triple-S-FiveYearCalifornia-RateBased --targetPattern=Triple_S_FiveYearCalifornia_RateBased --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/california/three-months-models/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=-Combined --targetPattern=_Combined --disableRecursive --disableDryRun;
popd;

#pushd /var/www/html/csep/us/results/data/us/usc/california/three-months-models-V9.4/results;
#python /home/scec/csep-usc/utils/renameFile.py --searchPattern=-Combined --targetPattern=_Combined --disableRecursive --disableDryRun;
#popd;

pushd /var/www/html/csep/us/results/data/us/usc/global/one-year-models/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=Triple-SOneYearGlobal-RateBased --targetPattern=Triple_SOneYearGlobal_RateBased --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/nwpacific/one-year-models/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=Triple-S --targetPattern=Triple_S --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/nwpacific/one-year-models-V9.1/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=Triple-S --targetPattern=Triple_S --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/swpacific/one-year-models/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=Triple-S --targetPattern=Triple_S --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/swpacific/one-year-models-V9.1/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=Triple-S --targetPattern=Triple_S --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/california/RELM-mainshock-aftershock-models/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=bird-liu --targetPattern=bird_liu --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=helmstetter-et-al --targetPattern=helmstetter_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=kagan-et-al --targetPattern=kagan_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=shen-et-al --targetPattern=shen_et_al --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/california/RELM-mainshock-aftershock-models-corrected/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=bird-liu --targetPattern=bird_liu --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=helmstetter-et-al --targetPattern=helmstetter_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=kagan-et-al --targetPattern=kagan_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=shen-et-al --targetPattern=shen_et_al --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/california/RELM-mainshock-models/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=helmstetter-et-al --targetPattern=helmstetter_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=kagan-et-al --targetPattern=kagan_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=shen-et-al --targetPattern=shen_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=wiemer-schorlemmer --targetPattern=wiemer_schorlemmer --disableRecursive --disableDryRun;
popd;

pushd /var/www/html/csep/us/results/data/us/usc/california/RELM-mainshock-models-corrected/results;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=helmstetter-et-al --targetPattern=helmstetter_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=kagan-et-al --targetPattern=kagan_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=shen-et-al --targetPattern=shen_et_al --disableRecursive --disableDryRun;
python /home/scec/csep-usc/utils/renameFile.py --searchPattern=wiemer-schorlemmer --targetPattern=wiemer_schorlemmer --disableRecursive --disableDryRun;
popd;
