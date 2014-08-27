package org.corssa.predictiontesting;

import java.util.Arrays;

public class MathUtil {

    public MathUtil() {
    }

    /**
     * erf approximated by Maclaurin series as listed at http://mathworld.wolfram.com/Erf.html 50 steps is chosen arbitrarily for now, this could be optimized later
     *
     * @param z value at which we want to evaluate erf
     * @return erf(z)
     */
    public static double erf1(double z) {
        if (Math.abs(z) > 3.86) {
            // if z > 2.86 erf(z) is, for all intents and purposes, unity
            // if z < -2.86 erf(z) is, for all intents and purposes, -unity
            return Math.signum(z);

        } else if (z == 0) {
            return 0;
        }
        double sum = 0;

        for (int i = 0; i < 50; i++) {
            //double nFactorial = MathUtil.factorial(i);
            double newTermNumerator = Math.pow(-1.0, i) * Math.pow(z, (2 * i + 1));
            double newTerm = newTermNumerator / (2 * i + 1);

            for (int j = 2; j <= i; j++) {
                newTerm /= j;
            }
            //System.out.println("newTerm=" + newTerm);
            sum += newTerm;
        //sum += (Math.pow( -1.0, i) * Math.pow(z, (2 * i + 1))) / (nFactorial * (2 * i + 1));
        }

        sum *= 2.0 / Math.sqrt(Math.PI);

        //System.out.println("erf(" + z + ")=" + sum);
        return sum;
    }

    /**
     * erf approximated by Horner's method (fractional error in math formula less than 1.2 * 10 ^ -7).  Although subject to catastrophic cancellation when z in very close to 0
     * from http://www.cs.princeton.edu/introcs/home/
     *
     * @param z value at which we want to evaluate erf
     * @return erf(z)
     */
    public static double erf(double z) {
        if (Math.abs(z) > 3.86) {
            // if z > 3.86 erf(z) is, for all intents and purposes, unity
            // if z < -3.86 erf(z) is, for all intents and purposes, -unity
            return Math.signum(z);

        } else if (z == 0) {
            return 0;
        }
        double t = 1.0 / (1.0 + 0.5 * Math.abs(z));

        // use Horner's method
        double ans = 1 - t * Math.exp(-z * z - 1.26551223 +
                t * (1.00002368 +
                t * (0.37409196 +
                t * (0.09678418 +
                t * (-0.18628806 +
                t * (0.27886807 +
                t * (-1.13520398 +
                t * (1.48851587 +
                t * (-0.82215223 +
                t * (0.17087277))))))))));
        if (z >= 0) {
            return ans;
        } else {
            return -ans;
        }
    }

    /**
     * erf approximated fractional error less than x.xx * 10 ^ -4, found somewhere on the web that I've since lost
     * 
     * @param z value at which we want to evaluate erf
     * @return erf(z)
     */
    public static double erf2(double z) {
        double t = 1.0 / (1.0 + 0.47047 * Math.abs(z));
        double poly = t * (0.3480242 + t * (-0.0958798 + t * (0.7478556)));
        double ans = 1.0 - poly * Math.exp(-z * z);
        if (z >= 0) {
            return ans;
        } else {
            return -ans;
        }
    }

    /**
     * Compute the Poisson probability of observing some number of occurrences of an event happening given that we expect a specified number of events.
     *
     * @param numberOfOccurrences number of occurrences observed
     * @param expectedNumberOfOccurrences the expected number of occurrences
     * @return the Poisson probability of observing the specified number given the expected number
     */
    private static double poissonProbability(int numberOfOccurrences, double expectedNumberOfOccurrences) {
        int x = numberOfOccurrences;
        double mu = expectedNumberOfOccurrences;
        if (x == 0) {
            return Math.exp(-mu);
        } else {
            return (mu / (double) x * MathUtil.poissonProbability(x - 1, mu));
        }
    }

    /**
     * Compute the Poisson cumulative probability of observing some number of occurrences of an event happening given that we expect a specified number of events.
     *
     * @param numberOfOccurrences number of occurrences observed
     * @param expectedNumberOfOccurrences the expected number of occurrences
     * @return the probability of obtaining at most the specified number of successes given the expected number of successes
     */
    public static double poissonProbabilityCumulative(int numberOfOccurrences, double expectedNumberOfOccurrences) {
        double prob = 0;
        double mu = expectedNumberOfOccurrences;
        for (int i = 0; i <= numberOfOccurrences; i++) {
            prob += MathUtil.poissonProbability(i, mu);
        }
        return prob;
    }

    /**
     * Compute the binomial probability that, given a specified number of trials each having the same specified probability of success, we obtain a specified number of successes
     *
     *
     * @param numberOfSuccesses number of observed successes
     * @param numberOfTrials number of trials
     * @param binomialProbabilityOfSuccess each trial's probability of success
     * @return the probability of obtaining the specified number of successes in the specified number of trials given the specified probability of success and assuming the trials
     *  are binomial
     */
    private static double binomialProbability(int numberOfSuccesses, int numberOfTrials, double probabilityOfSuccess) {
        double prob = 0.0;
        int m = numberOfSuccesses;
        int n = numberOfTrials;
        double p = probabilityOfSuccess;

        prob = Math.pow(p, m) * Math.pow(1 - p, n - m) * MathUtil.choose(n, m);
        return prob;
    }

    /**
     * Compute the number of ways that x objects can be chosen from n objects
     *
     * @param n the total number of objects available
     * @param x the number of objects each subset should contain
     * @return the number of unique subsets that can be formed by choosing x objects out of n
     */
    private static double choose(int n, int x) {
        if (x == 1) {
            return n;
        } else if (x == 0) {
            return 1.0;
        } else {
//            double choose = (double)MathUtil.factorial(n) /
//                    (double) MathUtil.factorial(n-x) /
//                    (double) MathUtil.factorial(x);
            return ((double) (n - x + 1) / (double) (x) * MathUtil.choose(n, (x - 1)));
//            return choose;
        }
    }

    /**
     * For the specified binomial distribution (some number of trials each w/ some probability of success), compute the cumulative probability of observing at least the 
     * specified number of successes
     *
     * @param numberOfTrials number of binomial trials in experiment
     * @param binomialProbabilityOfSuccess probability of success for each trial in the experiment
     * @param numberOfSuccesses minimum number of successes in which we're interested
     * @return probability of obtaining at least the specified number of successes
     */
    public static double binomialComplementaryCDFValue(int numberOfSuccesses, int numberOfTrials, double probabilityOfSuccess) {
        double cdfValue = 0.0;

        // we're after the cdf; we can get this by summing the individual probabilities of obtaining (x to N) successes, or, by summing the probabilities of obtaining (0 to x-1) 
        // successes and subtracting this sum from unity.  We'll use the latter approach if the number of successes  is less than 1/2 of N.
        if ((double) numberOfSuccesses > (double) numberOfTrials * 0.5) {
            for (int i = numberOfSuccesses; i <= numberOfTrials; i++) {
                cdfValue += MathUtil.binomialProbability(i, numberOfTrials, probabilityOfSuccess);
            }
        } else {
            cdfValue = 1.0;
            for (int i = 0; i < numberOfSuccesses; i++) {
                cdfValue -= MathUtil.binomialProbability(i, numberOfTrials, probabilityOfSuccess);
            }
        }
        return cdfValue;
    }

