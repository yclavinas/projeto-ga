function [fLogLikelihood] = relm_LogLikelihoodOptimized(vForecast, vObservation, vPrecomputedZeroLikelihood);
% --------------------------------------------------------------------------------------------------------------
% Computation of the log-likelihood of events in the catalog.
%
% Input parameters:
%
%   vForecast         Forecast model
%   vObservation    Catalog of events
%   vPrecomputedZeroLikelihood     Precomputed likelihood values for the case of zeros events in the bins
%
% Output paramters:
%   fLogLikelihood    Likelihood
%
% Copyright (C) 2008 by Danijel Schorlemmer
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


vLikelihood = zeros(length(vForecast(:,1)),1);

% Select bins with zero events observed
vSel = (vObservation == 0);
% Copy the precomputed values into the likelihood vector
vLogLikelihood(vSel) = vPrecomputedZeroLikelihood(vSel);

% Select bins with one or more events observed and compute the likelihoods for these bins
vLogLikelihood(~vSel) = calc_logpoisspdf(vObservation(~vSel), vForecast(~vSel));

% Sum over the likelihood column
fLogLikelihood = sum(vLogLikelihood);
