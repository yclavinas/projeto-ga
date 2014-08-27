package org.corssa.predictiontesting;

import java.util.Random;

/**
 *
 * @author J. Douglas Zechar, zechar at usc.edu
 */
public class LikelihoodTools {

    /**
     * Compute the log of the Poisson joint likelihood of a given set of
     * observations, given a set of expectations, using the 6th eqn on p 19 of
     * Schorlemmer et al 2007.
     *
     * @param forecast array of forecast expectations, the number of
     *          earthquakes forecast in each bin
     * @param observation array of observed number of earthquakes in each bin
     * @return the joint log-likelihood of the observations conditional on the
     *          forecast
     */
    public static float poissonJointLogLikelihood(float[] forecast,
            short[] observation) {
        float sum = 0.0f;
        int bins = forecast.length;
        for (int i = 0; i < bins; i++) {
            if (!Float.isInfinite(forecast[i])) {
                sum -= forecast[i];
                if (observation[i] > 0) {
                    if (forecast[i] == 0.0f) {
                        forecast[i] = Float.MIN_VALUE;
                    }
                    sum += observation[i] * Math.log(forecast[i])
                            - Math.log(MathUtil.factorial(observation[i]));
                }
            }
        }
        return sum;
    }

    /**
     * Compute the ratio of the log of the Poisson joint likelihoods of an
     * observation given two forecasts, using the 7th eqn on p 19 of Schorlemmer
     * et al 2007.
     *
     * @param forecastA array of model A expectations, the number of
     *          earthquakes expected in each bin according to model A
     * @param forecastB array of model B expectations, the number of
     *          earthquakes expected in each bin according to model B
     * @param observation array of observed number of earthquakes in each bin
     * @return the log-likelihood ratio of the models conditional on the
     *          observed seismicity.
     */
    public static float logLikelihoodRatio(float[] forecastA, float[] forecastB,
            short[] observation) {
        float llr = 0.0f;
        for (int i = 0; i < forecastA.length; i++) {
            if (!Float.isInfinite(forecastA[i]) && !Float.isInfinite(forecastB[i])) {
                llr += forecastB[i] - forecastA[i];
                if (observation[i] > 0) {
                    llr += observation[i] * Math.log(forecastA[i]
                            / forecastB[i]);
                }
            }
        }
        return llr;
    }

    /**
     * Create a simulated catalog that is consistent with the rates specified 
     * in the expectation vector, as described on p 1186 of Zechar et al 2010
     * (first full paragraph following eq 12)
     *
     * @param forecast vector of model rates for each lat/lon/mag bin
     * @return simulated catalog, represented as a vector with each entry
     *      representing the number of earthquakes occurring in each bin.
     */
    public static short[] simulatedEqkCatalog(float[] forecast) {
        int bins = forecast.length;
        float expectedNumberOfEvents = ArrayUtil.sum(forecast, 0);

        // Sample the Poisson distribution with the specified expectation to
        // determine how many events to simulate
        Random rndgen = new Random();
        float rnd = rndgen.nextFloat();
        int numberOfEventsToSimulate = MathUtil.inverseCumulativePoisson(rnd,
                expectedNumberOfEvents);

        // Normalize the expectations so that their sum is unity, use this
        // construct to build the simulated catalog
        float[] normalizedExpectations =
                ArrayUtil.normalizeIgnoreNegativeValues(forecast);

        float[] cumulativeFractionConstruct =
                new float[normalizedExpectations.length];
        cumulativeFractionConstruct[0] = normalizedExpectations[0];
        for (int i = 1; i < cumulativeFractionConstruct.length; i++) {
            if (!Float.isInfinite(normalizedExpectations[i])) {
                cumulativeFractionConstruct[i] = cumulativeFractionConstruct[i - 1]
                        + normalizedExpectations[i];
            } else {
                cumulativeFractionConstruct[i] = cumulativeFractionConstruct[i - 1];
            }
        }

        // Simulate the catalog by drawing random numbers and mapping each
        // random number to a given forecast bin, based on its normalized rate
        short[] simulatedObservations = new short[bins];
        for (int i = 0; i < numberOfEventsToSimulate; i++) {
            rnd = rndgen.nextFloat();
            for (int j = 0; j < normalizedExpectations.length; j++) {
                if (rnd < cumulativeFractionConstruct[j]) {
                    simulatedObservations[j]++;
                    break;
                }
            }
        }
        return simulatedObservations;
    }

    /**
     * Create a simulated catalog that is consistent with the rates specified
     * in the expectation vector, as described on p 1186 of Zechar et al 2010
     * (first full paragraph following eq 12)
     *
     * @param forecast vector of model rates for each lat/lon/mag bin
     * @param numberOfEventsToSimulate number of events to simulate
     * @return simulated catalog, represented as a vector with each entry
     *      representing the number of earthquakes occurring in each bin.
     */
    public static short[] simulatedEqkCatalog(float[] forecast,
            int numberOfEventsToSimulate) {
        int bins = forecast.length;
        Random rndgen = new Random();
        float rnd = rndgen.nextFloat();

        // Normalize the expectations so that their sum is unity, use this
        // construct to build the simulated catalog
        float[] normalizedExpectations =
                ArrayUtil.normalizeIgnoreNegativeValues(forecast);

        float[] cumulativeFractionConstruct =
                new float[normalizedExpectations.length];
        cumulativeFractionConstruct[0] = normalizedExpectations[0];
        for (int i = 1; i < cumulativeFractionConstruct.length; i++) {
            cumulativeFractionConstruct[i] = cumulativeFractionConstruct[i - 1]
                    + normalizedExpectations[i];
        }

        // Simulate the catalog by drawing random numbers and mapping each
        // random number to a given forecast bin, based on its normalized rate
        short[] simulatedObservations = new short[bins];
        for (int i = 0; i < numberOfEventsToSimulate; i++) {
            rnd = rndgen.nextFloat();
            for (int j = 0; j < normalizedExpectations.length; j++) {
                if (rnd < cumulativeFractionConstruct[j]) {
                    simulatedObservations[j]++;
                    break;
                }
            }
        }
        return simulatedObservations;
    }