    /**
     * Compute the value of the cumulative Gaussian distribution up to the specified value.  The math is based on wikipedia/Normal_distribution and 
     * mathworld/NormalDistribution.html
     *
     * @param mean mean of the Gaussian
     * @param std standard deviation of the Gaussian
     * @param x value at which to compute the CDF
     * @return CDF value of the specified Gaussian at the specified point
     */
    public static double gaussianCDFValue(double x, double mean, double std) {
        double cdfValue = 0.0;
        cdfValue = 0.5 * (1 + MathUtil.erf((x - mean) / (std * Math.sqrt(2.0))));
//        System.out.println("(x,mean,std,cdf)=("+ x + "," + mean + "," + std + "," + cdfValue + ")");
        return cdfValue;
    }

    /**
     * Find the two-sided alpha confidence bounds from the given array of data.  In other words, sort the array and find the array values that correspond to the alpha and 
     * (1-alpha) percentiles
     *
     * @param array unsorted doubles
     * @param alpha one-sided confidence levels
     * @return array containing two elements: the values corresponding to the alpha and (1-alpha) percentiles, respectively
     */
    public static float[] confidenceBounds(float[] array, float alpha) {
        // given the array, find the lower and upper confidence bounds corresponding to alpha and 1-alpha
        float lowerBound = 1.0f;
        float upperBound = 0.0f;

        // sort the array in ascending order
        Arrays.sort(array);

        int lowerPoint = (int) Math.floor(array.length * alpha) - 1;
        int upperPoint = (int) Math.floor(array.length * (1.0 - alpha)) - 1;
        lowerBound = array[lowerPoint];
        upperBound = array[upperPoint];
        float[] bounds = new float[2];
        bounds[0] = lowerBound;
        bounds[1] = upperBound;

        return bounds;
    }
    
    /**
     * Find the two-sided alpha confidence bounds from the given array of data.  In other words, sort the array and find the array values that correspond to the alpha and 
     * (1-alpha) percentiles
     *
     * @param array unsorted doubles
     * @param alpha one-sided confidence levels
     * @return array containing two elements: the values corresponding to the alpha and (1-alpha) percentiles, respectively
     */
    public static int[] confidenceBounds(int[] array, float alpha) {
        // given the array, find the lower and upper confidence bounds corresponding to alpha and 1-alpha
        int lowerBound = 1;
        int upperBound = 0;

        // sort the array in ascending order
        Arrays.sort(array);

        int lowerPoint = (int) Math.floor(array.length * alpha) - 1;
        int upperPoint = (int) Math.floor(array.length * (1.0 - alpha)) - 1;
        lowerBound = array[lowerPoint];
        upperBound = array[upperPoint];
        int [] bounds = new int[2];
        bounds[0] = lowerBound;
        bounds[1] = upperBound;

        return bounds;
    }

    /**
     * Find the one-sided alpha confidence bounds from the given array of data.  In other words, sort the array and find the array values that correspond to the alpha and 
     * (1-alpha) percentiles
     *
     * @param array unsorted doubles
     * @param alpha one-sided confidence levels
     * @return the value corresponding to the alpha percentile
     */
    public static float confidenceBound(float[] array, float alpha) {
        // given the array, find the confidence bound corresponding to alpha
        float lowerBound = Float.MAX_VALUE;

        // sort the array in ascending order
        Arrays.sort(array);

        int lowerPoint = Math.max((int) Math.floor(array.length * alpha) - 1, 0);
        lowerBound = array[lowerPoint];

        return lowerBound;
    }
    
    /**
     * Find the one-sided alpha confidence bounds from the given array of data.  In other words, sort the array and find the array values that correspond to the alpha and 
     * (1-alpha) percentiles
     *
     * @param array unsorted integers
     * @param alpha one-sided confidence levels
     * @return the value corresponding to the alpha percentile
     */
    public static Object confidenceBound(Object[] array, float alpha) {
//        float lowerBound = Float.MAX_VALUE;

        // sort the array in ascending order
        Arrays.sort(array);

        int lowerPoint = Math.max((int) Math.floor(array.length * alpha) - 1, 0);
        Object lowerBound = array[lowerPoint];

        return lowerBound;
    }

    /**
     * compute the sample standard deviation, based on http://mathworld.wolfram.com/StandardDeviation.html
     *
     * @param array data of interest
     * @return sample standard deviation of data
     */
    public static float standardDeviation(float[] array) {
        float sum = 0.0f;
        float mean = ArrayUtil.average(array);
        float n = (float) array.length;

        for (int i = 0; i < array.length; i++) {
            sum += Math.pow(array[i] - mean, 2);
        }
        float std = (float) Math.sqrt(sum / (float) (n - 1));
        return std;
    }

    /**
     * Compute the skewness of the specified array of numbers using the formula from Excel's help section, namely:
     * skew=n/((n-1)(n-2))*sum_over_j(((x_j-mean)/std)^3)
     *
     * @param array data of interest
     * @return estimated skewness of data
     */
    public static float skewness(float[] array) {
        int n = array.length;
        double sum = 0.0;

        float mean = ArrayUtil.average(array);
        float stdev = MathUtil.standardDeviation(array);
        for (int counter = 0; counter < n; counter++) {
            sum += Math.pow((array[counter] - mean) / stdev, 3);
        }
        double multiplicationFactor = (double) n / (n - 1) / (n - 2);
        float skew = (float) (sum * multiplicationFactor);
        return skew;
    }

