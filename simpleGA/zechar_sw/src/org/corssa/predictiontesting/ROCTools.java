package org.corssa.predictiontesting;

import java.io.OutputStreamWriter;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.BufferedWriter;
import java.util.Calendar;
import java.text.SimpleDateFormat;
import java.util.Random;

public class ROCTools {

    public ROCTools() {
    }

    /**
     * Generate a random ROC trajectory for an experiment, taking into account
     * the specified distribution of target events and the discretization of the
     * specified forecast.  This trajectory will have N+2 elements; f_0=0 and
     * f_1, f_2, ..., f_N, and the final entry will be the number of active
     * cells in the forecat; here f_i represents the minimum number of false
     * alarms obtained to obtain at least i hits.  The values f_1, f_2, etc. do
     * not have to be unique unless the eqk distribution is such that no more
     * than one target eqk falls w/i a given bin.  In fact, we determine how
     * many bins contain at least one target eqk, and this is the number of
     * random numbers we need to draw.  Then, we construct the random ROC by
     * distributing the random numbers in a way such that if two target eqks
     * fall w/i a bin, two of the f_i values are equal.
     *
     * @param bins number of active bins in the experiment
     * @param observation distribution of target eqks
     * @param seed value w/ which to seed the random number generator
     * @return a sorted array of random jumps representing the performance of 
     *          a random predictor of this observation
     */
    private static int[] randomROC(int bins, short[] observation, long seed) {
        int N = ArrayUtil.sum(observation); // number of observed target eqks

        // The random ROC should contain N + 1 elements (
        // f_0 = 0, f_1, f_2, ..., f_N are random)
        int[] randomROC = new int[N + 1];
        randomROC[0] = 0;

        int trajectoryPosition = 1;
        // determine the number of target eqks occurring in each bin that
        // contains at least one target eqk
        short[] eqkDistribution = ArrayUtil.positiveEntries(observation);

        // how many bins contain at least one target eqk?
        int numberOfBinsObtainingEqks = eqkDistribution.length;

        // shuffle the number of target eqks occurring in each bin that 
        // contains at least one target eqk
        eqkDistribution = ArrayUtil.shuffle(eqkDistribution, seed);
        // for each bin containing at least one target eqk, get a random number 
        // b/w 1 and the total number of bins in the forecast
        // (get f_1, f_2, ..., f_N)
        int[] orderedRandomNumbers = ArrayUtil.orderedRandomIntegers(
                numberOfBinsObtainingEqks, bins, seed);

        // Distribute the random numbers to construct a random ROC
        // iterate over each of the bins which contain at least one target eqk
        for (int i = 0; i < eqkDistribution.length; i++) {
            // append this value of false alarms for as many eqks as there are
            // in this bin
            for (int j = 0; j < eqkDistribution[i]; j++) {

                randomROC[trajectoryPosition] = orderedRandomNumbers[i];
                trajectoryPosition++;
            }
        }

        return randomROC;
    }

    /**
     * Compute the confidence bounds for unskilled predictions on the ROC for 
     * the specified observation.  The confidence bounds are obtained by
     * simulating many random ROCs and computing the empricial bounds on false
     * alarm rate f at each value of hit rate h_i; that is, if I want the 10%
     * bound at a given value of h, I find the value of f below which 10% of the
     * simulated ROCs obtain hit rate h_i.
     *
     * @param bins the number of bins in the experiment of interest
     * @param observations number of target eqks in each bin
     * @param alpha significance value of interest
     * @param seed value w/ which to seed the random number generator
     * @return array containing, for each value of hit rate h_i, the number 
     *          of false alarms below which (alpha * 100)% of all unskilled
     *          predictors obtained h_i
     */
    private static int[][] confidenceBounds(int bins, short[] observations,
            float alpha, long seed) {
        int N = ArrayUtil.sum(observations);
        // These will hold the confidence bound points
        int[][] falseAlarmBounds = new int[N + 1][2];

        int numberOfSimulations = 10000;
        int[][] randomTrajectories = new int[numberOfSimulations][N + 1];

        Random rndgen = new Random(seed);
        for (int i = 0; i < numberOfSimulations; i++) {
            // we want each simulated trajectory to be unique
            long nextSeed = rndgen.nextLong();
            randomTrajectories[i] = ROCTools.randomROC(bins, observations, nextSeed);
        }

        // For each hit rate, compute the corresponding confidence value
        for (int i = 0; i <= N; i++) {
            int[] fsAtGivenH = new int[numberOfSimulations];
            for (int j = 0; j < numberOfSimulations; j++) {
                // Each random trajectory has N + 1 entries, w/ the
                // 0th entry = 0
                fsAtGivenH[j] = randomTrajectories[j][i];
            }
            falseAlarmBounds[i] = MathUtil.confidenceBounds(fsAtGivenH, alpha);
        }

        return falseAlarmBounds;
    }

