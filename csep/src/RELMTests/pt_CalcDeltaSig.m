function [fSigmaDistance, fMu, fSigma] = pt_CalcDeltaSig(mValues, fTestValue);
% function [fSignificanceLevel, fMu, fSigma] = pt_CalcDeltaSig(mValues, fTestValue)
% ---------------------------------------------------------------------------------
% Calculates the Delta_sigma measure of significance of fTestValue  
%
% Input parameters:
%   mValues               Value distribution (assumed to be a normal distribution)
%   fTestValue            Value to be tested
%
% Output parameter:
%   fSigmaDistance        Delat_sigma measure
%   fMu                   Mu of distribution
%   fSigma                Sigma of distribution
%
% Copyright (C) 2003-2006 by Danijel Schorlemmer
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

global bDebug;
if bDebug
  disp('This is /src/danijel/probfore/pt_CalcDeltaSig.m');
end  

% Select all non-nan values of the distribution
vSelection = ~isnan(mValues);
mNoNanValues = mValues(vSelection);

% Compute the mean and standard deviation of the non-parameterized distribution 
fMu = mean(mNoNanValues);
fSigma = calc_StdDev(mNoNanValues);

% Return the Delta_sigma measure of the testvalue (+: test hypothesis wins)
fSigmaDistance = (fMu - fTestValue)/fSigma;