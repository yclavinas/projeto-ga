
import java.util.Random;
import java.util.Arrays;

/**
 *
 * @author jzechar has now made a minor change
 */
public class ArrayUtil {

    public ArrayUtil() {
    }

    /**
     * Generate an array with n random integers from {1, 2,..., x}, sorted in increasing order, using random numbers from the specified generator seed
     *
     * @param n number of samples to generate
     * @param x maximum value of uniform distribution
     * @param seed value w/ which to seed the random number generator
     * @return array of n random positive integer from {1, 2, ..., x}
     */
    public static int[] orderedRandomIntegers(int n, int x, long seed) {
        int[] randomArray = new int[n];

        // generate an unordered array of random numbers
        Random rndgen = new Random(seed);
        for (int i = 0; i < n; i++) {
            randomArray[i] = rndgen.nextInt(x) + 1;
        }
        // now sort the random array in increasing order
        Arrays.sort(randomArray);
        return randomArray;
    }

    /**
     * Normalize the specified array so that the sum of its values is unity.
     * We do this by finding the sum of the original contents and dividing each
     * entry by this sum
     * @param array array to normalize
     */
    public static float[] normalize(float[] array) {
        float[] arrayCopy = new float[array.length];
        System.arraycopy(array, 0, arrayCopy, 0, array.length);
        float sum = ArrayUtil.sum(array);

        // divide each entry by this sum
        for (int i = 0; i < array.length; i++) {
            arrayCopy[i] /= sum;
        }
        return arrayCopy;
    }

    /**
     * Normalize the specified array so that the sum of its values is unity, disregarding any negative entries.
     * We do this by finding the sum of the original contents and dividing each entry by this sum
     * 
     * @param array array to normalize
     * @return normalized array
     */
    public static float[] normalizeIgnoreNegativeValues(float[] array) {
        float[] arrayCopy = new float[array.length];
        System.arraycopy(array, 0, arrayCopy, 0, array.length);
        float sum = ArrayUtil.sum(array, 0f);
        

        // divide each entry by this sum
        for (int i = 0; i < array.length; i++) {
            arrayCopy[i] /= sum;
        }
        return arrayCopy;
    }

    /**
     * Normalize the specified array so that the sum of its values is unity.
     * We do this by finding the sum of the original contents and dividing each
     * entry by this sum
     * @param array array to normalize
     */
    public static float[] normalize(short[] array) {
        float[] arrayCopy = new float[array.length];
        for (int i = 0; i < array.length; i++) {
            arrayCopy[i] = (float) array[i];
        }
        float sum = ArrayUtil.sum(arrayCopy);

        // divide each entry by this sum
        for (int i = 0; i < array.length; i++) {
            arrayCopy[i] /= sum;
        }
        return arrayCopy;
    }

    /**
     * Given an array of floats, find and return the minimum value greater
     * than zero.
     *
     * @param array array of floats
     * @return minimum positive value in array
     */
    public static float minimumPositiveValue(float[] array) {
        int entries = array.length;
        float min = Float.POSITIVE_INFINITY;

        for (int i = 0; i < entries; i++) {
            if ((array[i] < min) && (array[i] > 0.0f)) {
                min = array[i];
            }
        }

        return min;
    }

    /**
     * Given an array of floats, find and return the minimum value.
     *
     * @param array array of floats
     * @return minimum value in array
     */
    public static float minimum(float[] array) {
        int entries = array.length;
        float min = array[0];

        for (int i = 1; i < entries; i++) {
            if (array[i] < min) {
                min = array[i];
            }
        }

        return min;
    }

    /**
     * Given an array of floats, find and return the maximum value.
     *
     * @param array array of floats
     * @return minimum value in array
     */
    public static float maximum(float[] array) {
        int entries = array.length;
        float max = array[0];

        for (int i = 1; i < entries; i++) {
            if (array[i] > max) {
                max = array[i];
            }
        }

        return max;
    }

    /**
     * Compute sum of array values.
     * @param array over which to sum
     * @return sum of array values.
     */
    public static int sum(int[] array) {
        int sum = 0;
        for (int i = 0; i < array.length; i++) {
            sum += array[i];
        }
        return sum;
    }

    /**
     * Compute sum of array values.
     * @param array over which to sum
     * @return sum of array values.
     */
    public static float sum(float[] array) {
        float sum = 0;
        for (int i = 0; i < array.length; i++) {
            sum += array[i];
        }
        return sum;
    }

    /**
     * Compute sum of array values above given threshold.
     * @param array over which to sum
     * @param minThreshold value above which the entry will be included in sum
     * @return sum of array values.
     */
    public static float sum(float[] array, float minThreshold) {
        float sum = 0;
        for (int i = 0; i < array.length; i++) {
            float entry = array[i];
            if (entry > minThreshold) {
                sum += entry;
            }
        }
        return sum;
    }

    /**
     * Compute sum of array values.
     * 
     * @param array over which to sum
     * @return sum of array values.
     */
    public static short sum(short[] array) {
        short sum = 0;
        for (int i = 0; i < array.length; i++) {
            sum += array[i];
        }
        return sum;
    }