    /**
     * Compute the kurtosis of the specified array of numbers using the formula from Excel's help section, namely:
     * kurt=n(n+1)/((n-1)(n-2)(n-3))*sum_over_j(((x_j-mean)/std)^4)-3(n-1)^2/((n-2)(n-3)
     *
     * @param array data of interest
     * @return estimated kurtosis of data
     */
    public static float kurtosis(float[] array) {
        int n = array.length;
        double sum = 0.0f;

        float mean = ArrayUtil.average(array);
        float stdev = MathUtil.standardDeviation(array);
        for (int counter = 0; counter < n; counter++) {
            sum += Math.pow((array[counter] - mean) / stdev, 4);
        }
        // I broke down the computation into pieces below in order to ensure accurracy of the computation for large values of n
        //System.out.println("sum=" + sum);
        double multiplicativeFactor = (double) n * (n + 1) / (n - 1) / (n - 2) / (n - 3);
        //System.out.println("multiplicativeFactor=" + multiplicativeFactor);
        double kurtWithoutSubtraction = multiplicativeFactor * sum;
        //System.out.println("kurtWithoutSubtraction=" + kurtWithoutSubtraction);
        double subtractionFactor = (double) 3.0 * (n - 1) * (n - 1) / (n - 2) / (n - 3);
        //System.out.println("subtractionFactor=" + subtractionFactor);
        float kurt = (float) (kurtWithoutSubtraction - subtractionFactor);
        return kurt;
    }

    /**
     * Print histogram data for a given data set and given histogram bins.
     *
     * @param data input data set to be binned
     * @param minBin start value of the lowest histogram bin
     * @param maxBin start value of the highest histogram bin
     * @param binSize size of each histogram bin
     */
    public static void printHistogram(float[] data, float minBin, float maxBin, float binSize) {
        // create an array that contains all histogram bins and one additional
        // bin that will contain any data not falling w/i the specified bins
        int numberOfHistogramBins = Math.round((maxBin - minBin) / binSize) + 1;
        int[] histogram = new int[numberOfHistogramBins];

        // Translate the bin endpoints into integral values
        int minBin_translated = (int) (minBin / binSize);
        int maxBin_translated = (int) (maxBin / binSize);

        int numberOfDataPoints = data.length;
        for (int counter = 0; counter < numberOfDataPoints; counter++) {
            // translate the data into an integral value
            int data_translated = (int) Math.floor(data[counter] / binSize);
            // check to make sure this event is in the study region
            if (data_translated >= minBin_translated && data_translated < maxBin_translated) {
                // translate the data into the bin-specific reference frame
                int dataPosition = data_translated - minBin_translated;
                // increment the number of data points in the corresponding histogram bin
                histogram[dataPosition]++;
            } else {
                // if we're in here, it's b/c the data point doesn't fit in the specified histogram bins, we'll add it to the end in the 'more' bin
                histogram[histogram.length - 1]++;
            }
        }

        // print out the histogram values and cumulative %
        System.out.println("bin\tfrequency\tcumulative %");
        int cumulativeFrequency = 0;
        for (int counter = 0; counter < histogram.length - 1; counter++) {
            float binStart = minBin + (float) (counter + 1) * binSize;
            cumulativeFrequency += histogram[counter];
            float cumulativePercentage = (float) cumulativeFrequency / (float) numberOfDataPoints;
            System.out.println(binStart + "\t" + histogram[counter] + "\t" + cumulativePercentage);
        }
        System.out.println("More\t" + histogram[histogram.length - 1] + "\t1");
    }

    /**
     * Return histogram data for a given data set and given histogram bins.
     *
     * @param data input data set to be binned
     * @param minBin start value of the lowest histogram bin
     * @param maxBin start value of the highest histogram bin
     * @param binSize size of each histogram bin
     * @return histogram in array w/ the following format:
     * [0] = histogram bin  [1] = frequency [2] = cumulative %
     */
    public static float[][] histogram(float[] data, float minBin, float maxBin, float binSize) {
        // create an array that contains all histogram bins and one additional bin that will contain any data not falling w/i the specified bins
        int numberOfHistogramBins = Math.round((maxBin - minBin) / binSize) + 1;
//        int [] histogram = new int[numberOfHistogramBins];
        float[][] results = new float[numberOfHistogramBins][3];

        // Set the histogram bin values
        for (int i = 0; i < results.length; i++) {
            results[i][0] = minBin + (float) i * binSize;
        }

        // Translate the bin endpoints into integral values
        int minBin_translated = (int) (minBin / binSize);
        int maxBin_translated = (int) (maxBin / binSize);

        int numberOfDataPoints = data.length;
        for (int i = 0; i < numberOfDataPoints; i++) {
            // translate the data into an integral value
            if (data[i] == 13) {
//                System.out.println("got a 13");
            }
            int data_translated = (int) Math.floor(data[i] / binSize);
            // check to make sure this event is in the study region
            if (data_translated >= minBin_translated && data_translated < maxBin_translated) {
                // translate the data into the bin-specific reference fram
                int dataPosition = data_translated - minBin_translated;
                // increment the number of data points in the corresponding histogram bin
//                histogram[dataPosition]++;
                results[dataPosition][1] += 1.0f;
//                if (dataPosition == 14){
//                    System.out.println("got 13");
//                }
            } else {
                // if we're in here, it's b/c the data point doesn't fit in the specified histogram bins, we'll add it to the end in the 'more' bin
//                histogram[histogram.length - 1]++;
                results[results.length - 1][1] += 1.0f;
            }
        }

        // set the cumulative % values
        results[0][2] = results[0][1] / (float) numberOfDataPoints;
        for (int i = 1; i < results.length; i++) {
            results[i][2] = results[i - 1][2] + results[i][1] / (float) numberOfDataPoints;
        }

        return results;
    }

    /**
     * Return histogram data for a given data set and given histogram bins.
     *
     * @param data input data set to be binned
     * @param minBin start value of the lowest histogram bin
     * @param maxBin start value of the highest histogram bin
     * @param binSize size of each histogram bin
     * @return histogram in array w/ the following format:
     * [0] = frequency for given bin
     */
    public static int[] histogramFrequencyOnly(float[] data, double minBin, double maxBin, double binSize) {
        // create an array that contains all histogram bins and one additional bin that will contain any data not falling w/i the specified bins
        int numberOfHistogramBins = (int) Math.round((maxBin - minBin) / binSize) + 1;
//        int [] histogram = new int[numberOfHistogramBins];
        int[] results = new int[numberOfHistogramBins];

        // Translate the bin endpoints into integral values
        int minBin_translated = (int) (minBin / binSize);
        int maxBin_translated = (int) (maxBin / binSize);

        int numberOfDataPoints = data.length;
        for (int i = 0; i < numberOfDataPoints; i++) {
            // translate the data into an integral value

            int data_translated = (int) Math.floor(data[i] / binSize);
            // check to make sure this event is in the study region
            if (data_translated >= minBin_translated && data_translated < maxBin_translated) {
                // translate the data into the bin-specific reference fram
                int dataPosition = data_translated - minBin_translated;
                // increment the number of data points in the corresponding histogram bin
//                histogram[dataPosition]++;
                results[dataPosition]++;
            } else {
                // if we're in here, it's b/c the data point doesn't fit in the specified histogram bins, we'll add it to the end in the 'more' bin
//                histogram[histogram.length - 1]++;
                results[results.length - 1]++;
            }
        }

        return results;
    }