    /**
     * Calculate the ROC trajecory for the given observation using the specified
     * forecast.  The idea here is to sort the forecast rates in descending
     * order and keep the binned target eqks synchronized. Then we use the
     * target eqks directly to determine the trajectory point associated w/ each
     * threshold.  This may result in some equal threshold values having
     * different H/F values, so we take another pass at the trajectory, starting
     * from the end; if two thresholds are equal, they are assigned the
     * maximum H/minimum F value associated w/ this threshold.  The final step
     * is to reduce the full trajectory to the simple jumps-only representation.
     * A difference b/w the ROC trajectory implementation and the Molchan
     * trajectory implementation is that we can here work w/ integers, as the
     * false alarm rates will all be rational numbers, each given by the number
     * of false alarms normalized by the number of active bins.  Therefore, here
     * we compute the trajectory in terms of the number of false alarms, rather
     * than the false alarm rate.
     *
     * @param forecast forecast object including rate forecast
     * @param observation binned representation of target eqk distribution,
     *          each entry contains the number of target epicenters contained
     *          w/i this bin
     * @return ROC trajectory containing the jumps, the minimum number of false
     *          alarms at which each hit rate is obtained
     */
    public static int[] roc(float[] forecast, short[] observation) {
        // copy the forecast values so that we're not changing the forecast
        // itself when we sort below
        float[] forecastValues = new float[forecast.length];
        System.arraycopy(forecast, 0, forecastValues, 0, forecast.length);

        // copy the eqk distribution so that we're not changing the
        // distribution itself when we sort below
        short[] eqkMap = new short[observation.length];
        System.arraycopy(observation, 0, eqkMap, 0, observation.length);

        short N = ArrayUtil.sum(eqkMap);
        // the first jump is always 0, so we need N+1 entries
        int[] trajectory = new int[N + 1];

        trajectory[0] = 0;

        // sort the afv in descending order and keep the target eqk distribution
        // synchronized
        // Shell sort
        for (int i = forecastValues.length / 2; i > 0;
                i = (i == 2 ? 1 : (int) Math.round(i / 2.2))) {
            for (int j = i; j < forecastValues.length; j++) {
                float forecast_temp = forecastValues[j];
                short eqk_temp = eqkMap[j];
                for (int k = j; k >= i && forecastValues[k - i] < forecast_temp;
                        k -= i) {
                    forecastValues[k] = forecastValues[k - i];
                    forecastValues[k - i] = forecast_temp;

                    eqkMap[k] = eqkMap[k - i];
                    eqkMap[k - i] = eqk_temp;
                }
            }
        }

        int falseAlarms = 0;
        short hits = 0;

        for (int i = 0; i < eqkMap.length; i++) {
            // only process this bin if it is an active part of the forecast
            // (the rate is greater than -Infinity)
            if (forecastValues[i] > Float.NEGATIVE_INFINITY) {

                short hitsInThisCell = eqkMap[i];
                if (hitsInThisCell > 0) {
                    float thresholdInThisCell = forecastValues[i];
                    float thresholdInNextCell = forecastValues[Math.min(i + 1,
                            forecastValues.length - 1)];
                    while (thresholdInThisCell == thresholdInNextCell && 
                            i < forecastValues.length - 2) {
                        i++;
                        hitsInThisCell += eqkMap[i];
                        thresholdInNextCell = forecastValues[i + 1];
                        if (eqkMap[i] == 0) {
                            falseAlarms++;
                        }
                    }
                    for (int j = 0; j < hitsInThisCell; j++) {
                        trajectory[hits + j + 1] = falseAlarms;
                    }
                    hits += hitsInThisCell;
                    if (hits == N) {
                        break;
                    }
                } else {
                    falseAlarms++;
                }
            }
        }
        return trajectory;
    }