    /**
     * Compute sum of array values, returning an int in case the sum of the shorts exceeds the maximum short.
     * 
     * @param array over which to sum
     * @return sum of array values.
     */
    public static int sumShorts(short[] array) {
        int sum = 0;
        for (int i = 0; i < array.length; i++) {
            sum += array[i];
        }
        return sum;
    }

    /**
     * Count the number of entries in the specified array that are as large as
     * or larger than the specified value.
     * @param array array over which we'll search
     * @param value value of interest
     * @return number of entries in the specified array that are >= the specified
     * value
     */
    public static int numberOfEntriesAsLargeAsValue(float[] array, float value) {
        int entries = array.length;
        int numberOfEntries = 0;
        for (int i = 0; i < entries; i++) {
            if (array[i] >= value) {
                numberOfEntries++;
            }
        }

        return numberOfEntries;
    }

    /**
     * Given two sets of points, count the number of points in the first set that
     * are greater than the corresponding points in the second set.  In
     * particular, let the first set be some sample from a process and the
     * second set be the theoretical upper limit confidence bounds; then we can
     * use this function repeatedly to determine the number of outliers based
     * on many samples.  Here, corresponding happens to mean we compare the ith
     * element in the sample to the (i-1)th element in the reference.
     *
     * @param numberOfPointsAbove array containing the number of points above
     *  the reference points from previous samples
     * @param referencePoints array of reference points to which we'll be comparing
     * the sample
     * @param samplePoints sample points in which we're interested for testing
     * @return array of cumulative number of points above the reference points
     */
    public static int[] numberOfPointsAbove(int[] numberOfPointsAbove, float[] referencePoints, float[] samplePoints) {
        for (int i = 0; i < referencePoints.length; i++) {
            if (samplePoints[i + 1] > referencePoints[i]) {
                numberOfPointsAbove[i]++;
            }
        }
        return numberOfPointsAbove;
    }

    /**
     * Given three sets of points, count the number of points in the first set
     * that fall within the bounds set by the corresponding points in the 2nd
     * and 3rd sets.  Imagine the first set be some sample from a process and the
     * 2nd set to be the theoretical lower limit confidence bounds and the 3rd
     * is the theoretically derived upper limit confidence bounds; then we can
     * use this function repeatedly to determine the number of outliers based
     * on many samples.  Here, corresponding happens to mean we compare the ith
     * element in the sample to the (i-1)th element in the bounds.
     *
     * @param numberOfPointsInside array containing the number of points inside
     *  the bounds from previous samples
     * @param lowerBounds array of minimum reference points to which we'll be
     * comparing the sample
     * @param upperBounds array of maximum reference points to which we'll be
     * comparing the sample
     * @param samplePoints sample points in which we're interested for testing
     * @return array of cumulative number of points within the bounds
     */
    public static int[] numberOfPointsInside(int[] numberOfPointsInside, float[] lowerBounds, float[] upperBounds, float[] samplePoints) {
        for (int i = 0; i < lowerBounds.length; i++) {
            if (samplePoints[i + 1] > lowerBounds[i] && samplePoints[i + 1] < upperBounds[i]) {
                numberOfPointsInside[i]++;
            }
        }
        return numberOfPointsInside;
    }

    /**
     * Given two sets of points, count the number of points in the first set that
     * are less than the corresponding points in the second set.  In
     * particular, let the first set be some sample from a process and the
     * second set be the theoretical lower limit confidence bounds; then we can
     * use this function repeatedly to determine the number of outliers based
     * on many samples.  Here, corresponding happens to mean we compare the ith
     * element in the sample to the ith element in the reference.
     *
     * @param numberOfPointsBelow array containing the number of points below
     *  the reference points from previous samples
     * @param referencePoints array of reference points to which we'll be comparing
     * the sample
     * @param samplePoints sample points in which we're interested for testing
     * @return array of cumulative number of points below the reference points
     */
    public static int[] numberOfPointsBelow(int[] numberOfPointsBelow, float[] referencePoints, float[][] samplePoints) {
        for (int i = 0; i < referencePoints.length; i++) {
            if (samplePoints[i][1] < referencePoints[i]) {
                numberOfPointsBelow[i]++;
            }
        }
        return numberOfPointsBelow;
    }

    /**
     * Given an integer array, count the number of nonnegative, nonzero entries
     *
     * @param array array in which we're interested
     * @return number of nonzero entries in the specified array
     */
    public static short numberOfPositiveEntries(short[] array) {
        short numberOfEntriesGreaterThanZero = 0;
        for (int i = 0; i < array.length; i++) {
            if (array[i] > 0) {
                numberOfEntriesGreaterThanZero++;
            }
        }
        return numberOfEntriesGreaterThanZero;
    }

    /**
     * Given an integer array, return the nonnegative, nonzero entries
     *
     * @param array array in which we're interested
     * @return array of nonzero entries in the specified array
     */
    public static short[] positiveEntries(short[] array) {
        int entries = array.length;
        int numberOfEntriesGreaterThanZero = ArrayUtil.numberOfPositiveEntries(array);
        short[] positiveEntries = new short[numberOfEntriesGreaterThanZero];
        int positiveEntryPosition = 0;
        for (int i = 0; i < entries; i++) {
            if (array[i] > 0) {
                positiveEntries[positiveEntryPosition++] = array[i];
            }
        }

        return positiveEntries;
    }

