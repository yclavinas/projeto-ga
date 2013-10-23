% Convert log-likelihood test result structure to XML format and write it to the file.
%
% Input parameters:
% rTest - RELM test output structure
% sFilename - Name for the xml file
% sTrueVarName - Variable name for true test result
% fTrueVarValue - Value for true test result
% sModelName - Name of the model for the test
%
% Output parameters:
% None.
%
function writeXMLLTestResults(rTest, sFilename, sTrueVarName, fTrueVarValue, sModelName);

%%% Create XML document
document = com.mathworks.xml.XMLUtils.createDocument('CSEPResult');

%%% Get root element of the document
root_node = document.getDocumentElement();
root_node.setAttribute('xmlns', 'http://www.scec.org/xml-ns/csep/0.1');


%%% Create resultData element
result_node = document.createElement('resultData');
result_node.setAttribute('publicID', 'smi://org.scec/csep/results/1');
root_node.appendChild(result_node);


%%% Create test element
% Regex to extract test name from a given string that 
% includes test and model names: is it underscore separated
sTestNameCell = regexp(rTest.sName, '^([^_]+)', 'match');

% Remove '-' from the test name that is in conflict with code generator
sTestNameCell = regexprep(sTestNameCell, '-', '');
test_name = sTestNameCell{1};

test_node = document.createElement(test_name);
test_node.setAttribute('publicID', sprintf('smi://org.scec/csep/tests/%s/1', ...
                                 lower(test_name)));
result_node.appendChild(test_node);                                 
                                 
                                 
%%% Create creationInfo element
creation_node = document.createElement('creationInfo');
                           
% Set creation time
creation_node.setAttribute('creationTime', datestr(now, 'yyyy-mm-ddTHH:MM:SS'));                                 
test_node.appendChild(creation_node);      


%%% Create simulationData element
simulation_node = document.createElement('simulationData');
simulation_node.setAttribute('publicID', 'smi://local/simulationdata/1');
test_node.appendChild(simulation_node);

%%% Create count element for simulationData
count_node = document.createElement('simulationCount');
count_node. appendChild(document.createTextNode(num2str(rTest.nSimulationCount)));
simulation_node.appendChild(count_node);

%%% Create simulation values element
values_node = document.createElement('simulation');
values_string = sprintf(' %d', rTest.vSimulation(:));
values_node.appendChild(document.createTextNode(values_string));
simulation_node.appendChild(values_node);
	
	
if isfield(rTest, 'vModification')
	% Convert catalog uncertainties to the XML format	
	%%% Create modificationData (catalog variations) element
	modification_node = document.createElement('modificationData');
	modification_node.setAttribute('publicID', 'smi://local/modificationdata/1');
	test_node.appendChild(modification_node);
	
	%%% Create count element for modificationData
	count_node = document.createElement('modificationCount');
	count_node. appendChild(document.createTextNode(num2str(rTest.nModificationCount)));
	modification_node.appendChild(count_node);
	
	%%% Create modifications values element
	values_node = document.createElement('modification');
	values_string = sprintf(' %d', rTest.vModification(:));
	values_node.appendChild(document.createTextNode(values_string));
	modification_node.appendChild(values_node);
end;


%%% Create log-likelihood element
loglikelihood_node = document.createElement('logLikelihood');
loglikelihood_node.appendChild(document.createTextNode(num2str(rTest.fLogLikelihood)));
test_node.appendChild(loglikelihood_node);

%%% Create gamma element
true_var_node = document.createElement(sTrueVarName);
if isscalar(fTrueVarValue)
   true_var_node.appendChild(document.createTextNode(num2str(fTrueVarValue)));
else
   values_string = sprintf(' %d', fTrueVarValue(:));
   true_var_node.appendChild(document.createTextNode(values_string));
end;
test_node.appendChild(true_var_node);


%%% Create test dates element if any
if isfield(rTest, 'sTestDates')
   dates_node = document.createElement('testDate');
   dates_cells = cellstr(rTest.sTestDates);
   values_string = sprintf(' %s', dates_cells{:});
   dates_node.appendChild(document.createTextNode(values_string));   
   
   test_node.appendChild(dates_node);
end;



%%% Create name element
name_node = document.createElement('name');
name_node.appendChild(document.createTextNode(sModelName));
test_node.appendChild(name_node);


%%% Create description element
description_node = document.createElement('description');
description_node.appendChild(document.createTextNode(...
                                sprintf('This is %s for %s model.', ...
                                        test_name, sModelName)));
test_node.appendChild(description_node);


% write XML format file
xmlwrite(sFilename, document)
