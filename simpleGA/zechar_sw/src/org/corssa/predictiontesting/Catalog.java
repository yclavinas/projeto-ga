package org.corssa.predictiontesting;

import java.io.OutputStreamWriter;
import java.io.BufferedOutputStream;
import java.io.FileOutputStream;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.BufferedInputStream;
import java.io.FileInputStream;
import java.io.BufferedReader;
import java.util.StringTokenizer;
import java.util.Date;

/**
 * @author J. Douglas Zechar zechar at usc.edu
 */
public class Catalog {

    private String[] times;
    private float[] lats;
    private float[] lons;
    private float[] depths;
    private float[] mags;

    /**
     * Get the origin time of each event
     */
    public String[] times() {
        return this.times;
    }

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

    public Catalog() {
    }

    /**
     * In the simplest case, we can create a catalog from arrays of data
     * 
     * @param times array of strings of the form yyyy/MM/dd HH:mm:ss
     * @param lats array of epicentral latitude points
     * @param lons array of epicentral longitude points
     * @param depths array of hypocentral depths
     * @param mags array of magnitudes
     */
    public Catalog(String[] times, float[] lats, float[] lons, float[] depths,
            float[] mags) {
        this.times = new String[times.length];
        this.lats = new float[lats.length];
        this.lons = new float[lons.length];
        this.depths = new float[depths.length];
        this.mags = new float[mags.length];

        System.arraycopy(times, 0, this.times, 0, times.length);
        System.arraycopy(lats, 0, this.lats, 0, lats.length);
        System.arraycopy(lons, 0, this.lons, 0, lons.length);
        System.arraycopy(depths, 0, this.depths, 0, depths.length);
        System.arraycopy(mags, 0, this.mags, 0, mags.length);
    }

