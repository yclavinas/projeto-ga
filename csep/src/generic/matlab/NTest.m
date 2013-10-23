% Execute N-Test.
%
% Input parameters:
% sForecastFile - Path to the forecast file.
% sCatalogFile - Path to the declustered catalog file.
% sDir - Directory for the output data files.
%
% Output parameters:
% None.
%
function NTest(sForecastFile, sCatalogFile, sModificationsFile, sDir);

% Declare global variables
global RELM_DRAW_FIGURE;


[vScaledForecast, sModelName, cCatalog, mModifications] = ...
   prepareTestData(sForecastFile, sCatalogFile, sModificationsFile);


sTest = sprintf('N-Test_%s', sModelName);

% Run N-test
rNTest = relm_NTestNoRandom(vScaledForecast, cCatalog, mModifications);


% Write results to the file, and display plots
writeTestData(rNTest, sDir, sTest, sModelName);                      


% Plot result data
if RELM_DRAW_FIGURE
   % Pass name of the model as description
   relm_PaintNTestCumPlot(rNTest, sModelName);
end;  
