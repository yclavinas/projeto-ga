function[fSpaceRange,fTimeRange] = CalcMonteGKWinParms()

fSpace1 = 10.^(0.1238*fMagnitude+0.983);
if fMagnitude >= 6.5
    fTime1 = (10.^(0.032*fMagnitude+2.7389))/365; 
else
    fTime1 = (10.^(0.5409*fMagnitude-0.547))/365;
end;

%disp('Using Gruenthal, pers. communication')
fSpace2 = exp(1.77+sqrt(0.037+1.02*fMagnitude));
if fMagnitude < 6.5
    fTime2 = abs((exp(-3.95+sqrt(0.62+17.32*fMagnitude)))/365);
else
    fTime2 = (10.^(2.8+0.024*fMagnitude))/365;
end;
%disp('Urhammer, 1976');
fSpace3 = exp(-1.024+0.804*fMagnitude);
fTime3 = (exp(-2.87+1.235*fMagnitude))/365;

fSpaceMin = min([fSpace1,fSpace2,fSpace3]);
fSpaceMax = max([fSpace1,fSpace2,fSpace3]);
fSpaceRange = [fSpaceMin fSpaceMax];

fTimeMin = min([fTime1,fTime2,fTime3]);
fTimeMax = max([ftime1,fTime2,fTime3]);
fTimeRange = [fTimeMin fTimeMax];