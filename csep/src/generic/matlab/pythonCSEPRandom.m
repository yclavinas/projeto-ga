function [mRandom] = pythonCSEPRandom(nRows, nCols);
% function [mRandom] = pythonCSEPRandom(nRows, nCols);
% --------------------------------------------------------------------------------------------------------------
% Generate a matrix of random numbers with given dimentions.
%
% Input parameters:
%   nRows    Number of rows.
%   nCols    Number of columns. 
%
% Output parameters:
%   mRandom  Matrix with random numbers
%   fSeed    Seed used by random numbers generator

global UseRandomFile;
global TestRandomFile;
global TestRandomNumbersFilePostfix;


% Matrix of random numbers used by simulations
mRandom = [];

s_python_executable = sprintf('python %s/src/generic/cseprandom.py', getenv('CENTERCODE'));

num_random = nRows * nCols;

% Read random seed from the file
s_read_from_file_option = '-r true';

if ~UseRandomFile
	% Don't use '-r' option to read seed from file - force new seed generation
	s_read_from_file_option = ' ';
end;

s_random_numbers_file = sprintf('%s%s', TestRandomFile, TestRandomNumbersFilePostfix);
command = sprintf('%s %s -f %s -n %d -o %s', ...
                  s_python_executable, s_read_from_file_option, ...
                  TestRandomFile, num_random, s_random_numbers_file);

% Profiling
%start_time = now;
[return_code, return_str] = unix(command);
%delta_time = now - start_time


if return_code
   disp(['pythonCSEPRandom Error: ', return_str]);
end;
                  
% Open random numbers file and read them into a matrix
fid = fopen(s_random_numbers_file);
mRandom = fscanf(fid, '%g', [nRows, nCols]);
fclose(fid);

% Get rid of random numbers file since it can be reproduced given the same seed
delete(s_random_numbers_file);

% When reading matrix from result string returned by the process
%mRandom = sscanf(return_str, '%g', [nRows, nCols]);