    /**
     * Given an integer array, shuffle the entries
     *
     * @param array array in which we're interested
     * @param seed value w/ which to seed the random number generator
     * @return array with same values as input array, only shuffled
     */
    public static short[] shuffle(short[] array, long seed) {
        int numberOfShufflesPerEntry = 4;
        short[] shuffledArray = new short[array.length];
        Random rndgen = new Random(seed);

        // make a copy of the contents
        System.arraycopy(array, 0, shuffledArray, 0, array.length);

        for (int i = 0; i < shuffledArray.length; i++) {
            for (int j = 0; j < numberOfShufflesPerEntry; j++) {
                int positionToSwap = rndgen.nextInt(array.length);
                short currentValue = shuffledArray[i];
                short newValue = shuffledArray[positionToSwap];
                shuffledArray[i] = newValue;
                shuffledArray[positionToSwap] = currentValue;
            }
        }

        return shuffledArray;
    }

    /**
     * Given a float array, return the average of the entries
     *
     * @param array array in which we're interested
     * @return average of all entry values
     */
    public static float average(float[] array) {
        float sum = ArrayUtil.sum(array);
        float avg = sum / (float) array.length;
        return avg;
    }

    /**
     * Given a binning specified by minimum value, maximum value, and bin size,
     * determine to which bin a given value belongs.
     *
     * @param gridMin minimum grid value
     * @param gridMax maximum grid value
     * @param binSize size of each bin
     * @param value value which we want to bin
     * @param allowOverflow answer to the question of whether the value should
     * be allowed to reside outside the grid.  If allowOverflow is false and
     * the value doesn't belong in the grid, -1 is returned.  Otherwise, the
     * bin number is returned, regardless of whether it falls outside the grid
     * limits.
     * @return the bin to which the value of interest belongs
     */
    public static int binToWhichValueBelongs(float gridMin, float gridMax, float binSize, float value, boolean allowOverflow) {
        int bigNumber = 10000;

        // Scale the minimum bin value.  To avoid rounding errors, we floor the absolute value of the scaled value, then multiply this by the sign of the original value
        int min_int = (int) (Math.signum(gridMin) * (float) Math.floor(Math.abs(gridMin * bigNumber)));
        // Scale the cell size.
        int cellSize_int = Math.round(binSize * bigNumber);
        //  Scale the value to be binned.  Avoid rounding errors as above
        int value_int = (int) (Math.signum(value) * (float) Math.floor(Math.abs(value * bigNumber)));
//        int value_int = (int) Math.floor(value * bigNumber);
        if ((value < gridMin) || (value >= gridMax) && !allowOverflow) {
            return -1;
        }
        float position_f = (float) (value_int - min_int) / (float) cellSize_int;
        int position = (int) Math.floor(position_f);
        return position;
    }

    /**
     * For a given normalized array (its entries sum to one, compute and print
     * all the sums possible by combinations of the entries.  Clearly, each unique
     * entry is itself a sum of a combination.  Then, we try every other sum by
     * brute force (looping)
     *
     * @param array array in which we're interested in finding possible sums
     */
    public static void allPossibleSums(float[] array) {
        int entries = array.length;

        // There are (entries) sums containing one summand, there is one sum
        // containing (entries) summands, the number of sums for an arbitrary
        //  number of summands x is given by (entries) CHOOSE (x).  Therefore
        //  the total number of sums is given by the sum from (0 to entries) of
        //  2 ^ x, or just (2 ^ entries) - 1
        int numberOfSums = (int) Math.pow(2, entries) - 1;

//        float[] sums = new float[numberOfSums];
        System.out.print("sums=[");
        for (int i = 1; i <= numberOfSums; i++) {
            System.out.print(ArrayUtil.encodedSumOfProducts(i, array) + ", ");
//            sums[i - 1] = this.encodedSumOfProducts(i, array);
        }
        System.out.println("];");

        System.out.print("i=[");
        for (int i = 1; i <= numberOfSums; i++) {
            System.out.print(i + ", ");
        }
        System.out.println("];");

    }

    /**
     * Compute the sum of products of an integer and an array, where the integer
     * in binary represents the coefficients by which we want to multiply the
     * array entries
     *
     * @param coefficient encoded coefficients by which to multiply the array
     * entries
     * @param array array of interest
     * @return sum of products of encoded integer and array
     */
    private static float encodedSumOfProducts(int coefficient, float[] array) {
        int entries = array.length;
        int[] coefficients = new int[entries];
        float sum = 0.0f;
        int subtractor = 0;
        // decode the coefficients and mulitply
        for (int i = coefficients.length - 1; i >= 0; i--) {
//            if (i == 0)
//                System.out.println("jesus");
            coefficients[i] = (int) Math.floor(coefficient / Math.pow(2, i));
            subtractor = (int) (coefficients[i] * Math.pow(2, i));
            coefficient -= subtractor;
            sum += coefficients[i] * array[i];
//            if (coefficient == 0)
//                System.out.println("jesus");
        }
        return sum;
    }

