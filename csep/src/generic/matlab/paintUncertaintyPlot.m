function paintNewTestUncertaintyPlot(rRelmTest, sXLabel);
%
% Creates plots of events and CDF based on test catalogs for the N-test.
%
% This function creates plots of observed events in one of the RELM N-tests and
% of distribution based on uncertainties of the catalog containing these events.
%
% Input parameters:
% rRelmTest	      Record of results from RELM N-test
%


% Identify "true" result
nTrueResult = nan;

if isfield(rRelmTest, 'fEventCount') 
   nTrueResult = rRelmTest.fEventCount;
elseif isfield(rRelmTest, 'fLogLikelihood')
   nTrueResult = rRelmTest.fLogLikelihood;
elseif isfield(rRelmTest, 'fLogLikelihoodRatio')
   nTrueResult = rRelmTest.fLogLikelihoodRatio;   
end;


% Check if modifications information exists in the test results
if isfield(rRelmTest, 'vModification')
	   
	figure('Name', 'Catalog Modifications', 'NumberTitle', 'off');
	hAxes = newplot;
	
	% Activate newly created axes
	axes(hAxes);
	
	% Plot the CDF and the lines of observed data
	vIndex = [1:rRelmTest.nModificationCount]/rRelmTest.nModificationCount;
	
	vObservedX = [nTrueResult, nTrueResult];
	vObservedY = [0,1];
	plot(sort(rRelmTest.vModification), vIndex, 'b', ...
	      vObservedX, vObservedY, 'r', 'linewidth', 1);
	
	
	% Add information
	ylabel('Fraction of cases');
	xlabel(sXLabel);
	
end;