% Combine distribution info and write it to the file.
%
% Input parameters:
% rTest - RELM test output structure
% sDir - Directory for the output data files
% sTestName - Name of the test: consists of the test name and participating models
% sModelName1 - Name of 1st model for the test
% sModelName2 - Name of the 2nd model for the test (if applicable)
%
% Output parameters:
% None.
%
function writeTestData(rTest, sDir, sTestName, sModelName1, sModelName2);

global TestRandomFile;
global ENABLE_DEBUG;


% Set flag if cumulative plots of distribution based on uncertainty should be displayed
bDisplayModifications = false;
if isfield(rTest, 'vModification')
	bDisplayModifications = true;
end;	


% Capture name of the test
rTest.sName=sTestName;


% save result to the file in Matlab format
file_name = sprintf('%s/rTest_%s.mat', sDir, sTestName);
save(file_name, 'rTest');   

% save result to the file in ASCII format
if ENABLE_DEBUG
	file_name = sprintf('%s/rTest_%s.dat', sDir, sTestName);
	save(file_name, '-struct', 'rTest', '-ascii', '-double', '-tabs');   
end;

% save result to the file in XML format
test_id = sTestName(1);
file_name = sprintf('%s/rTest_%s.xml', sDir, sTestName);

% The same function for conversion to XML is used for L, S, and M tests:
% define the name of true test result, and value for it 
true_var_value = 0;
true_var_name = '';

switch lower(test_id)
   case 'l'
      true_var_name = 'gamma';
      true_var_value = rTest.fGamma;
   case 's'
      true_var_name = 'zeta';
      true_var_value = rTest.fZeta;
   case 'm'
      true_var_name = 'kappa';
      true_var_value = rTest.fKappa;
   otherwise
end;
      
       
% Invoke conversion function specific to the evaluation test results
switch lower(test_id)
   case 'n'
      writeXMLNTestResults(rTest, file_name, sModelName1);  
      if bDisplayModifications == true
         paintUncertaintyPlot(rTest, 'Number of Earthquakes');
      end;
   case {'l', 's', 'm'}
      writeXMLLTestResults(rTest, file_name, true_var_name, true_var_value, sModelName1);     
      if bDisplayModifications == true      
         paintUncertaintyPlot(rTest, 'Log-likelihood');
      end;
   case 'r'
      writeXMLRTestResults(rTest, file_name, sModelName1, sModelName2);     
      if bDisplayModifications == true   
         paintUncertaintyPlot(rTest, 'Log-likelihood Ratio');
      end;
   otherwise
      disp(['Unknown test type for XML presentation: ', sTestName, ...
              '. Skipping XML file generation...']);
end;  

