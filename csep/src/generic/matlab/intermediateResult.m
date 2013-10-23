function intermediateResult(sResultFile, sIntermediateFile, sDate);
% function intermediateResult(sResultFile, sIntermediateFile);
% --------------------------------------------------------------------------------------------------------------
% Computation of the intermediate result for the RELM framework
%
% Input parameters:
%   sResultFile               RELM evaluation test result file
%   sIntermediateFile           RELM evaluation intermediate test result file
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


% Flag if intermediate file was just created
bCreated = false;

% Load result file and identify if it's N, L or R test result
rLoad = load(sResultFile);
   
if isfield(rLoad, 'rTest')
   rResult = rLoad.rTest;
   
   if ~exist(sIntermediateFile, 'file')
      % Create a copy of result file to be first intermediate result
      rTest = rResult;
      
      % Update with date information
      rTest.sTestDates = sDate;
      save(sIntermediateFile, 'rTest');
      
      bCreated = true;
   end;   
      
   
   % Load cumulative test results
   rLoad = load(sIntermediateFile);
   
   if isfield(rLoad, 'rTest')
      rIntermediate = rLoad.rTest;
      
      test_id = rResult.sName(1);
   
      % Update file if it already existed
      if bCreated == false
          % Identify type of evaluation test
		  switch lower(test_id)
		     case 'n'
			   
			    % N-test - record new delta
			    rIntermediate.fDelta = [rIntermediate.fDelta; ...
			                            rResult.fDelta];
		     
		     	rIntermediate.fEventCount = [rIntermediate.fEventCount; ...
		     	                             rResult.fEventCount];
			 case 'l'
		  
			    % L-test - record new gamma
			    rIntermediate.fGamma = [rIntermediate.fGamma;
				                        rResult.fGamma];
		     
		     case 'r'
		  
			    % R-test - record new alpha and gamma
			    rIntermediate.fAlpha = [rIntermediate.fAlpha;
			                            rResult.fAlpha];
			    rIntermediate.fBeta = [rIntermediate.fBeta;
			                           rResult.fBeta];
		     
		     otherwise
				disp(['Unexpected test type specified by the ', sResultFile, ...
				      ' result file. Expected N, L, or R as a first letter of ', ...
				      rResult.sName, ' - rTest.sName field. Exiting the test.']);
	      end; % end of switch
	      
	      % Update dates
	      rIntermediate.sTestDates = [rIntermediate.sTestDates; sDate];	      
	      
	  end; % end of (if bCreated) 
      
      % Append 'intermediate' to the name of result structure
      intermediate_pattern = '(intermediate results)';
      if isempty(strfind(rIntermediate.sName, intermediate_pattern))
         rIntermediate.sName = sprintf('%s %s', rIntermediate.sName, intermediate_pattern);
      end;
       
      
      % Overwrite intermediate results file
      rTest = rIntermediate;
      save(sIntermediateFile, 'rTest');   
      
      % Save intermediate results in XML format - replace file extension
      file_extension_pattern = '.mat$';
	  xml_filename = regexprep(sIntermediateFile, file_extension_pattern, '');
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
	  disp(['Unexpected variable is specified by the ', sIntermediateFile, ...
		    ' intermediate result file. Expected rTest. Exiting the test.']);
	  pause;      
   end;
   
else
   disp(['Unexpected variable is specified by the ', sResultFile, ...
	     ' result file. Expected rTest. Exiting the test.']);
   pause;      
end;

