function [rRelmTest] = relm_LTest(vForecast, cObservedCatalog, ...
                                  vModifiedCatalogs, nNumberSimulation);
% function [rRelmTest] = relm_LTest(vForecast, cObservedCatalog, 
%                                   vModifiedCatalogs, nNumberSimulation);
% --------------------------------------------------------------------------------------------------------------
% Computation of the L-test for the RELM framework
%
% Input parameters:
%   vForecast                 Forecast model
%   cObservedCatalog          Catalog with observered events
%   vModifiedCatalogs         Catalogs with applied uncertainties
%   nNumberSimulation         Number of random simulations
%
% Output paramters:
%   rRelmTest.fGamma             Gamma-value of the cumulative density
%   rRelmTest.vSimulation        Vector containing the simulated numbers of events
%   rRelmTest.nSimulationCount   Number of random simulations
%   rRelmTest.fLogLikelihood     Log-likelihood
%   rRelmTest.nModificationCount Number of catalog modifications
%   rRelmTest.vModification      Vector containing the numbers of events for 
%                                modified catalogs.
%
% Copyright (C) 2002-2007 by Danijel Schorlemmer
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


global Forecast_Rate;
global TestRandomFile;
global Forecast_PrecomputedZeroLikelihood;


% Pre-compute the log-likelihood for zero events per bin and add to the forecast model
vForecast(:, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(zeros(length(vForecast(:,1)),1), vForecast(:,Forecast_Rate));

% Compute the "true" result
% Log-likelihood of the forecast given the observation
fLogLikelihood = relm_LogLikelihoodCatalogOptimizedShort(vForecast, cObservedCatalog);


% Number of modified catalogs
nNumberModification = length(vModifiedCatalogs);

% Compute the "results" of the modifications
vLogLikelihoodsModifications = zeros(nNumberModification, 1);
for nCnt = 1:nNumberModification
   cCatalog = vModifiedCatalogs{nCnt};
   vLogLikelihoodsModifications(nCnt)  = relm_LogLikelihoodCatalogOptimizedShort(vForecast, cCatalog) - fLogLikelihood;
end;

% Number of rows for random numbers for all simulations
[rows, cols] = size(vForecast);

% Remember original filename for the random seed file
s_test_file = TestRandomFile;

% Compute the "results" of the simulations
vLogLikelihoodsSimulations = zeros(nNumberSimulation, 1);

for nCnt = 1:nNumberSimulation

    % Compute the simulated number of events and sum them up
    vLogLikelihoodsSimulations(nCnt)  = relm_LTestSimulation(vForecast, nCnt, s_test_file) - ...
                                        fLogLikelihood;
end;


% Compute Gamma and store the important parameters
rRelmTest.vSimulation = vLogLikelihoodsSimulations;
rRelmTest.fGamma = probability(vLogLikelihoodsSimulations, 0, nNumberSimulation);
rRelmTest.nSimulationCount = nNumberSimulation;
% normalized "true" result
rRelmTest.fLogLikelihood = 0; 
rRelmTest.nModificationCount = nNumberModification;
rRelmTest.vModification = vLogLikelihoodsModifications;