    /**
     * Compute gamma, the fraction of 1000 simulated log likelihoods that are
     * less than the observed log likelihood for the given forecast and
     * observation.  See Zechar et al 2010 pp 1186-87
     *
     * @param forecast expected number of earthquakes in each bin
     * @param observation observed number of earthquakes in each bin
     * @return the fraction of simulations for which the specified expectations
     *          obtains a lower log likelihood than the observed log likelihood.
     */
    public static float lTest(float[] forecast, short[] observation) {
        float lObserved = poissonJointLogLikelihood(forecast, observation);

        int numberOfSimulations = 1000;
        float[] lSimulated = new float[numberOfSimulations];

        for (int i = 0; i < numberOfSimulations; i++) {
            short[] simulatedObservation = simulatedEqkCatalog(forecast);
            lSimulated[i] = poissonJointLogLikelihood(forecast,
                    simulatedObservation);
        }
        float gamma = MathUtil.percentile(lObserved, lSimulated);
        return gamma;
    }

    /**
     * Compute gamma hat (or kappa or zeta) the fraction of 1000 simulated
     * conditional log likelihoods that are less than the observed log
     * likelihood for the given forecast and observation.  This functionality
     * is the same for the M-, S-, and L-hat tests (the summing over space-, or
     * magnitude-, is done external to this functionality).  See Zechar et al
     * 2010, p 1187 and Werner et al 2010 BSSA
     *
     * @param forecast expected number of earthquakes in each bin
     * @param observation observed number of earthquakes in each bin
     * @return the fraction of simulations for which the specified expectations
     *          obtains a lower log likelihood than the observed log likelihood.
     */
    public static float conditionalLTest(float[] forecast,
            short[] observation) {
        short numberOfEventsToSimulate = ArrayUtil.sum(observation);

        // normalize the forecast to match the observed number of events
        float[] normalizedForecast = ArrayUtil.normalize(forecast);
        for (int i = 0; i < normalizedForecast.length; i++) {
            normalizedForecast[i] = normalizedForecast[i]
                    * (float) numberOfEventsToSimulate;
        }

        float lHatObserved = poissonJointLogLikelihood(normalizedForecast,
                observation);

        int numberOfSimulations = 1000;
        float[] lHatSimulated = new float[numberOfSimulations];

        for (int i = 0; i < numberOfSimulations; i++) {
            short[] simulatedObservation = simulatedEqkCatalog(normalizedForecast,
                    numberOfEventsToSimulate);
            lHatSimulated[i] = poissonJointLogLikelihood(normalizedForecast,
                    simulatedObservation);
        }
        float gamma = MathUtil.percentile(lHatObserved, lHatSimulated);
        return gamma;
    }

    /**
     * Compute delta_1 and delta_2, the probability that a) at least and b) at
     * most N events would occur under the given forecast (with Poisson
     * uncertainty), where N is the number of observed events.  See Zechar et al
     * 2010 pp 1185-86.
     *
     * @param forecast expected number of earthquakes in each bin
     * @param observation observed number of earthquakes in each bin
     * @return the probability that at least this many eqks should be expected,
     *          and the probability that at most this many eqks should be
     *          expected, given the forecast, where "this many" eqks is the
     *          number of eqks in the given observation
     */
    public static float[] nTest(float[] forecast, short[] observation) {
        int nObserved = ArrayUtil.sum(observation);
        float nExpected = ArrayUtil.sum(forecast, 0f);
        float delta_1 = 1f - (float) MathUtil.poissonProbabilityCumulative(
                nObserved - 1, nExpected);
        float delta_2 = (float) MathUtil.poissonProbabilityCumulative(nObserved,
                nExpected);
        float[] delta = {delta_1, delta_2};
        return delta;
    }

    /**
     * Compute alpha, the fraction of simulated log likelihood ratios that are
     * less than the observed log likelihood ratio for the given sets of
     * expectations and observations.  See Schorlemmer et al p 19, 21
     *
     * @param forecastA expected number of earthquakes in each bin according
     *          to model A
     * @param forecastB expected number of earthquakes in each bin according
     *          to model B
     * @param observation observed number of earthquakes in each bin
     * 
     * @return the fraction of simulations for which modelARates obtains a 
     *          lower log likelihood ratio than the observed log likelihood
     *          ratio
     */
    public static float rTest(float[] forecastA, float[] forecastB,
            short[] observation) {
        float rObserved = logLikelihoodRatio(forecastA, forecastB, observation);
        int numberOfSimulations = 1000;
        float[] rSimulated = new float[numberOfSimulations];

        for (int i = 0; i < numberOfSimulations; i++) {
            short[] simulatedRates = simulatedEqkCatalog(forecastA);
            rSimulated[i] = logLikelihoodRatio(forecastA, forecastB,
                    simulatedRates);
        }

        float alpha = MathUtil.percentile(rObserved, rSimulated);
        return alpha;
    }
}
