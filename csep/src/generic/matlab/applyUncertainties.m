% Apply uncertainties to the catalog.
%
% Input parameters:
% mCatalog - Catalog data.
% nNumberCatalogs - Number of catalogs with uncertainties to generate.
% sTestAreaFile - Filename that stores longitude/latitude of the area of interest.
% sUncertDir - Directory to write output files to.
%
% Output parameters: None.
%
function [mModifications] = applyUncertainties(mCatalog, nNumberSimulations, ...
							           			        sTestAreaFile, sUncertDir);

% Declare globals
global ZMAP_Magnitude;
global ZMAP_Depth;
global ZMAP_DepthError;
global ZMAP_MagnitudeError;
global ZMAP_COL_PROBABILITY;
global Deg2Rad;
global UseRandomFile;
global TestRandomFile;
global UncertaintiesRandomFile;
global TestRandomFilePostfix;
global ENABLE_DEBUG;
global ENABLE_DEPTH_ERROR;
global ENABLE_MAGNITUDE_ERROR;
global ENABLE_HORIZONTAL_ERROR;


% Define indeces to access random matrix
DISTANCE_INDEX = 1;
ANGLE_INDEX = 2;
DEPTH_INDEX = 3;
MAGNITUDE_INDEX = 4;
PROBABILITY_INDEX = 5;


disp('Applying uncertainties to the catalog...');
mkdir(sUncertDir); 


% Save catalog before uncertainties
if ENABLE_DEBUG
   file_name = sprintf('%s/catalog.mat', sUncertDir);
   save(file_name, 'mCatalog');
end;

% Result cell array of catalog modifications
mModifications = {};

% No need to apply uncertainties to an empty catalog
if ~isempty(mCatalog)

	% Get dimensions for random matrix
	[nRandomRows, cols] = size(mCatalog);
	nRandomCols = MAGNITUDE_INDEX;

   if ZMAP_COL_PROBABILITY > 0
      nRandomCols = PROBABILITY_INDEX;
   end;
	
	for nCnt = 1:nNumberSimulations
	
		disp(['Generating uncertainty catalog ', num2str(nCnt), '...']);
		
		% Catalog with uncertainties:
		mUncertainty = mCatalog;
		
		% Format seed filename for the simulation random numbers
        TestRandomFile = sprintf('%s/%s.%d%s', sUncertDir, ...
      	                         UncertaintiesRandomFile, ...
		                         nCnt, TestRandomFilePostfix);

		% Matrix of random numbers used to generate catalog uncertainties:
		% Horizontal Error 
		% Angle
		% Depth
		% Magnitude
		% Probability
	   mRandom = pythonCSEPRandom(nRandomRows, nRandomCols);
		   
   	   vRandomDist = mRandom(:,  DISTANCE_INDEX);
	   vRandomAngle = mRandom(:, ANGLE_INDEX);
	   vRandomDepth = mRandom(:, DEPTH_INDEX);
	   vRandomMagn = mRandom(:, MAGNITUDE_INDEX);
	   vRandomProb = [];
		   
	   % The column exists only for declustered catalog
	   if ZMAP_COL_PROBABILITY > 0
	      vRandomProb = mRandom(:, PROBABILITY_INDEX);
	   end;
	   
	   % Apply horizontal error if enabled	
       if ENABLE_HORIZONTAL_ERROR
	      % Apply horizontal error to longitude and latitude: 
		  mUncertainty = shiftEvents(mUncertainty, vRandomDist, vRandomAngle);
	   end;   
		
	   
	   % Apply depth error if enabled
	   if ENABLE_DEPTH_ERROR
          % Randomize depth error
	      mUncertainty(:, ZMAP_DepthError) = ...
	   		   normalRandom(mUncertainty(:, ZMAP_DepthError), vRandomDepth);
	   	
          % Apply depth error      
	      mUncertainty(:, ZMAP_Depth) = ...
	         mUncertainty(:, ZMAP_Depth) + mUncertainty(:, ZMAP_DepthError);	      
	   end;   
	   
	    
	   % Apply magnitude error if enabled    
	   if ENABLE_MAGNITUDE_ERROR
	      % Randomize magnitude error
	      mUncertainty(:, ZMAP_MagnitudeError) = ...
	         normalRandom(mUncertainty(:, ZMAP_MagnitudeError), vRandomMagn);
	      
   	      % Apply magnitude error   
	      mUncertainty(:, ZMAP_Magnitude) = ...
	          mUncertainty(:, ZMAP_Magnitude) + mUncertainty(:, ZMAP_MagnitudeError);	   
	   end;
	   
	   
	   % Randomize independence probability if such column is defined
	   if ZMAP_COL_PROBABILITY > 0
		   
		   % Get rid of events that have '0' independence probability, and
		   % remove corresponding random numbers for those events
		   vSel = (mUncertainty(:, ZMAP_COL_PROBABILITY) ~= 0);
		   mUncertainty = mUncertainty(vSel, :);
		   vRandomProb = vRandomProb(vSel, :);
		   
		   % Don't use random number if original independence probability is '1'
		   vSel = mUncertainty(:, ZMAP_COL_PROBABILITY) == 1;
		   % Reset random numbers for such probabilities to original value of '1'            
		   vRandomProb(vSel, :) = mUncertainty(vSel, ZMAP_COL_PROBABILITY);
		   
		   % Remove events that have random numbers larger than original independence 
		   % probability
		   vSel = (vRandomProb(:, 1) <= mUncertainty(:, ZMAP_COL_PROBABILITY));
		   
		   % Reduce catalog
		   mUncertainty = mUncertainty(vSel, :);
		   
	   end;
		   
	
	   if ENABLE_DEBUG
	       % Save catalog data in Matlab format 
		   file_name = sprintf('%s/catalog.uncert.%d.mat', sUncertDir, nCnt);
		   save(file_name, 'mUncertainty');	
		
		   % Save catalog data in ascii format
		   file_name = sprintf('%s/catalog.uncert.%d.dat', sUncertDir, nCnt);
     	   save(file_name, 'mUncertainty', '-ascii', '-double', '-tabs');		
       end;
		
		
		% Append new catalog
		mModifications{nCnt} = filterEvents(mUncertainty, sTestAreaFile);
			
	end;   % all simulations
end;   % non-empty catalog

disp('Done with catalog uncertainties.');

