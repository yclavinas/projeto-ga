function[] = MonteGK(numSim)

[fSpaceRange,fTimeRange] = CalcMonteGKWinParms();
fSpaceDiff = fSpaceRange(2) - fSpaceRange(1);
fTimeDiff = fTimeDiff(2) - fTimeDiff(1);

% set the rand number generator state
rand('state',sum(100*clock));

for simNum = 1:numSim
    nRand = rand(1,2);
    fSpace = fSpaceRange(1) + fSpaceDiff*nRand(1);
    fTime = fTimeRange(1) + fTimeDiff*nRand(2);
    
    [mCatDecluster, mCatAfter, vCluster, vCl, vMainCluster] = GKDeclus(mCatalog,fSpace,fTime)