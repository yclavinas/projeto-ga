% Generate normally distributed random errors.
%
% Input parameters:
% vErrorValue - Vector of errors to randomize.
% vRandom - Vector of random numbers.
% 
% Output parameters:
% vErrorValue - Normally distributed random value.
%
function[vErrorValue] = normalRandom(vErrorValue, vRandom);


% MU is zero
MU = zeros(size(vRandom));

% Sigma is equal to vErrorValue
vErrorValue = norminv(vRandom, MU, vErrorValue);