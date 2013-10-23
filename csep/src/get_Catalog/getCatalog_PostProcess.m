function getCatalog_PostProcess(nYear, nMonth, nDay, sCatalogFile);

% Declare globals
global NumDeclusterSimulations;
global NumUncertaintyCatalogs;
global DECLUSTERED_CATALOG_FILENAME;
global NON_DECLUSTERED_CATALOG_FILENAME;


% Import Catalog into Matlab
mCatalog = getCatalog_Import('import_processed.dat');

% Cut catalog according to collection area
[mCatalog] = getCatalog_Cut2Area(mCatalog, 'getCatalog_CollectionArea.mat');

% Cut according to last testing day
fDay = decyear([nYear nMonth nDay 0 0 0]);
vSel = mCatalog(:,3) <= fDay;
mCatalog = mCatalog(vSel,:);


% Apply uncertainties to catalog as specified by sCatalogFile filename
% (declustered or undeclustered).
mCatalogUncert = [];
sUncertDir='uncertainties';
sTestAreaFile='getCatalog_TestArea.mat';
file_extension_pattern = '.mat$';

if strcmp(sCatalogFile, DECLUSTERED_CATALOG_FILENAME)

	% Decluster catalog only if declustered catalog is specified by the input
	% parameters.
    mDecluster = mc_Decluster(mCatalog, NumDeclusterSimulations, ...
                              'DeclusterParameter.mat');

	disp('Declustered catalog is used for catalog modifications...');
	mCatalogUncert = mDecluster;
                                                       
	% Cut catalog according to test area, filter events
	[mCatalogDecl] = filterEvents(mDecluster, sTestAreaFile);
	
	% Save catalog in Matlab format
	save(DECLUSTERED_CATALOG_FILENAME, 'mCatalogDecl');	
	
	% Save catalog in ASCII format
	% Remove file extension
   sFilename = regexprep(DECLUSTERED_CATALOG_FILENAME, file_extension_pattern, '');
   sAsciiFilename = sprintf('%s.dat', sFilename);
	save(sAsciiFilename, 'mCatalogDecl', '-ascii', '-double', '-tabs');

else
	disp('Undeclustered catalog is used for catalog modifications...');
	mCatalogUncert = mCatalog;	
end;


applyUncertainties(mCatalogUncert, NumUncertaintyCatalogs, ...
								   sTestAreaFile, sUncertDir);

% Cut catalog according to test area, filter events
[mCatalogNoDecl] = filterEvents(mCatalog, sTestAreaFile);


% Save catalog in Matlab format
save(NON_DECLUSTERED_CATALOG_FILENAME, 'mCatalogNoDecl');

% Save catalog in ASCII format
% Remove file extension
sFilename = regexprep(NON_DECLUSTERED_CATALOG_FILENAME, file_extension_pattern, '');
sAsciiFilename = sprintf('%s.dat', sFilename);
save(sAsciiFilename, 'mCatalogNoDecl', '-ascii', '-double', '-tabs');
