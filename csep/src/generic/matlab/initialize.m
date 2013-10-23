% Initialize global variables
%
% Input parameters:
% bUseRandomFiles - Flag if random values should be read from the files.
% nDeclusterNum - Number of simulations for declustering algorithm
%
function initialize(bUseRandomFiles, nDeclusterNum)

global NumDeclusterSimulations;

% ZMAP-format identifiers
ZMAPFormat;

% Forecast format identifiers
ForecastFormat;

% Simulations initializations
initializeRandom(bUseRandomFiles, nDeclusterNum);
