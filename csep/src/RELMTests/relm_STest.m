function [rRelmTest] = relm_STest(vForecast, cObservedCatalog, ...
                                  vModifiedCatalogs, nNumberSimulation);
% function [rRelmTest] = relm_STest(vForecast, cObservedCatalog, 
%                                   vModifiedCatalogs, nNumberSimulation);
% --------------------------------------------------------------------------------------------------------------
% Computation of the S-test for the RELM framework.  For this computation,
% we renormalize the forecast so that the total number of forecasted events
% matches the total number of observed events, then we conduct the L-test
% with the normalized forecast.  This means that all simulated catalogs
% should also have a fixed number of events rather than having Poisson
% distribution in the number of events.  For this functionality, we can use
% Schorlemmer's implementation of converting the forecast to an ECDF and
% then dropping events in.
%
%
% Input parameters:
%   vForecast                 Forecast model
%   cObservedCatalog          Catalog with observered events
%   vModifiedCatalogs         Catalogs with applied uncertainties
%   nNumberSimulation         Number of random simulations
%
% Output paramters:
%   rRelmTest.fZeta             Zeta-value of the cumulative density
%   rRelmTest.vSimulation        Vector containing the simulated numbers of events
%   rRelmTest.nSimulationCount   Number of random simulations
%   rRelmTest.fLogLikelihood     Normalized Log-likelihood
%   rRelmTest.nModificationCount Number of catalog modifications
%   rRelmTest.vModification      Vector containing the numbers of events for 
%                                modified catalogs.
%
% Copyright (C) 2008 by J. Douglas Zechar
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


global Forecast_MinLongitude;
global Forecast_MaxLongitude;
global Forecast_MinLatitude;
global Forecast_MaxLatitude;
global Forecast_DepthTop;
global Forecast_DepthBottom;
global Forecast_MinMagnitude;
global Forecast_MaxMagnitude;
global Forecast_Rate;
global TestRandomFile;
global Forecast_PrecomputedZeroLikelihood;
global Forecast_MaskBit;

% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Reduce the forecast to a spatial forecast only, by finding the unique
% spatial bins and summing the rates over the constituent bins
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Find the number of unique spatial cells
nNumberSpatialCells = length(unique(vForecast(:, Forecast_MinLongitude:Forecast_MaxLatitude), 'rows'));

% Make enough room for each spatial cell
vSpatialForecast = zeros(nNumberSpatialCells, length(vForecast(1, :)));

% Set the min/max lat/lon for each spatial cell
vSpatialForecast(:, Forecast_MinLongitude:Forecast_MaxLatitude) = unique(vForecast(:, Forecast_MinLongitude:Forecast_MaxLatitude), 'rows');
vSpatialForecast(:, Forecast_MaskBit) = 1;

% Set the rate in each spatial cell by summing over the relevant bins , set
% the min/max depth/mag for this cell
for i=1:length(vSpatialForecast)
    % Find the bins that cover this cell, I discovered that four individual
    % find statements that take a progressive search approach is faster
    % than one find statement that has all the logic inside
    vSel = vForecast(find(vForecast(:,Forecast_MinLongitude) == vSpatialForecast(i, Forecast_MinLongitude)), :);
    vSel = vSel(find(vSel(:, Forecast_MaxLongitude) == vSpatialForecast(i, Forecast_MaxLongitude)), :);
    vSel = vSel(find(vSel(:, Forecast_MinLatitude) == vSpatialForecast(i, Forecast_MinLatitude)), :);
    vSel = vSel(find(vSel(:, Forecast_MaxLatitude) == vSpatialForecast(i, Forecast_MaxLatitude)), :);
    
