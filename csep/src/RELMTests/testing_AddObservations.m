function [vRates] = testing_AddObservations(vRates, mCatalog);

% Declare global variables
global USE_FORECAST_WEIGHTS;
global Forecast_MinLongitude;
global Forecast_MaxLongitude;
global Forecast_MinLatitude;
global Forecast_MaxLatitude;
global Forecast_DepthTop;
global Forecast_DepthBottom;
global Forecast_MinMagnitude;
global Forecast_MaxMagnitude;
global Forecast_MaskBit;
global Forecast_Observations;


% Get the number of earthquakes in catalog
[nRow] = length(mCatalog(:,1));

% Delete any observation in column 11
vRates(:, Forecast_Observations) = zeros(length(vRates(:,1)),1);

for nCnt = 1:nRow
  x = mCatalog(nCnt,1);
  y = mCatalog(nCnt,2);
  z = mCatalog(nCnt,7);
  m = mCatalog(nCnt,6);

  vSel = ((vRates(:, Forecast_MinLongitude) <= x) & (vRates(:, Forecast_MaxLongitude) > x) & ...
          (vRates(:, Forecast_MinLatitude) <= y) & (vRates(:, Forecast_MaxLatitude) > y) & ...
          (vRates(:, Forecast_DepthTop) <= z) & (vRates(:, Forecast_DepthBottom) > z) & ...
          (vRates(:, Forecast_MinMagnitude) <= m) & (vRates(:, Forecast_MaxMagnitude) > m));
          
  vRates(vSel, Forecast_Observations) = vRates(vSel, Forecast_Observations) + 1;
end;