    /**
     * Express the given integer number in binary form w/ the given number of
     * bits.
     *
     * @param number integer which we wish to represent as a binary number
     * @param numberOfBits maximum number of bits to be used to represent the
     * specified number
     * @return binary representation of the specified number using the specified
     * number of bits
     */
    public static int[] binaryRepresentation(int number, int numberOfBits) {
        int originalNumber = number;
        if (number > (int) Math.pow(2, numberOfBits) - 1) {
            System.err.println("not enough bits to represent " + number);
            System.exit(-1);
        }

        int[] binaryRep = new int[numberOfBits];
        int subtractor = 0;
        // decode the number
        for (int i = binaryRep.length - 1; i >= 0; i--) {
//            if (i == 0)
//                System.out.println("jesus");
            binaryRep[i] = (int) Math.floor(number / Math.pow(2, i));
            subtractor = (int) (binaryRep[i] * Math.pow(2, i));
            number -= subtractor;
        }
//        System.out.println("number = " + originalNumber + ", rep (in reverse) = "
//                + Arrays.toString(binaryRep));
        return binaryRep;
    }

    /**
     * Express the given binary number in integer form
     *
     * @param binaryRep array representation of number which we wish to represent
     * as an integer
     * @return decimal representation of the specified number
     */
    public static int decimalRepresentation(int[] binaryRep) {
        int number = 0;
        for (int i = 0; i < binaryRep.length; i++) {
            number += (int) Math.pow(2, i) * binaryRep[i];
        }
        return number;
    }

    /**
     * When we're using the specified array to define intersections and we find
     * that the given intersection yields the empty set, we know that any other
     * intersection that contains this intersection will also yield the empty
     * set.  The intersection bitmap tells us whether or not we should compute
     * the corresponding intersection.  Here, we update the bitmap once we know
     * the intersection specified by the given array is the empty set.  Let's
     * consider an example.  Let's say we have 4 sets A, B, C, and D.  We
     * represent the intersection of A and B as 0011.  If we know that this
     * intersection is the empty set, then we also know that 0111 and 1011 and
     * 1111 are also the empty set.  In decimal terms, we're being told that
     * 3 -> 0 ==> 7 -> 0, 11 -> 0, and 15 ->0 and we should update the computation
     * bitmap accordingly
     *
     * @param encodedIntersection intersection which we're being told yields the
     * empty set
     * @param computeBitmap bitmap telling us which intersections we should compute,
     * we'll update these values
     * @return an updated bitmap telling us which intersections might be non-empty
     */
    public static boolean[] intersectionBitmap(int[] encodedIntersection, boolean[] computeBitmap) {
        int numberOfIntersections = computeBitmap.length;
        int decodedIntersection = ArrayUtil.decimalRepresentation(encodedIntersection);
        boolean[] bitmapCopy = new boolean[computeBitmap.length];
        System.arraycopy(computeBitmap, 0, bitmapCopy, 0, computeBitmap.length);

        for (int i = decodedIntersection + 1; i <= numberOfIntersections; i++) {
            // if we already know this one is being skipped, don't bother
            if (bitmapCopy[i - 1]) {
                int[] residual = new int[encodedIntersection.length];
                System.arraycopy(encodedIntersection, 0, residual, 0,
                        encodedIntersection.length);
                int[] encodedNumber = ArrayUtil.binaryRepresentation(i, encodedIntersection.length);

                // check to see if this encoded intersection is a superset
                for (int j = 0; j < encodedNumber.length; j++) {
                    residual[j] -= encodedNumber[j];
                }
                boolean isSuperset = true;
                for (int j = 0; j < encodedNumber.length; j++) {
                    if (residual[j] == 1) {
                        isSuperset = false;
                        break;
                    }
                }
                if (isSuperset) {
                    bitmapCopy[i - 1] = false;
                }
            }
        }

        return bitmapCopy;
    }

    /**
     * Given a 2D gridding specified by minimum values, maximum values, and grid
     * sizes, determine to which grid cell a given (xValue, yValue) belongs.
     * We do this by determining the appropriate row and appropriate column
     * based on their respective discretization, then we map this row and column
     * to a cell number based on the number of columns in the grid.  We deal
     * with values that don't fit into the grid by bringing them to the closest
     * cell inside the grid.  For example, if a value falls to the "west" of the
     * beginning of the 24th row, we bin this value into the first column of the
     * 24th row.  If the value falls to the east of the 17th row, we bin it into
     * the last column of the 17th row.  The same method is applied to values
     * north or south of the grid.
     *
     * @param xMin minimum x value
     * @param xMax maximum x value
     * @param yMin minimum y value
     * @param yMax maximum y value
     * @param xBinSize discretization in x direction
     * @param yBinSize discretization in y direction
     * @param xValue x value which we want to bin
     * @param yValue y value which we want to bin
     * @return the cell to which (xValue, yValue) belongs
     */
    public static int cellToWhichValueBelongs(float xMin, float xMax, float yMin, float yMax, float xBinSize, float yBinSize, float xValue, float yValue) {
        int numberOfColumns = Math.round((xMax - xMin) / xBinSize);
        int numberOfRows = Math.round((yMax - yMin) / yBinSize);

//        if (xValue == -0.42f && yValue == -0.18f){
//            System.out.println("aim...");
//        }
        int column = ArrayUtil.binToWhichValueBelongs(xMin, xMax, xBinSize, xValue, true);
        // if the value falls outside the grid to the west, put it in the first column
        if (column < 0) {
            column = 0;
//            System.out.println("Overflow to the west");
        }
        // if the value falls outside the grid to the east, put it in the last column
        if (column >= numberOfColumns) {
            column = numberOfColumns - 1;
//            System.out.println("overflow to the east");
        }

        int row = ArrayUtil.binToWhichValueBelongs(yMin, yMax, yBinSize, yValue, true);
        // if the value falls outside the grid to the south, put it in the first row
        if (row < 0) {
            row = 0;
//            System.out.println("overflow to the south");
        }
        // if the value falls outside the grid to the north, put it in the last row
        if (row >= numberOfRows) {
            row = numberOfRows - 1;
//            System.out.println("overflow to the north");
        }

        // transform the (row, col) point into the cell number
        int cell = row * numberOfColumns + column;
        return cell;
    }

