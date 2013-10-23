
import java.io.OutputStreamWriter;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.util.StringTokenizer;

public class CatalogNoTime {

    protected float[] lats;
    protected float[] lons;
    protected float[] depths;
    protected float[] mags;
    public static final short ANSS = 0;
    public static final short CMT_CSEP_ONE_LINE_FORMAT = 1;
    public static final short JMA = 2;
    public static final short JEREMY_GENERATED = 37; // my personal format
    public static final short CSEP_ZMAP = 13;
    public static final short JEREMY_GENERATED_NO_TIME = 69; // my personal format w/ no origin time information

    public static final short CMT_PSMECA = 3;
    public static final short CMT_TABLE = 4;

    /**
     * Get the latitude of each event's epicenter
     */
    public float[] lats() {
        return this.lats;
    }

    /**
     * Get the longitude of each event's epicenter
     */
    public float[] lons() {
        return this.lons;
    }

    /**
     * Get the depth of each event's hypocenter
     */
    public float[] depths() {
        return this.depths;
    }

    /**
     * Get the magnitude of each event
     */
    public float[] mags() {
        return this.mags;
    }

    /**
     * In the simplest case, we can create a catalog from arrays of data
     * 
     * @param lats array of epicentral latitude points
     * @param lons array of epicentral longitude points
     * @param depths array of hypocentral depths
     * @param mags array of magnitudes
     */
    public CatalogNoTime(float[] lats, float[] lons, float[] depths, float[] mags) {
        this.lats = new float[lats.length];
        this.lons = new float[lons.length];
        this.depths = new float[depths.length];
        this.mags = new float[mags.length];

        System.arraycopy(lats, 0, this.lats, 0, lats.length);
        System.arraycopy(lons, 0, this.lons, 0, lons.length);
        System.arraycopy(depths, 0, this.depths, 0, depths.length);
        System.arraycopy(mags, 0, this.mags, 0, mags.length);

        if (!((lats.length == lons.length) && (lats.length == depths.length) && (lats.length == mags.length))) {
            System.err.println("The catalog is not well-defined b/c each array is not of the same dimension");
            System.exit(-1);
        }
    }

    public CatalogNoTime() {
    }

