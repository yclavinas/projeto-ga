% Scale Forecast rates by specified factor.
%
% Input parameters:
% sForecastFile - Path to the forecast file.
% mScaleFactor - Scale factor to apply to the rate column of the forecast.
%
% Output parameters:
% vRates - Scaled forecast data.
%
function[mModel] = scaleForecast(sForecastFile, mScaleFactor);

% Declare globals
global Forecast_Rate;


% Load forecast file (into mModel variable)
[mModel] = loadForecastFile(sForecastFile);

% Scale the 'Rate' of the forecast
mModel(:, Forecast_Rate) = mModel(:, Forecast_Rate)*mScaleFactor;