    /**
     * Add the contents of 2 arrays of equal length
     *
     * @param a first array to consider
     * @param b second array to consider
     * @return the sum of a and b
     */
    public static float[] add(float[] a, float[] b) {
        if (a.length != b.length) {
            System.err.println("Arrays are not of the same length");
            System.exit(-1);
        }
        float[] c = new float[a.length];
        System.arraycopy(a, 0, c, 0, a.length);

        for (int i = 0; i < b.length; i++) {
            c[i] += b[i];
        }

        return c;
    }

    /**
     * Add the contents of 2 arrays of equal length
     *
     * @param a first array to consider
     * @param b second array to consider
     * @return the sum of a and b
     */
    public static short[] add(short[] a, short[] b) {
        if (a.length != b.length) {
            System.err.println("Arrays are not of the same length");
            System.exit(-1);
        }
        short[] c = new short[a.length];
        System.arraycopy(a, 0, c, 0, a.length);

        for (int i = 0; i < b.length; i++) {
            c[i] += b[i];
        }

        return c;
    }

    /**
     * Given a 3D gridding specified by minimum values, maximum values, and grid sizes, determine to which grid box a given (xValue, yValue, zValue) belongs.  We do this by determining the
     * appropriate row/column/depth based on the respective discretization, then we map this to a box number.  We deal with values that don't fit into the grid by bringing them to the closest
     * box inside the grid.  For example, if a value falls to the "west" of the beginning of the 24th row, we bin this value into the first column of the 24th row.  If the value falls to the east of the 17th
     * row, we bin it into the last column of the 17th row.  The same method is applied to values north or south of the grid, or above or below the grid.
     *
     * @param xMin minimum x value
     * @param xMax maximum x value
     * @param yMin minimum y value
     * @param yMax maximum y value
     * @param zMin minimum z value
     * @param zMax maximum z value
     * @param xBinSize discretization in x direction
     * @param yBinSize discretization in y direction
     * @param zBinSize discretization in z direction
     * @param xValue x value which we want to bin
     * @param yValue y value which we want to bin
     * @param zValue z value which we want to bin
     * @return the box to which (xValue, yValue, zValue) belongs
     */
    public static int boxToWhichValueBelongs(float xMin, float xMax, float yMin, float yMax, float zMin, float zMax, float xBinSize, float yBinSize,
            float zBinSize, float xValue, float yValue, float zValue) {
        int numberOfColumns = Math.round((xMax - xMin) / xBinSize);
        int numberOfRows = Math.round((yMax - yMin) / yBinSize);
        int numberOfDepthSlices = Math.round((zMax - zMin) / zBinSize);

        int column = ArrayUtil.binToWhichValueBelongs(xMin, xMax, xBinSize, xValue, true);

        // if the value falls outside the grid to the west, put it in the first column
        if (column < 0) {
            column = 0;
        }
        // if the value falls outside the grid to the east, put it in the last column
        if (column >= numberOfColumns) {
            column = numberOfColumns - 1;
        }

        int row = ArrayUtil.binToWhichValueBelongs(yMin, yMax, yBinSize, yValue, true);
        // if the value falls outside the grid to the south, put it in the first row
        if (row < 0) {
            row = 0;
        }
        // if the value falls outside the grid to the north, put it in the last row
        if (row >= numberOfRows) {
            row = numberOfRows - 1;
        }

        int slice = ArrayUtil.binToWhichValueBelongs(zMin, zMax, zBinSize, zValue, true);
        // if the value falls above the gridded volume, put it in the first depth slice
        if (slice < 0) {
            slice = 0;
        }
        // if the value falls below the gridded volume, put it in the last depth slice
        if (slice >= numberOfDepthSlices) {
            slice = numberOfDepthSlices - 1;
        }

        // transform the (row, col, slice) point into the box number using the convention that we increment by column, then by row, then by depth slice
        // indicating that box = depth * numberOfLatBoxes * numberOfLonBoxes + row * numberOfLonBoxes + col
        int box = slice * numberOfColumns * numberOfRows + row * numberOfColumns + column;
        return box;
    }

