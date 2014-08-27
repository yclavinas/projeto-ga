package org.corssa.predictiontesting;

import java.util.Random;
import java.util.Arrays;

/**
 * @author J. Douglas Zechar zechar at usc.edu
 */
public class ArrayUtil {

    public ArrayUtil() {
    }

    /**
     * Generate an array with n random integers from {1, 2,..., x}, sorted in
     * increasing order, using random numbers from the specified generator seed
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
     * Normalize the specified array so that the sum of its values is unity, 
     * disregarding any negative entries. We do this by finding the sum of the
     * original contents and dividing each entry by this sum
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
     * Compute sum of array values, returning an int in case the sum of the
     * shorts exceeds the maximum short.
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
        int numberOfEntriesGreaterThanZero =
                ArrayUtil.numberOfPositiveEntries(array);
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
    public static int binToWhichValueBelongs(float gridMin, float gridMax,
            float binSize, float value, boolean allowOverflow) {
        int bigNumber = 10000;

        // Scale the minimum bin value.  To avoid rounding errors, we floor the 
        // absolute value of the scaled value, then multiply this by the sign
        // of the original value
        int min_int = (int) (Math.signum(gridMin) *
                (float) Math.floor(Math.abs(gridMin * bigNumber)));
        // Scale the cell size.
        int cellSize_int = Math.round(binSize * bigNumber);
        //  Scale the value to be binned.  Avoid rounding errors as above
        int value_int = (int) (Math.signum(value) * (float) Math.floor(
                Math.abs(value * bigNumber)));
//        int value_int = (int) Math.floor(value * bigNumber);
        if ((value < gridMin) || (value >= gridMax) && !allowOverflow) {
            return -1;
        }
        float position_f = (float) (value_int - min_int) / (float) cellSize_int;
        int position = (int) Math.floor(position_f);
        return position;
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
    public static int cellToWhichValueBelongs(float xMin, float xMax, 
            float yMin, float yMax, float xBinSize, float yBinSize,
            float xValue, float yValue) {
        int numberOfColumns = Math.round((xMax - xMin) / xBinSize);
        int numberOfRows = Math.round((yMax - yMin) / yBinSize);

        int column = ArrayUtil.binToWhichValueBelongs(xMin, xMax, xBinSize,
                xValue, true);
        // if the value falls outside the grid to the west, put it in the
        // first column
        if (column < 0) {
            column = 0;
        }
        // if the value falls outside the grid to the east, put it in the last
        // column
        if (column >= numberOfColumns) {
            column = numberOfColumns - 1;
        }

        int row = ArrayUtil.binToWhichValueBelongs(yMin, yMax, yBinSize,
                yValue, true);
        // if the value falls outside the grid to the south, put it in the
        // first row
        if (row < 0) {
            row = 0;
        }
        // if the value falls outside the grid to the north, put it in the
        // last row
        if (row >= numberOfRows) {
            row = numberOfRows - 1;
        }

        // transform the (row, col) point into the cell number
        int cell = row * numberOfColumns + column;
        return cell;
    }

    /**
     * Given a 3D gridding specified by minimum values, maximum values, and grid
     * sizes, determine to which grid box a given (xValue, yValue, zValue)
     * belongs.  We do this by determining the appropriate row/column/depth
     * based on the respective discretization, then we map this to a box number.
     * We deal with values that don't fit into the grid by bringing them to the
     * closest box inside the grid.  For example, if a value falls to the "west"
     * of the beginning of the 24th row, we bin this value into the first column
     * of the 24th row.  If the value falls to the east of the 17th row, we bin
     * it into the last column of the 17th row.  The same method is applied to
     * values north or south of the grid, or above or below the grid.
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
    public static int boxToWhichValueBelongs(float xMin, float xMax, float yMin,
            float yMax, float zMin, float zMax, float xBinSize, float yBinSize,
            float zBinSize, float xValue, float yValue, float zValue) {
        int numCols = Math.round((xMax - xMin) / xBinSize);
        int numRows = Math.round((yMax - yMin) / yBinSize);
        int numDepthSlices = Math.round((zMax - zMin) / zBinSize);

        int col = ArrayUtil.binToWhichValueBelongs(xMin, xMax, xBinSize,
                xValue, true);

        // if the value falls outside the grid to the west, put it in the
        // first column
        if (col < 0) {
            col = 0;
        }
        // if the value falls outside the grid to the east, put it in the
        // last column
        if (col >= numCols) {
            col = numCols - 1;
        }

        int row = ArrayUtil.binToWhichValueBelongs(yMin, yMax, yBinSize,
                yValue, true);
        // if the value falls outside the grid to the south, put it in the
        // first row
        if (row < 0) {
            row = 0;
        }
        // if the value falls outside the grid to the north, put it in the
        // last row
        if (row >= numRows) {
            row = numRows - 1;
        }

        int slice = ArrayUtil.binToWhichValueBelongs(zMin, zMax, zBinSize,
                zValue, true);
        // if the value falls above the gridded volume, put it in the
        // first depth slice
        if (slice < 0) {
            slice = 0;
        }
        // if the value falls below the gridded volume, put it in the
        // last depth slice
        if (slice >= numDepthSlices) {
            slice = numDepthSlices - 1;
        }

        // transform the (row, col, slice) point into the box number using the
        // convention that we increment by column, then by row, then by depth
        // slice indicating that
        // box = slice * numCols * numRows + row * numCols + col
        int box = slice * numCols * numRows + row * numCols + col;
        return box;
    }

    /**
     * Given a 2D gridding specified by minimum values, maximum values, and
     * grid sizes, determine the x/y indices corresponding to the specified
     * cell number.  We do this by determining the appropriate row and
     * appropriate column based on their respective discretization, then we map
     * this row and column to x/y based on the grid specification.
     *
     * @param xMin minimum x value
     * @param xMax maximum x value
     * @param yMin minimum y value
     * @param yMax maximum y value
     * @param xBinSize discretization in x direction
     * @param yBinSize discretization in y direction
     * @param cell cell index in which we're interested
     * @return an array of x/y coordinates corresponding to the minimum (x, y)
     *          value of specified cell, of the format
     *      [0] = x value
     *      [1] = y value
     */
    public static float[] arrayIndicesCorrespondingToCell(float xMin, 
            float xMax, float yMin, float yMax, float xBinSize, float yBinSize,
            int cell) {
        int numberOfColumns = Math.round((xMax - xMin) / xBinSize);
        int rowIndex = cell / numberOfColumns;
        int colIndex = cell - rowIndex * numberOfColumns;

        float xValue = xMin + colIndex * xBinSize;
        float yValue = yMin + rowIndex * yBinSize;

        float[] results = {xValue, yValue};
        return results;
    }

