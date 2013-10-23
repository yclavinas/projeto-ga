% Global variables that define columns in ZMAP-format.
%
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
global ZMAP_HorizontalError;
global ZMAP_DepthError;
global ZMAP_MagnitudeError;
global ZMAP_NetworkName;
global ZMAP_COL_PROBABILITY;

ZMAP_Longitude=1;
ZMAP_Latitude=2;
ZMAP_DecimalYear=3;
ZMAP_Month=4;
ZMAP_Day=5;
ZMAP_Magnitude=6;
ZMAP_Depth=7;
ZMAP_Hour=8;
ZMAP_Minute=9;
ZMAP_Second=10;

% Error columns
ZMAP_HorizontalError=11;
ZMAP_DepthError=12;
ZMAP_MagnitudeError=13;

ZMAP_NetworkName=14;

% This column is generated only for declustered catalogs
ZMAP_COL_PROBABILITY = 0;
