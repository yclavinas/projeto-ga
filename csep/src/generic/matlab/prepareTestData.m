% Prepare data for the RELM test.
%
% Input parameters:
% sForecastFile - Path to the forecast file.
% sCatalogFile - Path to the declustered catalog file.
% sModificationsFile - Path to the catalog uncertainties file.
% vWeights - Optional weight vector for the forecast model.
%
% Output parameters:
% vScaledForecast - Scaled down forecast model.
% sModelName - Forecast model name.
% cCatalog - Observations.
% mModifications - Catalog modifications.
%
function [vScaledForecast, sModelName, cCatalog, mModifications] = ...
   prepareTestData(sForecastFile, sCatalogFile, sModificationsFile, vWeights);

% Declare global variables
global ForecastScaleFactor;
global Forecast_MaskBit;
global USE_FORECAST_WEIGHTS;


[vScaledForecast] = scaleForecast(sForecastFile, ForecastScaleFactor);


% Reduce forecast to the valid locations if weights flag is enabled
if USE_FORECAST_WEIGHTS
   vWeightCombined = [];
      
   if exist('vWeights')
      vWeightCombined = vScaledForecast(:, Forecast_MaskBit) .* vWeights;
   else
      vWeightCombined = vScaledForecast(:, Forecast_MaskBit);
   end;
      
    % Select the rows to be used
	vSel = (vWeightCombined > 0);
	vScaledForecast = vScaledForecast(vSel,:);
end;

    
% Regex to extract filename of the forecast from given path
sModelNameCell = regexp(sForecastFile, '([^/]+)$', 'match');

% Remove file extension
file_extension_pattern = '.mat$';
sModelNameCell = regexprep(sModelNameCell, file_extension_pattern, '');
sModelName = sModelNameCell{1};     


% Load declustered catalog ('mCatalogDecl' variable) or 
% undeclustered catalog ('mCatalog' variable)
rLoad = load(sCatalogFile);

if isfield (rLoad, 'mCatalogDecl')	
   cCatalog = rLoad.mCatalogDecl;
elseif isfield (rLoad, 'mCatalogNoDecl')
   cCatalog = rLoad.mCatalogNoDecl;
else
   	disp(['Unexpected variable is specified by the ', sCatalogFile, ...
   	        ' catalog file. Expected one of mCatalogNoDecl OR mCatalogDecl. ', ...
	           'Exiting the test.']);
	pause;
end;

	
% Filter catalog data based on forecast group parameters: magnitude, depth,
% beginning of forecast (in case the same observation catalog is re-used by
% multiple forecast groups with different starting date)
cCatalog = filterEvents(cCatalog);	

	
% Load catalog modifications if any
mModifications = [];

if exist(sModificationsFile, 'file')
   rLoad = load(sModificationsFile);
   
   if isfield(rLoad, 'mModifications')
      mModifications = rLoad.mModifications;
   else
		disp(['Unexpected variable is specified by the ', sModificationsFile, ...
		      ' modifications file. Expected mModifications. Exiting the test.']);
		pause;      
   end;
   
   % Number of modified catalogs
   nNumberModification = length(mModifications);
   for nCnt = 1:nNumberModification
      mModifications{nCnt} = filterEvents(mModifications{nCnt});
   end;
   
   
else
	disp(['Modifications file ', sModificationsFile, ...
	      ' does not exist, skipping loading of the file...']);
end;   	