%     vSel = find(vForecast(:,Forecast_MinLongitude) == vSpatialForecast(i, Forecast_MinLongitude) & ...
%         vForecast(:, Forecast_MaxLongitude) == vSpatialForecast(i, Forecast_MaxLongitude) & ...
%         vForecast(:, Forecast_MinLatitude) == vSpatialForecast(i, Forecast_MinLatitude) & ...
%         vForecast(:, Forecast_MaxLatitude) == vSpatialForecast(i, Forecast_MaxLatitude));
%     vSpatialForecast(i, Forecast_Rate) = sum(vForecast(vSel, Forecast_Rate));

    % The spatial rate is the sum over all constituent bins
    vSpatialForecast(i, Forecast_Rate) = sum(vSel(:, Forecast_Rate));
    
    % The min/max depth/mag for this new bin should be set to the min/max
    % depth/mag over all the bins in this spatial cell
    vSpatialForecast(i, Forecast_DepthTop) = min(vSel(:, Forecast_DepthTop));
    vSpatialForecast(i, Forecast_DepthBottom) = max(vSel(:, Forecast_DepthBottom));
    vSpatialForecast(i, Forecast_MinMagnitude) = min(vSel(:, Forecast_MinMagnitude));
    vSpatialForecast(i, Forecast_MaxMagnitude) = max(vSel(:, Forecast_MaxMagnitude));    
end;

% Normalize the forecast rates so that the total number of forecast events
% matches the total number of observed events.  To do this, we divide each
% rate by the total number of forecast events, then multiply each rate by
% the total number of observed events.
nNumberQuakesObserved = relm_NumberEventsCatalog(vForecast, cObservedCatalog);
fNumberQuakesForecast = relm_NumberEvents(vSpatialForecast(:, Forecast_Rate));

vNormalizedForecast = vSpatialForecast;
vNormalizedForecast(:,Forecast_Rate) = vNormalizedForecast(:,Forecast_Rate) / fNumberQuakesForecast * nNumberQuakesObserved;

% Pre-compute the log-likelihood for zero events per bin and add to the forecast model
vNormalizedForecast(:, Forecast_PrecomputedZeroLikelihood) = ...
    calc_logpoisspdf(zeros(length(vNormalizedForecast(:,1)),1), ...
    vNormalizedForecast(:,Forecast_Rate));

% Compute the "true" result
% Log-likelihood of the normalized forecast given the observation
fLogLikelihood = relm_LogLikelihoodCatalogOptimizedShort(vNormalizedForecast, ...
    cObservedCatalog);


% Number of modified catalogs
nNumberModification = length(vModifiedCatalogs);

% Compute the "results" of the modifications
vLogLikelihoodsModifications = zeros(nNumberModification, 1);
for nCnt = 1:nNumberModification
    cCatalog = vModifiedCatalogs{nCnt};
    % We want to renormalize the forecast so that the total number of
    % events forecast matches the total number of events in the
    % modification of interest
    nTempNumberQuakesObserved = relm_NumberEventsCatalog(vForecast, cCatalog);
    vTempNormalizedForecast = vSpatialForecast;
    vTempNormalizedForecast(:,Forecast_Rate) = vTempNormalizedForecast(:,Forecast_Rate) / fNumberQuakesForecast * nTempNumberQuakesObserved;   
    % Pre-compute the log-likelihood for zero events per bin and add to the forecast model
    vTempNormalizedForecast(:, Forecast_PrecomputedZeroLikelihood) = ...
    calc_logpoisspdf(zeros(length(vTempNormalizedForecast(:,1)),1), ...
    vTempNormalizedForecast(:,Forecast_Rate));

    vLogLikelihoodsModifications(nCnt)  = relm_LogLikelihoodCatalogOptimizedShort(vTempNormalizedForecast, cCatalog) - fLogLikelihood;
end;

% Remember original filename for the random seed file
s_test_file = TestRandomFile;

% Compute the "results" of the simulations
vLogLikelihoodsSimulations = zeros(nNumberSimulation, 1);

for nCnt = 1:nNumberSimulation
    % Compute the simulated number of events and sum them up
    vLogLikelihoodsSimulations(nCnt)  = relm_STestSimulation(vNormalizedForecast, nCnt, nNumberQuakesObserved, s_test_file) - ...
                                        fLogLikelihood;
end;


% Compute zeta and store the important parameters
rRelmTest.vSimulation = vLogLikelihoodsSimulations;
rRelmTest.fZeta = probability(vLogLikelihoodsSimulations, 0, nNumberSimulation);
rRelmTest.nSimulationCount = nNumberSimulation;
% normalized "true" result
rRelmTest.fLogLikelihood = 0; 
rRelmTest.nModificationCount = nNumberModification;
rRelmTest.vModification = vLogLikelihoodsModifications;

