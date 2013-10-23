function [uOutput] = getCatalog_ImportZMAP(sFilename);

% get catalog in 13-column ZMAP ASCII format as used by CSEP
% convert to Matlab matrix

global ZMAP_HorizontalError;
global ZMAP_DepthError;
global ZMAP_MagnitudeError;

uOutput = load(sFilename);

% Check if downloaded catalog has valid error values (must be non-zero)

% Horizontal error can't be equal to zero
vSel = (uOutput(:, ZMAP_HorizontalError) == 0.0);
uOutput(vSel, ZMAP_HorizontalError) = 1.0;  % Default horizontal error

% Depth error can't be equal to zero
vSel = (uOutput(:, ZMAP_DepthError) == 0.0);
uOutput(vSel, ZMAP_DepthError) = 3.0;  % Default depth error

% Magnitude error can't be equal to zero
vSel = (uOutput(:, ZMAP_MagnitudeError) == 0.0);
uOutput(vSel, ZMAP_MagnitudeError) = 0.1;  % Default magnitude error
        
% save('foo.mat', uOutput);
