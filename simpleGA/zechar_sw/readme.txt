To run the project from the command line, go to the folder where
CORSSA Theme VI Tools.jar resides and execute the following:

java -jar "CORSSA Theme VI Tools.jar" configFile

configFile should be a configuration of the format discussed below 

For example, to compute L/N/S/R/ASS/Molchan/ROC tests for the Double Branching Model (Marzocchi & Lombardi) and TripleS (Zechar & Jordan) forecasts using an example 1 year SW Pacific catalog, type

java -jar "CORSSA Theme VI Tools.jar" /pathToConfigFile/swConfig.txt

To compute an M test for the smoothed seismicity model of Helmstetter et al. type

java -jar "CORSSA Theme VI Tools.jar" /pathToConfigFile/hkjConfig.txt

To compute an M test for Ward's simulation model, type

java -jar "CORSSA Theme VI Tools.jar" /pathToConfigFile/wardSimConfig.txt

If yr system produces OutOfMemory errors, try prepending the -Xmx option, which increases the maximum amount of memory to be allocated.  For example, try

java -Xmx512m -jar "CORSSA Theme VI Tools.jar" /pathToConfigFile/hkjConfig.txt

I have included three example configuration files.  To make yr own custom configuration file, make sure it is in the following format:

forecastFile=path to forecast you wish to evaluate in ForecastML format (can be alarm function or Poisson rate forecast)
observationFile=path to catalog to which to compare the forecast of interest in ZMAP ASCII format
referenceForecastFile=path to reference forecast, only required/used when executing Molchan or ASS or GamblingScore tests
executeLTest=boolean ("true" or "false") indicating whether or not an L-test should be executed
executeMTest=boolean ("true" or "false") indicating whether or not an M-test should be executed
executeNTest=boolean ("true" or "false") indicating whether or not an N-test should be executed
executeRTest=boolean ("true" or "false") indicating whether or not an R-test should be executed
executeSTest=boolean ("true" or "false") indicating whether or not an S-test should be executed
executeMolchanTest=boolean ("true" or "false") indicating whether or not  Molchan-test should be executed
executeASSTest=boolean ("true" or "false") indicating whether or not an ASS-test should be executed
executeROCTest=boolean ("true" or "false") indicating whether or not an ROC-test should be executed
executeGamblingTest=boolean ("true" or "false") indicating whether or not a gambling score-test should be executed
resultsFile=path to file to which the results of all tests will be saved

The documented source code is also included in this package.

- J. Douglas Zechar, Zurich, June 2010
zechar at usc.edu