function [rRelmTest] = relm_MTest(vForecast, cObservedCatalog, ...
                                  vModifiedCatalogs, nNumberSimulation);
% function [rRelmTest] = relm_MTest(vForecast, cObservedCatalog, 
%                                   vModifiedCatalogs, nNumberSimulation);
% --------------------------------------------------------------------------------------------------------------
% Computation of the M-test for the RELM framework.  For this computation,
% we renormalize the forecast so that the total number of forecasted events
% matches the total number of observed events, then we conduct the L-test
% with the normalized forecast, considering only the distribution in 
% magnitude space.  This means that all simulated catalogs should also 
% have a fixed number of events rather than having Poisson distribution in 
% the number of events.  For this functionality, we can use Schorlemmer's 
% implementation of converting the forecast to an ECDF and then dropping 
% events in.
%
%
% Input parameters:
%   vForecast                 Forecast model
%   cObservedCatalog          Catalog with observered events
%   vModifiedCatalogs         Catalogs with applied uncertainties
%   nNumberSimulation         Number of random simulations
%
% Output paramters:
%   rRelmTest.fKappa             Kappa-value of the cumulative density
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
% Reduce the forecast to a magnitude forecast only, by finding the unique
% magnitude cells and summing the rates over the constituent bins
% % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % % 
% Find the number of unique magnitude cells
nNumberMagnitudeCells = length(unique(vForecast(:, Forecast_MinMagnitude:Forecast_MaxMagnitude), 'rows'));

% Make enough room for each magnitude cell
vMagnitudeForecast = zeros(nNumberMagnitudeCells, length(vForecast(1, :)));

% Set the min/max magnitude for each cell
vMagnitudeForecast(:, Forecast_MinMagnitude:Forecast_MaxMagnitude) = unique(vForecast(:, Forecast_MinMagnitude:Forecast_MaxMagnitude), 'rows');
vMagnitudeForecast(:, Forecast_MaskBit) = 1;

% Set the rate in each magnitude cell by summing over the relevant bins , set
% the min/max lat/lon/depth for this cell
for i=1:length(vMagnitudeForecast(:, 1))
    % Find the bins that cover this cell, I discovered that individual
    % find statements that take a progressive search approach is faster
    % than one find statement that has all the logic inside
    vSel = vForecast(find(vForecast(:,Forecast_MinMagnitude) == vMagnitudeForecast(i, Forecast_MinMagnitude)), :);
    vSel = vSel(find(vSel(:, Forecast_MaxMagnitude) == vMagnitudeForecast(i, Forecast_MaxMagnitude)), :);
    
    % The magnitude rate is the sum over all constituent bins
    vMagnitudeForecast(i, Forecast_Rate) = sum(vSel(:, Forecast_Rate));
    
    % The min/max depth/lat/lon for this new bin should be set to the min/max
    % depth/mag over all the bins in this spatial cell
    vMagnitudeForecast(i, Forecast_MinLongitude) = min(vSel(:, Forecast_MinLongitude));
    vMagnitudeForecast(i, Forecast_MaxLongitude) = max(vSel(:, Forecast_MaxLongitude));
    vMagnitudeForecast(i, Forecast_MinLatitude) = min(vSel(:, Forecast_MinLatitude));
    vMagnitudeForecast(i, Forecast_MaxLatitude) = max(vSel(:, Forecast_MaxLatitude));    
    vMagnitudeForecast(i, Forecast_DepthTop) = min(vSel(:, Forecast_DepthTop));
    vMagnitudeForecast(i, Forecast_DepthBottom) = max(vSel(:, Forecast_DepthBottom));
end;

% Normalize the forecast rates so that the total number of forecast events
% matches the total number of observed events.  To do this, we divide each
% rate by the total number of forecast events, then multiply each rate by
% the total number of observed events.
nNumberQuakesObserved = relm_NumberEventsCatalog(vForecast, cObservedCatalog);
fNumberQuakesForecast = relm_NumberEvents(vMagnitudeForecast(:, Forecast_Rate));

vNormalizedForecast = vMagnitudeForecast;
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
    vTempNormalizedForecast = vMagnitudeForecast;
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
rRelmTest.fKappa = probability(vLogLikelihoodsSimulations, 0, nNumberSimulation);
rRelmTest.nSimulationCount = nNumberSimulation;
% normalized "true" result
rRelmTest.fLogLikelihood = 0; 
rRelmTest.nModificationCount = nNumberModification;
rRelmTest.vModification = vLogLikelihoodsModifications;

