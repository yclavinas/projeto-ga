function [rRelmTest, mRandom] = relm_LEvaluationTest(vForecast, cObservedCatalog, ...
                                                                                 vModifiedCatalogs, nNumberSimulation);
% function [rRelmTest, mRandom] = relm_LEvaluationTest(vForecast, cObservedCatalog, 
%                                                                                   vModifiedCatalogs, nNumberSimulation);
% --------------------------------------------------------------------------------------------------------------
% Computation of the L-test for the RELM framework
%
% Input parameters:
%   vForecast                       Forecast model
%   cObservedCatalog          Catalog with observered events
%   vModifiedCatalogs          Catalogs with applied uncertainties
%   nNumberSimulation         Number of random simulations
%
% Output paramters:
%   rRelmTest.fGamma                  Gamma-value of the cumulative density
%   rRelmTest.vSimulation              Vector containing the simulated numbers of events
%   rRelmTest.nSimulationCount      Number of random simulations
%   rRelmTest.fLogLikelihood          Log-likelihood
%   rRelmTest.nModificationCount   Number of catalog modifications
%   rRelmTest.vModification           Vector containing the numbers of events for modified
%                                                 catalogs.
%   mRandom                               Random numbers used by the simulations
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


global UseRandomFile;
global TestRandomFile;
global Forecast_Rate;


% Matrix of random numbers
mRandom = [];


if ~UseRandomFile
   % Randomize
   rand('state',sum(100*clock));
else
   mRandom = loadRandomFile(TestRandomFile);
end;


% Compute the "true" result
% Log-likelihood of the forecast given the observation
fLogLikelihood = relm_LogLikelihoodCatalog(vForecast, cObservedCatalog);


% Number of modified catalogs
nNumberModification = length(vModifiedCatalogs);

% Compute the "results" of the modifications
vLogLikelihoodsModifications = zeros(nNumberModification, 1);
for nCnt = 1:nNumberModification
   cCatalog = vModifiedCatalogs{nCnt};
   vLogLikelihoodsModifications(nCnt)  = relm_LogLikelihoodCatalog(vForecast, cCatalog) - fLogLikelihood;
end;


% Compute the "results" of the simulations
vLogLikelihoodsSimulations = zeros(nNumberSimulation, 1);
nRandomNum = length(vForecast(:, Forecast_Rate));

for nCnt = 1:nNumberSimulation

    if ~UseRandomFile
       % Create the random numbers for the simulation
       vRandom = rand(nRandomNum, 1);
       % Remember random numbers
       mRandom = [mRandom, vRandom];
    else
       vRandom = mRandom(:, nCnt);
    end; 

    % Compute the simulated number of events and sum them up
    vRealization = poissinv(vRandom, vForecast(:, Forecast_Rate));
    vLogLikelihoodsSimulations(nCnt)  = relm_LogLikelihood(vForecast(:, Forecast_Rate), vRealization) - ...
                                                        fLogLikelihood;
  end;


% Compute Gamma and store the important parameters
rRelmTest.vSimulation = vLogLikelihoodsSimulations;
rRelmTest.fGamma = sum(vLogLikelihoodsSimulations > 0)/nNumberSimulation;
rRelmTest.nSimulationCount = nNumberSimulation;
% normalized "true" result
rRelmTest.fLogLikelihood = 0; 
rRelmTest.nModificationCount = nNumberModification;
rRelmTest.vModification = vLogLikelihoodsModifications;

