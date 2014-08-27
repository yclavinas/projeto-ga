package org.corssa.predictiontesting;

import java.io.FileOutputStream;
import java.io.BufferedOutputStream;
import java.io.OutputStreamWriter;
import java.io.BufferedWriter;
import java.util.Calendar;
import java.text.SimpleDateFormat;
import java.util.Random;

/**
 * @author J. Douglas Zechar zechar at usc.edu
 */
public class MolchanTools {

    /**
     * Compute area skill score: 1 - normalized area under the Molchan 
     * trajectory up to specified tau; that is, 1 - the area/tau
     * 
     * @param molchanTrajectory sorted Molchan trajectory (fully specified by
     *          the tau values at which the "jumps" occur)
     * @param tau value up to which we want to evaluate the ASS
     * @return area skill score for the given trajectory up to the given tau
     */
    public static float ass(float[] molchanTrajectory, float tau) {
        float ass = 1.0f - MolchanTools.areaUnderMolchanTrajectory(
                molchanTrajectory, tau);
        return ass;
    }

    /**
     * Compute normalized area under the Molchan trajectory up to given tau; 
     * that is, calculate the area and divide it by tau
     * 
     * @param taus sorted Molchan trajectory (fully specified by
     *          the tau values at which the "jumps" occur)
     * @param tau value up to which we want to evaluate the ASS (value by which
     *          we'll normalize the area)
     * @return normalized area under the specified trajectory up to given tau
     */
    private static float areaUnderMolchanTrajectory(float[] taus, float tau) {
        // there are always N+1 jumps
        int N = taus.length - 1;

        // determine on which leg of the error trajectory tau falls
        int n = MolchanTools.whichLegAreWeOn(taus, tau);
        float[] nus = new float[N + 1];
        // set the nu values
        for (int j = 0; j < nus.length; j++) {
            nus[j] = (float) (N - j) / (float) N;
        }

        float area = 0.0f;
        // Sum the area under the trajectory up until the nth leg
        for (int i = 0; i <= n - 1; i++) {
            area += nus[i] * (taus[i + 1] - taus[i]);
        }
        // add the final bit of area under the trajecory
        area += nus[n] * (tau - taus[n]);

        // normalize the area by dividing by tau
        area /= tau;
        return area;
    }

    /**
     * For the specified Molchan trajectory, compute ASS trajectory as a 
     * function of tau (step every 0.01)
     *
     * @param molchanTrajectory sorted Molchan trajectory (fully specified by
     *          the tau values at which the "jumps" occur)
     * @return ass trajectory as a function of tau
     */
    public static float[] assTrajectory(float[] molchanTrajectory) {
        float[] assTrajectory = new float[100];

        for (int i = 1; i < 101; i++) {
            float tau = i * 0.01f;
            float ass = MolchanTools.ass(molchanTrajectory, tau);
            assTrajectory[i - 1] = ass;
        }
        return assTrajectory;
    }

    /**
     * Given the specified trajectory, determine on which leg of the trajectory
     * tau falls.  In particular, this answers the question: How many jumps have
     * occurred up to tau?
     * 
     * @param molchanTrajectory sorted Molchan trajectory (fully specified by
     *          the tau values at which the "jumps" occur)
     * @param tau value up to which we're evaluating
     * @return the leg of the specified trajectory at the specified tau
     */
    private static int whichLegAreWeOn(float[] molchanTrajectory, float tau) {
        // By default, we'll start on the 0th leg
        int n = 0;

        // If tau > jump_i, then we've obtained at least i hits, keep looking
        for (int i = 1; i < molchanTrajectory.length; i++) {
            if (molchanTrajectory[i] < tau) {
                n = i;
            } else {
                return i - 1;
            }
        }
        return n;
    }