    /**
     * Compute the value at which the Gaussian cumulative distribution function with the given mean and standard deviation equals the specified alpha value
     *
     * @param mean the mean of the Gaussian under consideration
     * @param std the standard deviation of the Gaussian under consideration
     * @param alpha significance value in which we're interested
     * @return value at which the cumulative Gaussian is equal to alpha
     */
    public static float significanceValueFromGaussian(float mean, float std,
            float alpha) {
        float x = (float) (MathUtil.erfInverse(2 * alpha - 1) * Math.sqrt(2) * std + mean);
        return x;
    }

    /**
     * erfinverse approximated by series as listed at http://functions.wolfram.com/GammaBetaErf/InverseErf/ This seems to show excellent accuracy in the range abs(z)<0.8
     *
     * @param z value at which we want to evaluate erfinverse
     * @return erfinverse(z)
     */
    public static double erfInverse(double z) {
        if (z >= 1) {
            // if z>=1, erfInverse(z)=Infinity
            return Double.POSITIVE_INFINITY;
        } else if (z <= -1) {
            // if z<=-1, erfInverse(z)=Infinity
            return Double.NEGATIVE_INFINITY;
        }
        double sum = 0.0;
        double[] numerators = new double[10];
        numerators[0] = 1;
        numerators[1] = 1;
        numerators[2] = 7;
        numerators[3] = 127;
        numerators[4] = 4369;
        numerators[5] = 34807;
        numerators[6] = 20036983;
        numerators[7] = 2280356863L;
        numerators[8] = 49020204823L;
        numerators[9] = 65967241200001L;

        double[] denominators = new double[10];
        denominators[0] = 1;
        denominators[1] = 12;
        denominators[2] = 480;
        denominators[3] = 40320;
        denominators[4] = 5806080;
        denominators[5] = 182476800;
        denominators[6] = 398529331200L;
        denominators[7] = 167382319104000L;
        denominators[8] = 13007997370368000L;
        denominators[9] = 62282291409321984L * 1000L;

        for (int i = 0; i < numerators.length; i++) {
            sum += Math.pow(Math.PI, i) * Math.pow(z, 2 * i + 1) * numerators[i] / denominators[i];
        }
        sum *= 0.5 * Math.sqrt(Math.PI);

        return sum;
    }

    /**
     * Compute the correlation coefficient of two arrays
     *
     * @param x array of interest
     * @param y array of interest
     * @return correlation coefficient of x and y, b/w -1 and 1
     */
    public static float correlationCoefficient(float[] x, float[] y) {
        // correl'n coefficient is equal to Cov(x, y)/(sigma_x * sigma_y)
        float cov = MathUtil.covariance(x, y);
        float sigma_x = MathUtil.standardDeviation(x);
        float sigma_y = MathUtil.standardDeviation(y);
        float correl = cov / (sigma_x * sigma_y);
        //System.out.println("correl=" + correl);
        return correl;
    }

    /**
     * Compute the covariance of two arrays
     *
     * @param x array of interest
     * @param y array of interest
     * @return covariance of x and y
     */
    public static float covariance(float[] x, float[] y) {
        // cov(x,y) = 1/n * sum from j = 1 to n((x_j - mu_x)(y_j - mu_y)) where mu_i is the average of the i array
        float n = x.length;
        float mu_x = ArrayUtil.average(x);
        float mu_y = ArrayUtil.average(y);

        float sum = 0.0f;
        for (int j = 0; j < n; j++) {
            sum += (x[j] - mu_x) * (y[j] - mu_y);
        }
        float cov = sum / n;
//        System.out.println("cov=" + cov);
        return cov;
    }

    /**
     * Use least squares regression to determine the best fit line b/w the specified data arrays.  We do this by solving for the slope and intercept of the line that minimizes the 
     * misfit b/w the line described by a+bx and the observed data set y.  The misfit can be written in terms of the  intercept (a) and the slope (b) as
     *          R^2(a,b) = sum(i=1 to n)((y_i - (a + bx_i))^2).
     * We then set the partial derivatives w/r/t a and b equal to zero and solve; here, we've implemented the sol'n following the notes at 
     * http://mathworld.wolfram.com/LeastSquaresFitting.html
     *
     * @param xy 2-D array of observations
     * @return array containing 
     *      [0] = slope of best fit line 
     *      [1] = intercept of best fit line 
     *      [2] = correlation coefficient 
     *      [3] = standard error for slope
     *      [4] standard error for intercept
     */
    public static float[] leastSquaresRegression(float[][] xy) {
        int n = xy.length;
        float[] x = new float[n];
        float[] y = new float[n];

        for (int i = 0; i < n; i++) {
            x[i] = xy[i][0];
            y[i] = xy[i][1];
        }

        float averageX = ArrayUtil.average(x);
        float averageY = ArrayUtil.average(y);
        float sumOfSquaresOfXs = 0.0f;
        float sumOfProductsOfXAndY = 0.0f;
        float sumOfSquaresOfYs = 0.0f;

        for (int i = 0; i < n; i++) {
            sumOfSquaresOfXs += x[i] * x[i];
            sumOfProductsOfXAndY += x[i] * y[i];
            sumOfSquaresOfYs += y[i] * y[i];
        }

        float ss_xx = sumOfSquaresOfXs - n * averageX * averageX;
        float ss_yy = sumOfSquaresOfYs - n * averageY * averageY;
        float ss_xy = sumOfProductsOfXAndY - n * averageX * averageY;

        float b = ss_xy / ss_xx;
        float a = averageY - b * averageX;
        float r = MathUtil.correlationCoefficient(x, y);
        float rSquared = r * r;

        double nDouble = (double) n;
        double s = Math.sqrt((ss_yy - b * ss_xy) / (nDouble - 2));
        float se_a = (float) (s * Math.sqrt((1 / nDouble) + averageX * averageX / ss_xx));
        float se_b = (float) (s / Math.sqrt(ss_xx));

        float[] results = new float[5];
        results[0] = b; // slope
        results[1] = a; // intercept
        results[2] = rSquared; // misfit
        results[3] = se_b; // standard error for slope
        results[4] = se_a; // standard error for intercept
//        System.out.print("(slope, int, corr, se_slope, se_int)=(" + results[0] + ", " + results[1] + ", " + results[2] +  ", " + results[3] + ", " + results[4] + ")");
        return results;
    }

