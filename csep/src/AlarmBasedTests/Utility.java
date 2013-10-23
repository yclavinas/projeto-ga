import java.util.Random;
import java.io.OutputStreamWriter;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.util.Calendar;
import java.io.File;

public class Utility {

    public static String SEP = File.separator; // the platform-dependent directory name separator

    public static final short NORTH_CONTAINING = 1;
    public static final short SOUTH_CONTAINING = 2;
    public static final short EAST_CONTAINING = 3;
    public static final short WEST_CONTAINING = 4;
    public static final short NORTHWEST = 5;
    public static final short NORTHEAST = 6;
    public static final short SOUTHEAST = 7;
    public static final short SOUTHWEST = 8;
    public static final short CONTAINED = 9;
    public static final short CONTAINING = 10;
    public static final short NO_OVERLAP = 11;
    public static final short NORTH_CONTAINED = 12;
    public static final short SOUTH_CONTAINED = 13;
    public static final short EAST_CONTAINED = 14;
    public static final short WEST_CONTAINED = 15;

    /**
     * Bin the given catalog into the given grid.  The result is a grid with the number of epicenters occurring in each grid box. USE THIS IMPLEMENTATION ONLY IF THE 
     * CATALOG IS NOT ALREADY IN MEMORY!
     *
     * @param catalogFile path to eqk catalog (must be JEREMY_GENERATED)
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @return array representing the grid with each entry denoting the number of epicenters occuring in the grid box
     */
    public static short[] eventMapFromCatalog(String catalogFile, float minLat, float maxLat, float minLon, float maxLon, float boxSize) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        short[] eventMap = new short[numberOfLatBoxes * numberOfLonBoxes];

