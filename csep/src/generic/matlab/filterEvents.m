% Filter catalog events.
%
% Filter criteria is based on the test area, decimal year, magnitude, and depth.
%
% Input parameters:
% mCatalog - Catalog data
% sAreaFile - File identifying area of interest
%
% Output parameters:
% mCatalogs - Filtered catalog data
%
function[mCatalog] = filterEvents(mCatalog, sAreaFile);

% Declare globals
global ZMAP_DecimalYear;
global ZMAP_Magnitude;
global ZMAP_Depth;
global ForecastMagnitudeThreshold;
global ForecastDecYearThreshold;
global ForecastDepthThreshold;


% Filter out events that are:
%    Outside of test area
%    Before year ForecastDecYearThreshold
%    Depth > ForecastDepthThreshold 
%    Magnitude < ForecastMagnitudeThreshold

if exist('sAreaFile')
   mCatalog = getCatalog_Cut2Area(mCatalog, sAreaFile);  
end;  

								
% Prepare catalog
vSel = mCatalog(:, ZMAP_DecimalYear) >= ForecastDecYearThreshold;
mCatalog = mCatalog(vSel,:);
	
vSel = mCatalog(:, ZMAP_Magnitude) >= ForecastMagnitudeThreshold;
mCatalog = mCatalog(vSel,:);
	
vSel = mCatalog(:, ZMAP_Depth) <= ForecastDepthThreshold;
mCatalog = mCatalog(vSel,:);

% Ignore events above Earth surface
vSel = mCatalog(:, ZMAP_Depth) >= 0;
mCatalog = mCatalog(vSel,:);