    /**
     * Concatenate the two given arrays
     *
     * @param x first array
     * @param y second array
     * @return array whose values are simply x's values and y's values
     */
    public static double[] concatenate(double[] x, double[] y) {
        double[] concatArray = new double[x.length + y.length];
        System.arraycopy(x, 0, concatArray, 0, x.length);
        System.arraycopy(y, 0, concatArray, x.length, y.length);
        return concatArray;
    }

    /**
     * Given an array of numbers, return an array indicating the ascending sorted order of cells.  That is, if we are provided the array {0.43, 12, 168, 0.21}, we return
     * the array {3,0,1,2}
     * 
     * @param arrayToOrder array for which we want to know the order of elements
     * @return array indicating the order of elements
     */
    public static short[] orderOfArrayAscending(float[] arrayToOrder) {
        short[] cellIndices = new short[arrayToOrder.length];

        for (short i = 0; i < cellIndices.length; i++) {
            cellIndices[i] = i;
        }

        for (int i = 0; i < arrayToOrder.length - 1; i++) { // simple bubble sort

            boolean isSorted = true;
            for (int j = 1; j < arrayToOrder.length - i; j++) {

                if (arrayToOrder[j] < arrayToOrder[j - 1]) { // swap the values

                    float tempValue = arrayToOrder[j];
                    short tempIndex = cellIndices[j];

                    arrayToOrder[j] = arrayToOrder[j - 1];
                    cellIndices[j] = cellIndices[j - 1];

                    arrayToOrder[j - 1] = tempValue;
                    cellIndices[j - 1] = tempIndex;

                    isSorted = false;
                }
            }
            if (isSorted) {
                break;
            }
        }

        return cellIndices;
    }

    /**
     * Given an array of numbers, return an array indicating the ascending sorted order of cells.  That is, if we are provided the array {0.43, 12, 168, 0.21}, we return
     * the array {2, 1, 0, 3}
     * 
     * @param arrayToOrder array for which we want to know the order of elements
     * @return array indicating the order of elements
     */
    public static short[] orderOfArrayDescending(float[] arrayToOrder) {
        short[] cellIndices = new short[arrayToOrder.length];

        for (short i = 0; i < cellIndices.length; i++) {
            cellIndices[i] = i;
        }

        for (int i = 0; i < arrayToOrder.length - 1; i++) { // simple bubble sort

            boolean isSorted = true;
            for (int j = 1; j < arrayToOrder.length - i; j++) {

                if (arrayToOrder[j] > arrayToOrder[j - 1]) { // swap the values

                    float tempValue = arrayToOrder[j];
                    short tempIndex = cellIndices[j];

                    arrayToOrder[j] = arrayToOrder[j - 1];
                    cellIndices[j] = cellIndices[j - 1];

                    arrayToOrder[j - 1] = tempValue;
                    cellIndices[j - 1] = tempIndex;

                    isSorted = false;
                }
            }
            if (isSorted) {
                break;
            }
        }

        return cellIndices;
    }

    /**
     * For the specified monotonically increasing function (specified as an array), determine the indices of the function that capture the specified  upper and lower bound values.
     * For example, I'm going to use this by specifying lower and upper bound of tau values and figuring out the trajectory points that fall b/w these
     * 
     * @param array the monotonically increasing function of interest
     * @param lowerBound lower bound value of interest
     * @param upperBound upper bound value of interest
     * @return array of two indices indicating the function indices that capture the range specified by the upper and lower bound
     */
    public static int[] boundingIndices(float[] array, float lowerBound, float upperBound) {
        int lowerIndex = array.length;
        int upperIndex = 0;

//        Determine lower bound index, the minimum index for which the function exceeds the specified lower bound
        for (int i = 0; i < array.length; i++) {
            float value = array[i];
            if (value > lowerBound) {
                lowerIndex = i;
                break;
            }
        }

//        Determine upper bound index, the minimum index for which the function equals or exceeds the specified upper bound
        for (int i = lowerIndex; i < array.length; i++) {
            float value = array[i];
            if (value >= upperBound) {
                upperIndex = i;
                break;
            }
        }

        int[] indices = {lowerIndex, upperIndex};
        return indices;
    }

    /**
     * Given an array that represents a p.d.f. of its elements, compute the desired moment about the origin
     *
     * @param array array in which we're interested, which represents a p.d.f. of its elements (i.e., array[0] = p(1), array[1] = p(2), ...)
     * @param momentIndex the moment of interest
     * @return specified moment about the origin of the p.d.f. specified by the array
     */
    public static float momentOfpdfAbtTheOrigin(float[] array, short momentIndex) {
        float[] normalizedpdf = ArrayUtil.normalize(array);
        float momentAbtTheOrigin = 0f;
        for (int i = 0; i < normalizedpdf.length; i++) {
            float p_x = normalizedpdf[i];
            int x = i + 1;
            momentAbtTheOrigin += (float) Math.pow(x, momentIndex) * p_x;
        }

        return momentAbtTheOrigin;
    }

