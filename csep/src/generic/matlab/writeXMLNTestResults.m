% Convert N-test result structure to XML format and write it to the file.
%
% Input parameters:
% rTest - RELM test output structure
% sFilename - Name for the xml file
% sModelName - Name of the model for the test
%
% Output parameters:
% None.
%
function writeXMLNTestResults(rTest, sFilename, sModelName);

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


%%% Create cdfData element
cdf_node = document.createElement('cdfData');
cdf_node.setAttribute('publicID', 'smi://local/cdfdata/1');
test_node.appendChild(cdf_node);


%%% Create count element for cdfData
count_node = document.createElement('cdfCount');
count_node. appendChild(document.createTextNode(num2str(rTest.nCDFCount)));
cdf_node.appendChild(count_node);


%%% Create cdf values and ticks elements
values_node = document.createElement('cdfValues');
values_string = sprintf(' %d', rTest.vCDFValues(:));
values_node.appendChild(document.createTextNode(values_string));
cdf_node.appendChild(values_node);
	
ticks_node = document.createElement('cdfEventCount');
values_string = sprintf(' %d', rTest.vCDFEventCount(:));
ticks_node.appendChild(document.createTextNode(values_string));
cdf_node.appendChild(ticks_node);

	
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


%%% Create true event count element
event_count_node = document.createElement('eventCount');
if isscalar(rTest.fEventCount)
   event_count_node.appendChild(document.createTextNode(num2str(rTest.fEventCount)));
else
   values_string = sprintf(' %d', rTest.fEventCount(:));
   event_count_node.appendChild(document.createTextNode(values_string));
end;
test_node.appendChild(event_count_node);


%%% Create forecast event count element
event_count_node = document.createElement('eventCountForecast');
if isscalar(rTest.fEventCountForecast)
   event_count_node.appendChild(document.createTextNode(num2str(rTest.fEventCountForecast)));
else
   values_string = sprintf(' %d', rTest.fEventCountForecast(:));
   event_count_node.appendChild(document.createTextNode(values_string));
end;
test_node.appendChild(event_count_node);


%%% Create delta elements
delta_node = document.createElement('delta1');
if isscalar(rTest.fDelta1)
   delta_node.appendChild(document.createTextNode(num2str(rTest.fDelta1)));
else
   values_string = sprintf(' %d', rTest.fDelta1(:));
   delta_node.appendChild(document.createTextNode(values_string));
end;
test_node.appendChild(delta_node);

delta_node = document.createElement('delta2');
if isscalar(rTest.fDelta2)
   delta_node.appendChild(document.createTextNode(num2str(rTest.fDelta2)));
else
   values_string = sprintf(' %d', rTest.fDelta2(:));
   delta_node.appendChild(document.createTextNode(values_string));
end;
test_node.appendChild(delta_node);


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