    /**
     * Compute the percentile of the given value relative to the given sample of values.  To do this, sort the sample values and count the number of sample values that are less 
     * than the value of interest.
     *
     * @param value value for which we want to compute the percentile
     * @param sample array of sample values to which we'll compare "value"
     * @return percentile score, the percentage of sample values that are less than the value of interest
     */
    public static float percentile(float value, float[] sample) {
        int numberOfSamples = sample.length;
        float[] sampleCopy = new float[numberOfSamples];
        System.arraycopy(sample, 0, sampleCopy, 0, numberOfSamples);
        Arrays.sort(sampleCopy);
//        System.out.println("sample = " + Arrays.toString(sample));
//        System.out.println("value = " + value);
        for (int i = 0; i < numberOfSamples; i++) {
            if (value <= sampleCopy[i]) {
                return (float) (i) / (float) numberOfSamples;
            }
        }
        return 1.0f;
    }

    /**
     * Compute the inverse cumulative Poisson distribution for the specified probability and expectation.  In other words, what is the minimum number of successes that yields 
     * a Poissonian CDF value greater than or equal to the specified probability.  To do this, I loop over integer values and compute the CDF for each value; the first number 
     * that yields a CDF greater than the specified probability is returned.  This is equivalent to the Matlab poissinv function
     *
     * @param probability probability in which we're interested
     * @param expectation parameter of the Poisson distribution
     * @return minimum positive integer for which the Poisson CDF w/ the specified parameter is greater than or equal to the specified probability value
     */
    public static int inverseCumulativePoisson(double probability, double expectation) {
        double cdf = 0;
        // compute the CDF incrementally
        for (int i = 0; i < Integer.MAX_VALUE; i++) {
            cdf += MathUtil.poissonProbability(i, expectation);
            if (cdf >= probability) {
                return i;
            }
        }
        return Integer.MAX_VALUE;
    }

    /**
     * The binomial probability distribution gives the probability of observing (n-m) successes out of n binomial trials, given independent trials each with a given success 
     * probability (we'll call it tau).  Here, we perform a linear search in order to solve for the success probability given n-m (numberOfSuccesses), n (numberOfTrials), and the
     * cumulative binomial probability (probability).  Recall that the binomial probability distribution looks like this:
     *          p = n! / (m! * (n - m)!) * tau ^ m * (1 - tau) ^ (n - m)
     * To solve for tau, we take 3 passes of increasing resolution.  In the first pass, we start at tau = 0 and compute the corresponding complementary binomial CDF (that is, 
     * what is the probability that we have achieved numberOfSuccesses or more hits with a success probability of 0).  We then compute the residual: the absolute difference 
     * b/w the CDF value we just computed and the cdf value of interest.  As we increase in tau, this residual will continue to shrink until we've passed the correct value of tau.  
     * Therefore, we can break out of the loop once we see an increase in the residual.  We then repeat this process for the new range we obtained from the first pass and at 
     * higher resolution.  We do another final iteration to increase resolution.
     *
     * @param numberOfTrials number of binomial trials to simulate
     * @param numberOfSuccesses number of binomial successes to simulate
     * @param probability value of the binomial CDF in which we're interested
     * @return the probability of success which yields the given cumulative probability value of interest with the specified number of trials and successes
     */
    public static double binomialProbabilityOfSuccess(int numberOfTrials,
            int numberOfSuccesses, double probability) {
        if (numberOfSuccesses == 0) {
            return 0.0;
        }
        double bigStep = 0.01;
        double mediumStep = 0.0001;
        double smallStep = 0.000001;
        double tauMinEstimate = 0.0;
        double tauMaxEstimate = 1.0;

        // start w/ the assumption that the answer is 0, in which case the absolute value of the residual is just the probability.  We multiply and round the residuals by 1e7 in order 
        //        to avoid incorrect inequalities due to very small differences
        int residual = Math.round((float) (probability * 1e7));


        int numberOfBigSteps = (int) (1.0 / bigStep);
        // take a first pass and get a rough estimate at tau
        for (int i = 0; i <= numberOfBigSteps; i++) {
            double tau = i * bigStep;
            int newResidual = Math.round((float) (Math.abs(MathUtil.binomialComplementaryCDFValue(numberOfSuccesses, numberOfTrials, tau) - probability) * 1e7));
            if (newResidual <= residual) {
                tauMinEstimate = tau;
                residual = newResidual;
            //System.out.println("tauMinEstimate=" + tauMinEstimate +", res=" + residual);
            } else {
                tauMaxEstimate = tau;
                break;
            }
        }

        // widen the search a little bit to be conservative, but make sure we don't search over tau < 0 or tau > 1
        tauMinEstimate -= bigStep;
        if (tauMinEstimate < 0) {
            tauMinEstimate = 0;
        }

        tauMaxEstimate += bigStep;
        if (tauMaxEstimate > 1) {
            tauMaxEstimate = 1;
        }

        // set the residual to the current min estimate of tau
        residual = Math.round((float) (Math.abs(
                MathUtil.binomialComplementaryCDFValue(numberOfSuccesses, numberOfTrials, tauMinEstimate) - probability) * 1e7));

        double firstTauMin = tauMinEstimate;
        //System.out.println("After first pass, (min, max) = (" + tauMinEstimate + ", " + tauMaxEstimate + ") and res = " + residual);

        int numberOfMediumSteps = (int) ((tauMaxEstimate - tauMinEstimate) / mediumStep);
//        residual = 1.0;

        // take a second pass for better resolution
        for (int i = 0; i <= numberOfMediumSteps; i++) {
            double tau = firstTauMin + i * mediumStep;
            int newResidual = Math.round((float) (Math.abs(MathUtil.binomialComplementaryCDFValue(numberOfSuccesses, numberOfTrials, tau) - probability) * 1e7));
            if (newResidual <= residual) {
                tauMinEstimate = tau;
                residual = newResidual;
            } else {
                tauMaxEstimate = tau;
                break;
            }
        }
        // widen the search a little bit to be conservative, but make sure we don't search over tau < 0 or tau > 1
        tauMinEstimate -= mediumStep;
        if (tauMinEstimate < 0) {
            tauMinEstimate = 0;
        }
        tauMaxEstimate += mediumStep;
        if (tauMaxEstimate > 1) {
            tauMaxEstimate = 1;
        }

        // set the residual to the current min estimate of tau
        residual = Math.round((float) (Math.abs(MathUtil.binomialComplementaryCDFValue(numberOfSuccesses, numberOfTrials, tauMinEstimate) - probability) * 1e7));
        double secondTauMin = tauMinEstimate;
//        System.out.println("After second pass, (min, max) = (" + tauMinEstimate + ", " + tauMaxEstimate + ") and res = " + residual);

        int numberOfSmallSteps = (int) ((tauMaxEstimate - tauMinEstimate) / smallStep);

        // take a third and final pass for best resolution
        for (int i = 0; i <= numberOfSmallSteps; i++) {
            double tau = secondTauMin + i * smallStep;
            int newResidual = Math.round((float) (Math.abs(MathUtil.binomialComplementaryCDFValue(numberOfSuccesses, numberOfTrials, tau) - probability) * 1e7));
            if (newResidual <= residual) {
                tauMinEstimate = tau;
                residual = newResidual;
            } else {
                tauMaxEstimate = tau;
                break;
            }
        }
        //System.out.println("After third pass, (min, max) = (" + tauMinEstimate + ", " + tauMaxEstimate + ") and res = " + residual);
        return tauMinEstimate;
    }

