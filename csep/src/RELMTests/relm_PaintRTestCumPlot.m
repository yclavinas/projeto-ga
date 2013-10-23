function relm_PaintRTestCumPlot(rRelmTest, sXLabelDescription, hAxes);
% function relm_PaintRTestCumPlot(rRelmTest, sXLabelDescription, hAxes)
% -----------------------------------------------------
% Creates the result plots of one of the RELM R-tests
%
% Input parameters:
%   rRelmTest		Record of results from one of the RELM tests
%   sXLabelDescription		Description for the Label of X-axis (optional)
%   hAxes		Handle of existing axes. If not specified, a figure is created
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

sXLabel = 'Log-likelihood Ratio';
if exist('sXLabelDescription') && (length(sXLabelDescription) ~= 0)
   sXLabel = sprintf('%s (%s)', sXLabel, sXLabelDescription);
end;

 
if ~exist('hAxes')
  figure('Name', 'Result plot', 'NumberTitle', 'off');
  hAxes = newplot;
end;

% Activate the given or newly created axes
axes(hAxes);

% Plot the CDF and the line of observed data
vIndex = [1:rRelmTest.nSimulationCount]/rRelmTest.nSimulationCount;
vObservedX = [rRelmTest.fLogLikelihoodRatio, rRelmTest.fLogLikelihoodRatio];
vObservedY = [0,1];
plot(sort(rRelmTest.vSimulation1), vIndex, 'g', sort(rRelmTest.vSimulation2), vIndex, 'r', vObservedX, vObservedY, 'k', 'linewidth', 1);

% Add the patches
set(hAxes, 'NextPlot', 'add');
vPatch1Y = [1 1 0.975 0.975];
vPatch2Y = [0.025 0.025 0 0];
vXLim = xlim;
vPatch1X = [vXLim(1) rRelmTest.fLogLikelihoodRatio rRelmTest.fLogLikelihoodRatio vXLim(1)];
vPatch2X = [rRelmTest.fLogLikelihoodRatio vXLim(2) vXLim(2) rRelmTest.fLogLikelihoodRatio];
patch(vPatch1X, vPatch1Y, [0.8 0.8 0.8], 'facealpha', 0.7);
patch(vPatch2X, vPatch2Y, [0.8 0.8 0.8], 'facealpha', 0.7);

% Add information
title(['\alpha = ' num2str(rRelmTest.fAlpha) ', \beta = ' num2str(rRelmTest.fBeta)]);
ylabel('Fraction of cases');
xlabel(sXLabel);



