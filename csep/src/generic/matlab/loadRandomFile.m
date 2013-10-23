% Load random numbers from the file.
%
% The function relies on the variable name 'mRandom' that is stored in the matlab formatted file.
%
% Input parameters:
% sRandomFile - Path to the file with random numbers.
%
% Output parameters:
% mRandom - Matrix with random numbers.
%
function[mRandom] = loadRandomFile(sRandomFile);

% Load random file (into mRandom variable)
rLoad = load(sRandomFile);

% Check if expected variable was loaded from the file
if isfield (rLoad, 'mRandom')
	disp(['mRandom was loaded from the file ', sRandomFile]);
	mRandom = rLoad.mRandom;
else
	disp(['Unexpected variable is specified by the ', sRandomFile, ...
	      ' file. Expected variable name is mRandom. Exiting the test.']);
	pause;
end;