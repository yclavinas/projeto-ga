function [fLikelihoodRatio] = relm_LogLikelihoodRatioCatalog(vForecast1, vForecast2, mCatalog);
% --------------------------------------------------------------------------------------------------------------
% Computation of the log-likelihood ratio for two forecast models.
%
% Input parameters:
%   vForecast1       First forecast model
%   vForecast2       Second forecast model
%   mCatalog         Catalog of events
%
% Output paramters:
%   fLikelihoodRatio       Likelihood ratio
%
% Copyright (C) 2007 by Danijel Schorlemmer
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
vForecast1(:, Forecast_Observations) = zeros(length(vForecast1(:,1)),1);
vForecast2(:, Forecast_Observations) = zeros(length(vForecast2(:,1)),1);

for nCnt = 1:nRow
  x = mCatalog(nCnt,1);
  y = mCatalog(nCnt,2);
  z = mCatalog(nCnt,7);
  m = mCatalog(nCnt,6);

  vSel1 = ((vForecast1(:, Forecast_MinLongitude) <= x) & (vForecast1(:, Forecast_MaxLongitude) > x) & ...
          (vForecast1(:, Forecast_MinLatitude)  <= y) & (vForecast1(:, Forecast_MaxLatitude)  > y) & ...
          (vForecast1(:, Forecast_DepthTop)     <= z) & (vForecast1(:, Forecast_DepthBottom)  > z) & ...
          (vForecast1(:, Forecast_MinMagnitude) <= m) & (vForecast1(:, Forecast_MaxMagnitude) > m));
  nIndex1 = find(vSel1);

  vSel2 = ((vForecast2(:, Forecast_MinLongitude) <= x) & (vForecast2(:, Forecast_MaxLongitude) > x) & ...
          (vForecast2(:, Forecast_MinLatitude)  <= y) & (vForecast2(:, Forecast_MaxLatitude)  > y) & ...
          (vForecast2(:, Forecast_DepthTop)     <= z) & (vForecast2(:, Forecast_DepthBottom)  > z) & ...
          (vForecast2(:, Forecast_MinMagnitude) <= m) & (vForecast2(:, Forecast_MaxMagnitude) > m));
  nIndex2 = find(vSel2);
  
  vForecast1(nIndex1, Forecast_Observations) = vForecast1(nIndex1, Forecast_Observations) + 1;
  vForecast2(nIndex2, Forecast_Observations) = vForecast2(nIndex2, Forecast_Observations) + 1;
  vForecast1(nIndex1, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(vForecast1(nIndex1, Forecast_Observations), vForecast1(nIndex1, Forecast_Rate));
  vForecast2(nIndex2, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(vForecast2(nIndex2, Forecast_Observations), vForecast2(nIndex2, Forecast_Rate));
end;

fLikelihoodRatio = sum(vForecast1(:, Forecast_PrecomputedZeroLikelihood)) - sum(vForecast2(:, Forecast_PrecomputedZeroLikelihood));