    /**
     * Given an array that represents a p.d.f. of its elements, compute the desired moment about the origin
     *
     * @param array array in which we're interested, which represents a p.d.f. of its elements (i.e., array[0] = p(1), array[1] = p(2), ...)
     * @param momentIndex the moment of interest
     * @return specified moment about the origin of the p.d.f. specified by the array
     */
    public static float momentOfpdfAbtTheOrigin(short[] array, short momentIndex) {
        float[] normalizedpdf = ArrayUtil.normalize(array);
        float momentAbtTheOrigin = 0f;
        for (int i = 0; i < normalizedpdf.length; i++) {
            float p_x = normalizedpdf[i];
            int x = i + 1;
            momentAbtTheOrigin += (float) Math.pow(x, momentIndex) * p_x;
        }

        return momentAbtTheOrigin;
    }

    /**
     * Given a short array, return the average of the entries
     *
     * @param array array in which we're interested
     * @return average of all entry values
     */
    public static float average(short[] array) {
        int sum = ArrayUtil.sumShorts(array);
        float avg = (float) sum / (float) array.length;
        return avg;
    }

    /**
     * Given a short array, return the variance of the entries
     * 
     * @param array array in which we're interested
     * @return variance of all entries
     */
    public static float variance(short[] array) {
        float average = ArrayUtil.average(array);
        float squaredSumOfErrors = 0f;
        for (int i = 0; i < array.length; i++) {
            squaredSumOfErrors += (array[i] - average) * (array[i] - average);
        }
        float variance = squaredSumOfErrors / ((float) array.length - 1);

        return variance;
    }

    /**
     * Given the specified irregular binning, determine to which bin a given value belongs.
     *
     * @param gridValues a vector of the maximum values contained by this bin; therefore, when we find the minimum bin for which the value is less than the bin value, we know this is
     * the right bin
     * @param value value which we want to bin
     * @return the bin to which the value of interest belongs
     */
    public static int binToWhichValueBelongs(float[] gridValues, float value) {
        for (int i = 0; i < gridValues.length; i++) {
            float f = gridValues[i];
            if (value < f) {
                return i;
            }
        }
        return -1;
    }

    /**
     * Given a 2D gridding specified by minimum values, maximum values, and grid sizes, determine the x/y indices corresponding to the specified cell number.
     * We do this by determining the appropriate row and appropriate column based on their respective discretization, then we map this row and column
     * to x/y based on the grid specification.
     *
     * @param xMin minimum x value
     * @param xMax maximum x value
     * @param yMin minimum y value
     * @param yMax maximum y value
     * @param xBinSize discretization in x direction
     * @param yBinSize discretization in y direction
     * @param cell cell index in which we're interested
     * @return an array of x/y coordinates corresponding to the minimum (x, y) value of specified cell, of the format
     *      [0] = x value
     *      [1] = y value
     */
    public static float[] arrayIndicesCorrespondingToCell(float xMin, float xMax, float yMin, float yMax, float xBinSize, float yBinSize, int cell) {
        int numberOfColumns = Math.round((xMax - xMin) / xBinSize);
        int rowIndex = cell / numberOfColumns;
        int colIndex = cell - rowIndex * numberOfColumns;

        float xValue = xMin + colIndex * xBinSize;
        float yValue = yMin + rowIndex * yBinSize;

        float[] results = {xValue, yValue};
        return results;
    }

    /**
     * Compute the "distance" b/w two arrays, where the distance is given by the sum of absolute value of difference of corresponding elements
     * 
     * @param a first array
     * @param b second array
     * @return a - b, where (a-b)_i = |a_i - b_i|
     */
    public static float distance(float[] a, float[] b) {
        float difference = 0f;
        for (int i = 0; i < b.length; i++) {
            difference += Math.abs(a[i] - b[i]);
        }
        return difference;
    }

    /**
     * quicksort inner workings, as implemented at http://cg.scs.carleton.ca/%7Emorin/misc/sortalg/QSortAlgorithm.java
     *
     * @param a array to sort
     */
    private void quicksortDetails(float[] a, int lo0, int hi0) {
        int lo = lo0;
        int hi = hi0;
        if (lo >= hi) {
            return;
        }
        float mid = a[(lo + hi) / 2];
        while (lo < hi) {
            while (lo < hi && a[lo] < mid) {
                lo++;
            }
            while (lo < hi && a[hi] > mid) {
                hi--;
            }
            if (lo < hi) {
                float T = a[lo];
                a[lo] = a[hi];
                a[hi] = T;
            }
        }
        if (hi < lo) {
            int T = hi;
            hi = lo;
            lo = T;
        }
        quicksortDetails(a, lo0, lo);
        quicksortDetails(a, lo == lo0 ? lo + 1 : lo, hi0);
    }

    /**
     * quicksort wrapper, as implemented at http://cg.scs.carleton.ca/%7Emorin/misc/sortalg/QSortAlgorithm.java
     *
     * @param a array to sort
     */
    public void quicksort(float[] a) {
        quicksortDetails(a, 0, a.length - 1);
    }

