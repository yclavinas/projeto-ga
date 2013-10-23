% Format filename for the random seed file used by one of the RELM evaluation 
% simulations.
%
% Input parameters:
% nSimulation - Simulation index 
% nIteration - Iteration index for simulation
% sTestFilename - Base filename for the evaluation test
%
% Output parameters:
% sFilename - Formatted filename for the simulation random seed.
%
function [sFilename] = seedSeedFilename(nSimulation, nIteration, sTestFilename);


global TestRandomFilePostfix;
global TestRandomFile;


s_postfix = sprintf('-simulation%d_%d%s', nSimulation, nIteration, ...
                    TestRandomFilePostfix);

% Format filename
sFilename = regexprep(sTestFilename, ...
                      TestRandomFilePostfix, s_postfix);