    /**
     * Compute the two-sided confidence bounds for unskilled predictions
     * Molchan and ASS trajectories for the specified target eqk distribution
     * and reference model.  The confidence bounds are obtained by simulating
     * many random alarm functions, computing the corresponding Molchan/ASS
     * trajectories and computing the empirical bounds.  For Molchan bounds,
     * we're interested in the empirical bound on tau at each  value of nu_i
     * and for ASS bounds, we're interested in the empirical bound on ASS at
     * each value of tau; that is,  if I want the 10% Molchan bound at a given
     * value of nu, I find the value of tau below which and above which 10% of
     * the simulated trajectories obtain miss rate nu_i.
     * 
     * @param observation array describing the number of observed target eqks
     *          in each forecast bin
     * @param reference reference model to use in computing Molchan trajectories
     * @param alpha significance value of interest
     * @param seed value w/ which to seed the random number generator
     * @return array containing Molchan and ASS confidence bounds; the first N 
     *          values are the Molchan bounds, the remaining 100 values are the
     *          ASS bounds
     */
    private static float[][] confidenceBoundsMolchanAndASS(short[] observation,
            float[] reference, float alpha, long seed) {
        int N = ArrayUtil.sum(observation);

        // These will hold the upper and lower confidence bound points; N+1
        // Molchan bounds and 100 ASS bounds
        float[][] bounds = new float[N + 101][2];

        // How many random alarm functions should we simulate?
        int numberOfSimulations = 1000;

        // Make room to temporarily store each Molchan trajectory and each ASS
        // trajectory
        float[][] randomTrajectories = new float[numberOfSimulations][N + 1];
        float[][] randomASSTrajectories = new float[numberOfSimulations][100];

        Random rndgen = new Random(seed);
        for (int i = 0; i < numberOfSimulations; i++) {
            long nextSeed = rndgen.nextLong();
            // Simulate a random alarm function
            float[] randomAlarmFunctionValues = Utility.randomForecast(
                    reference, nextSeed);
            // Compute the Molchan trajectory
            randomTrajectories[i] = MolchanTools.molchanTrajectory(
                    randomAlarmFunctionValues, reference, observation);
            // Compute the corresponding ASS trajectory
            randomASSTrajectories[i] = MolchanTools.assTrajectory(
                    randomTrajectories[i]);

        }

        // For each nu_i for i = 0 to N, construct an array containing the 
        // simulated tau_i and determine the empirical confidence bounds for
        // this nu_i
        float[] tausAtGivenNu = new float[numberOfSimulations];
        for (int i = 0; i <= N; i++) {
            for (int j = 0; j < numberOfSimulations; j++) {
                tausAtGivenNu[j] = randomTrajectories[j][i];
            }
            bounds[i] = MathUtil.confidenceBounds(tausAtGivenNu, alpha);
        }

        // For each tau in 0.01:0.01:1, construct an array containing the 
        // simulated tau_i and determine the empirical confidence bounds for
        // this nu_i
        float[] assesAtGivenTau = new float[numberOfSimulations];
        // For each value of tau, compute the corresponding confidence value
        for (int i = 0; i < 100; i++) {
            for (int j = 0; j < numberOfSimulations; j++) {
                assesAtGivenTau[j] = randomASSTrajectories[j][i];
            }
            bounds[N + 1 + i] = MathUtil.confidenceBounds(assesAtGivenTau,
                    alpha);
        }

        return bounds;
    }

