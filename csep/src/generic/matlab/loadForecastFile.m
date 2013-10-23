% Load forecast model from the file.
%
% Input parameters:
% sForecastFile - Path to the forecast file.
%
% Output parameters:
% vForecast - Forecast data.
%
function[vForecast] = loadForecastFile(sForecastFile);


% Load forecast file (into mModel variable)
rLoad = load(sForecastFile);

% Check if expected variable was loaded from the file
if isfield (rLoad, 'mModel')
   vForecast = rLoad.mModel;
else
   disp(['Unexpected variable is specified by the ', sForecastFile, ...
		      ' forecast file. Expected mModel. Exiting the test.']);
   pause;
end;