    /**
     * Compute the factorial of the specified number in the simplest fashion
     *
     * @param n the number for which we want to compute the factorial
     * @return n! = n * (n - 1) * (n - 2) * ... * 2
     */
    public static int factorial(int n) {
        if (n < 0 || n > 12) {
            // n < 0 is undefined and n > 12 causes overflow
            System.err.println("0 <= n <= 12");
            System.exit(-1);
        }
        int result = 1;
        for (int i = 2; i <= n; i++) {
            result *= i;
        }
        return result;
    }

    /**
     * Compute the best fit line using general orthogonal regression technique, as described by Castellaro et al 2006 GJI.
     *
     * @param x array of independent variable data
     * @param y array of dependent variable data
     * @param errorVarianceRatio ratio of measurement error variances
     * @return array containing estimate of
     * [0] = slope
     * [1] = intercept
     * for best-fit line using GOR
     */
    public static float[] bestFitLineGOR(float[] x, float[] y, float errorVarianceRatio) {
        float sx = MathUtil.standardDeviation(x);
        float sxSquared = sx * sx;
        float sy = MathUtil.standardDeviation(y);
        float sySquared = sy * sy;
        float eta = errorVarianceRatio;
        float sxy = MathUtil.covariance(x, y);
        float sxySquared = sxy * sxy;
        float beta = (sySquared - eta * sxSquared + (float) Math.sqrt(Math.pow(sySquared - eta * sxSquared, 2) + 4 * eta * sxySquared)) / (2 * sxy);
        float alpha = ArrayUtil.average(y) - beta * ArrayUtil.average(x);

        float[] bestFitParameters = new float[2];
        bestFitParameters[0] = beta;
        bestFitParameters[1] = alpha;

        return bestFitParameters;
    }

    /**
     * Determine the necessary number of decimal digits required to represent the given number x.  The number of decimal places required to represent x is found by 
     * determining the minimum value of y >= 0 that satisfies
     *      x % (10 ^ -y) == 0
     *
     * It is readily shown that
     *         x % 1 == 0 --> we need 0 decimal points
     *         x % .1 == 0 --> we need 1 decimal points
     *         x % .01 == 0 --> we need 2 decimal points
     * and so on.  Here, b/c of rounding errors, we check to see if the absolute value of the modulus result is smaller than some number close to zero or if the result, when 
     * subtracted from the modulator, is smaller than a number close to zero.  DUE TO ROUNDING ERRORS, THIS SHOULD ONLY BE USED WHEN TRYING TO DECIDE IF 
     * 0, 1, OR 2 DECIMAL PLACES ARE NEEDED
     *
     * @param x the number we wish to represent
     * @return the minimum number of decimal places required to represent x
     */
    public static int numberOfDecimalPointsRequired(float x) {
        // we're only concerned w/ abs value of x
        x = Math.abs(x);
        int decimalPlacesRequired = 0;

        // determine the number of decimal places required to represent x
        int i = 0;
        while (i <= 3) { // the smallest float is ~ 1.4E-45
            decimalPlacesRequired = i;
            float modulator = (float) (Math.pow(10, -i));
            // a number close to zero and many orders of magnitude smaller than the
            // modulator
            float epsilon = (float) (Math.pow(10, -(i + 5)));
            float remainder = Math.abs(x % modulator);
            float remainderComplement = Math.abs(modulator - remainder);
            if (remainder < epsilon || remainderComplement < epsilon) {
                break;
            }
            i++;
        }
        if (decimalPlacesRequired == 3) {
            System.err.println("It appears that " + x + " requires 3 or more" + " decimal places to be represented.");
        }
        return decimalPlacesRequired;
    }

    /**
     * Compute the inverse cumulative Gaussian for the specified cumulative probability, standard deviation, and mean.  In other words, given c(x, mu, sigma), where we know 
     * mu and sigma, invert for x.  Given that
     *
     *  c(x, mu, sigma) = 0.5 * (1 + erf((x - mu) / (sigma * sqrt(2))))
     *
     * we know that
     *
     *  x = (sigma * sqrt(2) * erfinv(2 * c(x, mu, sigma) - 1)) + mu
     *
     * @param probability value of c(x, mu, sigma) we wish to invert
     * @param mu mean of Gaussian
     * @param sigma standard deviation of Gaussian
     * @return x which corresponds to the specified value of c(x, mu, sigma)
     */
    public static float inverseCumulativeGaussian(float probability, float mu, float sigma) {
        double x = (sigma * Math.sqrt(2) * MathUtil.erfInverse(2 * probability - 1)) + mu;
        return ((float) x);
    }