    /**
     * Calculate the error trajecory for the given target eqk catalog using the 
     * specified alarm function and reference; each of these is provided as array
     * that represents a 1-D mapping of the gridded study region.  The idea here
     * is to sort the alarm function values in descending order and keep the
     * target eqks and reference synchronized (so the bins match). Then we use
     * the target eqks and the reference directly to determine the trajectory
     * point associated w/ each threshold.  This may result in some equal
     * threshold values having different tau/nu values, so we take another pass
     * at the trajectory, starting from the end; if two thresholds are equal,
     * they are assigned the maximum tau/minimum nu value associated w/ this
     * threshold.  The final step is to reduce the full trajectory to the simple
     * jumps-only representation.
     *
     * @param forecast alarm function values
     * @param reference representation of the "cost" for occupying each box with
     *          an alarm.
     * @param observation representation of target eqk distribution, each entry
     *          contains the number of target epicenters contained w/i this bin
     * @return error trajectory containing the jumps; the minimum value of tau
     *          at which each miss rate is obtained
     */
    public static float[] molchanTrajectory(float[] forecast,
            float[] reference, short[] observation) {
        // copy the forecast values so that we're not changing the forecast
        // itself when we sort below
        float[] forecastValues = new float[forecast.length];
        System.arraycopy(forecast, 0, forecastValues, 0, forecast.length);

        // normalize a copy of the reference values so that we're not changing
        // the reference forecast itself when we sort below
        float[] referenceValues = ArrayUtil.normalizeIgnoreNegativeValues(
                reference);

        // copy the eqk distribution so that we're not changing the distribution
        // itself when we sort below
        short[] eqkMap = new short[observation.length];
        System.arraycopy(observation, 0, eqkMap, 0, observation.length);

        short N = ArrayUtil.sum(eqkMap);
        float[] trajectory = new float[N + 1];
        trajectory[0] = 0f;

        // sort the forecast rates in descending order and keep everything else
        // synchronized
        // Shell sort
        for (int i = forecastValues.length / 2; i > 0;
                i = (i == 2 ? 1 : (int) Math.round(i / 2.2))) {
            for (int j = i; j < forecastValues.length; j++) {
                float afv_temp = forecastValues[j];
                float reference_temp = referenceValues[j];
                short eqk_temp = eqkMap[j];
                for (int k = j; k >= i && forecastValues[k - i] < afv_temp;
                        k -= i) {
                    forecastValues[k] = forecastValues[k - i];
                    forecastValues[k - i] = afv_temp;

                    referenceValues[k] = referenceValues[k - i];
                    referenceValues[k - i] = reference_temp;

                    eqkMap[k] = eqkMap[k - i];
                    eqkMap[k - i] = eqk_temp;
                }
            }
        }

        float tau = 0f;
        short hits = 0;
        for (int i = 0; i < eqkMap.length; i++) {
            tau += referenceValues[i];
            short hitsInThisCell = eqkMap[i];
            if (hitsInThisCell > 0) {
                float thresholdInThisCell = forecastValues[i];
                float thresholdInNextCell = forecastValues[Math.min(i + 1,
                        forecastValues.length - 1)];
                while (thresholdInThisCell == thresholdInNextCell && i
                        <= forecastValues.length - 2) {
                    i++;
                    tau += referenceValues[i];
                    hitsInThisCell += eqkMap[i];
                    if (i < forecastValues.length - 1) {
                        thresholdInNextCell = forecastValues[i + 1];
                    } else {
                        thresholdInNextCell = Float.POSITIVE_INFINITY;
                    }
                }
                for (int j = 0; j < hitsInThisCell; j++) {
                    trajectory[hits + j + 1] = tau;
                }
                hits += hitsInThisCell;
                if (hits == N) {
//                    System.out.println(i);
                    break;
                }
            }
        }

        return trajectory;
    }

