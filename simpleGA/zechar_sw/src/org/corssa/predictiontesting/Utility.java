package org.corssa.predictiontesting;

import java.util.Random;
import java.io.OutputStreamWriter;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.io.File;

/**
 * @author J. Douglas Zechar zechar at usc.edu
 */
public class Utility {

    public static String SEP = File.separator; // the platform-dependent directory name separator

    /**
     * Count the number of events in the specified catalog
     *
     * @param catalogFile path to catalog of interest
     * @return the number of events in the catalog
     */
    public static int numberOfEventsInCatalog(String catalogFile) {
        int numberOfEvents = 0;

        try {
            String sRecord = null;

            // Get a handle to the catalog file
            FileInputStream oFIS = new FileInputStream(catalogFile);
            BufferedInputStream oBIS = new BufferedInputStream(oFIS);
            BufferedReader oReader = new BufferedReader(new InputStreamReader(oBIS));

            // pass through the catalog and bin each event
            while ((sRecord = oReader.readLine()) != null) {
                while (Character.isLetter(sRecord.charAt(0))) {
                    sRecord = oReader.readLine();

                    if (sRecord == null) {
                        break;
                    }
                }
                if (sRecord == null) {
                    break;
                }
                numberOfEvents++;
            }
            oReader.close();
            oBIS.close();
            oFIS.close();
        } catch (Exception ex) {
            System.out.println("Error in Utility.getNumberOfEventsInCatalog(" + catalogFile + ")");
            ex.printStackTrace();
            System.exit(-1);
        }
        return numberOfEvents;
    }

