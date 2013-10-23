% Compute fProbability value for the RELM evaluation test based on simulations.
%
% Input parameters:
% vSimulation - Vector of simulation values
% nEventCount - True event count
% nNumberSimulation - Number of simulations used for the test
%
% Output parameters:
% fDelta - Computed delta value.
%
function [fProbability] = probability(vSimulation, nEventCount, nNumberSimulation);

fProbability = sum(vSimulation <= nEventCount)/nNumberSimulation;