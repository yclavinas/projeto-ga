package org.corssa.predictiontesting;

import java.util.Random;

/**
 *
 * @author J. Douglas Zechar, zechar at usc.edu
 */
public class GamblingScoreTools {

    /**
     * Compute the reputation gain for the set of specified binary predictions,
     * observation, and reference forecast
     *
     * @param forecast array of binary predictions (all entries 0 or 1)
     * @param observation array of observed number of earthquakes in each bin
     * @param reference array of reference probabilities for each forecast bin
     * @return the change in reputation
     */
    public static float changeInReputation_Binary(boolean[] forecast,
            short[] observation, float[] reference) {
        float gain = 0;
        for (int i = 0; i < forecast.length; i++) { // sum over all predictions
            int x = 0;
            if (forecast[i]) {
                x = 1;
            }

            int y = 0;
            if (observation[i] > 0) {
                y = 1;
            }
            float p0 = reference[i];
            if (p0 > 0) {
                gain += x * y * (1 - p0) / p0 // hits
                        - (1 - x) * y // misses
                        - x * (1 - y) // false alarms
                        + (1 - x) * (1 - y) * p0 / (1 - p0); // correct negatives
            }
        }
        return gain;
    }

    /**
     * Compute the reputation gain for the set of specified probabilistic
     * forecasts, observation, and reference forecast
     *
     * @param forecast array of probabilistic forecasts (all entries b/w 0 & 1)
     * @param observation array of observed number of earthquakes in each bin
     * @param reference array of reference probabilities for each forecast bin
     * @return the change in reputation
     */
    public static float changeInReputation_Probabilistic(float[] forecast,
            short[] observation, float[] reference) {
        float gain = 0;
        for (int i = 0; i < forecast.length; i++) { // sum over all predictions
            float p = forecast[i];
            int y = 0;
            if (observation[i] > 0) {
                y = 1;
            }
            float p0 = reference[i];
            if (p0 > 0 && p > 0) {
                gain += y * (p * (1 - p0) / p0 - (1 - p))
                        + (1 - y) * (-p + (1 - p) * (p0) / (1 - p0));
            }
        }
        return gain;
    }

    /**
     * Compute the reputation gain for the set of specified Poisson rate
     * forecasts, observation, and reference forecast.  To do this, we convert
     * the rate and reference forecasts to probabilities (using p = 1-exp(-rt) =
     * 1 - exp(-\lambda)
     *
     * @param forecast array of probabilistic forecasts (all entries b/w 0 & 1)
     * @param observation array of observed number of earthquakes in each bin
     * @param reference array of reference probabilities for each forecast bin
     * @return the change in reputation
     */
    public static float changeInReputation_RateForecasts(float[] forecast,
            short[] observation, float[] reference) {
        float[] forecast_prob = new float[forecast.length];
        float[] reference_prob = new float[forecast.length];
        for (int i = 0; i < forecast_prob.length; i++) {
            if (!Float.isInfinite(forecast[i])) {
                forecast_prob[i] = 1f - (float) Math.exp(-forecast[i]);
            }
            if (!Float.isInfinite(reference[i])) {
                reference_prob[i] = 1f - (float) Math.exp(-reference[i]);
            }
        }
        float gain = GamblingScoreTools.changeInReputation_Probabilistic(
                forecast_prob, observation, reference_prob);
        return gain;
    }

    /**
     * For the observation and reference forecast, simulate many random
     * forecasts consistent with the reference model and compute the change in
     * reputation for each
     *
     * @param observation array of observed number of earthquakes in each bin
     * @param reference array of reference probabilities for each forecast bin
     * @return an array that represents the distribution of scores that could
     *          be expected from predictors following the reference model
     */
    public static float[] reputationGainDistribution(short[] observation,
            float[] reference) {
        float[] simulatedReputationGains = new float[1000];
        Random rndgen = new Random();

        for (int i = 0; i < simulatedReputationGains.length; i++) {
            boolean[] forecast = new boolean[reference.length];
            for (int j = 0; j < forecast.length; j++) { // simulate a forecast
                float rand = rndgen.nextFloat();
                if (rand < reference[j]) {
                    forecast[j] = true;
                } else {
                    forecast[j] = false;
                }
            }

            simulatedReputationGains[i] =
                    GamblingScoreTools.changeInReputation_Binary(forecast,
                    observation, reference);
        }
        return simulatedReputationGains;
    }

    /**
     * For the set of specified binary predictions, observation, and reference
     * forecast, compute the reputation gain and estimate its significance--what
     * is the probability that a larger reputation gain would be obtained by
     * guessing consistent with the reference forecast.
     *
     * @param forecast array of binary predictions (all entries 0 or 1)
     * @param observation array of observed number of earthquakes in each bin
     * @param reference array of reference probabilities for each forecast bin
     * @return an array that represents the distribution of scores that could
     *          be expected from predictors following the reference model
     */
    public static float significanceOfReputationGain(boolean[] forecast,
            short[] observation, float[] reference) {

        float reputationGain =
                GamblingScoreTools.changeInReputation_Binary(forecast,
                observation, reference);
        float[] simulatedReputationGains =
                GamblingScoreTools.reputationGainDistribution(observation,
                reference);
        float significance = 1f - MathUtil.percentile(reputationGain,
                simulatedReputationGains);

        return significance;
    }

    /**
     * For the set of specified rate forecast, observation, and reference
     * forecast, compute the reputation gain and estimate its significance--what
     * is the probability that a larger reputation gain would be obtained by
     * guessing consistent with the reference forecast.
     *
     * @param forecast array of rate  forecasts
     * @param observation array of observed number of earthquakes in each bin
     * @param reference array of reference probabilities for each forecast bin
     * @return an array that represents the distribution of scores that could
     *          be expected from predictors following the reference model
     */
    public static float significanceOfReputationGain(float[] forecast,
            short[] observation, float[] reference) {

        float reputationGain =
                GamblingScoreTools.changeInReputation_RateForecasts(forecast,
                observation, reference);
        float[] simulatedReputationGains =
                GamblingScoreTools.reputationGainDistribution(observation,
                reference);
        float significance = 1f - MathUtil.percentile(reputationGain,
                simulatedReputationGains);

        return significance;
    }
}
