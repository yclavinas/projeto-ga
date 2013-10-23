function [mCatalog] = testing_ApplyUncertainties(mCatalog, fLon, fLat, fMag);

for nCnt = 1:length(mCatalog(:,1))
  mCatalog(nCnt,1) = calc_RandomNormal(mCatalog(nCnt,1), fLon);
  mCatalog(nCnt,2) = calc_RandomNormal(mCatalog(nCnt,2), fLat);
  mCatalog(nCnt,6) = calc_RandomNormal(mCatalog(nCnt,6), fMag);
end;