    /**
     * Bin the given catalog into the given lat/lon/mag grid.  The result is a grid with the number of epicenters occurring in each grid box.
     *
     * @param catalogOfInterest eqk catalog
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize spatial grid spacing
     * @param minMag minimum magnitude event to include
     * @param maxMag minimum magnitude event to include
     * @param magSpacing size of magnitude cells
     * @return array representing the grid with each entry denoting the number of epicenters occuring in the grid box
     */
    public static short[] eventMapFromCatalog(Catalog catalogOfInterest, float minLat, float maxLat, float minLon, float maxLon, float boxSize, float minMag,
            float maxMag, float magSpacing) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        int numberOfMagBoxes = Math.round((maxMag - minMag) / magSpacing);
        short[] eventMap = new short[numberOfLatBoxes * numberOfLonBoxes * numberOfMagBoxes];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        float[] mags = catalogOfInterest.mags();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);
            int magPosition = ArrayUtil.binToWhichValueBelongs(minMag, maxMag, magSpacing, mags[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1 && magPosition > -1) {
                int cellPosition = latPosition * numberOfLonBoxes * numberOfMagBoxes + lonPosition * numberOfMagBoxes + magPosition;
                // add this event in the appropriate box
                eventMap[cellPosition]++;
            }
        }
        return eventMap;
    }

    /**
     * Bin the given catalog into the given grid.  The result is a grid with the number of epicenters occurring in each grid box.  We save these values in a formatted file.
     *
     * @param catalogOfInterest eqk catalog
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @param afvFile path to file we'll save
     */
    public static void eventMapFromCatalog(Catalog catalogOfInterest, float minLat, float maxLat, float minLon, float maxLon, float boxSize, String afvFile) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        int[][] eventMap = new int[numberOfLatBoxes][numberOfLonBoxes];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                // add this event in the appropriate box
                eventMap[latPosition][lonPosition]++;
            }
        }
        try {
            // Write out the afv values to a file
            FileOutputStream oOutFIS = new FileOutputStream(afvFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This is an RI AFV file created automatically by  Utility.eventMapFromCatalog with the following parameters:\n");
            oWriter.write("catalog=unknown\n");
            oWriter.write("minLat=" + minLat + "\n");
            oWriter.write("maxLat=" + maxLat + "\n");
            oWriter.write("minLon=" + minLon + "\n");
            oWriter.write("maxLon=" + maxLon + "\n");
            oWriter.write("boxSize=" + boxSize + "\n");
            oWriter.write("minMag=1\n");
            oWriter.write("maxMag=1\n");
            oWriter.write("magSize=1");

            int numberOfLats = eventMap.length;
            int numberOfLons = eventMap[0].length;
            for (int i = 0; i < numberOfLats; i++) {
                float lat = minLat + boxSize * i;
                for (int j = 0; j < numberOfLons; j++) {
                    float lon = minLon + boxSize * j;
                    oWriter.write("\n" + lon + "\t" + lat + "\t" + eventMap[i][j]);
                }
            }

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

        } catch (Exception ex) {
            System.out.println("Error in Utility.getEventMapFromCatalog()");
            ex.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Given the specified grid parameters, determine the latitude/longitude at the specified grid position.
     *
     * @param cellPosition integer position w/i the grid
     * @param minLat minimum latitude of the grid
     * @param minLon minimum longitude of the grid
     * @param maxLon maximum longitude of the grid
     * @param boxSize grid spacing
     * @return 2 element array containing
     * [0] = latitude at grid position
     * [1] = longitude at grid position
     */
    public static float[] latlonFromCellPosition(int cellPosition, float minLat, float minLon, float maxLon, float boxSize) {
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        int latPosition = cellPosition / numberOfLonBoxes;
        int lonPosition = cellPosition % numberOfLonBoxes;

        float lat = minLat + latPosition * boxSize;
        float lon = minLon + lonPosition * boxSize;
        float[] latLon = {lat, lon};
        return latLon;
    }

    /**
     * Given the specified grid parameters, determine the latitude/longitude/magnitude at the specified grid position.
     *
     * @param cellPosition integer position w/i the grid
     * @param minLat minimum latitude of the grid
     * @param maxLat maximum latitude of the grid
     * @param minLon minimum longitude of the grid
     * @param maxLon maximum longitude of the grid
     * @param minMag minimum magnitude of the grid
     * @param spatialCellSize spatial grid spacing
     * @param magCellSize magnitude grid spacing
     * @return 3 element array containing
     * [0] = latitude at grid position
     * [1] = longitude at grid position
     * [2] = magnitude at grid position
     */
    public static float[] latlonMagFromCellPosition(int cellPosition, float minLat, float maxLat, float minLon, float maxLon, float minMag, float spatialCellSize,
            float magCellSize) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / spatialCellSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / spatialCellSize);

        int magPosition = cellPosition / (numberOfLonBoxes * numberOfLatBoxes);
        int latPosition = (cellPosition - (magPosition * numberOfLatBoxes * numberOfLonBoxes)) / numberOfLonBoxes;
        int lonPosition = cellPosition % numberOfLonBoxes;

        float lat = minLat + latPosition * spatialCellSize;
        float lon = minLon + lonPosition * spatialCellSize;
        float mag = minMag + magPosition * magCellSize;
        float[] latLonMag = {lat, lon, mag};
        return latLonMag;
    }

    /**
     * Bin the given epicenters into the given grid.  The result is a grid with the number of epicenters occurring in each grid box.
     *
     * @param eqkLats array of eqk epicenter latitudes
     * @param eqkLons array of eqk epicenter longitudes
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @return array representing the grid with each entry denoting the number of epicenters occuring in the grid box
     */
    public static short[] eventMapFromCatalog(float[] eqkLats, float[] eqkLons, float minLat, float maxLat, float minLon, float maxLon, float boxSize) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        short[] eventMap = new short[numberOfLatBoxes * numberOfLonBoxes];

        int numberOfEqks = eqkLats.length;

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, eqkLats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, eqkLons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                int cellPosition = latPosition * numberOfLonBoxes + lonPosition;
                // add this event in the appropriate box
                if (cellPosition > eventMap.length) {
                    System.out.println("what?");
                    latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, eqkLats[i], false);
                    lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, eqkLons[i], false);
                }
                eventMap[cellPosition]++;
            }
        }
        return eventMap;
    }

    /**
     * Given the specified grid parameters, determine the depth/latitude/longitude/magnitude at the specified voxel.  Here, we assume that voxels are determined by 
     *      depth   lat     lon     mag
     *
     * @param voxel integer position w/i the 4D grid
     * @param minDepth minimum depth of the grid
     * @param minLat minimum latitude of the grid
     * @param maxLat maximum latitude of the grid
     * @param minLon minimum longitude of the grid
     * @param maxLon maximum longitude of the grid
     * @param minMag minimum magnitude of the grid
     * @param minMag minimum magnitude of the grid     
     * @param depthDiscretization spacing of depths w/i grid
     * @param latDiscretization spacing of latitudes w/i grid
     * @param lonDiscretization spacing of longitudes w/i grid
     * @param magDiscretization spacing of magnitudes w/i grid
     * @return 4 element array containing
     * [0] = depth at specified voxel
     * [1] = latitude at specified voxel
     * [2] = longitude at specified voxel
     * [3] = magnitude at specified voxel
     */
    public static float[] depthLatLonMagFromVoxel(int voxel, float minDepth, float minLat, float maxLat, float minLon, float maxLon, float minMag, float maxMag,
            float depthDiscretization, float latDiscretization, float lonDiscretization, float magDiscretization) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / latDiscretization);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / lonDiscretization);
        int numberOfMagBoxes = Math.round((maxMag - minMag) / magDiscretization);

        int depthBox = voxel / (numberOfLatBoxes * numberOfLonBoxes * numberOfMagBoxes);
        voxel -= depthBox * (numberOfLatBoxes * numberOfLonBoxes * numberOfMagBoxes);
        int latBox = voxel / (numberOfLonBoxes * numberOfMagBoxes);
        voxel -= latBox * (numberOfLonBoxes * numberOfMagBoxes);
        int lonBox = voxel / numberOfMagBoxes;
        int magBox = voxel % numberOfMagBoxes;

        float depth = minDepth + depthBox * depthDiscretization;
        float lat = minLat + latBox * latDiscretization;
        float lon = minLon + lonBox * lonDiscretization;
        float mag = minMag + magBox * magDiscretization;

        float[] depthLatLonMag = {depth, lat, lon, mag};
        return depthLatLonMag;
    }

    /**
     * For the gridding used by the reference forecast, generate a random forecast: for each active bin in this forecast, set the forecast value to a random number b/w 0 and 1
     * 
     * @param referenceForecast reference forecast values, where inactive bins are marked by having a forecast of -Infinity
     * @param seed value w/ which to seed the random number generator
     * @return a random rate forecast
     */
    public static float[] randomForecast(float[] referenceForecast, long seed) {
        float[] randomForecast = new float[referenceForecast.length];
        Random rndgen = new Random(seed);
        for (int i = 0; i < referenceForecast.length; i++) {
            if (referenceForecast[i] > Float.NEGATIVE_INFINITY) {
                randomForecast[i] = rndgen.nextFloat();
            } else {
                randomForecast[i] = Float.NEGATIVE_INFINITY;
            }
        }
        return randomForecast;
    }
    
    /**
     * Determine the overlap b/w the two specified forecasts.  Modify each forecast so that they only have forecast rates in the overlapping region.
     * 
     * @param forecast1 first forecast of interest
     * @param forecast2 second forecast of interest
     */
    public static boolean[] determineForecastOverlapFilter(boolean[] filter, float[] forecastValues){
//        System.out.println("Filter length: " + filter.length + ", " + forecastValues.length);
        for (int i = 0; i < forecastValues.length;i++){
            if (forecastValues[i] == Float.NEGATIVE_INFINITY){
                filter[i] = false;
            }
        }
        return filter;
    }
}