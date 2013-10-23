% Execute M-Test.
%
% Input parameters:
% sForecastFile - Path to the forecast file.
% sCatalogFile - Path to the declustered catalog file.
% sDir - Directory for the output data files.
%
% Output parameters:
% None.
%
function MTest(sForecastFile, sCatalogFile, sModificationsFile, sDir);

global NumRELMTestSimulations;
global RELM_DRAW_FIGURE;
global TestRandomFile;
global TestRandomFilePostfix;
     
% Prepare data
[vScaledForecast, sModelName, cCatalog, mModifications] = ...
   prepareTestData(sForecastFile, sCatalogFile, sModificationsFile);


sTest = sprintf('M-Test_%s', sModelName);
TestRandomFile = sprintf('%s/%s-randomSeed/%s%s', ...
                         sDir, sTest, sTest, TestRandomFilePostfix);

% Run L-test
rMTest = relm_MTest(vScaledForecast, cCatalog, ...
                    mModifications, NumRELMTestSimulations);


% Write results to the file, and display plots
writeTestData(rMTest, sDir, sTest, sModelName);                      


% Plot result data
if RELM_DRAW_FIGURE
   % Pass name of the model as description
   relm_PaintLTestCumPlot(rMTest, sModelName);
end;  
