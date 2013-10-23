function [rRelmTest] = relm_NTestNoRandom(vForecast, cObservedCatalog, vModifiedCatalogs);
% function [rRelmTest] = relm_NTestNoRandom(vForecast, cObservedCatalog, vModifiedCatalogs);
% --------------------------------------------------------------------------------------------------------------
% Computation of the N-test for the RELM framework.  Here, we have observed
% w events and the specified forecast has predicted l events.  We want to
% know if the observation is consistent with the prediction, assuming that
% the distribution of the number of events forecast is Poissonian.  To quantify this
% consistency, we assume that the forecast is true and compute the
% probability that we would observe fewer than w events (or at least w events).  This is the
% probability of observing 0, 1,..., or w-1 events, or w, w+1, ..., Inf events.
% in other words we're going to use the cdf.  We call these probabilities
% delta, and delta1 = poisscdf(w-eps, l), delta2 = poisscdf(w+eps, l), where eps
% is some small positive number << 1.  For plotting purposes, we also want to return
% the cdf, and the number of events in each modified catalog.  To show the
% complete cdf, we would need to compute it at 0, 1,..., Inf.  Rather than
% doing this, we find the point at which the cdf is very close to unity,
% and only return the cdf out to this point.  This point is given as x =
% poissinv(0.9999, l), so we return a vector with (x + 1) elements
% containing the cdf value at 0, 1,..., x.
% 
%
% Input parameters:
%   vForecast                 Forecast model
%   cObservedCatalog          Catalog with observered events
%   vModifiedCatalogs         Catalogs with applied uncertainties
%   nNumberSimulation         Number of random simulations
%
% Output paramters:
%   rRelmTest.fEventCount         Number of observed events
%   rRelmTest.nModificationCount  Number of catalog modifications
%   rRelmTest.vModification       Vector containing the numbers of events
%                                 in each modified catalog.
%   rRelmTest.fDelta              Value of the cumulative density function
%                                 at (fEventCount - epsilon) and
%                                 (fEventCount + epsilon)
%   rRelmTest.nSimulationCount    Number of points to plot in CDF
%   rRelmTest.vSimulation         Vector of CDF values at -1, 0, 1,...,
%                                 (nCDFValuesCount - 1)
%
% Copyright (C) 2002-2007 by Danijel Schorlemmer
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
global TestRandomFile;
global USE_FORECAST_WEIGHTS;
global Forecast_MaskBit;

% Number of events in the observed catalog
nNumberQuakes = relm_NumberEventsCatalog(vForecast, cObservedCatalog);

% Number of modified catalogs
nNumberModification = length(vModifiedCatalogs);

% Compute the number of events in each modified catalog
vNumberQuakesModifications = zeros(nNumberModification, 1);
for nCnt = 1:nNumberModification
   cCatalog = vModifiedCatalogs{nCnt};
   vNumberQuakesModifications(nCnt)  = relm_NumberEventsCatalog(vForecast, ...
                                                                cCatalog);
end;

% Total number of events forecast
nNumberQuakesForecast = nansum(vForecast(:, Forecast_Rate));

if USE_FORECAST_WEIGHTS
   vSel = (vForecast(:, Forecast_MaskBit) == 1);
   nNumberQuakesForecast = nansum(vForecast(vSel, Forecast_Rate));
end;

% Compute the number of points we should include in the CDF
nNumberOfEventsAtWhichCDFIsNearUnity = poissinv(0.9999, nNumberQuakesForecast);

vPoissCDFQuakes = -1:nNumberOfEventsAtWhichCDFIsNearUnity;
vPoissCDF = poisscdf(vPoissCDFQuakes, nNumberQuakesForecast);

epsilon = 1e-6;
% Compute Delta and store the important parameters
rRelmTest.fEventCount = nNumberQuakes;
rRelmTest.nModificationCount = nNumberModification;
rRelmTest.vModification = vNumberQuakesModifications;
rRelmTest.fDelta1 = 1 - poisscdf(nNumberQuakes - epsilon, nNumberQuakesForecast);
rRelmTest.fDelta2 = poisscdf(nNumberQuakes + epsilon, nNumberQuakesForecast);
rRelmTest.nCDFCount = length(vPoissCDF);
rRelmTest.vCDFEventCount = vPoissCDFQuakes;
rRelmTest.vCDFValues = vPoissCDF;
rRelmTest.fEventCountForecast = nNumberQuakesForecast;

