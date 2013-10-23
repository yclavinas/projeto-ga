function [uOutput] = getCatalog_Import(sFilename);

global ZMAP_Magnitude;
global ZMAP_HorizontalError;
global ZMAP_DepthError;


% Determine how many lines are in the catalog file - pre-allocate the matrix
% to avoid memory fragmentation 
command = sprintf('wc -l %s', sFilename);
[return_code, return_str] = unix(command);

if return_code
   disp(['getCatalog_Import Error: ', return_str]);
end;

nRows = sscanf(return_str, '%g');
nCols = 14;

uOutput = zeros(nRows, nCols);
nCnt = 0;

hFile = fopen(sFilename);
while ~feof(hFile)
  mData = fgetl(hFile);
  nCnt = nCnt + 1;
  try
    uOutput(nCnt,1)  = str2num(mData(1:10));   % Longitude
    uOutput(nCnt,2)  = str2num(mData(12:20));  % Latitude
    uOutput(nCnt,3)  = str2num(mData(22:25));  % Year
    uOutput(nCnt,4)  = str2num(mData(27:28));  % Month
    uOutput(nCnt,5)  = str2num(mData(30:31));  % Day
    uOutput(nCnt,6)  = str2num(mData(33:37));  % Magnitude
    uOutput(nCnt,7)  = str2num(mData(39:46));  % Depth
    uOutput(nCnt,8)  = str2num(mData(48:49));  % Hour
    uOutput(nCnt,9)  = str2num(mData(51:52));  % Minute
    uOutput(nCnt,10) = str2num(mData(54:60));  % Second
    try
      uOutput(nCnt,11) = str2num(mData(62:68));  % Horizontal error
    catch
      uOutput(nCnt,11) = 2;  % Default horizontal error
    end;
    try
      uOutput(nCnt,12) = str2num(mData(70:76));  % Depth error
    catch
      uOutput(nCnt,12) = 5;  % Default depth error
    end;
    uOutput(nCnt,13) = 0.1;  % Default magnitude error
    uOutput(nCnt,14) = str2num(mData(78:80));    % Seismic Network 
  catch
    % Notify operator
  end;
  uOutput(nCnt,3) = decyear([uOutput(nCnt,3) uOutput(nCnt,4) uOutput(nCnt,5) uOutput(nCnt,8) uOutput(nCnt,9) uOutput(nCnt,10)]);
end;


% Condition data 
vSel = (uOutput(:, ZMAP_Magnitude) >= 0.0);
uOutput = uOutput(vSel, :);


% Check if downloaded catalog has valid error values (must be non-zero)

% Horizontal error can't be equal to zero
vSel = (uOutput(:, ZMAP_HorizontalError) == 0.0);
uOutput(vSel, ZMAP_HorizontalError) = 1.0;  % Default horizontal error

% Depth error can't be equal to zero
vSel = (uOutput(:, ZMAP_DepthError) == 0.0);
uOutput(vSel, ZMAP_DepthError) = 3.0;  % Default depth error
