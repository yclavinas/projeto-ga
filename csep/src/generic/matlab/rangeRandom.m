% Generate random error within specific range.
%
% Input parameters:
% fMinRange - Lower limit of the range.
% fMaxRange - Upper limit of the range.
% vErrorValue - Vector of errors to randomize (used to determine dimentions of 
%               the result vector, or contains the random numbers already).
% 
% Output parameters:
% vErrorValue - Vector of random values within specified range.
%
function[vErrorValue] = rangeRandom(fMinRange, fMaxRange, vErrorValue);

vRandom = vErrorValue;

% Generate vector of random values for each error     
vErrorValue = fMinRange + (fMaxRange - fMinRange)*vRandom;                      
