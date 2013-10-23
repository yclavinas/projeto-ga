function [fLikelihoodRatio] = relm_RTestSimulation(vForecast1, vForecast2, ...
                                                   nSimForecast, nCnt, sSeedFile);


global Forecast_Rate;
global Forecast_Observations;
global Forecast_PrecomputedZeroLikelihood;
global TestRandomFile;


if nSimForecast == 1
  nIteration = 1;
  vForecast = vForecast1;
else
  nIteration = 3;
  vForecast = vForecast2;
end;

fTotalForecastRate = sum(vForecast(:, Forecast_Rate));

% Create filename for simulation random seed file
TestRandomFile = simulationSeedFilename(nCnt, nIteration, sSeedFile);

% Random numbers used by simulations
fRandom = pythonCSEPRandom(1, 1);

nNumberEvents = poissinv(fRandom, fTotalForecastRate);

% Create filename for simulation random seed file
nIteration = nIteration + 1;
TestRandomFile = simulationSeedFilename(nCnt, nIteration, sSeedFile);

% Random numbers used by simulations
vRandom = pythonCSEPRandom(nNumberEvents, 1);

vRatesCDF = [cumsum(vForecast(:, Forecast_Rate)./fTotalForecastRate)];

for nCnt = 1:nNumberEvents
  nIndex = min(find((vRandom(nCnt) < vRatesCDF)));
  binOfInterest = vForecast(nIndex, 1:8);
  nIndex1 = find(vForecast1(:, 1) == binOfInterest(1) & vForecast1(:, 3) == binOfInterest(3) & vForecast1(:, 5) == binOfInterest(5) & vForecast1(:, 7) == binOfInterest(7));
  vForecast1(nIndex1, Forecast_Observations) = vForecast1(nIndex1, Forecast_Observations) + 1;
  vForecast1(nIndex1, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(vForecast1(nIndex1, Forecast_Observations), vForecast1(nIndex1, Forecast_Rate));
  nIndex2 = find(vForecast2(:, 1) == binOfInterest(1) & vForecast2(:, 3) == binOfInterest(3) & vForecast2(:, 5) == binOfInterest(5) & vForecast2(:, 7) == binOfInterest(7));
  vForecast2(nIndex2, Forecast_Observations) = vForecast2(nIndex2, Forecast_Observations) + 1;
  vForecast2(nIndex2, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(vForecast2(nIndex2, Forecast_Observations), vForecast2(nIndex2, Forecast_Rate));
end;

fLikelihoodRatio = sum(vForecast1(:, Forecast_PrecomputedZeroLikelihood)) - sum(vForecast2(:, Forecast_PrecomputedZeroLikelihood));