    /**
     * quicksort inner workings, as implemented at http://cg.scs.carleton.ca/%7Emorin/misc/sortalg/QSortAlgorithm.java
     *
     * @param a array to sort
     */
    private void quicksortDetails(float[][] a, int lo0, int hi0) {
        int lo = lo0;
        int hi = hi0;
        if (lo >= hi) {
            return;
        }
        float mid = a[(lo + hi) / 2][0];
        while (lo < hi) {
            while (lo < hi && a[lo][0] > mid) {
                lo++;
            }
            while (lo < hi && a[hi][0] < mid) {
                hi--;
            }
            if (lo < hi) {
                float T0 = a[lo][0];
                float T1 = a[lo][1];
                float T2 = a[lo][2];

                a[lo][0] = a[hi][0];
                a[lo][1] = a[hi][1];
                a[lo][2] = a[hi][2];
                a[hi][0] = T0;
                a[hi][1] = T1;
                a[hi][2] = T2;
            }
        }
        if (hi < lo) {
            int T = hi;
            hi = lo;
            lo = T;
        }
        quicksortDetails(a, lo0, lo);
        quicksortDetails(a, lo == lo0 ? lo + 1 : lo, hi0);
    }

    /**
     * quicksort wrapper, as implemented at http://cg.scs.carleton.ca/%7Emorin/misc/sortalg/QSortAlgorithm.java
     *
     * @param a array to sort
     */
    public void quicksort(float[][] a) {
        quicksortDetails(a, 0, a.length - 1);
    }

    /**
     * Given a 4D gridding specified by minimum values, maximum values, and grid sizes, determine to which grid box a given (xValue, yValue, zValue) belongs.  We do this by 
     * determining the appropriate row/column/depth/timestep based on the respective discretization, then we map this to a voxel number.  We deal with values that don't fit into 
     * the grid by bringing them to the closest box inside the grid.  For example, if a value falls to the "west" of the beginning of the 24th row, we bin this value into the first 
     * column of the 24th row.  If the value falls to the east of the 17th row, we bin it into the last column of the 17th row.  The same method is applied to values north or south 
     * of the grid, or above or below the grid, or before or after the grid.
     *
     * @param xMin minimum x value
     * @param xMax maximum x value
     * @param yMin minimum y value
     * @param yMax maximum y value
     * @param zMin minimum z value
     * @param zMax maximum z value
     * @param tMin minimum t value
     * @param tMax maximum t value
     * @param xBinSize discretization in x direction
     * @param yBinSize discretization in y direction
     * @param zBinSize discretization in z direction
     * @param tBinSize discretization in t direction
     * @param xValue x value which we want to bin
     * @param yValue y value which we want to bin
     * @param zValue z value which we want to bin
     * @param tValue t value which we want to bin
     * @return the voxel to which (xValue, yValue, zValue, tValue) belongs
     */
    public static int voxelToWhichValueBelongs(float xMin, float xMax, float yMin, float yMax, float zMin, float zMax, float tMin, float tMax, float xBinSize, float yBinSize,
            float zBinSize, float tBinSize, float xValue, float yValue, float zValue, float tValue) {
        int numberOfColumns = Math.round((xMax - xMin) / xBinSize);
        int numberOfRows = Math.round((yMax - yMin) / yBinSize);
        int numberOfDepthSlices = Math.round((zMax - zMin) / zBinSize);
        int numberOfTimeSlices = Math.round((tMax - tMin) / tBinSize);

        int column = ArrayUtil.binToWhichValueBelongs(xMin, xMax, xBinSize, xValue, true);
        // if the value falls outside the grid to the west, put it in the first column
        if (column < 0) {
            column = 0;
        }
        // if the value falls outside the grid to the east, put it in the last column
        if (column >= numberOfColumns) {
            column = numberOfColumns - 1;
        }

        int row = ArrayUtil.binToWhichValueBelongs(yMin, yMax, yBinSize, yValue, true);
        // if the value falls outside the grid to the south, put it in the first row
        if (row < 0) {
            row = 0;
        }
        // if the value falls outside the grid to the north, put it in the last row
        if (row >= numberOfRows) {
            row = numberOfRows - 1;
        }

        int depthSlice = ArrayUtil.binToWhichValueBelongs(zMin, zMax, zBinSize, zValue, true);
        // if the value falls above the gridded volume, put it in the first depth slice
        if (depthSlice < 0) {
            depthSlice = 0;
        }
        // if the value falls below the gridded volume, put it in the last depth slice
        if (depthSlice >= numberOfDepthSlices) {
            depthSlice = numberOfDepthSlices - 1;
        }

        int timeSlice = ArrayUtil.binToWhichValueBelongs(tMin, tMax, tBinSize, tValue, true);
        // if the value falls before the gridded volume, put it in the first time slice
        if (timeSlice < 0) {
            timeSlice = 0;
        }
        // if the value falls after the gridded volume, put it in the last time slice
        if (timeSlice >= numberOfTimeSlices) {
            timeSlice = numberOfTimeSlices - 1;
        }

        // transform the (col, row, depthSlice, timeSlice) point into the voxel number using the convention that we increment by time slice, then by depth slice, then by row,
        // then by column
        int voxel = column * numberOfRows * numberOfDepthSlices * numberOfTimeSlices + row * numberOfDepthSlices * numberOfTimeSlices + depthSlice * numberOfTimeSlices + timeSlice;
        return voxel;
    }
}
