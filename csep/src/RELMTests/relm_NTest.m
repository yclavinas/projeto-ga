function [rRelmTest] = relm_NTest(vForecast, cObservedCatalog, vModifiedCatalogs, ...
                                  nNumberSimulation);
% function [rRelmTest] = relm_NTest(vForecast, cObservedCatalog, vModifiedCatalogs, ...
%                                   nNumberSimulation);
% --------------------------------------------------------------------------------------------------------------
% Computation of the N-test for the RELM framework
%
% Input parameters:
%   vForecast                 Forecast model
%   cObservedCatalog          Catalog with observered events
%   vModifiedCatalogs         Catalogs with applied uncertainties
%   nNumberSimulation         Number of random simulations
%
% Output paramters:
%   rRelmTest.fDelta              Delta-value of the cumulative density
%   rRelmTest.vSimulation         Vector containing the simulated numbers of events
%   rRelmTest.nSimulationCount    Number of random simulations
%   rRelmTest.fEventCount         Observed total number of events
%   rRelmTest.nModificationCount  Number of catalog modifications
%   rRelmTest.vModification       Vector containing the numbers of events for 
%                                 modified catalogs.
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


% Compute the "true" result
% Number of events in the catalog
nNumberQuakes = relm_NumberEventsCatalog(vForecast, cObservedCatalog);


% Number of catalogs with modifications
nNumberModification = length(vModifiedCatalogs);

% Compute the "results" of the modifications
vNumberQuakesModifications = zeros(nNumberModification, 1);
for nCnt = 1:nNumberModification
   cCatalog = vModifiedCatalogs{nCnt};
   vNumberQuakesModifications(nCnt)  = relm_NumberEventsCatalog(vForecast, ...
                                                                cCatalog);
end;


% Number of rows for random numbers for all simulations
[rows, cols] = size(vForecast);

% Remember original filename for the random seed file
s_test_file = TestRandomFile;

% Compute the "results" of the simulations
vNumberQuakesSimulations = zeros(nNumberSimulation, 1);

for nCnt = 1:nNumberSimulation

	 % Create filename for simulation random seed file
    TestRandomFile = simulationSeedFilename(nCnt, s_test_file);

    % Random numbers used by simulations
    vRandom = pythonCSEPRandom(rows, 1);

    % Compute the simulated number of events and sum them up
    vRealization = poissinv(vRandom, vForecast(:, Forecast_Rate));
    vNumberQuakesSimulations(nCnt)  = relm_NumberEvents(vRealization);
end;


% Compute Delta and store the important parameters
rRelmTest.vSimulation = vNumberQuakesSimulations;
rRelmTest.fDelta = probability(vNumberQuakesSimulations, nNumberQuakes, ...
                               nNumberSimulation);
rRelmTest.nSimulationCount = nNumberSimulation;
rRelmTest.fEventCount = nNumberQuakes;
rRelmTest.nModificationCount = nNumberModification;
rRelmTest.vModification = vNumberQuakesModifications;

