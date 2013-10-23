% Write scale factor for the forecasts to the file
%
% Input parameters:
% sScaleFile - Filename to store forecast scaling factor for the test.
%
% Output parameters:
% None.
%
function writeScaleFactor(sScaleFile);


% Declare globals
global ForecastScaleFactor;

% Forecast scale factor is the same for all models within the group
save(sScaleFile, 'ForecastScaleFactor', '-ascii', '-double', '-tabs');		

