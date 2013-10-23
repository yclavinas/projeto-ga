% Initialize environment variables specific to the forecast models.
%
% Input parameters:
% nYear - Year of the test date
% nMonth - Month of the test date
% nDay - Day of the test date
% nDuration - Time duration for the forecast models.
% nMagnitude - Minimum magnitude for forecast models.
% nDepth - Maximum depth for forecast models.
% nStartYear - Year of the forecast start date
% nMonth - Month of the forecast start date
% nStartDay - Day of the forecast start date
%
% Output parameters:
% None.
%
function initializeForecast(nYear, nMonth, nDay, nDuration, nMagnitude, nDepth, ...
                                     nStartYear, nStartMonth, nStartDay);

% Forecast format identifiers
ForecastFormat;

% Set global variables to specified values
global ForecastMagnitudeThreshold;
global ForecastDecYearThreshold;
global ForecastDuration;
global ForecastScaleFactor;
global ForecastDepthThreshold;


ForecastMagnitudeThreshold = nMagnitude;
ForecastDuration = nDuration;
ForecastDepthThreshold = nDepth;
ForecastDecYearThreshold = decyear([nStartYear nStartMonth nStartDay 0 0 0]);

% Calculate scale factor for the forecast model based on the test date
fDay = decyear([nYear nMonth nDay 0 0 0]);
fDiff = fDay - ForecastDecYearThreshold;

% Fraction of the forecast duration
if fDiff == 0
	%%% If the same date is passed as test day and start date for the forecast (in case of
	%%% one day forecast), use scale factor of '1'.
   ForecastScaleFactor = 1;
else
	ForecastScaleFactor = fDiff/ForecastDuration;
end;
