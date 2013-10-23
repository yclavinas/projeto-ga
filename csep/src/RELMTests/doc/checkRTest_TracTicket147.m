initialize(false, false, true, 0, 1000, 0, true);
initializeForecast(2009, 2, 14, 1, 4.95, 30, 2008, 7, 1);
sForecastFile1='KJSSOneYearNWPacific_7_1_2008-fromXML.mat';
sForecastFile2='Triple_SNWPacific_7_1_2008-fromXML.mat';
sModificationsFile='';
sDir='temp\\';
sCatalogFile='catalog.nodecl.mat';
RTest(sForecastFile1, sForecastFile2, sCatalogFile, sModificationsFile, sDir);
RTest(sForecastFile2, sForecastFile1, sCatalogFile, sModificationsFile, sDir);

sForecastFile2='Triple_SNWPacific_7_1_2008-fromXML2.mat';
RTest(sForecastFile1, sForecastFile2, sCatalogFile, sModificationsFile, sDir);
RTest(sForecastFile2, sForecastFile1, sCatalogFile, sModificationsFile, sDir);