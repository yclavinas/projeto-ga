

function [fLikelihood] = relm_STestSimulation(vForecast, nCnt, nNumberOfObservedEvents, sSeedFile);


global Forecast_Rate;
global Forecast_Observations;
global Forecast_PrecomputedZeroLikelihood;
global TestRandomFile;

fTotalForecastRate = sum(vForecast(:, Forecast_Rate));

% Create filename for simulation random seed file
nIteration = 1;
TestRandomFile = simulationSeedFilename(nCnt, nIteration, sSeedFile);

nNumberEvents = nNumberOfObservedEvents;

% Random numbers used by simulations
vRandom = pythonCSEPRandom(nNumberEvents, 1);

vRatesCDF = [cumsum(vForecast(:, Forecast_Rate)./fTotalForecastRate)];

for nCnt = 1:nNumberEvents
  nIndex = min(find((vRandom(nCnt) < vRatesCDF)));
  vForecast(nIndex, Forecast_Observations) = vForecast(nIndex, Forecast_Observations) + 1;
  vForecast(nIndex, Forecast_PrecomputedZeroLikelihood) = calc_logpoisspdf(vForecast(nIndex, Forecast_Observations), vForecast(nIndex, Forecast_Rate));
end;

fLikelihood = sum(vForecast(:, Forecast_PrecomputedZeroLikelihood));