    /**
     * Given a 4D gridding specified by minimum values, maximum values, and
     * grid sizes, determine the col/row/depth/time indices corresponding to the specified
     * voxel number.
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
     * @param voxel voxel index in which we're interested
     * @return an array  indicating the corresponding indices
     *      [0] = time index (least significant)
     *      [1] = depth index
     *      [2] = row index
     *      [3] = col index (most significant)
     */
    public static int[] arrayIndicesCorrespondingToVoxel(float xMin,
            float xMax, float yMin, float yMax, float zMin, float zMax, float tMin, float tMax,
            float xBinSize, float yBinSize, float zBinSize, float tBinSize, int voxel) {
        int numberOfRows = Math.round((yMax - yMin) / yBinSize);
        int numberOfDepthSlices = Math.round((zMax - zMin) / zBinSize);
        int numberOfTimeSlices = Math.round((tMax - tMin) / tBinSize);

        int colIndex = voxel / numberOfRows / numberOfDepthSlices / numberOfTimeSlices;
        int rowIndex = (voxel - colIndex * numberOfRows * numberOfDepthSlices * numberOfTimeSlices)  /
                (numberOfDepthSlices * numberOfTimeSlices);
        int depthSliceIndex = (voxel -
                colIndex * numberOfRows * numberOfDepthSlices * numberOfTimeSlices -
                rowIndex * numberOfDepthSlices * numberOfTimeSlices)  /
                numberOfTimeSlices;
        int timeSliceIndex = voxel % numberOfTimeSlices;

        int[] results = {timeSliceIndex, depthSliceIndex, rowIndex, colIndex};
        return results;
    }