    /**
     * Compute the Euclidean distance b/w two points
     *
     * @param x1 x-value of first point
     * @param y1 y-value of first point
     * @param x2 x-value of second point
     * @param y2 y-value of second point
     * @return Euclidean distance b/w (x1, y1) and (x2, y2)
     */
    public static double euclideanDistance(double x1, double y1, double x2, double y2) {
        double distance = Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1));
        return distance;
    }

    /**
     * Compute 1 / (factorial of the specified number) in the simplest fashion
     *
     * @param n the number for which we want to compute the factorial
     * @return 1 / n! = 1 / n / (n - 1) / (n - 2) / ... / 2
     */
    public static double inverseFactorial(int n) {
        // Java type specification states that the smallest double value is 4.94065645841246544e-324d; thus, n can be up to 177 before 1 / (n!) goes to zero
        if (n < 0 || n > 177) {
            // n < 0 is undefined and n > 177 causes overflow
            System.err.println("0 <= n <= 177");
            System.exit(-1);
        }
        double result = 1;
        for (int i = 2; i <= n; i++) {
            result /= i;
        }
        return result;
    }

    /**
     * Compute the probability density of the sum of n iid random variables chosen from uniform distribution b/w (0, 1) at the point s, using the formula of
     * Sadooghi-Alvandi et al 2007:
     *
     *  f_n(s) = 1 / (n - 1)! * sum_k=0_to_[s] {(-1)^k * (nCk) * (s - k) ^ (n - 1)}
     *
     * where [s] = Floor(s) and 0 < s < n
     *
     * @param n number of random variables to sum
     * @param s value at which to evaluate the probability density
     * @return probability density of f_n(s)
     */
    public static double uniformSumDensity(int n, double s) {
        if (n < 1) {
            System.err.println("MathUtil.uniformSumDensity: n must be greater than 0");
            System.exit(-1);
        }
        if (s <= 0 || s >= n) { // density is everywhere zero except where 0 < s < n
            return 0;
        }
        if (n == 1) {
            // formula of Sadooghi-Alvandi et al is only applicable for n >= 2
            return 1;
        }

        double multiplicativeFactor = MathUtil.inverseFactorial(n - 1);
        double sum = 0;
        int sFloored = (int) Math.floor(s);

        for (int k = 0; k <= sFloored; k++) {
            int sign = 1;
            if (k % 2 == 1) // if k is odd, the sign is flipped
            {
                sign = -1;
            }
            double choiceFactor = MathUtil.choose(n, k);
            double powerFactor = Math.pow(s - k, n - 1);
            sum += sign * choiceFactor * powerFactor;
        }
        sum *= multiplicativeFactor;
        return sum;
    }

    /**
     * Compute the cumulative density of the sum of n iid random variables chosen from uniform distribution b/w (0, 1) at the point s, by summing the
     * probability densities up to point s, stepping in small increments
     *
     * @param n number of random variables to sum
     * @param s value at which to evaluate the cumulative density
     * @return cumulative density of f_n(s)
     */
    public static double uniformSumCumulativeDensity(int n, double s) {
        if (n < 1) {
            System.err.println("MathUtil.uniformSumCumulativeDensity: n must be greater than 0");
            System.exit(-1);
        }
        if (s <= 0) {
            return 0;
        }
        if (s >= n) {
            return 1;
        }
        if (n == 1) {
            return s;
        }

        // sum probability densities up to s, making steps of n / 1000
        double sum = 0;
        int totalNumberOfSteps = 1000 * n;

        for (int i = 0; i < totalNumberOfSteps; i++) {
            double x = (double) i * (double) n / 1000.0;
            if (x > s) {
                break;
            }
            sum += MathUtil.uniformSumDensity(n, x);
        }

        return sum;
    }

    /**
     * Given the specified data set and the values at which we wish to define the ECDF, compute the ECDF
     *
     * @param x dataset
     * @param valuesAtWhichToComputeECDF values at which we want to define the ECDF
     * @return the ECDF of x defined at the desired values
     */
    public static double[] empiricalCDF(double[] x, double[] valuesAtWhichToComputeECDF) {
        // Make sorted local copies of the data
        int entries = x.length;
        double[] xCopy = new double[entries];
        System.arraycopy(x, 0, xCopy, 0, x.length);
        Arrays.sort(xCopy);

        double[] xCDF = new double[valuesAtWhichToComputeECDF.length];

        int previousCDFMarker = 0;
        for (int i = 0; i < xCopy.length; i++) {
            double xValue = xCopy[i];
            for (int j = previousCDFMarker; j < xCDF.length; j++) {
                double ecdfValue = valuesAtWhichToComputeECDF[j];
                if (xValue < ecdfValue) {
                    for (int k = j - 1; k < xCDF.length; k++) {
                        xCDF[k] += 1.0 / x.length;
                    }
                    previousCDFMarker = j - 1;
                    break;
                }
            }
        }
        xCDF[xCDF.length - 1] = 1;
        return xCDF;
    }

    /**
     * Approximate the cumulative Kolmogorov distribution by summing the first 100 terms of the infinite sequence which describes the exact distribution:
     *
     * Pr(K<=x) = sqrt(2pi) / x * sum(i=1 to Inf)[exp(-(2i-1)^2*pi^2/(8x^2))]
     *
     * from http://en.wikipedia.org/wiki/Kolmogorov-Smirnov_test
     *
     * @param x value at which to evaluate the cdf
     * @return the cdf value at x
     */
    public static double kolmogorovCDF(double x) {
        if (x <= 0) {
            return 0;
        }
//        if (x >= 1){
//            return 1;
//        }
        double sum = 0;
        for (int i = 1; i < 101; i++) {
            sum += Math.exp(-(2 * i - 1) * (2 * i - 1) * Math.PI * Math.PI / (8 * x * x));
        }
        double cdfValue = sum * Math.sqrt(2 * Math.PI) / x;
//        System.out.println("JZ CDF = " + cdfValue);
//        return cdfValue;

        // Implementation below is translated from C++ implementation at http://root.cern.ch/root/html/src/TMath.cxx.html (TMath::KolmogorovProb)
//Double_t fj[4] = {-2,-8,-18,-32}, r[4];
        double[] fj = {-2, -8, -18, -32};
        double[] r = new double[4];
//   const Double_t w = 2.50662827;
        double w = 2.50662827;
//   // c1 - -pi**2/8, c2 = 9*c1, c3 = 25*c1
//   const Double_t c1 = -1.2337005501361697;
        double c1 = -1.2337005501361697;
//   const Double_t c2 = -11.103304951225528;
        double c2 = -11.103304951225528;
//   const Double_t c3 = -30.842513753404244;
        double c3 = -30.842513753404244;
//
//   Double_t u = TMath::Abs(z);
        double u = Math.abs(x);
//   Double_t p;
        double p = 0;
//   if (u < 0.2) {
        if (u < 0.2) {
//      p = 1;
            p = 1;
//   } else if (u < 0.755) {
        } else if (u < 0.755) {
//      Double_t v = 1./(u*u);
            double v = 1 / (u * u);
//      p = 1 - w*(TMath::Exp(c1*v) + TMath::Exp(c2*v) + TMath::Exp(c3*v))/u;
            p = 1 - w * (Math.exp(c1 * v) + Math.exp(c2 * v) + Math.exp(c3 * v)) / u;
//   } else if (u < 6.8116) {
        } else if (u < 6.8116) {
//      r[1] = 0;
            r[1] = 0;
//      r[2] = 0;
            r[2] = 0;
//      r[3] = 0;
            r[3] = 0;
//      Double_t v = u*u;
            double v = u * u;
//      Int_t maxj = TMath::Max(1,TMath::Nint(3./u));
            int maxj = Math.max(1, Math.round(3f / (float) u));
//      for (Int_t j=0; j<maxj;j++) {
            for (int j = 0; j < maxj; j++) {
//         r[j] = TMath::Exp(fj[j]*v);
                r[j] = Math.exp(fj[j] * v);
//      }
            }
//      p = 2*(r[0] - r[1] +r[2] - r[3]);
            p = 2 * (r[0] - r[1] + r[2] - r[3]);
//   } else {
        } else {
//      p = 0;
            p = 0;
//   }
        }
//   return p;
        p = 1 - p;
//        System.out.println("C++ CDF = " + p);
        return p;
    }

    /**
     * Given the specified probability density function, compute the ECDF
     *
     * @param x pdf
     * @return the corresponding ecdf
     */
    public static float[] empiricalCDF(float[] x) {
        // Make sorted local copies of the data
        int entries = x.length;

        float[] xCDF = new float[entries];
        xCDF[0] = x[0];
        for (int i = 1; i < xCDF.length; i++) {
            xCDF[i] = xCDF[i - 1] + x[i];
        }

        return xCDF;
    }

    /**
     * Determine if the ray specified by the two ordered pairs--the first ordered pair being the ray endpoint-- intersects the line segment by the second set of two ordered
     * pairs.  To do this, we determine the intersection of the two lines corresponding to the ray and the segment and determine if this intersection point falls on the line segment
     * and on the ray.  The line corresponding to the ray is given:
     * 
     * y = (y4 - y1) / (x4 - x1) * x + y4 - (y4 - y1) / (x4 - x1) * x4
     * 
     * and the line corresponding to the line segment is given:
     * 
     * y = (y3 - y2) / (x3 - x2) * x + y3 - (y3 - y2) / (x3 - x2) * x3
     * 
     * We determine the intersection (x*, y*) of these two lines and determine if this point falls on the ray and on the line segment by checking the following conditions:
     *
     * min(x2, x3) <= x* <= max(x2, x3)
     * min(y2, y3) <= y* <= max(y2, y3)
     *
     * x* >= x1 if x1 < x4
     * x* <= x1 if x1 > x4
     * y* >= y1 if y1 < y4
     * y* <= y1 if y1 > y4
     * 
     * @param x1 x-value of the ray endpoint
     * @param y1 y-value of the ray endpoint
     * @param x4 x-value of arbitrary point on the ray
     * @param y4 y-value of arbitrary point on the ray
     * @param x2 x-value of the first line segment endpoint
     * @param y2 y-value of the first line segment endpoint
     * @param x3 x-value of the second  line segment endpoint
     * @param y3 y-value of the second  line segment endpoint
     * @return boolean answering the question "Does the specified ray intersect the specified line segment?"
     */
    public static boolean doesRayIntersectLineSegment(float x1, float y1, float x4, float y4, float x2, float y2, float x3, float y3) {
        // determine the intersection
        float xStar = (y3 - (y3 - y2) / (x3 - x2) * x3 - y4 + (y4 - y1) / (x4 - x1) * x4) / ((y4 - y1) / (x4 - x1) - (y3 - y2) / (x3 - x2));
        // If the line segment is vertical, then x* is just x2
        if (x2 == x3) {
            xStar = x2;
        }
        float yStar = (y4 - y1) / (x4 - x1) * xStar + y4 - (y4 - y1) / (x4 - x1) * x4;

//        if (Float.isNaN(xStar)  || Float.isNaN(yStar)){
//            return false;
//        }

        // determine if the intersection falls on the line segment
        if (xStar < (float) Math.min(x2, x3)) {
            return false;
        }
        if (xStar > (float) Math.max(x2, x3)) {
            return false;
        }
        if (yStar < (float) Math.min(y2, y3)) {
            return false;
        }
        if (yStar > (float) Math.max(y2, y3)) {
            return false;
        }

        // determine if the intersection falls on the ray
        if (x1 < x4 && xStar < x1) {
            return false;
        }
        if (x1 > x4 && xStar > x1) {
            return false;
        }
        if (y1 < y4 && yStar < y1) {
            return false;
        }
        if (y1 > y4 && yStar > y1) {
            return false;
        }


        // If we're here, it means the intersection falls on the line segment and on the ray, indicating that the ray does intersect the line segment
        return true;
    }

    /**
     * Given two ordered pairs, determine the slope b/w them
     * 
     * @param x1 x-value of first ordered pair
     * @param y1 y-value of first ordered pair
     * @param x2 x-value of second ordered pair
     * @param y2 y-value of second ordered pair
     * @return slope of line b/w ordered pairs (x1, y1) and (x2, y2)
     */
    public static float slope(float x1, float y1, float x2, float y2) {
        float slope = (y2 - y1) / (x2 - x1);
        return slope;
    }

    /**
     * Given one ordered pair and the slope of the line through this point, compute the x-value of the ordered pair on the same line with the specified y-value
     * 
     * @param x1 x-value of first ordered pair
     * @param y1 y-value of first ordered pair
     * @param y2 y-value of second ordered pair
     * @param slope of line b/w ordered pairs (x1, y1) and (x2, y2)
     * @return x2 x-value of second ordered pair
     */
    public static float valueAtGivenY(float x1, float y1, float y2, float slope) {
//        y1 = mx1 + b ==> b = y1 - mx1
        float b = y1 - slope * x1;
//        y2 = mx2 + b ==> x2 = (y2 - b) / m
        float x2 = (y2 - b) / slope;
        return x2;
    }
    
    /**
     * Given a set of ordered pairs, taken to be connected by line segments, determine the y-value at the specified x-value
     * 
     * @param xs ordered pair x values
     * @param ys ordered pair y values
     * @param x value of interest
     * @return y-value at specified x-value, given that the ordered pairs are connected by line segments
     */
    public static float valueAtGivenX(float[] xs, float[] ys, float x){
        // Determine b/w which 2 ordered pairs the given value of x falls
        int upperIndex = 0;
        for (int i = 0; i < ys.length; i++) {
            float currentX = xs[i];
            if (currentX > x){
                upperIndex = i;
                break;
            }
        }
        
        float x1 = xs[Math.max(upperIndex - 1, 0)];
        float y1 = ys[Math.max(upperIndex - 1, 0)];
        float x2 = xs[Math.min(upperIndex, xs.length - 1)];
        float y2 = ys[Math.min(upperIndex, ys.length - 1)];
        
        float slope = slope(x1, y1, x2, y2);
//        y1 = mx1 + b ==> b = y1 - mx1
        float b = y1 - slope * x1;        
        // y = mx + b
        float y = slope * x + b;
        return y;
    }
    
    /**
     * Round the given number to the nearest specified interval
     * 
     * @param number number to be rounded
     * @param interval interval to which the number should be rounded
     * @return number, rounded to the nearest parameter
     */
    public static float roundedToNearest(float number, float interval){
        int intermediateQuotient = Math.round(number / interval);
        float roundedNumber = (float)intermediateQuotient * interval;
        return roundedNumber;
    }
}
