function [fLikelihood] = relm_LogLikelihoodCatalogOptimizedShort(vForecast, mCatalog);
% --------------------------------------------------------------------------------------------------------------
% Computation of the number of events in the catalog.
%
% Input parameters:
%   vForecast         Forecast model
%   mCatalog          Catalog of events
%
% Output paramters:
%   fvLikelihood      Likelihood
%
% Copyright (C) 2007-2008 by Danijel Schorlemmer & Maria Liukis
%
% This program is free software; you can redistribute it and/or modify
% it under the terms of the GNU General Public License as published by
% the Free Software Foundation; either version 2 of the License, or
% (at your option) any later version.
%
% This program is distributed in the hope that it will be useful,
% but WITHOUT ANY WARRANTY; without even the implied warranty of
% MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
% GNU General Public License for more details.
%
% You should have received a copy of the GNU General Public License
% along with this program; if not, write to the
% Free Software Foundation, Inc.,
% 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

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
global Forecast_Rate;
global Forecast_MaskBit;
global Forecast_Observations;
global Forecast_PrecomputedZeroLikelihood;


% Get the number of earthquakes in catalog
[nRow] = length(mCatalog(:,1));

% Delete any observation in column "Forecast_Observations"
vForecast(:, Forecast_Observations) = zeros(length(vForecast(:,1)),1);

for nCnt = 1:nRow
  x = mCatalog(nCnt,1);
  y = mCatalog(nCnt,2);
  z = mCatalog(nCnt,7);
  m = mCatalog(nCnt,6);

  vSel = ((vForecast(:, Forecast_MinLongitude) <= x) & (vForecast(:, Forecast_MaxLongitude) > x) & ...
          (vForecast(:, Forecast_MinLatitude) <= y) & (vForecast(:, Forecast_MaxLatitude) > y) & ...
          (vForecast(:, Forecast_DepthTop) <= z) & (vForecast(:, Forecast_DepthBottom) > z) & ...
          (vForecast(:, Forecast_MinMagnitude) <= m) & (vForecast(:, Forecast_MaxMagnitude) > m));
  nIndex = find(vSel);

  vForecast(nIndex, Forecast_Observations) = vForecast(nIndex, Forecast_Observations) + 1;
  vForecast(nIndex, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(vForecast(nIndex, Forecast_Observations), vForecast(nIndex, Forecast_Rate));
end;

fLikelihood = sum(vForecast(:, Forecast_PrecomputedZeroLikelihood));
