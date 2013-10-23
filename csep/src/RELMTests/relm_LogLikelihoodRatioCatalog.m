function [vLikelihoodRatio] = relm_LogLikelihoodRatioCatalog(vForecast1, vForecast2, mCatalog);
% --------------------------------------------------------------------------------------------------------------
% Computation of the log-likelihood ratio for two forecast models.
%
% Input parameters:
%   vForecast1       First forecast model
%   vForecast2       Second forecast model
%   mCatalog         Catalog of events
%
% Output paramters:
%   vLikelihoodRatio       Likelihood ratio
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


global Forecast_Rate;

% Column into the binned catalog containing number of observed events per bin
NUM_EVENTS_COLUMN = 11;


% Combine observations with first forecast model
[vBinnedCatalog] = testing_AddObservations(vForecast1, mCatalog);

[vLikelihoodRatio] = relm_LogLikelihoodRatio(vForecast1(:, Forecast_Rate), ...
                                                                  vForecast2(:, Forecast_Rate), ...
                                                                  vBinnedCatalog(:, NUM_EVENTS_COLUMN));
                                           