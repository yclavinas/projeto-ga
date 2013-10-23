% Execute R-Test.
%
% Input parameters:
% sForecastFile1 - Path to the first forecast model.
% sForecastFile2 - Path to the second forecast model.
% sCatalogFile - Path to the catalog file.
% sDir - Directory for the output data files.
%
% Output parameters:
% None.
%
function RTest(sForecastFile1, sForecastFile2, ...
               sCatalogFile, sModificationsFile, sDir);

global NumRELMTestSimulations;
global RELM_DRAW_FIGURE;

global TestRandomFile;
global TestRandomFilePostfix;
global Forecast_MaskBit;

     
% Prepare data
% Load second forecast file to obtain the weights
[vForecast] = loadForecastFile(sForecastFile2);

[vScaledForecast1, sModelName1, cCatalog, mModifications] = ...
   prepareTestData(sForecastFile1, sCatalogFile, sModificationsFile, ...
                   vForecast(:, Forecast_MaskBit));
   
% Load first forecast file to obtain the weights   
[vForecast] = loadForecastFile(sForecastFile1);   

[vScaledForecast2, sModelName2, cCatalog, mModifications] = ...
   prepareTestData(sForecastFile2, sCatalogFile, sModificationsFile, ...
                   vForecast(:, Forecast_MaskBit));


% Run R-test
sModelNames = sprintf('%s/%s', sModelName1, sModelName2);

sTest = sprintf('R-Test_%s_%s', sModelName1, sModelName2);
TestRandomFile = sprintf('%s/%s-randomSeed/%s%s', ...
                         sDir, sTest, sTest, TestRandomFilePostfix);

rRTest = relm_RTest(vScaledForecast1, vScaledForecast2, ...
 	                 cCatalog, mModifications, ...
     	              NumRELMTestSimulations);

% Write results to the file, and display plots
writeTestData(rRTest, sDir, sTest, sModelName1, sModelName2);                      


% Plot result data
if RELM_DRAW_FIGURE
   % Pass name of the model as description
   relm_PaintRTestCumPlot(rRTest, sModelNames);
end;  