    /**
     * For the specified reference forecast and the forecasts w/ which to
     * compare it, compute the Molchan trajectory and the desired confidence
     * bounds for the specified target eqk catalog and save the results in XML
     * format and (optionally) Matlab format
     *
     * @param referenceForecast forecast to use as the reference model in
     *          computing Molchan trajectory
     * @param forecastsToCompare array of forecast paths w/ which we will
     *          compare the reference forecast
     * @param targetEqkCatalog catalog of observed target eqks of interest
     * @param resultsML path to file to which we'll be writing the Molchan
     *          results
     * @param seed value w/ which to seed the random number generator
     * @param alpha significance value of interest; we'll compute two-sided
     *          confidence bounds (i.e., alpha and (1 - alpha))
     * @param saveInMatlabFormat Do you also want to save the results in Matlab
     *          format?
     * @param useMaskBit Should we pay attention to the forecast masking bit
     */
    public static void molchanAndASS(String referenceForecastPath,
            String[] forecastsToCompare, Catalog targetEqkCatalog,
            String resultsMLFile, float alpha, long seed,
            boolean saveInMatlabFormat, boolean useMaskBit) {
        Forecast referenceForecast = new Forecast(referenceForecastPath,
                useMaskBit);
        float[] originalReferenceValues = referenceForecast.values();
        boolean[] forecastOverlapFilter =
                new boolean[originalReferenceValues.length];
        for (int i = 0; i < forecastOverlapFilter.length; i++) {
            forecastOverlapFilter[i] = true;
        }

        // If we want to honor the forecast masking bit, we will calculate the
        // spatially overlapping section
        if (useMaskBit) {
            forecastOverlapFilter = Utility.determineForecastOverlapFilter(
                    forecastOverlapFilter, referenceForecast.values());


            for (int i = 0; i < forecastsToCompare.length; i++) {
                Forecast forecastToCompare = new Forecast(forecastsToCompare[i],
                        useMaskBit);
                forecastOverlapFilter = Utility.determineForecastOverlapFilter(
                        forecastOverlapFilter, forecastToCompare.values());
            }
        }

        referenceForecast = new Forecast(referenceForecastPath,
                forecastOverlapFilter);
        // Bin the target eqk catalog into the forecast grid
        short[] targetEqksMap = referenceForecast.binnedCatalog(
                targetEqkCatalog);
        short N = ArrayUtil.sum(targetEqksMap); // total number of target eqks

        String[] forecastsToCompareNames = new String[forecastsToCompare.length];

        // We'll need room for a trajectory for every forecast in 
        // forecastsToCompare, as well as one for the reference forecast
        // relative to itself, and each trajectory will contain N + 1 elements
        float[][] molchanTrajectories = new float[forecastsToCompare.length + 1][N + 1];
        float[][] assTrajectories = new float[forecastsToCompare.length + 1][100];

        // Compute the self-trajectory
        float[] referenceValues = referenceForecast.values();
        molchanTrajectories[molchanTrajectories.length - 1] =
                MolchanTools.molchanTrajectory(referenceValues, referenceValues,
                targetEqksMap);
        assTrajectories[assTrajectories.length - 1] =
                MolchanTools.assTrajectory(molchanTrajectories[molchanTrajectories.length - 1]);

        // Compute the trajectories for all other forecasts relative to the
        // reference trajectory
        for (int i = 0; i < forecastsToCompare.length; i++) {
            Forecast forecastToCompare = new Forecast(forecastsToCompare[i],
                    forecastOverlapFilter);
            forecastsToCompareNames[i] = forecastToCompare.modelName();
            molchanTrajectories[i] = MolchanTools.molchanTrajectory(
                    forecastToCompare.values(), referenceValues, targetEqksMap);
            assTrajectories[i] = MolchanTools.assTrajectory(
                    molchanTrajectories[i]);
        }

        // Compute the confidence bounds for the specified target eqk
        // distribution and reference model gridding
        float[][] bounds = MolchanTools.confidenceBoundsMolchanAndASS(
                targetEqksMap, referenceValues, alpha, seed);

        Calendar startTime = Calendar.getInstance();
        SimpleDateFormat df = new SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'");
        String creationTime = df.format(startTime.getTime());

        // Write out the trajectories to the results file
        try {
            FileOutputStream oOutFIS = new FileOutputStream(resultsMLFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(
                    oOutBIS));

            oWriter.write("<?xml version=\"1.0\" encoding=\"utf-8\"?>\n");
            oWriter.write("<CSEPResult xmlns=\"http://www.scec.org/xml-ns"
                    + "/csep/0.1\">\n");
            oWriter.write("   <resultData publicID=\"smi://org.scec/csep/"
                    + "results/1\">\n");
            oWriter.write("      <MolchanASSTest publicID=\"smi://org.scec/"
                    + "csep/tests/molchanasstest/1\">\n");
            oWriter.write("         <creationInfo creationTime=\""
                    + creationTime + "\" />\n");
            oWriter.write("         <seed value=\"" + seed + "\" />\n");

            oWriter.write("         <name>Molchan-ASS-Test_"
                    + referenceForecast.modelName() + "</name>\n");

            oWriter.write("         <molchanNu>");
            for (int i = N; i >= 0; i--) {
                oWriter.write((float) i / (float) N + " ");
            }
            oWriter.write("         </molchanNu>\n");

            oWriter.write("         <molchanTrajectories>");
            // Write out the trajectories for each forecast we're comparing
            for (int i = 0; i < forecastsToCompare.length; i++) {
                oWriter.write("            <molchanTrajectory forecast=\""
                        + forecastsToCompareNames[i] + "\">");
                for (int j = 0; j < molchanTrajectories[i].length; j++) {
                    oWriter.write(molchanTrajectories[i][j] + " ");
                }
                oWriter.write("            </molchanTrajectory>\n");
            }
            // Write the self-trajectory
            oWriter.write("            <molchanTrajectory forecast=\""
                    + referenceForecast.modelName() + "\">");
            for (int i = 0;
                    i < molchanTrajectories[molchanTrajectories.length - 1].length;
                    i++) {
                oWriter.write(
                        molchanTrajectories[molchanTrajectories.length - 1][i]
                        + " ");
            }
            oWriter.write("            </molchanTrajectory>\n");
            oWriter.write("         </molchanTrajectories>\n");

            oWriter.write("         <molchanLowerConfidence>");
            for (int i = 0; i <= N; i++) {
                oWriter.write(bounds[i][0] + " ");
            }
            oWriter.write("         </molchanLowerConfidence>\n");

            oWriter.write("         <molchanUpperConfidence>");
            for (int i = 0; i <= N; i++) {
                oWriter.write(bounds[i][1] + " ");
            }
            oWriter.write("         </molchanUpperConfidence>\n");

            oWriter.write("         <assTau>");
            for (int i = 1; i < 101; i++) {
                oWriter.write((float) i * 0.01f + " ");
            }
            oWriter.write("         </assTau>\n");

            oWriter.write("         <assTrajectories>");
            // Write out the trajectories for each forecast we're comparing
            for (int i = 0; i < forecastsToCompare.length; i++) {
                oWriter.write("            <assTrajectory forecast=\""
                        + forecastsToCompareNames[i] + "\">");
                for (int j = 0; j < assTrajectories[i].length; j++) {
                    oWriter.write(assTrajectories[i][j] + " ");
                }
                oWriter.write("            </assTrajectory>\n");
            }
            // Write the self-trajectory
            oWriter.write("            <assTrajectory forecast=\""
                    + referenceForecast.modelName() + "\">");
            for (int i = 0;
                    i < assTrajectories[assTrajectories.length - 1].length;
                    i++) {
                oWriter.write(assTrajectories[assTrajectories.length - 1][i]
                        + " ");
            }
            oWriter.write("            </assTrajectory>\n");
            oWriter.write("         </assTrajectories>\n");

            oWriter.write("         <assLowerConfidence>");
            for (int i = N + 1; i < N + 101; i++) {
                oWriter.write(bounds[i][0] + " ");
            }
            oWriter.write("         </assLowerConfidence>\n");

            oWriter.write("         <assUpperConfidence>");
            for (int i = N + 1; i < N + 101; i++) {
                oWriter.write(bounds[i][1] + " ");
            }
            oWriter.write("         </assUpperConfidence>\n");

            oWriter.write("      </MolchanASSTest>\n");
            oWriter.write("   </resultData>\n");
            oWriter.write("</CSEPResult>\n");

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

            if (saveInMatlabFormat) {
                String matlabFile = resultsMLFile.replace(".xml", ".m");
                matlabFile = matlabFile.replace("-", "_");
                oOutFIS = new FileOutputStream(matlabFile);
                oOutBIS = new BufferedOutputStream(oOutFIS);
                oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

                // Generate Matlab script to plot Molchan trajectories and
                // confidence bounds
                oWriter.write("close all;\n");
                oWriter.write("nu = [1:-1/" + N + ":0];\n");
                oWriter.write("figure;\n");
                oWriter.write("hold on;\n");
                oWriter.write("axis([0 1 0 1]);\n");
                oWriter.write("daspect([1 1 1]);\n");
                oWriter.write("xlabel('Fraction of space-time occupied by " +
                        "alarm (\\tau)');\n");
                oWriter.write("ylabel('Miss rate (\\nu)');\n");

                for (int i = 0; i < molchanTrajectories.length; i++) {
                    oWriter.write("tau = [");
                    for (int j = 0; j < molchanTrajectories[i].length; j++) {
                        oWriter.write(molchanTrajectories[i][j] + ";");
                    }
                    oWriter.write("];\n");
                    oWriter.write("plot(tau, nu, 'ok', 'MarkerFaceColor', " +
                            "'black');\n");
                }

                oWriter.write("legend(");
                for (int i = 0; i < forecastsToCompare.length; i++) {
                    oWriter.write("'" + forecastsToCompareNames[i].replace(
                            "_", ".") + "', ");
                }
                oWriter.write("'" + referenceForecast.modelName().replace(
                        "_", ".") + "');\n");

                oWriter.write("lowerMolchanBounds = [");
                for (int i = 0; i <= N; i++) {
                    oWriter.write(bounds[i][0] + ";");
                }
                oWriter.write("];\n");

                oWriter.write("upperMolchanBounds = [");
                for (int i = 0; i <= N; i++) {
                    oWriter.write(bounds[i][1] + ";");
                }
                oWriter.write("];\n");

                oWriter.write("hold on;\n");
                oWriter.write("plot(lowerMolchanBounds, nu, '--k');\n");
                oWriter.write("plot(upperMolchanBounds, nu, '--k');\n");

                // Generate Matlab script to plot ASS trajectories and
                // confidence bounds
                oWriter.write("figure;\n");
                oWriter.write("hold on;\n");
                oWriter.write("tau = [0.01:0.01:1];\n");
                oWriter.write("axis([0 1 0 1]);\n");
                oWriter.write("daspect([1 2 1]);\n");
                oWriter.write("xlabel('Fraction of space-time occupied by " +
                        "alarm (\\tau)');\n");
                oWriter.write("ylabel('Area skill score');\n");

                for (int i = 0; i < assTrajectories.length; i++) {
                    oWriter.write("ass = [");
                    for (int j = 0; j < assTrajectories[i].length; j++) {
                        oWriter.write(assTrajectories[i][j] + ";");
                    }
                    oWriter.write("];\n");
                    oWriter.write("plot(tau, ass, '.');\n");
                }

                oWriter.write("legend(");
                for (int i = 0; i < forecastsToCompare.length; i++) {
                    oWriter.write("'" + forecastsToCompareNames[i].replace
                            ("_", ".") + "', ");
                }
                oWriter.write("'" + referenceForecast.modelName().replace
                        ("_", ".") + "');\n");

                oWriter.write("lowerASSBounds = [");
                for (int i = N + 1; i < N + 101; i++) {
                    oWriter.write(bounds[i][0] + ";");
                }
                oWriter.write("];\n");

                oWriter.write("upperASSBounds = [");
                for (int i = N + 1; i < N + 101; i++) {
                    oWriter.write(bounds[i][1] + ";");
                }
                oWriter.write("];\n");

                oWriter.write("hold on;\n");
                oWriter.write("plot(tau, lowerASSBounds, '--k');\n");
                oWriter.write("plot(tau, upperASSBounds, '--k');\n");

                oWriter.close();
                oOutBIS.close();
                oOutFIS.close();
            }
        } catch (Exception ex) {
            System.out.println("Error in MolchanTools.molchan()");
            ex.printStackTrace();
            System.exit(-1);
        }
    }
}
