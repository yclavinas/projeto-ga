function [vLogLikelihoodRatio] = relm_LogLikelihoodRatio(vForecast1, vForecast2, vObservation);
% --------------------------------------------------------------------------------------------------------------
% Computation of the log-likelihood ratio of events in the catalog.
%
% Input parameters:
%
%   vForecast1        First forecast model
%   vForecast2        Second forecast model
%   vObservation    Catalog of events
%
% Output paramters:
%   vLogLikelihoodRatio    Likelihood ratio
%
% Copyright (C) 2007 by Danijel Schorlemmer
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


vLogLikelihoodRatio = relm_LogLikelihood(vForecast1, vObservation) - ...
                                  relm_LogLikelihood(vForecast2, vObservation);
