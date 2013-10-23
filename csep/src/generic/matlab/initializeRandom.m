% Initialize global variables associated with random numbers
%
% Input parameters:
% bUseFiles - Flag if random values should be read from the 
%                   files instead of being drawn by the system.
% nDeclusterNum - Number of simulations for declustering algorithm
%
function initializeRandom(bUseFiles, nDeclusterNum)

global NumDeclusterSimulations;

global UseRandomFile;
global UncertaintiesRandomFile;
global TestRandomFile;
global TestRandomFilePostfix;
global TestRandomNumbersFilePostfix;


NumDeclusterSimulations = nDeclusterNum;

% Flag to indicate if random numbers should be read from the file
UseRandomFile = bUseFiles;

% Filename base to store random numbers for catalog uncertainties.
UncertaintiesRandomFile = 'uncertainty';

% Variables used to construct a filename to store random numbers used by evaluation tests.
TestRandomFile = '';
TestRandomFilePostfix = '-randomSeed.txt';
TestRandomNumbersFilePostfix = '.randomNumbers';