        Catalog catalogOfInterest = new Catalog(catalogFile, Catalog.JEREMY_GENERATED);
        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                int cellPosition = latPosition * numberOfLonBoxes + lonPosition;
                // add this event in the appropriate box
                eventMap[cellPosition]++;
            }
        }
        return eventMap;
    }

    /**
     * Bin the given catalog into the given grid.  The result is a grid with the number of epicenters occurring in each grid box.  We save these values in a formatted file.  USE 
     * THIS IMPLEMENTATION ONLY IF THE CATALOG IS NOT ALREADY IN MEMORY!
     *
     * @param catalogFile path to eqk catalog (must be JEREMY_GENERATED)
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @param afvFile path to file we'll save
     */
    public static void eventMapFromCatalog(String catalogFile, float minLat, float maxLat, float minLon, float maxLon, float boxSize, String afvFile) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        int[][] eventMap = new int[numberOfLatBoxes][numberOfLonBoxes];

        Catalog catalogOfInterest = new Catalog(catalogFile, Catalog.JEREMY_GENERATED);
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

            oWriter.write("This is an RI AFV file created automatically by Utility.eventMapFromCatalog with the following parameters:\n");
            oWriter.write("catalog=" + catalogFile + "\n");
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
            System.out.println("Error in Utility.getEventMapFromCatalog(" + catalogFile + ")");
            ex.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Bin the given catalog into the given grid.  The result is a grid with the approximated scaled energy release occurring in each grid box.  We also save the values in a 
     * formatted file. USE THIS IMPLEMENTATION ONLY IF THE CATALOG IS NOT ALREADY IN MEMORY!
     *
     * @param catalogFile path to eqk catalog (must be JEREMY_GENERATED)
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @param afvFile path to file we'll save
     * @param minMag reference magnitude to which catalog magnitudes will be compared (in order to compute relative energy release)
     */
    public static void energyMapFromCatalog(String catalogFile, float minLat, float maxLat, float minLon, float maxLon, float boxSize, String afvFile, float minMag) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        float[][] energyMap = new float[numberOfLatBoxes][numberOfLonBoxes];

        Catalog catalogOfInterest = new Catalog(catalogFile, Catalog.JEREMY_GENERATED);
        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        float[] mags = catalogOfInterest.mags();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                // We follow the rule of thumb that, for every unit increase in magnitude, energy increases 32 times.  In our case, an event w/ magnitude minMag will have 
                //                energy=1.0.
                float energy = (float) Math.pow(32.0, (double) (mags[i] - minMag));
                // add the energy of this event in the appropriate box
                energyMap[latPosition][lonPosition] += energy;
            }
        }
        try {
            // Write out the afv values to a file
            FileOutputStream oOutFIS = new FileOutputStream(afvFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This is an RE AFV file created automatically by Utility.getEnergyMapFromCatalog with the following parameters:\n");
            oWriter.write("catalog=" + catalogFile + "\n");
            oWriter.write("minLat=" + minLat + "\n");
            oWriter.write("maxLat=" + maxLat + "\n");
            oWriter.write("minLon=" + minLon + "\n");
            oWriter.write("maxLon=" + maxLon + "\n");
            oWriter.write("boxSize=" + boxSize + "\n");
            oWriter.write("minMag=1\n");
            oWriter.write("maxMag=1\n");
            oWriter.write("magSize=1");

            int numberOfLats = energyMap.length;
            int numberOfLons = energyMap[0].length;
            for (int i = 0; i < numberOfLats; i++) {
                float lat = minLat + boxSize * i;
                for (int j = 0; j < numberOfLons; j++) {
                    float lon = minLon + boxSize * j;
                    oWriter.write("\n" + lon + "\t" + lat + "\t" + energyMap[i][j]);
                }
            }

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

        } catch (Exception ex) {
            System.out.println("Error in Utility.getEnergyMapFromCatalog(" + catalogFile + ")");
            ex.printStackTrace();
            System.exit(-1);
        }
    }

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
     * Bin the eqks into the given grid and print the grid contents.
     *
     * @param eqkCatalog catalog file (of type JEREMY_GENERATED)
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize length of the side of one grid box
     */
    public static void printCatalogSpatialDistribution(String eqkCatalog, float minLat, float maxLat, float minLon, float maxLon, float boxSize) {
        short[] eqkMap = Utility.eventMapFromCatalog(eqkCatalog, minLat, maxLat, minLon, maxLon, boxSize);

        System.out.println("lon\tlat\t# eqks\n========================");

        for (int i = 0; i < eqkMap.length; i++) {
            float[] latlon = Utility.latlonFromCellPosition(i, minLat, minLon, maxLon, boxSize);

            float lat = latlon[0];
            float lon = latlon[1];

            System.out.println(lon + "\t" + lat + "\t" + eqkMap[i]);
        }
    }

    /**
     * Bin the given catalog into the given lat/lon/mag grid.  The result is a grid with the number of epicenters occurring in each grid box. USE THIS IMPLEMENTATION ONLY 
     * IF THE CATALOG IS NOT ALREADY IN MEMORY!
     *
     * @param catalogFile path to eqk catalog (must be JEREMY_GENERATED)
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
    public static short[] eventMapFromCatalog(String catalogFile, float minLat, float maxLat, float minLon, float maxLon, float boxSize, float minMag, float maxMag,
            float magSpacing) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        int numberOfMagBoxes = Math.round((maxMag - minMag) / magSpacing);
        short[] eventMap = new short[numberOfLatBoxes * numberOfLonBoxes * numberOfMagBoxes];

        Catalog catalogOfInterest = new Catalog(catalogFile, Catalog.JEREMY_GENERATED);
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
     * Bin the given catalog into the given grid.  The result is a grid with the time-weighted epicenters occurring in each grid box.  We also save the values in a formatted file.  
     * Each epicenter is weighted by the inverse length of time b/w its origin time and the final time in the catalog.  USE THIS IMPLEMENTATION ONLY IF THE CATALOG IS 
     * NOT ALREADY IN MEMORY!
     *
     * @param catalogFile path to eqk catalog (must be JEREMY_GENERATED)
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @param afvFile path to file we'll save
     */
    public static void eventMapTimeWeightedFromCatalog(String catalogFile, float minLat, float maxLat, float minLon, float maxLon, float boxSize, String afvFile) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        float[][] timeWeightedEventMap = new float[numberOfLatBoxes][numberOfLonBoxes];

        Catalog catalogOfInterest = new Catalog(catalogFile, Catalog.JEREMY_GENERATED);
        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        String[] times = catalogOfInterest.times();
        String finalEventTime = DateUtil.offsetDate(times[times.length], Calendar.DATE, 1);

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                float daysSinceEqk = DateUtil.durationInOrderedDays(times[i], finalEventTime);
                float timeWeight = 1.0f / daysSinceEqk;
                // add the time-weighted event in the appropriate box
                timeWeightedEventMap[latPosition][lonPosition] += timeWeight;
            }
        }

        try {
            // Write out the alarm function values to a file
            FileOutputStream oOutFIS = new FileOutputStream(afvFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This is an RI time-weighted file created automatically by Utility.eventMapTimeWeightedFromCatalog with the following parameters:\n");
            oWriter.write("catalog=" + catalogFile + "\n");
            oWriter.write("minLat=" + minLat + "\n");
            oWriter.write("maxLat=" + maxLat + "\n");
            oWriter.write("minLon=" + minLon + "\n");
            oWriter.write("maxLon=" + maxLon + "\n");
            oWriter.write("boxSize=" + boxSize + "\n");
            oWriter.write("minMag=1\n");
            oWriter.write("maxMag=1\n");
            oWriter.write("magSize=1");

            int numberOfLats = timeWeightedEventMap.length;
            int numberOfLons = timeWeightedEventMap[0].length;
            for (int i = 0; i < numberOfLats; i++) {
                float lat = minLat + boxSize * i;
                for (int j = 0; j < numberOfLons; j++) {
                    float lon = minLon + boxSize * j;
                    oWriter.write("\n" + lon + "\t" + lat + "\t" + timeWeightedEventMap[i][j]);
                }
            }

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

        } catch (Exception ex) {
            System.out.println("Error in Utility.eventMapTimeWeightedFromCatalog(" + catalogFile + ")");
            ex.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Bin the given catalog into the given grid.  The result is a grid with the approximated scaled energy release occurring in each grid box.  We also save the values in a 
     * formatted file.
     *
     * @param catalogOfInterest eqk catalog
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @param afvFile path to file we'll save
     * @param minMag reference magnitude to which catalog magnitudes will be compared (in order to compute relative energy release)
     */
    public static void energyMapFromCatalog(Catalog catalogOfInterest, float minLat, float maxLat, float minLon, float maxLon, float boxSize, String afvFile,
            float minMag) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        float[][] energyMap = new float[numberOfLatBoxes][numberOfLonBoxes];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        float[] mags = catalogOfInterest.mags();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                // We follow the rule of thumb that, for every unit increase in magnitude, energy increases 32 times.  In our case, an event w/ magnitude minMag will have 
                //                energy=1.0.
                float energy = (float) Math.pow(32.0, (double) (mags[i] - minMag));
                // add the energy of this event in the appropriate box
                energyMap[latPosition][lonPosition] += energy;
            }
        }
        try {
            // Write out the afv values to a file
            FileOutputStream oOutFIS = new FileOutputStream(afvFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This is an RE RPF file created automatically by Utility.getEnergyMapFromCatalog with the following parameters:\n");
            oWriter.write("catalog=unknown\n");
            oWriter.write("minLat=" + minLat + "\n");
            oWriter.write("maxLat=" + maxLat + "\n");
            oWriter.write("minLon=" + minLon + "\n");
            oWriter.write("maxLon=" + maxLon + "\n");
            oWriter.write("boxSize=" + boxSize + "\n");
            oWriter.write("minMag=1\n");
            oWriter.write("maxMag=1\n");
            oWriter.write("magSize=1");

            int numberOfLats = energyMap.length;
            int numberOfLons = energyMap[0].length;
            for (int i = 0; i < numberOfLats; i++) {
                float lat = minLat + boxSize * i;
                for (int j = 0; j < numberOfLons; j++) {
                    float lon = minLon + boxSize * j;
                    oWriter.write("\n" + lon + "\t" + lat + "\t" + energyMap[i][j]);
                }
            }

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

        } catch (Exception ex) {
            System.out.println("Error in Utility.getEnergyMapFromCatalog()");
            ex.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Bin the given catalog into the given grid.  The result is a grid with the number of epicenters occurring in each grid box.
     *
     * @param catalogOfInterest eqk catalog
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @return array representing the grid with each entry denoting the number of epicenters occuring in the grid box
     */
    public static short[] eventMapFromCatalog(CatalogNoTime catalogOfInterest, float minLat, float maxLat, float minLon, float maxLon, float boxSize) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        short[] eventMap = new short[numberOfLatBoxes * numberOfLonBoxes];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                int cellPosition = latPosition * numberOfLonBoxes + lonPosition;
                // add this event in the appropriate box
                if (cellPosition > eventMap.length) {
                    System.out.println("what?");
                    latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
                    lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);
                }
                eventMap[cellPosition]++;
            }
        }
        return eventMap;
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
     * Bin the given catalog into the given grid.  The result is a grid with the time-weighted epicenters occurring in each grid box.  We also save the values in a formatted file.  
     * Each epicenter is weighted by the inverse length of time b/w its origin time and the final time in the catalog.
     *
     * @param catalogOfInterest eqk catalog
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @param afvFile path to file we'll save
     */
    public static void eventMapTimeWeightedFromCatalog(Catalog catalogOfInterest, float minLat, float maxLat, float minLon, float maxLon, float boxSize,
            String afvFile) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        float[][] timeWeightedEventMap = new float[numberOfLatBoxes][numberOfLonBoxes];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        String[] times = catalogOfInterest.times();

        String finalEventTime = DateUtil.offsetDate(times[times.length - 1], Calendar.DATE, 1);

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                float daysSinceEqk = DateUtil.durationInOrderedDays(times[i], finalEventTime);
                float timeWeight = 1.0f / daysSinceEqk;
                // add the time-weighted event in the appropriate box
                timeWeightedEventMap[latPosition][lonPosition] += timeWeight;
            }
        }

        try {
            // Write out the alarm function values to a file
            FileOutputStream oOutFIS = new FileOutputStream(afvFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This is an RI time-weighted file created automatically by Utility.eventMapTimeWeightedFromCatalog with the following parameters:\n");
            oWriter.write("catalog=unknown\n");
            oWriter.write("minLat=" + minLat + "\n");
            oWriter.write("maxLat=" + maxLat + "\n");
            oWriter.write("minLon=" + minLon + "\n");
            oWriter.write("maxLon=" + maxLon + "\n");
            oWriter.write("boxSize=" + boxSize + "\n");
            oWriter.write("minMag=1\n");
            oWriter.write("maxMag=1\n");
            oWriter.write("magSize=1");

            int numberOfLats = timeWeightedEventMap.length;
            int numberOfLons = timeWeightedEventMap[0].length;
            for (int i = 0; i < numberOfLats; i++) {
                float lat = minLat + boxSize * i;
                for (int j = 0; j < numberOfLons; j++) {
                    float lon = minLon + boxSize * j;
                    oWriter.write("\n" + lon + "\t" + lat + "\t" + timeWeightedEventMap[i][j]);
                }
            }

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

        } catch (Exception ex) {
            System.out.println("Error in Utility.eventMapTimeWeightedFromCatalog()");
            ex.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Bin the given catalog into the grid.  The result is a grid with the approximated moment release occurring in each grid box.  We also save the values in a formatted file.
     *
     * @param catalogOfInterest eqk catalog
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize grid spacing
     * @param afvFile path to file we'll save
     */
    public static void momentMapFromCatalog(Catalog catalogOfInterest, float minLat, float maxLat, float minLon, float maxLon, float boxSize, String afvFile) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        float[][] momentMap = new float[numberOfLatBoxes][numberOfLonBoxes];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        float[] mags = catalogOfInterest.mags();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1) {
                // We follow the rule of thumb that, for every unit increase in magnitude, moment increases 32 times.  In our case, an event w/ magnitude minMag will have 
                //                moment=1.0.
                float moment = (float) Math.pow(10, (double) (1.5 * mags[i] + 6.067));
                // add the moment of this event in the appropriate box
                momentMap[latPosition][lonPosition] += moment;
            }
        }
        try {
            // Write out the afv values to a file
            FileOutputStream oOutFIS = new FileOutputStream(afvFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This is an RE RPF file created automatically by Utility.getEnergyMapFromCatalog with the following parameters:\n");
            oWriter.write("catalog=unknown\n");
            oWriter.write("minLat=" + minLat + "\n");
            oWriter.write("maxLat=" + maxLat + "\n");
            oWriter.write("minLon=" + minLon + "\n");
            oWriter.write("maxLon=" + maxLon + "\n");
            oWriter.write("boxSize=" + boxSize + "\n");
            oWriter.write("minMag=1\n");
            oWriter.write("maxMag=1\n");
            oWriter.write("magSize=1\n");

            int numberOfLats = momentMap.length;
            int numberOfLons = momentMap[0].length;
            for (int i = 0; i < numberOfLats; i++) {
                float lat = minLat + boxSize * i;
                for (int j = 0; j < numberOfLons; j++) {
                    float lon = minLon + boxSize * j;
                    oWriter.write("\n" + lon + "\t" + lat + "\t" + momentMap[i][j]);
                }
            }

            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();

        } catch (Exception ex) {
            System.out.println("Error in Utility.getEnergyMapFromCatalog()");
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
     * Given the two square specifications, determine the relative positioning and coverage of Square A and Square B.  There are eleven possible cases:
     *
     * 1. Square A falls is completely contained by Square B.
     * 2. Square A is partially covered by and NW of Square B.
     * 3. Square A is partially covered by and N of Square B.
     * 4. Square A is partially covered by and NE of Square B.
     * 5. Square A is partially covered by and W of Square B.
     * 6. Square A is partially covered by and E of Square B.
     * 7. Square A is partially covered by and SW of Square B.
     * 8. Square A is partially covered by and S of Square B.
     * 9. Square A is partially covered by and SE of Square B.
     *10. Square A completely contains Square B.
     *11. Square A and Square B have no overlap
     *
     * @param minX_a minimum x-value of Square A
     * @param maxX_a maximum x-value of Square A
     * @param minY_a minimum y-value of Square A
     * @param maxY_a maximum y-value of Square A
     * @param minX_b minimum x-value of Square B
     * @param maxX_b maximum x-value of Square B
     * @param minY_b minimum y-value of Square B
     * @param maxY_b maximum y-value of Square B
     * @return position of cell relative to kernel.
     */
    public static short positionOfSquareARelativeToSquareB(float minX_a, float maxX_a, float minY_a, float maxY_a, float minX_b, float maxX_b, float minY_b,
            float maxY_b) {
        // if each point of Square A is inside Square B, Square A is contained by Square B
        if (Utility.pointIsInsideSquare(minX_a, minY_a, minX_b, maxX_b, minY_b, maxY_b)) {
            if (Utility.pointIsInsideSquare(minX_a, maxY_a, minX_b, maxX_b, minY_b, maxY_b)) {
                if (Utility.pointIsInsideSquare(maxX_a, minY_a, minX_b, maxX_b, minY_b, maxY_b)) {
                    if (Utility.pointIsInsideSquare(maxX_a, maxY_a, minX_b, maxX_b, minY_b, maxY_b)) {
                        return Utility.CONTAINED;
                    }
                }
            }
        } // if each point of Square B is inside Square B, Square A contains Square B
        else if (Utility.pointIsInsideSquare(minX_b, minY_b, minX_a, maxX_a, minY_a, maxY_a)) {
            if (Utility.pointIsInsideSquare(minX_b, maxY_b, minX_a, maxX_a, minY_a, maxY_a)) {
                if (Utility.pointIsInsideSquare(maxX_b, minY_b, minX_a, maxX_a, minY_a, maxY_a)) {
                    if (Utility.pointIsInsideSquare(maxX_b, maxY_b, minX_a, maxX_a, minY_a, maxY_a)) {
                        return Utility.CONTAINING;
                    }
                }
            }
        } // If Square A's points are all east or all west or all north or all south of Square B's points, there is no overlap
        else if (minX_a >= maxX_b || maxX_a <= minX_b || minY_a >= maxY_b || maxY_a <= minY_b) {
            return Utility.NO_OVERLAP;
        }

        // Otherwise, there is some overlap, which we'll determine by comparing corners
        // If the NW corner of Square B is inside Square A, A is either N, W, or NW of Square B
        if (Utility.pointIsInsideSquare(minX_b, maxY_b, minX_a, maxX_a, minY_a, maxY_a)) { // NW point of B is inside A

            if (Utility.pointIsInsideSquare(maxX_b, maxY_b, minX_a, maxX_a, minY_a, maxY_a)) { // NE point of B is inside A

                return Utility.NORTH_CONTAINING;
            } else if (Utility.pointIsInsideSquare(minX_b, minY_b, minX_a, maxX_a, minY_a, maxY_a)) { // SW point of B is inside A

                return Utility.WEST_CONTAINING;
            } else {
                return Utility.NORTHWEST;
            }
        }
        // If the NE corner of Square B is inside Square A, A is either E or NE of Square B
        if (Utility.pointIsInsideSquare(maxX_b, maxY_b, minX_a, maxX_a, minY_a, maxY_a)) { // NE point of B is inside A

            if (Utility.pointIsInsideSquare(maxX_b, minY_b, minX_a, maxX_a, minY_a, maxY_a)) { // SE point of B is inside A

                return Utility.EAST_CONTAINING;
            } else {
                return Utility.NORTHEAST;
            }
        }
        // If the SW corner of Square B is inside Square A, A is either S or SW of Square B
        if (Utility.pointIsInsideSquare(minX_b, minY_b, minX_a, maxX_a, minY_a, maxY_a)) { // SW point of B is inside A

            if (Utility.pointIsInsideSquare(maxX_b, minY_b, minX_a, maxX_a, minY_a, maxY_a)) { // SE point of B is inside A

                return Utility.SOUTH_CONTAINING;
            } else {
                return Utility.SOUTHWEST;
            }
        }
        // If the SE corner of Square B is inside Square A, A is SE of Square B
        if (Utility.pointIsInsideSquare(maxX_b, minY_b, minX_a, maxX_a, minY_a, maxY_a)) { // SE point of B is inside A

            return Utility.SOUTHEAST;
        }

        // If the NW corner of Square A is inside Square B, A is either S, E, or SE of Square B
        if (Utility.pointIsInsideSquare(minX_a, maxY_a, minX_b, maxX_b, minY_b, maxY_b)) { // NW point of A is inside B

            if (Utility.pointIsInsideSquare(maxX_a, maxY_a, minX_b, maxX_b, minY_b, maxY_b)) { // NE point of A is inside B

                return Utility.SOUTH_CONTAINED;
            } else if (Utility.pointIsInsideSquare(minX_a, minY_a, minX_b, maxX_b, minY_b, maxY_b)) { // SW point of A is inside B

                return Utility.EAST_CONTAINED;
            } else {
                return Utility.SOUTHEAST;
            }
        }
        // If the NE corner of Square A is inside Square B, A is either W or SW of Square B
        if (Utility.pointIsInsideSquare(maxX_a, maxY_a, minX_b, maxX_b, minY_b, maxY_b)) { // NE point of A is inside B

            if (Utility.pointIsInsideSquare(maxX_a, minY_a, minX_b, maxX_b, minY_b, maxY_b)) { // SE point of A is inside B

                return Utility.WEST_CONTAINED;
            } else {
                return Utility.SOUTHWEST;
            }
        }
        // If the SW corner of Square A is inside Square B, A is either N or NE of Square B
        if (Utility.pointIsInsideSquare(minX_a, minY_a, minX_b, maxX_b, minY_b, maxY_b)) { // SW point of A is inside B

            if (Utility.pointIsInsideSquare(maxX_a, minY_a, minX_b, maxX_b, minY_b, maxY_b)) { // SE point of A is inside B

                return Utility.NORTH_CONTAINED;
            } else {
                return Utility.NORTHEAST;
            }
        }
        // If the SE corner of Square A is inside Square B, A is NW of Square B
        if (Utility.pointIsInsideSquare(maxX_a, minY_a, minX_b, maxX_b, minY_b, maxY_b)) { // SE point of A is inside B

            return Utility.NORTHWEST;
        }
        System.err.println("Big trouble in Little China");
        return 0;
    }

    /**
     * Given the specified point and specified square, determine whether the specified point is inside or outside the square
     *
     * @param point_x x-value of point
     * @param point_y y-value of point
     * @param minX_square minimum x-value of Square
     * @param maxX_square maximum x-value of Square
     * @param minY_square minimum y-value of Square
     * @param maxY_square maximum y-value of Square
     * @return answer to the question: is the point inside the square?
     */
    public static boolean pointIsInsideSquare(float point_x, float point_y, float minX_square, float maxX_square, float minY_square, float maxY_square) {
        if (point_x >= minX_square) {
            if (point_x <= maxX_square) {
                if (point_y >= minY_square) {
                    if (point_y <= maxY_square) {
                        return true;
                    }
                }
            }
        }
        return false;
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
     * Bin the given catalog into the given grid.  The result is a grid with the number of epicenters occurring in each grid box.
     *
     * @param catalogOfInterest eqk catalog
     * @param minLat minimum latitude of grid
     * @param maxLat maximum latitude of grid
     * @param minLon minimum longitude of grid
     * @param maxLon maximum longitude of grid
     * @param boxSize lat/lon grid spacing
     * @param minMag minimum magnitude of grid
     * @param maxMag maximum magnitude of grid
     * @param magSize magnitude grid spacing
     * @return array representing the grid with each entry denoting the number of epicenters occuring in the grid box
     */
    public static short[] eventMapFromCatalog(CatalogNoTime catalogOfInterest, float minLat, float maxLat, float minLon, float maxLon, float boxSize, float minMag,
            float maxMag, float magSize) {
        int numberOfLatBoxes = Math.round((maxLat - minLat) / boxSize);
        int numberOfLonBoxes = Math.round((maxLon - minLon) / boxSize);
        int numberOfMagBoxes = Math.round((maxMag - minMag) / magSize);
        short[] eventMap = new short[numberOfLatBoxes * numberOfLonBoxes * numberOfMagBoxes];

        int numberOfEqks = catalogOfInterest.numberOfEqks();
        float[] lats = catalogOfInterest.lats();
        float[] lons = catalogOfInterest.lons();
        float[] mags = catalogOfInterest.mags();

        for (int i = 0; i < numberOfEqks; i++) {
            int latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
            int lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);
            int magPosition = ArrayUtil.binToWhichValueBelongs(minMag, maxMag, magSize, mags[i], false);

            // check to make sure this event is in the study region
            if (latPosition > -1 && lonPosition > -1 && magPosition > -1) {
                int cellPosition = ArrayUtil.boxToWhichValueBelongs(minLon, maxLon, minLat, maxLat, minMag, maxMag, boxSize, boxSize, magSize, lons[i], lats[i], mags[i]);

                // add this event in the appropriate box
                if (cellPosition > eventMap.length) {
                    System.out.println("what?");
                    latPosition = ArrayUtil.binToWhichValueBelongs(minLat, maxLat, boxSize, lats[i], false);
                    lonPosition = ArrayUtil.binToWhichValueBelongs(minLon, maxLon, boxSize, lons[i], false);
                }
                eventMap[cellPosition]++;
            }
        }
        return eventMap;
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
        for (int i = 0; i < forecastValues.length;i++){
            if (forecastValues[i] == Float.NEGATIVE_INFINITY){
                filter[i] = false;
            }
        }
        return filter;
    }
}