    /**
     * We can parse certain types of catalog files to create a catalog.  In particular, we here parse a catalog file that is of the common form for ANSS, JMA, PDE, or one that 
     * I've generated (JEREMY_GENERATED).
     * 
     * @param catalogFile file containing earthquake events
     * @param catalogType type of earthquake catalog (determines parsing details)
     */
    public CatalogNoTime(String catalogFile, short catalogType) {
        try {
            int numberOfEvents = this.numberOfEqksInFile(catalogFile, catalogType);
            if (numberOfEvents > 0) {
                this.lats = new float[numberOfEvents];
                this.lons = new float[numberOfEvents];
                this.depths = new float[numberOfEvents];
                this.mags = new float[numberOfEvents];

                String sRecord = null;

                // Get a handle to the input catalog file
                FileInputStream oFIS = new FileInputStream(catalogFile);
                BufferedInputStream oBIS = new BufferedInputStream(oFIS);
                BufferedReader oReader = new BufferedReader(new InputStreamReader(oBIS));

                int eventNumber = 0;

                String sLatitude = "0";
                String sLongitude = "0";
                String sDepth = "0";
                String sMagnitude = "0";

                float lat = 0.0f;
                float lon = 0.0f;
                float depth = 0.0f;
                float mag = 0.0f;

                // Parse each line of the catalog file
                while ((sRecord = oReader.readLine()) != null) {

                    // skip over any comment lines
                    while (Character.isLetter(sRecord.charAt(0))) {
                        sRecord = oReader.readLine();

                        if (sRecord == null) {
                            break;
                        }
                    }
                    if (sRecord == null) {
                        break;
                    }

                    // parse the details
                    String[] eqkDetails = eqkParametersFromRecord(sRecord, catalogType);

                    sLatitude = eqkDetails[0];
                    sLongitude = eqkDetails[1];
                    sMagnitude = eqkDetails[2];
                    sDepth = eqkDetails[3];

                    if (sLatitude.trim().length() > 0) {
                        lat = Float.parseFloat(sLatitude);
                    }
                    if (sLongitude.trim().length() > 0) {
                        lon = Float.parseFloat(sLongitude);
                    }
                    if (sDepth.trim().length() > 0) {
                        depth = Float.parseFloat(sDepth);
                    }
                    if (sMagnitude.trim().length() > 0) {
                        mag = Float.parseFloat(sMagnitude);
                    }

                    this.lats[eventNumber] = lat;
                    this.lons[eventNumber] = lon;
                    this.depths[eventNumber] = depth;
                    this.mags[eventNumber] = mag;

                    eventNumber++;
                }
            } else {
                System.err.println("There appear to be no events in the specified catalog: " + catalogFile);
                System.exit(-1);
            }
        } catch (Exception e) {
            System.out.println("error in CatalogNoTime(" + catalogFile + ")");
            e.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Create a subcatalog containing only events falling within the given magnitude range
     * 
     * @param minMag minimum magnitude of event we want in the subcatalog
     * @param maxMag maximum magnitude of event we want in the subcatalog
     * @return subcatalog containing the subset of original events which fall within the specified magnitude range
     */
    public CatalogNoTime subcatalogByMagnitude(float minMag, float maxMag) {
        if (minMag >= maxMag) {
            System.err.println("The minimum magnitude must be strictly less than the max magnitude.");
            System.exit(-1);
        }
        int numberOfQualifyingEvents = 0;
        int[] indicesOfQualifyingEvents = new int[this.lats.length]; // make room for the special case where every event in the catalog belongs to the subcatalog

        for (int i = 0; i < this.mags.length; i++) {
            float currentMag = this.mags[i];
            if (currentMag >= minMag && currentMag <= maxMag) {
                indicesOfQualifyingEvents[numberOfQualifyingEvents] = i;
                numberOfQualifyingEvents++;
            }
        }
        return this.subcatalogByIndices(indicesOfQualifyingEvents, numberOfQualifyingEvents);
    }

    /**
     * Create a subcatalog containing only the first N events
     *
     * @param numberOfEqks number of events we wish to keep
     * @return catalog containing the first N events
     */
    public CatalogNoTime subcatalogByNumberOfEvents(int numberOfEvents) {
        if ((numberOfEvents <= this.mags.length) && (numberOfEvents >= 0)) {
            float[] latsLocal = new float[numberOfEvents];
            float[] lonsLocal = new float[numberOfEvents];
            float[] depthsLocal = new float[numberOfEvents];
            float[] magsLocal = new float[numberOfEvents];

            for (int i = 0; i < numberOfEvents; i++) {
                latsLocal[i] = this.lats[i];
                lonsLocal[i] = this.lons[i];
                depthsLocal[i] = this.depths[i];
                magsLocal[i] = this.mags[i];
            }

            return new CatalogNoTime(latsLocal, lonsLocal, depthsLocal, magsLocal);
        } else {
            System.err.println("There aren't enough events in the catalog to create a catalog of " + numberOfEvents + " events.");
            System.err.println("There are only " + this.mags.length + " events.");
            System.exit(-1);
            return null;
        }
    }

    /**
     * Create a subcatalog containing only events falling within the given spatial domain
     * 
     * @param minLat minimum latitude of event we want in the subcatalog
     * @param maxLat maximum latitude of event we want in the subcatalog
     * @param minLon minimum longitude of event we want in the subcatalog
     * @param maxLon maximum longitude of event we want in the subcatalog
     * @return the subset of events which satisfy the spatial search
     */
    public CatalogNoTime subcatalogBySpace(float minLat, float maxLat, float minLon, float maxLon) {
        if (minLat >= maxLat || minLon >= maxLon) {
            System.err.println("Minimum values must be strictly smaller than  maximum values.");
            System.exit(-1);
        }

        int numberOfQualifyingEvents = 0;
        int[] indicesOfQualifyingEvents = new int[this.lats.length]; // make room for the special case where every event in the catalog belongs to the subcatalog

        for (int i = 0; i < this.mags.length; i++) {
            float currentLat = this.lats[i];
            float currentLon = this.lons[i];
            if (currentLat >= minLat && currentLat <= maxLat && currentLon >= minLon && currentLon <= maxLon) {
                indicesOfQualifyingEvents[numberOfQualifyingEvents] = i;
                numberOfQualifyingEvents++;
            }
        }
        return this.subcatalogByIndices(indicesOfQualifyingEvents, numberOfQualifyingEvents);
    }

    /**
     * Count the number of earthquakes in the current catalog.
     *
     * @return the number of events in the catalog
     */
    public int numberOfEqks() {
        return this.mags.length;
    }

    /**
     * Find the min/max lat/lon/depth.:
     * 
     * @return array containing min/max lat/lon/depth points of events in the catalog      in the format
     *      [0] = minLat
     *      [1] = maxLat
     *      [2] = minLon
     *      [3] = maxLon
     *      [4] = minDepth
     *      [5] = maxDepth
     */
    protected float[] region() {
        float[] region = new float[6];

        // get the min/max lats and lons
        float minLat = 90.0f;
        float maxLat = -90.0f;
        float minLon = 180.0f;
        float maxLon = -180.0f;
        float minDepth = 0.0f;
        float maxDepth = 0.0f;
        int numberOfEvents = this.lats.length;

        for (int counter = 0; counter < numberOfEvents; counter++) {
            float currentLat = this.lats[counter];
            float currentLon = this.lons[counter];
            float currentDepth = this.depths[counter];

            if (currentLat < minLat) {
                minLat = currentLat;
            }
            if (currentLat > maxLat) {
                maxLat = currentLat;
            }
            if (currentLon < minLon) {
                minLon = currentLon;
            }
            if (currentLon > maxLon) {
                maxLon = currentLon;
            }
            if (currentDepth < minDepth) {
                minDepth = currentDepth;
            }
            if (currentDepth > maxDepth) {
                maxDepth = currentDepth;
            }
        }

        region[0] = minLat;
        region[1] = maxLat;
        region[2] = minLon;
        region[3] = maxLon;
        region[4] = minDepth;
        region[5] = maxDepth;
        return region;
    }

    /**
     * Find the min/max magnitude in the catalog
     * 
     * @return array containing min/max magnitude in the format
     *      [0] = minMag
     *      [1] = maxMag       
     */
    protected float[] magnitudeRange() {
        float[] magnitudeRange = new float[2];

        // get the min/max mag
        float minMag = 10.0f;
        float maxMag = 0.0f;

        int numberOfEvents = this.mags.length;
        for (int i = 0; i < numberOfEvents; i++) {
            float currentMag = this.mags[i];

            if (currentMag < minMag) {
                minMag = currentMag;
            }
            if (currentMag > maxMag) {
                maxMag = currentMag;
            }
        }

        magnitudeRange[0] = minMag;
        magnitudeRange[1] = maxMag;

        return magnitudeRange;
    }

    /**
     * Save the current catalog events to a file w/ some minimal metadata; this catalog will be saved in the Catalog.JEREMY_GENERATED_NO_TIME format
     *
     * @param outputFile logical path to catalog file
     * @param comments any notes that should precede the earthquake listing
     */
    public void save(String outputFile, String comments) {
        float[] region = region();
        float[] magnitudeRange = magnitudeRange();

        try {
            FileOutputStream oOutFIS = new FileOutputStream(outputFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This catalog was automatically generated using predictionTools.CatalogNoTime.save with the following parameters:\n");

            oWriter.write("minLat=" + region[0] + "\n");
            oWriter.write("maxLat=" + region[1] + "\n");
            oWriter.write("minLon=" + region[2] + "\n");
            oWriter.write("maxLon=" + region[3] + "\n");
            oWriter.write("minDepth=" + region[4] + "\n");
            oWriter.write("maxDepth=" + region[5] + "\n");
            oWriter.write("minMag=" + magnitudeRange[0] + "\n");
            oWriter.write("maxMag=" + magnitudeRange[1]);

            if (comments.length() > 0) {
                oWriter.write("\n" + comments.trim());
            }

            for (int counter = 0; counter < this.mags.length; counter++) {
                oWriter.write("\n" + this.lats[counter] + "\t" + this.lons[counter] + "\t" + this.depths[counter] + "\t" + this.mags[counter]);
            }
            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();
        } catch (Exception ex) {
            System.out.println("Error in CatalogNoTime.save(" + outputFile + ")");
            ex.printStackTrace();
        }
    }

    /**
     * Parse earthquake parameters from a single line of a catalog file.
     *
     * @param sRecord chunk of text containing information on a single earthquake
     * @param catalogType type of catalog
     * @return array of earthquake parameters in the following form:
     *
     * [0]=latitude (in decimal degrees) of epicenter
     * [1]=longitude (in decimal degrees) of epicenter
     * [2]=magnitude
     * [3]=depth
     */
    protected String[] eqkParametersFromRecord(String sRecord, int catalogType) {
        String[] eqkParameters = new String[4];
        StringTokenizer st = new StringTokenizer(sRecord);

        String sLatitude = "0";
        String sLongitude = "0";
        String sDepth = "0";
        String sMagnitude = "0";

        if (catalogType == CatalogNoTime.ANSS) {
            st.nextToken(); // skip date

            st.nextToken(); // skip origin time

            sLatitude = st.nextToken();
            sLongitude = st.nextToken();
            sDepth = st.nextToken();
            sMagnitude = st.nextToken();

            // For some very old records from BK, there is a no depth assigned.  In this case, the sDepth variable will now contain the magnitude and the sMagnitude will contain
            //   the magnitude scale, either "un" or "ML".  So below we check the sMagnitude value and set it correctly if need
            //   be.
            if (sMagnitude.toLowerCase().contains("un") || sMagnitude.toLowerCase().contains("m")) {
                sMagnitude = sDepth;
            }
        } else if (catalogType == CatalogNoTime.JEREMY_GENERATED) {
            st.nextToken(); // skip date

            st.nextToken(); // skip origin time

            sLatitude = st.nextToken();
            sLongitude = st.nextToken();
            sDepth = st.nextToken();
            sMagnitude = st.nextToken();
        } else if (catalogType == CatalogNoTime.JEREMY_GENERATED_NO_TIME) {
            sLatitude = st.nextToken();
            sLongitude = st.nextToken();
            sDepth = st.nextToken();
            sMagnitude = st.nextToken();
        }

        eqkParameters[0] = sLatitude;
        eqkParameters[1] = sLongitude;
        eqkParameters[2] = sMagnitude;
        eqkParameters[3] = sDepth;
        return eqkParameters;
    }

    /**
     * Count the number of events in a catalog file, neglecting comment lines (marked by starting a line w/ a non-numeric character).
     *
     * @param catalogFile path to the catalog of interest
     * @param catalogType type of catalog
     * @return the number of events in the specified catalog file
     */
    protected int numberOfEqksInFile(String catalogFile, short catalogType) {
        int numberOfEqks = 0;

        try {
            String sRecord = null;

            // Get a handle to the catalog file
            FileInputStream oFIS = new FileInputStream(catalogFile);
            BufferedInputStream oBIS = new BufferedInputStream(oFIS);
            BufferedReader oReader = new BufferedReader(new InputStreamReader(oBIS));

            // pass through the file once quickly to see how many events there are
            while ((sRecord = oReader.readLine()) != null) {
                // In the JMA catalog, every line begins w/ a letter, so we don't allow comments in the JMA format -- every line is considered to be a single eqk, except those 
                //                starting w/ the letter U
                if (catalogType != CatalogNoTime.JMA) {
                    // if the first character of this line is a letter, we consider this a comment; otherwise, it is an event
                    while (Character.isLetter(sRecord.charAt(0))) {
                        sRecord = oReader.readLine();

                        if (sRecord == null) {
                            break;
                        }
                    }
                    if (sRecord == null) {
                        break;
                    }
                } else {// In the JMA catalog, we'll skip any line that starts w/ the letter U

                    while (sRecord.startsWith("U")) {
                        sRecord = oReader.readLine();

                        if (sRecord == null) {
                            break;
                        }
                    }
                    if (sRecord == null) {
                        break;
                    }
                }
                numberOfEqks++;
            }

            oReader.close();
            oReader = null;
            oBIS.close();
            oBIS = null;
            oFIS.close();
            oFIS = null;
        } catch (Exception ex) {
            System.err.println("Trouble counting the number of events in " + catalogFile);
            ex.printStackTrace();
            System.exit(-1);
        }

        return numberOfEqks;
    }

    /**
     * Create a subcatalog containing the events in the given range
     *
     * @param begin the beginning eqk index
     * @param end the ending eqk index
     * @return catalog containing the events b/w indices begin and end
     */
    public CatalogNoTime subcatalogByEventRange(int begin, int end) {
        int numberOfEvents = end - begin;
        if ((begin <= end) && (begin >= 0) && (end <= numberOfEqks())) {
            float[] latsLocal = new float[numberOfEvents];
            float[] lonsLocal = new float[numberOfEvents];
            float[] depthsLocal = new float[numberOfEvents];
            float[] magsLocal = new float[numberOfEvents];

            System.arraycopy(this.lats, begin, latsLocal, 0, numberOfEvents);
            System.arraycopy(this.lons, begin, lonsLocal, 0, numberOfEvents);
            System.arraycopy(this.mags, begin, magsLocal, 0, numberOfEvents);
            System.arraycopy(this.depths, begin, depthsLocal, 0, numberOfEvents);

            return new CatalogNoTime(latsLocal, lonsLocal, depthsLocal, magsLocal);
        } else {
            System.err.println("Error in CatalogNoTime.subcatalogByEventRange()");
            System.exit(-1);
        }
        return null;
    }

    /**
     * Determine an appropriate gridding for the events in this catalog.  To do this, we determine the min/max lat/lon and discretize into the number of specified bins
     *
     * @param boxes number of boxes to use in the maximum dimension (so the grid will be of dimensions boxes x something, where something is less than or equal to boxes)
     * @return array of floats specifying the gridding in the format of
     *  [0] = minLat
     *  [1] = maxLat
     *  [2] = minLon
     *  [3] = maxLon
     *  [4] = boxSize
     */
    public float[] suggestedDiscretization(int boxes) {
        // determine the min/max lat/lon reported in the catalog
        float minLatObserved = ArrayUtil.minimum(this.lats);
        float maxLatObserved = ArrayUtil.maximum(this.lats);
        float minLonObserved = ArrayUtil.minimum(this.lons);
        float maxLonObserved = ArrayUtil.maximum(this.lons);

        // the study region should be large enough to capture all events, so we push its borders out to the nearest degree
        float minLat = (float) Math.floor(minLatObserved);
        float maxLat = (float) Math.ceil(maxLatObserved);
        float minLon = (float) Math.floor(minLonObserved);
        float maxLon = (float) Math.ceil(maxLonObserved);

        // Determine which dimension is larger, the latitude or longitude, and then define the boxsize based on this dimension
        float maxDiff = Math.max(maxLat - minLat, maxLon - minLon);
        float boxSize = maxDiff / (float) boxes;

        // Construct the discretization parameter specification
        float[] discretizationParameters = new float[5];
        discretizationParameters[0] = minLat;
        discretizationParameters[1] = maxLat;
        discretizationParameters[2] = minLon;
        discretizationParameters[3] = maxLon;
        discretizationParameters[4] = boxSize;

        return discretizationParameters;
    }

    /**
     * Create a subcatalog with the specified number of eqks containing only the eqks that are specified by the array of event indices and the number
     * 
     * @param indices indices of events to include in the subcatalog
     * @param numberOfEqks number of eqks to include in the subcatalog
     * @return subset of events corresponding to the specified eqk indices
     */
    private CatalogNoTime subcatalogByIndices(int[] indices, int numberOfEqks) {
        float[] latsLocal = new float[numberOfEqks];
        float[] lonsLocal = new float[numberOfEqks];
        float[] depthsLocal = new float[numberOfEqks];
        float[] magsLocal = new float[numberOfEqks];

        for (int i = 0; i < numberOfEqks; i++) {
            int indexOfQualifyingEvent = indices[i];
            latsLocal[i] = this.lats[indexOfQualifyingEvent];
            lonsLocal[i] = this.lons[indexOfQualifyingEvent];
            depthsLocal[i] = this.depths[indexOfQualifyingEvent];
            magsLocal[i] = this.mags[indexOfQualifyingEvent];
        }

        CatalogNoTime subCatalog = new CatalogNoTime(latsLocal, lonsLocal, depthsLocal, magsLocal);
        return subCatalog;
    }
}