    /**
     * Parse the specified catalog file to create a catalog.
     *
     * @param catalogFile file containing earthquake events in ZMAP ASCII format
     */
    public Catalog(String catalogFile) {
        try {
            int numberOfEvents = numberOfEqksInFile(catalogFile);
            this.times = new String[numberOfEvents];
            this.lats = new float[numberOfEvents];
            this.lons = new float[numberOfEvents];
            this.depths = new float[numberOfEvents];
            this.mags = new float[numberOfEvents];

            String sRecord = null;

            // Get a handle to the input catalog file
            FileInputStream oFIS = new FileInputStream(catalogFile);
            BufferedInputStream oBIS = new BufferedInputStream(oFIS);
            BufferedReader oReader = new BufferedReader(
                    new InputStreamReader(oBIS));

            int eventNumber = 0;

            String time = "";
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

                // parse the details
                String[] eqkDetails = eqkParametersFromRecord(sRecord);

                time = eqkDetails[0];
                sLatitude = eqkDetails[1];
                sLongitude = eqkDetails[2];
                sMagnitude = eqkDetails[3];
                sDepth = eqkDetails[4];

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

                this.times[eventNumber] = time;
                this.lats[eventNumber] = lat;
                this.lons[eventNumber] = lon;
                this.depths[eventNumber] = depth;
                this.mags[eventNumber] = mag;

                eventNumber++;
            }
        } catch (Exception e) {
            System.out.println("error in Catalog(" + catalogFile + ")");
            e.printStackTrace();
            System.exit(-1);
        }
    }

    /**
     * Create a subcatalog containing only events falling within the given
     * magnitude range
     * 
     * @param minMag minimum magnitude of event we want in the subcatalog
     * @param maxMag maximum magnitude of event we want in the subcatalog
     */
    public Catalog subcatalogByMagnitude(float minMag, float maxMag) {
        int numberOfQualifyingEvents = 0;
        // make room for the special case where every event in the catalog 
        // belongs to the subcatalog
        int[] indicesOfQualifyingEvents = new int[this.lats.length];

        for (int i = 0; i < this.times.length; i++) {
            float currentMag = this.mags[i];
            if (currentMag >= minMag && currentMag <= maxMag) {
                indicesOfQualifyingEvents[numberOfQualifyingEvents] = i;
                numberOfQualifyingEvents++;
            }
        }
        return this.subcatalogByIndices(indicesOfQualifyingEvents,
                numberOfQualifyingEvents);
    }

    /**
     * Create a subcatalog containing only events falling within the given
     * spatial domain
     * 
     * @param minLat minimum latitude of event we want in the subcatalog
     * @param maxLat maximum latitude of event we want in the subcatalog
     * @param minLon minimum longitude of event we want in the subcatalog
     * @param maxLon maximum longitude of event we want in the subcatalog
     */
    public Catalog subcatalogBySpace(float minLat, float maxLat, float minLon,
            float maxLon) {
        int numberOfQualifyingEvents = 0;
        // make room for the special case where every event in the catalog 
        // belongs to the subcatalog
        int[] indicesOfQualifyingEvents = new int[this.lats.length];

        for (int i = 0; i < this.times.length; i++) {
            float currentLat = this.lats[i];
            float currentLon = this.lons[i];
            if (currentLat >= minLat && currentLat <= maxLat &&
                    currentLon >= minLon && currentLon <= maxLon) {
                indicesOfQualifyingEvents[numberOfQualifyingEvents] = i;
                numberOfQualifyingEvents++;
            }
        }
        return this.subcatalogByIndices(indicesOfQualifyingEvents,
                numberOfQualifyingEvents);
    }

    /**
     * Create a subcatalog with the specified number of eqks containing only the
     * eqks that are specified by the array of event indices and the number
     * 
     * @param indices indices of events to include in the subcatalog
     * @param numberOfEqks number of eqks to include in the subcatalog
     * @return subset of events corresponding to the specified eqk indices
     */
    private Catalog subcatalogByIndices(int[] indices, int numberOfEqks) {
        String[] timesLocal = new String[numberOfEqks];
        float[] latsLocal = new float[numberOfEqks];
        float[] lonsLocal = new float[numberOfEqks];
        float[] depthsLocal = new float[numberOfEqks];
        float[] magsLocal = new float[numberOfEqks];

        for (int i = 0; i < numberOfEqks; i++) {
            int indexOfQualifyingEvent = indices[i];
            timesLocal[i] = this.times[indexOfQualifyingEvent];
            latsLocal[i] = this.lats[indexOfQualifyingEvent];
            lonsLocal[i] = this.lons[indexOfQualifyingEvent];
            depthsLocal[i] = this.depths[indexOfQualifyingEvent];
            magsLocal[i] = this.mags[indexOfQualifyingEvent];
        }

        Catalog subCatalog = new Catalog(timesLocal, latsLocal, lonsLocal,
                depthsLocal, magsLocal);
        return subCatalog;
    }

    /**
     * Create a subcatalog containing only events falling within the given date
     * range
     * 
     * @param minDate minimum origin time of event we want in the subcatalog
     * @param maxDate maximum origin time of event we want in the subcatalog
     */
    public Catalog subcatalogByTime(String minDate, String maxDate) {
        int numberOfQualifyingEvents = 0;
        // make room for the special case where every event in the catalog 
        // belongs to the subcatalog
        int[] indicesOfQualifyingEvents = new int[this.lats.length];

        Date eventTime = new Date();
        Date start = DateUtil.dateFromString(minDate);
        Date end = DateUtil.dateFromString(maxDate);

        for (int i = 0; i < this.times.length; i++) {
            eventTime = DateUtil.dateFromString(this.times[i]);
            if (eventTime.after(start) && eventTime.before(end)) {
                indicesOfQualifyingEvents[numberOfQualifyingEvents] = i;
                numberOfQualifyingEvents++;
            }
            // Assume the catalog is ordered by time; the first event that 
            // occurs after the end period of interest marks the line after
            // which no events will fall in the subcatalog
            if (eventTime.after(end)) {
                break;
            }
        }

        return this.subcatalogByIndices(indicesOfQualifyingEvents,
                numberOfQualifyingEvents);
    }

    /**
     * Parse earthquake parameters from a single line of a catalog file
     * 
     * @param sRecord chunk of text containing information on a single
     *          earthquake
     * @param catalogType type of catalog
     * @return array of earthquake parameters in the following form:
     *              [0]=origin time
     *              [1]=latitude (in decimal degrees) of epicenter
     *              [2]=longitude (in decimal degrees) of epicenter
     *              [3]=magnitude
     *              [4]=depth
     */
    protected String[] eqkParametersFromRecord(String sRecord) {
        String[] eqkParameters = new String[5];
        StringTokenizer st = new StringTokenizer(sRecord);

        String sLongitude = String.valueOf(Float.parseFloat(st.nextToken()));
        String sLatitude = String.valueOf(Float.parseFloat(st.nextToken()));

        int iYear = (int) Math.floor(Float.parseFloat(st.nextToken()));
        String year = String.valueOf(iYear);

        int iMonth = (int) Math.floor(Float.parseFloat(st.nextToken()));
        String month = String.valueOf(iMonth);
        if (month.length() == 1) {
            month = "0" + month;
        }

        int iDay = (int) Math.floor(Float.parseFloat(st.nextToken()));
        String day = String.valueOf(iDay);
        if (day.length() == 1) {
            day = "0" + day;
        }

        String sMagnitude = String.valueOf(Float.parseFloat(st.nextToken()));
        String sDepth = String.valueOf(Float.parseFloat(st.nextToken()));

        int iHour = (int) Math.floor(Float.parseFloat(st.nextToken()));
        String hour = String.valueOf(iHour);
        if (hour.length() == 1) {
            hour = "0" + hour;
        }

        int iMinute = (int) Math.floor(Float.parseFloat(st.nextToken()));
        String minute = String.valueOf(iMinute);
        if (minute.length() == 1) {
            minute = "0" + minute;
        }

        int iSecond = (int) Math.floor(Float.parseFloat(st.nextToken()));
        String second = String.valueOf(iSecond);
        if (second.length() == 1) {
            second = "0" + second;
        }
        String time = year + "/" + month + "/" + day + " " + hour + ":" +
                minute + ":" + second;

        eqkParameters[0] = time;
        eqkParameters[1] = sLatitude;
        eqkParameters[2] = sLongitude;
        eqkParameters[3] = sMagnitude;
        eqkParameters[4] = sDepth;
        return eqkParameters;
    }

    /**
     * Create a subcatalog containing only target events; that is, those
     * falling within the specified space/time/magnitude range
     * 
     * @param minMag min magnitude for an event to be included in subcatalog
     * @param maxMag max magnitude for an event to be included in subcatalog
     * @param minTime min origin time for an event to be included in subcatalog
     * @param maxTime max origin time for an event to be included in subcatalog
     * @param minLat min latitude for an event to be included in subcatalog
     * @param maxLat max latitude for an event to be included in subcatalog
     * @param minLon min longitude for an event to be included in subcatalog
     * @param maxLon max longitude for an event to be included in subcatalog
     *
     */
    public Catalog subcatalogBySpaceTimeMagnitudeRange(float minMag,
            float maxMag, String minTime, String maxTime, float minLat,
            float maxLat, float minLon, float maxLon) {
        Catalog subcatalogByTime = subcatalogByTime(minTime, maxTime);
        Catalog subcatalogBySpaceTime = subcatalogByTime.subcatalogBySpace(
                minLat, maxLat, minLon, maxLon);
        Catalog subcatalogBySpaceTimeMag =
                subcatalogBySpaceTime.subcatalogByMagnitude(minMag, maxMag);
        return subcatalogBySpaceTimeMag;
    }

    /**
     * Count the number of events in a catalog file
     *
     * @param catalogFile path to the catalog of interest
     * @return the number of events in the specified catalog file
     */
    protected int numberOfEqksInFile(String catalogFile) {
        int numberOfEqks = 0;

        try {
            String sRecord = null;

            // Get a handle to the catalog file
            FileInputStream oFIS = new FileInputStream(catalogFile);
            BufferedInputStream oBIS = new BufferedInputStream(oFIS);
            BufferedReader oReader = new BufferedReader(new InputStreamReader(
                    oBIS));

            // pass through the file once quickly to see how many eqks there are
            while ((sRecord = oReader.readLine()) != null) {
                numberOfEqks++;
            }

            oReader.close();
            oReader = null;
            oBIS.close();
            oBIS = null;
            oFIS.close();
            oFIS = null;
        } catch (Exception ex) {
            System.err.println("Trouble counting the number of events in " +
                    catalogFile);
            ex.printStackTrace();
            System.exit(-1);
        }

        return numberOfEqks;
    }

    /**
     * Save the current catalog events to a file in ZMAP ASCII format
     *
     * @param outputFile logical path to catalog file
     */
    public void save(String outputFile) {
        try {
            FileOutputStream oOutFIS = new FileOutputStream(outputFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(
                    new OutputStreamWriter(oOutBIS));
            int numberOfEqks = numberOfEqks();
            for (int i = 0; i < numberOfEqks; i++) {
                String time = this.times[i];
                String year = Integer.toString(Integer.parseInt(
                        time.substring(0, 4)));
                String month = Integer.toString(Integer.parseInt(
                        time.substring(5, 7)));
                String day = Integer.toString(Integer.parseInt(
                        time.substring(8, 10)));
                String hour = Integer.toString(Integer.parseInt(
                        time.substring(11, 13)));
                String min = Integer.toString(Integer.parseInt(
                        time.substring(14, 16)));
                String sec = Integer.toString(Integer.parseInt(
                        time.substring(17, 19)));

                oWriter.write(this.lons[i] + "\t" + this.lats[i] + "\t" +
                        year + "\t" + month + "\t" + day + "\t" + this.mags[i] +
                        "\t" + this.depths[i] + "\t" + hour + "\t" + min + "\t"
                        + sec + "\n");
            }
            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();
        } catch (Exception ex) {
            System.out.println("Error in Catalog.save(" + outputFile + ")");
            ex.printStackTrace();
        }
    }

    /**
     * Count the number of earthquakes in the current catalog.
     *
     * @return the number of events in the catalog
     */
    public int numberOfEqks() {
        return this.mags.length;
    }
}
