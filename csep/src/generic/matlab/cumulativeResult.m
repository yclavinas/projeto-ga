function cumulativeResult(sResultFile, sCumulativeFile, sDate);
% function cumulativeResult(sResultFile, sCumulativeFile);
% --------------------------------------------------------------------------------------------------------------
% Computation of the cumulative result for the RELM framework
%
% Input parameters:
%   sResultFile               RELM evaluation test result file
%   sCumulativeFile           RELM evaluation cumulative test result file
%   sDate                     Date for the test results
%
% Output parameters: None
%
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


% Flag if cumulative file was just created
bCreated = false;

% Load result file and identify if it's N, L or R test result
rLoad = load(sResultFile);
   
if isfield(rLoad, 'rTest')
   rResult = rLoad.rTest;
   
   if ~exist(sCumulativeFile, 'file')
      % Create a copy of result file to be first cumulative result
      rTest = rResult;
      
      % Update with date information
      rTest.sTestDates = sDate;
      save(sCumulativeFile, 'rTest');
      
      bCreated = true;
   end;   
      
   
   % Load cumulative test results
   rLoad = load(sCumulativeFile);
   
   if isfield(rLoad, 'rTest')
      rCumulative = rLoad.rTest;
      
      test_id = rResult.sName(1);
   
      % Update file if it already existed
      if bCreated == false
          % Identify type of evaluation test
		  switch lower(test_id)
		     case 'n'
			   
			    % N-test - sum up simulation values, compute new delta
			    rCumulative.vSimulation = rCumulative.vSimulation + ...
			                              rResult.vSimulation;
			                              
			    % Sum up total number of observed events
			    rCumulative.fEventCount = rCumulative.fEventCount + ...
			                              rResult.fEventCount;
			                                      
			    % Append new delta based on cumulative result
			    rCumulative.fDelta = [rCumulative.fDelta; ...
			                          probability(rCumulative.vSimulation, ...
			                                      rCumulative.fEventCount, ...
			                                      rCumulative.nSimulationCount)];
		     
			 case 'l'
		  
			    % L-test - sum up simulation values, compute new gamma
			    rCumulative.vSimulation = rCumulative.vSimulation + ...
			                              rResult.vSimulation;
			    % Append new gamma based on cumulative result	                               
			    rCumulative.fGamma = [rCumulative.fGamma;
			                          probability(rCumulative.vSimulation, ...
			                                      rCumulative.fLogLikelihood, ...
			                                      rCumulative.nSimulationCount)];
		     
		     case 'r'
		  
			    % R-test - sum up simulation values, compute new alpha and gamma
			    rCumulative.vSimulation1 = rCumulative.vSimulation1 + ...
		  	                               rResult.vSimulation1;
			    rCumulative.vSimulation2 = rCumulative.vSimulation2 + ...
		  	                               rResult.vSimulation2;
		
			    % Append new alpha and beta based on cumulative result	                                 	                                
			    rCumulative.fAlpha = [rCumulative.fAlpha;
			                          probability(rCumulative.vSimulation2, ...
			                                      rCumulative.fLogLikelihoodRatio, ...
			                                      rCumulative.nSimulationCount)];
			    rCumulative.fBeta = [rCumulative.fBeta;
			                         probability(rCumulative.vSimulation1, ...
			                                     rCumulative.fLogLikelihoodRatio, ...
			                                     rCumulative.nSimulationCount)];
		     
		     otherwise
				disp(['Unexpected test type specified by the ', sResultFile, ...
				      ' result file. Expected N, L, or R as a first letter of ', ...
				      rResult.sName, ' - rTest.sName field. Exiting the test.']);
	      end; % end of switch
	      
	      % Update dates
	      rCumulative.sTestDates = [rCumulative.sTestDates; sDate];	      
	      
	  end; % end of (if bCreated) 
      
      % Append 'cumulative' to the name of result structure
      cumulative_pattern = '(cumulative results)';
      if isempty(strfind(rCumulative.sName, cumulative_pattern))
         rCumulative.sName = sprintf('%s %s', rCumulative.sName, cumulative_pattern);
      end;
       
      
      % Overwrite cumulative results file
      rTest = rCumulative;
      save(sCumulativeFile, 'rTest');   
      
      % Save cumulative results in XML format - replace file extension
      file_extension_pattern = '.mat$';
	  xml_filename = regexprep(sCumulativeFile, file_extension_pattern, '');
	  xml_filename = sprintf('%s.xml', xml_filename);
      
   	  % Invoke conversion function specific to the evaluation test results
	  switch lower(test_id)
	     case 'n'
	        writeXMLNTestResults(rTest, xml_filename);  
	     case 'l'
	        writeXMLLTestResults(rTest, xml_filename);     
	     case 'r'
	        writeXMLRTestResults(rTest, xml_filename);     
      end; % end of switch
   
   else
	  disp(['Unexpected variable is specified by the ', sCumulativeFile, ...
		    ' cumulative result file. Expected rTest. Exiting the test.']);
	  pause;      
   end;
   
else
   disp(['Unexpected variable is specified by the ', sResultFile, ...
	     ' result file. Expected rTest. Exiting the test.']);
   pause;      
end;