    /**
     * Given a 4D gridding specified by minimum values, maximum values, and grid
     * sizes, determine to which grid box a given (xValue, yValue, zValue)
     * belongs.  We do this by determining the appropriate row/column/depth/
     * timestep based on the respective discretization, then we map this to a
     * voxel number.  We deal with values that don't fit into the grid by
     * bringing them to the closest box inside the grid.  For example, if a
     * value falls to the "west" of the beginning of the 24th row, we bin this
     * value into the first column of the 24th row.  If the value falls to the
     * east of the 17th row, we bin it into the last column of the 17th row.
     * The same method is applied to values north or south of the grid, or above
     * or below the grid, or before or after the grid.
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
    public static int voxelToWhichValueBelongs(float xMin, float xMax,
            float yMin, float yMax, float zMin, float zMax, float tMin,
            float tMax, float xBinSize, float yBinSize, float zBinSize,
            float tBinSize, float xValue, float yValue, float zValue,
            float tValue) {
        int numberOfColumns = Math.round((xMax - xMin) / xBinSize);
        int numRows = Math.round((yMax - yMin) / yBinSize);
        int numDepthSlices = Math.round((zMax - zMin) / zBinSize);
        int numTimeSlices = Math.round((tMax - tMin) / tBinSize);

        int col = ArrayUtil.binToWhichValueBelongs(xMin, xMax, xBinSize,
                xValue, true);
        // if the value falls outside the grid to the west, put it in the
        // first column
        if (col < 0) {
            col = 0;
        }
        // if the value falls outside the grid to the east, put it in the
        // last column
        if (col >= numberOfColumns) {
            col = numberOfColumns - 1;
        }

        int row = ArrayUtil.binToWhichValueBelongs(yMin, yMax, yBinSize,
                yValue, true);
        // if the value falls outside the grid to the south, put it in the
        // first row
        if (row < 0) {
            row = 0;
        }
        // if the value falls outside the grid to the north, put it in the
        // last row
        if (row >= numRows) {
            row = numRows - 1;
        }

        int depthSlice = ArrayUtil.binToWhichValueBelongs(zMin, zMax, zBinSize,
                zValue, true);
        // if the value falls above the gridded volume, put it in the
        // first depth slice
        if (depthSlice < 0) {
            depthSlice = 0;
        }
        // if the value falls below the gridded volume, put it in the
        // last depth slice
        if (depthSlice >= numDepthSlices) {
            depthSlice = numDepthSlices - 1;
        }

        int timeSlice = ArrayUtil.binToWhichValueBelongs(tMin, tMax, tBinSize,
                tValue, true);
        // if the value falls before the gridded volume, put it in the
        // first time slice
        if (timeSlice < 0) {
            timeSlice = 0;
        }
        // if the value falls after the gridded volume, put it in the
        // last time slice
        if (timeSlice >= numTimeSlices) {
            timeSlice = numTimeSlices - 1;
        }

        // transform the (col, row, depthSlice, timeSlice) point into the voxel
        // number using the convention that we increment by time slice, then by
        // depth slice, then by row, then by column
        int voxel = col * numRows * numDepthSlices * numTimeSlices +
                row * numDepthSlices * numTimeSlices +
                depthSlice * numTimeSlices +
                timeSlice;
        return voxel;
    }
}
