function [mCatalog] = getCatalog_Cut2Area(mCatalog, sAreaFile);

load(sAreaFile);

% Get the number of earthquakes in catalog
[nRow] = length(mCatalog(:,1));

% Determine number of columns
[nRow, nCol] = size(mCatalog);
COL_INSIDE = nCol + 1;

% Use default values for the column if it doesn't get generated
mCatalog(:, COL_INSIDE) = 0;

% Fix for Trac ticket #114: floating point representation of mArea coordinates plus
% inclusive/exclusive boundary check was voiding valid events
fThreshold = 0.0001;

for nCnt = 1:nRow
  x = mCatalog(nCnt,1);
  y = mCatalog(nCnt,2);

  vSel = ((mArea(:,1)-0.05-x <= fThreshold) & (mArea(:,1)+0.05-x > fThreshold) & ...
          (mArea(:,2)-0.05-y <= fThreshold) & (mArea(:,2)+0.05-y > fThreshold));
  mCatalog(nCnt, COL_INSIDE) = sum(vSel);
end;

% Fix for ticket #1 : Keep only events that are within area of interest
vSel = (mCatalog(:, COL_INSIDE) > 0);

mCatalog = mCatalog(vSel, :);
