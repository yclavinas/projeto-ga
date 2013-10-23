function [nNum] = relm_NumberEventsCatalog(vForecast, mCatalog);
% --------------------------------------------------------------------------------------------------------------
% Computation of the number of events in the catalog.
%
% Input parameters:
%   mCatalog         Catalog of events
%
% Output paramters:
%   nNum              Number of events
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


% Column into the binned catalog containing number of observed events per bin
NUM_EVENTS_COLUMN = 11;


% Combine observations with forecast
[vBinnedCatalog] = testing_AddObservations(vForecast, mCatalog);

% Get the number of events
[nNum] = relm_NumberEvents(vBinnedCatalog(:, NUM_EVENTS_COLUMN));
