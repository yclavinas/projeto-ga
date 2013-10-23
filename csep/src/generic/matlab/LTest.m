% Execute L-Test.
%
% Input parameters:
% sForecastFile - Path to the forecast file.
% sCatalogFile - Path to the declustered catalog file.
% sDir - Directory for the output data files.
%
% Output parameters:
% None.
%
function LTest(sForecastFile, sCatalogFile, sModificationsFile, sDir);

global NumRELMTestSimulations;
global RELM_DRAW_FIGURE;
global TestRandomFile;
global TestRandomFilePostfix;
     
% Prepare data
[vScaledForecast, sModelName, cCatalog, mModifications] = ...
   prepareTestData(sForecastFile, sCatalogFile, sModificationsFile);


sTest = sprintf('L-Test_%s', sModelName);
TestRandomFile = sprintf('%s/%s-randomSeed/%s%s', ...
                         sDir, sTest, sTest, TestRandomFilePostfix);

% Run L-test
rLTest = relm_LTest(vScaledForecast, cCatalog, ...
                    mModifications, NumRELMTestSimulations);


% Write results to the file, and display plots
writeTestData(rLTest, sDir, sTest, sModelName);                      


% Plot result data
if RELM_DRAW_FIGURE
   % Pass name of the model as description
   relm_PaintLTestCumPlot(rLTest, sModelName);
end;  
