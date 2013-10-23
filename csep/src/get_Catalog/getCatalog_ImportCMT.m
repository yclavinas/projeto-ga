function [mOutput] = getCatalog_ImportCMT(sFilename);

global ZMAP_Longitude;
global ZMAP_Latitude;
global ZMAP_DecimalYear;
global ZMAP_Month;
global ZMAP_Day;
global ZMAP_Magnitude;
global ZMAP_Depth;
global ZMAP_Hour;
global ZMAP_Minute;
global ZMAP_Second;

% col    information
% ===================
% 1    eventid
% 2    2-digit year
% 3    month
% 4    day
% 5    time
% 6    centroid time offset
% 7    latitude
% 8    longitude
% 9    depth
% 10    scalar moment exponent
% 11    scalar moment base
% 12    eigenvector plunge
% 13    eigenvector azimuth
% 14    eigenvector plunge
% 15    eigenvector azimuth
% 16    nodal plane %1 strike
% 17    nodal plane %1 dip
% 18    nodal plane %1 rake
% 19    nodal plane %2 strike
% 20    nodal plane %2 dip
% 21    nodal plane %2 rake

fid = fopen(sFilename);

% Skip eventid
% Read 2-digit year, month, day: 1, 2, 3
% Read time: 4, 5, 6
% Skip centroid time offset
% Read latitude: 7
% Read longitude: 8
% Read depth: 9
% Skip scalar moment exponent
% Read magnitude - replaced by PostProcessing with moment magnitude: 10
% Skip remaining fields of the event
%
C = textscan(fid, '%*n%n%n%n%n:%n:%n%*n%n%n%n%*n%n%*n%*n%*n%*n%*n%*n%*n%*n%*n%*n', 'CollectOutput', 1);
fclose(fid);

% Create catalog in ZMAP format

nCols = 14;
[nRows, cols] = size(C{1});

mOutput = zeros(nRows, nCols);

% No need to populate empty catalog
if ~isempty(mOutput)

	% Longitude
	mOutput(:,ZMAP_Longitude) = C{1}(:,8);
	
	% Latitude
	mOutput(:,ZMAP_Latitude) = C{1}(:,7);
	
	% Year: CMT starts with 1976
	vSel = ((C{1}(:, 1) >= 76.0) & (C{1}(:, 1) <= 99.0));
	C{1}(vSel, 1) = C{1}(vSel, 1) + 1900;
	C{1}(not(vSel), 1) = C{1}(not(vSel), 1) + 2000;
	
	mOutput(:,ZMAP_DecimalYear) = C{1}(:,1);
	
	% Month
	mOutput(:,ZMAP_Month) = C{1}(:,2);
	
	% Day
	mOutput(:,ZMAP_Day) = C{1}(:,3);
	
	% Magnitude
	mOutput(:,ZMAP_Magnitude) = C{1}(:,10);
	
	% Depth
	mOutput(:,ZMAP_Depth) = C{1}(:,9);
	
	% Hour
	mOutput(:,ZMAP_Hour) = C{1}(:,4);
	
	% Minutes
	mOutput(:,ZMAP_Minute) = C{1}(:,5);
	
	% Seconds
	mOutput(:,ZMAP_Second) = C{1}(:,6);
	
	% Convert year to decimal year
	mOutput(:,ZMAP_DecimalYear) = decyear([mOutput(:,ZMAP_DecimalYear) ...
	                                              mOutput(:,ZMAP_Month) ...
	                                              mOutput(:,ZMAP_Day) ...
	                                              mOutput(:,ZMAP_Hour) ...
	                                              mOutput(:,ZMAP_Minute) ...
	                                              mOutput(:,ZMAP_Second)]);
	
end;