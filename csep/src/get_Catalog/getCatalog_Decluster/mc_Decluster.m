function [mDeclusteredCatalog, mIndepProbCatalog] = mc_Decluster(mCatalog, nSimNum, sParamFilename)
% Wrapper function to do Monte Carlo simulations of the
% input parameters into the Reasenberg Declustering algorithm
%
% Output: 
% mDeclusteredCatalog - declustered catalog
% mIndepProbCatalog - original catalog with supplemental independence probability
%

%%% Global variables declarations
global TestRandomFile;
global UseRandomFile;
global ZMAP_COL_PROBABILITY;


% Decluster catalog with default parameters
dfTaumin = 1;
dfTaumax = 10;
dfP      = 0.95;
dfXk     = 0.5;
dfXmeff  = 1.5;
dfRfact  = 10;
dfErr    = 1.5;
dfDerr   = 2;

[mDeclusteredCatalog, vIsMainshock] = ReasenbergDeclus(dfTaumin, dfTaumax, ...
                                                       dfXk, dfXmeff, dfP, ...
                                                       dfRfact, dfErr, dfDerr, ...
                                                       mCatalog);

% Determine number of columns
[nRow, nCol] = size(mCatalog);
ZMAP_COL_PROBABILITY = nCol + 1;

% Define ranges for Reasenberg input variables (default values in comments)
raTaumin = [.5 2.5];   % dfTaumin = 1;
raTaumax = [3 15];     % dfTaumax = 10;
raP      = [.9 .999];  % dfP      = 0.95;
raXk     = [0 1];      % dfXk     = 0.5;
raXmeff  = [3 3];      % dfXmeff  = 1.5;
raRfact  = [5 20];     % dfRfact  = 10;
raErr    = [2 2];      % dfErr    = 1.5;
raDerr   = [5 5];      % dfDerr   = 2;

fTauminDiff = (raTaumin(2) - raTaumin(1));
fTaumaxDiff = (raTaumax(2) - raTaumax(1));
fPDiff      = (raP(2) - raP(1));
fXkDiff     = (raXk(2) - raXk(1));
fXmeffDiff  = (raXmeff(2) - raXmeff(1));
fRfactDiff  = (raRfact(2) - raRfact(1));
fErrDiff    = raErr(2) - raErr(1);
fDerrDiff   = raDerr(2) - raDerr(1);

%% add column for independence probability (actually will just be number of
%% times the event has appeared in a catalogue (will need to divide by
%% simNum to get P

mCatalog(:,ZMAP_COL_PROBABILITY) = 0;

% Random numbers for simulations
TestRandomFile = sParamFilename;
mParameters = pythonCSEPRandom(nSimNum, 8);
% simulate parameter values and run the delcustering code

for nCnt = 1:nSimNum
   disp(num2str(nCnt));
  
   vRandom = mParameters(nCnt, :);
   fTaumin = raTaumin(1) + (fTauminDiff * vRandom(1));
   fTaumax = raTaumax(1) + (fTaumaxDiff * vRandom(2));
   fP      = raP(1) + (fPDiff * vRandom(3));
   fXk     = raXk(1) + (fXkDiff * vRandom(4));
   fXmeff  = raXmeff(1) + (fXmeffDiff * vRandom(5));
   fRfact  = raRfact(1) + (fRfactDiff * vRandom(6));
   fErr    = raErr(1) + (fErrDiff * vRandom(7));
   fDerr   = raDerr(1) + (fDerrDiff * vRandom(8));

  [mCatalogDeclus, vIsMainshock] = ReasenbergDeclus(fTaumin, fTaumax, ...
                                   fXk, fXmeff, fP, fRfact, fErr, fDerr, mCatalog);

  mCatalog(vIsMainshock,ZMAP_COL_PROBABILITY) = mCatalog(vIsMainshock,ZMAP_COL_PROBABILITY) + 1;

end;

mCatalog(:,ZMAP_COL_PROBABILITY) = mCatalog(:,ZMAP_COL_PROBABILITY)./nSimNum;
mIndepProbCatalog = mCatalog;