    /**
     * Compute the ROC and the desired confidence bounds for the specified 
     * forecast and observation and save the results in XML format and
     * (optionally) in Matlab format
     *
     * @param forecast rate forecast of interest
     * @param observation catalog of target eqks for this experiment
     * @param resultsML path to file to which we'll be writing the ROC results
     * @param alpha significance value of interest; we'll compute two-sided
     *          confidence bounds (i.e., alpha and (1 - alpha))
     * @param seed value w/ which to seed the random number generator
     * @param saveInMatlabFormat Do you also want to save the results in Matlab
     *          format?
     */
    public static void roc(Forecast forecast, Catalog observation,
            String resultsMLFile, float alpha, long seed,
            boolean saveInMatlabFormat) {
        // Bin the target eqk catalog into the forecast grid
        short[] targetEqksMap = forecast.binnedCatalog(observation);
        short N = ArrayUtil.sum(targetEqksMap);

        // Compute the complete ROC and the upper and lower confidence bounds
        int[] jumps = ROCTools.roc(forecast.values(), targetEqksMap);
        int numberOfActiveBins = forecast.numberOfActiveBins();
        int[][] confidenceJumps = ROCTools.confidenceBounds(numberOfActiveBins,
                targetEqksMap, alpha, seed);

        Calendar startTime = Calendar.getInstance();
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
        String creationTime = df.format(startTime.getTime());

        // Write out the trajectory information to the results file
        try {
            FileOutputStream oOutFIS = new FileOutputStream(resultsMLFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n");
            oWriter.write("<CSEPResult xmlns=\"http://www.scec.org/xml-ns/" +
                    "csep/0.1\">\n");
            oWriter.write("   <resultData publicID=\"smi://org.scec/csep/" +
                    "results/1\">\n");
            oWriter.write("      <ROCTest publicID=\"smi://org.scec/csep/" +
                    "tests/roctest/1\">\n");
            oWriter.write("         <creationInfo creationTime=\"" +
                    creationTime + "\" />\n");
            oWriter.write("         <seed value=\"" + seed + "\" />\n");

            oWriter.write("         <name>ROC-Test_" + forecast.modelName() +
                    "</name>\n");
            oWriter.write("         <hitRate>");
            for (int i = 0; i <= N; i++) {
                oWriter.write((float) i / (float) N + " ");
            }
            oWriter.write("         </hitRate>\n");

            oWriter.write("         <falseAlarmRate>");
            for (int i = 0; i < jumps.length; i++) {
                oWriter.write(((float) jumps[i] / (float) numberOfActiveBins) +
                        " ");
            }
            oWriter.write("         </falseAlarmRate>\n");

            oWriter.write("         <lowerConfidence>");
            for (int i = 0; i < confidenceJumps.length; i++) {
                oWriter.write(((float) confidenceJumps[i][0] /
                        (float) numberOfActiveBins) + " ");
            }
            oWriter.write("         </lowerConfidence>\n");

            oWriter.write("         <upperConfidence>");
            for (int i = 0; i < confidenceJumps.length; i++) {
                oWriter.write(((float) confidenceJumps[i][1] /
                        (float) numberOfActiveBins) + " ");
            }
            oWriter.write("         </upperConfidence>\n");


            oWriter.write("      </ROCTest>\n");
            oWriter.write("   </resultData>\n");
            oWriter.write("</CSEPResult>\n");

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

            // Save in Matlab format
            if (saveInMatlabFormat) {
                String matlabFile = resultsMLFile.replace(".xml", ".m");
                oOutFIS = new FileOutputStream(matlabFile);
                oOutBIS = new BufferedOutputStream(oOutFIS);
                oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

                oWriter.write("h = [0:1/" + N + ":1];\n");
                oWriter.write("f = [");
                for (int i = 0; i < jumps.length; i++) {
                    oWriter.write(jumps[i] + ";");
                }
                oWriter.write("];\n");
                oWriter.write("f = f / " + numberOfActiveBins + ";\n");

                oWriter.write("lowerBounds = [");
                for (int i = 0; i < confidenceJumps.length; i++) {
                    oWriter.write(confidenceJumps[i][0] + ";");
                }
                oWriter.write("];\n");
                oWriter.write("lowerBounds = lowerBounds / " +
                        numberOfActiveBins + ";\n");

                oWriter.write("upperBounds = [");
                for (int i = 0; i < confidenceJumps.length; i++) {
                    oWriter.write(confidenceJumps[i][1] + ";");
                }
                oWriter.write("];\n");
                oWriter.write("upperBounds = upperBounds / " +
                        numberOfActiveBins + ";\n");

                oWriter.write("hold on;\n");
                oWriter.write("plot(f, h, 'ok', 'MarkerFaceColor', " +
                        "'black');\n");
                oWriter.write("plot(lowerBounds, h, '--k');\n");
                oWriter.write("plot(upperBounds, h, '--k');\n");
                oWriter.write("axis([0 1 0 1]);\n");
                oWriter.write("daspect([1 1 1]);\n");
                oWriter.write("xlabel('False alarm rate');\n");
                oWriter.write("ylabel('Hit rate');\n");

                oWriter.close();
                oOutBIS.close();
                oOutFIS.close();
            }
        } catch (Exception ex) {
            System.out.println("Error in ROCTools.roc()");
            ex.printStackTrace();
            System.exit(-1);
        }
    }
}
