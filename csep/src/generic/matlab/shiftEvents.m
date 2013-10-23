% Shift catalog events according to the horizontal error.
%
%    This function applies horizontal error to longitude and latitude of each
% event in the catalog. The shift happens on the surface of the Earth.
%    It will store randomly drawn numbers (one for the total distance, and one 
% for the angle) as additional columns of the output catalog.
%
% Input parameters:
% mCatalog - Catalog data.
% vRandomDist - Vector of random numbers used to generate a total distance for the shift. Empty
%                        vector is specified if random numbers must be obtained by the system.
% vRandomAngle - Vector of random numbers used to generate an angle for the shift. Empty
%                          vector is specified if random numbers must be obtained by the system.
% 
% Output parameters:
% mCatalog - Catalog with shifted events.
%
function[mCatalog] = shiftEvents(mCatalog, ...
											vRandomDist, ...
											vRandomAngle);

% Declare globals
global ZMAP_Longitude;
global ZMAP_Latitude;
global ZMAP_HorizontalError;
global Deg2Rad;
global Rad2Deg;
global EarthCircumference;
global EarthRadius;


% Define constants
% Angle range limits
ANGLE_MIN_RANGE=0.0;
ANGLE_MAX_RANGE=2.0*pi;


% Apply horizontal error to longitude and latitude: 

% Randomize horizontal error - total distance to shift the event
mCatalog(:, ZMAP_HorizontalError) = ...
      normalRandom(mCatalog(:, ZMAP_HorizontalError), vRandomDist);
      
% Take absolute value of the distance      
mCatalog(:, ZMAP_HorizontalError) = abs(mCatalog(:, ZMAP_HorizontalError));

% Generate random angle (in radians) - to move event by computed distance
% in the direction of this angle.
vAlpha = rangeRandom(ANGLE_MIN_RANGE, ANGLE_MAX_RANGE, vRandomAngle)

 
% Do the shift (use spherical geometry)
vBSide = (90.0 - mCatalog(:, ZMAP_Latitude))*Deg2Rad;
vCSide = mCatalog(:, ZMAP_HorizontalError)*360.0*Deg2Rad/EarthCircumference;

% Use the cosine rule
vASide = acos(cos(vBSide).*cos(vCSide) + sin(vBSide).*sin(vCSide).*cos(vAlpha));

% New latitude
mCatalog(:, ZMAP_Latitude) = 90 - vASide*Rad2Deg;

% Use the sine rule
% vGamma is the difference of longitudes for two points
vGamma = asin(sin(vCSide).*sin(vAlpha)./sin(vASide));

% New longitude
mCatalog(:, ZMAP_Longitude) = mCatalog(:, ZMAP_Longitude) + vGamma*Rad2Deg;
