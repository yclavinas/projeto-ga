function [rRelmTest] = relm_RTest(vForecast1, vForecast2, cObservedCatalog, ...
                                  vModifiedCatalogs, nNumberSimulation, sRandomFile);
% function [rRelmTest] = relm_RTest(vForecast1, vForecast2, cObservedCatalog, 
%                                   vModifiedCatalogs, nNumberSimulation);
% --------------------------------------------------------------------------------------------------------------
% Computation of the R-test for the RELM framework
%
% Input parameters:
%   vForecast1                First forecast model
%   vForecast2                Second forecast model
%   cObservedCatalog          Catalog with observered events
%   vModifiedCatalogs         Catalogs with applied uncertainties
%   nNumberSimulation         Number of random simulations
%   sRandomFile               Optional filename for random numbers. 
%                             This is introduced only for acceptance test 
%                             purposes since we don't store random numbers
%                             to the file, only the seed to generate those numbers.
%
% Output paramters:
%   rRelmTest.fAlpha             Alpha value of the cumulative density
%   rRelmTest.fBeta              Beta value of the cumulative density
%   rRelmTest.vSimulation1       Vector containing the simulated numbers of 
%                                events for the first forecast model
%   rRelmTest.vSimulation2       Vector containing the simulated numbers of 
%                                events for the second forecast model
%   rRelmTest.nSimulationCount   Number of random simulations
%   rRelmTest.fLogLikelihood     Log-likelihood ratio
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

% Pre-compute the log-likelihood for zero events per bin and add to the forecast models
vForecast1(:, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(zeros(length(vForecast1(:,1)),1), vForecast1(:,Forecast_Rate));
vForecast2(:, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(zeros(length(vForecast2(:,1)),1), vForecast2(:,Forecast_Rate));

% Compute the "true" result
% Log-likelihood ratio of the forecasts given the observation
fLogLikelihoodRatio = relm_LogLikelihoodRatioCatalogOptimizedShort(vForecast1, ...
                                                                   vForecast2, ...
                                                                   cObservedCatalog);


% Number of modified catalogs
nNumberModification = length(vModifiedCatalogs);

% Compute the "results" of the modifications
vLogLikelihoodRatiosModifications = zeros(nNumberModification, 1);
for nCnt = 1:nNumberModification
   cCatalog = vModifiedCatalogs{nCnt};
   vLogLikelihoodRatiosModifications(nCnt)  = relm_LogLikelihoodRatioCatalogOptimizedShort(vForecast1, vForecast2, cCatalog) - fLogLikelihoodRatio;
end;


% Remember original filename for the random seed file
s_test_file = TestRandomFile;


% Compute the "results" of the simulations
vLogLikelihoodRatiosSimulations1 = zeros(nNumberSimulation, 1);
vLogLikelihoodRatiosSimulations2 = zeros(nNumberSimulation, 1);


for nCnt = 1:nNumberSimulation

    % Compute the simulated number of events and sum them up
    nSimForecast = 1;
    vLogLikelihoodRatiosSimulations2(nCnt)  = relm_RTestSimulation(vForecast1, ...
                                                                   vForecast2, ...
                                                                   nSimForecast, ...
                                                                   nCnt, ...
                                                                   s_test_file) - ...
                                              fLogLikelihoodRatio;
                                                                                                     
    % Obtain random numbers for the second model
    nSimForecast = 2;    
    vLogLikelihoodRatiosSimulations1(nCnt)  = -1.0 * relm_RTestSimulation(vForecast1, ...
                                                                       vForecast2, ...
                                                                       nSimForecast, ...
                                                                       nCnt, ...
                                                                       s_test_file) + ...
                                              fLogLikelihoodRatio;
  end;


% Compute Alpha, Beta and store the important parameters
rRelmTest.vSimulation1 = vLogLikelihoodRatiosSimulations1;
rRelmTest.vSimulation2 = vLogLikelihoodRatiosSimulations2;
rRelmTest.fAlpha = probability(vLogLikelihoodRatiosSimulations2, 0, nNumberSimulation);
rRelmTest.fBeta = probability(vLogLikelihoodRatiosSimulations1, 0, nNumberSimulation);
rRelmTest.nSimulationCount = nNumberSimulation;
% normalized "true" result
rRelmTest.fLogLikelihoodRatio = 0;
rRelmTest.nModificationCount = nNumberModification;
rRelmTest.vModification = vLogLikelihoodRatiosModifications;

