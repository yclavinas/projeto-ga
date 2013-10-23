
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

public class Catalog extends CatalogNoTime {

    protected String[] times;

    /**
     * Get the origin time of each event
     */
    public String[] times() {
        return this.times;
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
     * @param start start date of the catalog, in the form yyyy/MM/dd HH:mm:ss
     * @param end end date of the catalog, in the form yyyy/MM/dd HH:mm:ss
     */
    public Catalog(String[] times, float[] lats, float[] lons, float[] depths, float[] mags) {
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
     * We can parse certain types of catalog files to create a catalog.  In particular, we here parse a catalog file that is of the common form for ANSS or one that I've generated 
     * (JEREMY_GENERATED).
     *
     * @param catalogFile file containing earthquake events
     * @param catalogType type of earthquake catalog (determines parsing details)
     * @param start start date of the catalog (in my favorite format)
     * @param end end date of the catalog (in my favorite format)
     */
    public Catalog(String catalogFile, short catalogType) {
        try {
            int numberOfEvents = numberOfEqksInFile(catalogFile, catalogType);
            this.times = new String[numberOfEvents];
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
                // In the JMA catalog, every line begins w/ a letter, so we don't allow comments in the JMA format -- every line is considered to be a single eqk
                if (catalogType != Catalog.JMA) {

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

                // parse the details
                String[] eqkDetails = eqkParametersFromRecord(sRecord, catalogType);

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
     * Create a subcatalog containing only events falling within the given magnitude range
     * 
     * @param minMag minimum magnitude of event we want in the subcatalog
     * @param maxMag maximum magnitude of event we want in the subcatalog
     */
    public Catalog subcatalogByMagnitude(float minMag, float maxMag) {
        int numberOfQualifyingEvents = 0;
        int[] indicesOfQualifyingEvents = new int[this.lats.length]; // make room for the special case where every event in the catalog belongs to the subcatalog

        for (int i = 0; i < this.times.length; i++) {
            float currentMag = this.mags[i];
            if (currentMag >= minMag && currentMag <= maxMag) {
                indicesOfQualifyingEvents[numberOfQualifyingEvents] = i;
                numberOfQualifyingEvents++;
            }
        }
        return this.subcatalogByIndices(indicesOfQualifyingEvents, numberOfQualifyingEvents);
    }

    /**
     * Create a subcatalog containing only events falling within the given spatial domain
     * 
     * @param minLat minimum latitude of event we want in the subcatalog
     * @param maxLat maximum latitude of event we want in the subcatalog
     * @param minLon minimum longitude of event we want in the subcatalog
     * @param maxLon maximum longitude of event we want in the subcatalog
     */
    public Catalog subcatalogBySpace(float minLat, float maxLat, float minLon, float maxLon) {
        int numberOfQualifyingEvents = 0;
        int[] indicesOfQualifyingEvents = new int[this.lats.length]; // make room for the special case where every event in the catalog belongs to the subcatalog

        for (int i = 0; i < this.times.length; i++) {
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
     * Create a subcatalog with the specified number of eqks containing only the eqks that are specified by the array of event indices and the number
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

        Catalog subCatalog = new Catalog(timesLocal, latsLocal, lonsLocal, depthsLocal, magsLocal);
        return subCatalog;
    }

    /**
     * Create a subcatalog containing only events falling within the given date range
     * 
     * @param minDate minimum origin time of event we want in the subcatalog
     * @param maxDate maximum origin time of event we want in the subcatalog
     */
    public Catalog subcatalogByTime(String minDate, String maxDate) {
        int numberOfQualifyingEvents = 0;
        int[] indicesOfQualifyingEvents = new int[this.lats.length]; // make room for the special case where every event in the catalog belongs to the subcatalog

        Date eventTime = new Date();
        Date start = DateUtil.dateFromString(minDate);
        Date end = DateUtil.dateFromString(maxDate);

        for (int i = 0; i < this.times.length; i++) {
            eventTime = DateUtil.dateFromString(this.times[i]);
            //System.out.println("eventTime=" +eventTime.toString());
            if (eventTime.after(start) && eventTime.before(end)) {
                indicesOfQualifyingEvents[numberOfQualifyingEvents] = i;
                numberOfQualifyingEvents++;
            }
            // Assume the catalog is ordered by time; the first event that occurs after the end period of interest marks the line after which no events will fall in the subcatalog
            if (eventTime.after(end)) {
                break;
            }
        }

        return this.subcatalogByIndices(indicesOfQualifyingEvents, numberOfQualifyingEvents);
    }

    /**
     * Save the current catalog events to a file w/ some minimal metadata; this catalog will be saved in the Catalog.JEREMY_GENERATED format
     *
     * @param outputFile logical path to catalog file
     * @param comments any notes that should precede the earthquake listing
     */
    public void save(String outputFile, String comments) {
//        System.out.println("going to save " + outputFile);
        float[] region = region();
        float[] magnitudeRange = magnitudeRange();
        try {
            FileOutputStream oOutFIS = new FileOutputStream(outputFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This catalog was automatically generated using predictionTools.Catalog.save with the following parameters:\n");
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

            for (int counter = 0; counter < this.times.length; counter++) {
                oWriter.write("\n" + this.times[counter] + "\t" + this.lats[counter] + "\t" + this.lons[counter] + "\t" + this.depths[counter] + "\t" + this.mags[counter]);
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
     * Save the current catalog events to a file w/ some minimal metadata in the format required for RELM testing (per Maria Liukis) which is 
     * Lon lat year month day mag depth hour min second errors networkName
     *
     * @param outputFile logical path to catalog file
     */
    public void saveInRELMFormat(String outputFile) {
        float[] region = region();
        float[] magnitudeRange = magnitudeRange();

        try {
            FileOutputStream oOutFIS = new FileOutputStream(outputFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));

            oWriter.write("This catalog was automatically generated using predictionTools.Catalog.saveToRELMFormat with the following parameters:\n");
            oWriter.write("minLat=" + region[0] + "\n");
            oWriter.write("maxLat=" + region[1] + "\n");
            oWriter.write("minLon=" + region[2] + "\n");
            oWriter.write("maxLon=" + region[3] + "\n");
            oWriter.write("minDepth=" + region[4] + "\n");
            oWriter.write("maxDepth=" + region[5] + "\n");
            oWriter.write("minMag=" + magnitudeRange[0] + "\n");
            oWriter.write("maxMag=" + magnitudeRange[1]);

            // Lon lat year month day mag depth hour min second errors networkName
            for (int i = 0; i < this.times.length; i++) {
                // We need to parse the date information into individual components.  Recall that it is specified in the following format: yyyy/MM/dd HH:mm:ss
                String dateTime = this.times[i];
                String year = dateTime.substring(0, 4);
                String month = dateTime.substring(5, 7);
                String day = dateTime.substring(8, 10);
                String hour = dateTime.substring(11, 13);
                String min = dateTime.substring(14, 16);
                String sec = dateTime.substring(17);
                oWriter.write("\n" + this.lons[i] + "\t" + this.lats[i] + "\t" + year + "\t" + month + "\t" + day + "\t" + this.mags[i] + "\t" + this.depths[i] + "\t" + hour +
                        "\t" + min + "\t" + sec + "\t");
            }
            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();
        } catch (Exception ex) {
            System.out.println("Error in Catalog.saveToRELMFormat(" + outputFile + ")");
            ex.printStackTrace();
        }
    }

    /**
     * Parse earthquake parameters from a single line of a catalog file
     * 
     * @param sRecord chunk of text containing information on a single earthquake
     * @param catalogType type of catalog
     * @return array of earthquake parameters in the following form:
     * [0]=origin time
     * [1]=latitude (in decimal degrees) of epicenter
     * [2]=longitude (in decimal degrees) of epicenter
     * [3]=magnitude
     * [4]=depth
     */
    protected String[] eqkParametersFromRecord(String sRecord, int catalogType) {
        String[] eqkParameters = new String[5];
        StringTokenizer st = new StringTokenizer(sRecord);
        String time = "";
        String sLatitude = "0";
        String sLongitude = "0";
        String sDepth = "0";
        String sMagnitude = "0";

        if (catalogType == Catalog.ANSS) {
            time = st.nextToken(); // date

            time = time.concat(" " + st.nextToken()); // origin time

            sLatitude = st.nextToken();
            sLongitude = st.nextToken();
//            System.out.println(sRecord);
            sDepth = st.nextToken();
            sMagnitude = st.nextToken();

            // For some very old records from BK, there is a no depth assigned.  In this case, the sDepth variable will now contain the magnitude and sMagnitude will contain
            //   the magnitude scale, either "un" or "ML".  So below we check the sMagnitude value and set it correctly if need
            //   be.
            if (sMagnitude.toLowerCase().contains("un") || sMagnitude.toLowerCase().contains("m")) {
                sMagnitude = sDepth;
            }
        } else if (catalogType == Catalog.JEREMY_GENERATED) {
            time = st.nextToken(); // date

            time = time.concat(" " + st.nextToken()); // origin time

            sLatitude = st.nextToken();
            sLongitude = st.nextToken();
            sDepth = st.nextToken();
            sMagnitude = st.nextToken();
        } else if (catalogType == Catalog.JMA) {
            float lonDegrees = Float.parseFloat(sRecord.substring(32, 36).trim());
            String longitudeMinutes = sRecord.substring(36, 38).trim();
            float lonMinutes = 0;
            if (longitudeMinutes.length() > 0) {
                lonMinutes = Float.parseFloat(longitudeMinutes) / 60f;
            }
            sLongitude = String.valueOf(lonDegrees + lonMinutes);
            float latDegrees = Float.parseFloat(sRecord.substring(21, 24).trim());
            String latitudeMinutes = sRecord.substring(24, 26).trim();
            float latMinutes = 0;
            if (latitudeMinutes.length() > 0) {
                latMinutes = Float.parseFloat(latitudeMinutes) / 60f;
            }
            sLatitude = String.valueOf(latDegrees + latMinutes);

            String sYear = sRecord.substring(1, 5);
            String sMonth = sRecord.substring(5, 7);
            String sDay = sRecord.substring(7, 9);
            String sHour = sRecord.substring(9, 11);
            String sMinute = sRecord.substring(11, 13);
            time = sYear + "/" + sMonth + "/" + sDay + " " + sHour + ":" + sMinute + ":00"; // origin time

            sDepth = sRecord.substring(44, 47).trim();
            sMagnitude = sRecord.substring(52, 54);
            if (sMagnitude.trim().length() > 0) {
                sMagnitude = sMagnitude.replace("A", "-1");
                sMagnitude = sMagnitude.replace("B", "-2");
                sMagnitude = sMagnitude.replace("C", "-3");
                float iMag = Float.parseFloat(sMagnitude) / 10;
                sMagnitude = Float.toString(iMag);
            }
        } else if (catalogType == Catalog.CMT_CSEP_ONE_LINE_FORMAT) {
            st.nextToken(); // skip the event id

            String year = st.nextToken(); // 2 digit year

            int iYear = Integer.parseInt(year);
            if (iYear > 76) {
                year = "19" + year;
            } else {
                year = "20" + year;
            }
            String month = st.nextToken();
            String day = st.nextToken();
            String timeOfDay = st.nextToken();
            time = year + "/" + month + "/" + day + " " + timeOfDay + "0";
            st.nextToken(); // skip centroid time offset

            sLatitude = st.nextToken();
            sLongitude = st.nextToken();
            sDepth = st.nextToken();

            int momentExponent = Integer.parseInt(st.nextToken());
            float momentBase = Float.parseFloat(st.nextToken());
            float scalarMoment = momentBase * (float) Math.pow(10, momentExponent);
            float fMagnitude = GeoUtil.momentMagnitudeFromScalarMoment(scalarMoment);
            // Round magnitude to the nearest tenth as this is what is done in the CMT catalog
            fMagnitude = Math.round(fMagnitude * 10f) / 10f;
            sMagnitude = String.valueOf(fMagnitude);
        } else if (catalogType == Catalog.CSEP_ZMAP) {
            sLongitude = st.nextToken();
            sLatitude = st.nextToken();
            int iYear = Math.round(Float.parseFloat(st.nextToken()));
            String year = String.valueOf(iYear);
            String month = st.nextToken();
            if (month.length() == 1) {
                month = "0" + month;
            }
            String day = st.nextToken();
            if (day.length() == 1) {
                day = "0" + day;
            }
            sMagnitude = st.nextToken();
            sDepth = st.nextToken();
            String hour = st.nextToken();
            if (hour.length() == 1) {
                hour = "0" + hour;
            }
            String minute = st.nextToken();
            if (minute.length() == 1) {
                minute = "0" + minute;
            }
            int iSecond = Math.round(Float.parseFloat(st.nextToken()));
            String second = String.valueOf(iSecond);
            if (second.length() == 1){
                second = "0" + second;
            }

            time = year + "/" + month + "/" + day + " " + hour + ":" + minute + ":" + second;
        }

        eqkParameters[0] = time;
        eqkParameters[1] = sLatitude;
        eqkParameters[2] = sLongitude;
        eqkParameters[3] = sMagnitude;
        eqkParameters[4] = sDepth;
        return eqkParameters;
    }

    /**
     * Create a subcatalog containing only target events; that is, those falling within the specified space/time/magnitude range
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
    public Catalog subcatalogBySpaceTimeMagnitudeRange(float minMag, float maxMag, String minTime, String maxTime, float minLat, float maxLat, float minLon,
            float maxLon) {
        Catalog subcatalogByTime = subcatalogByTime(minTime, maxTime);
        Catalog subcatalogBySpaceTime = subcatalogByTime.subcatalogBySpace(minLat, maxLat, minLon, maxLon);
        Catalog subcatalogBySpaceTimeMag = subcatalogBySpaceTime.subcatalogByMagnitude(minMag, maxMag);
        return subcatalogBySpaceTimeMag;
    }

    /**
     * Save the current catalog events to a file in the ZMAP format
     * 
     * @param outputFile logical path to catalog file
     */
    public void saveAsZMAP(String outputFile) {
        try {
            FileOutputStream oOutFIS = new FileOutputStream(outputFile);
            BufferedOutputStream oOutBIS = new BufferedOutputStream(oOutFIS);
            BufferedWriter oWriter = new BufferedWriter(new OutputStreamWriter(oOutBIS));
            int numberOfEqks = numberOfEqks();
            for (int i = 0; i < numberOfEqks; i++) {
                String time = this.times[i];
                String year = time.substring(0, 4);
                String month = time.substring(5, 7);
                String day = time.substring(8, 10);
                String hour = time.substring(11, 13);
                String min = time.substring(14, 16);

                oWriter.write(this.lons[i] + "\t" + this.lats[i] + "\t" + year + "\t" + month + "\t" + day + "\t" + this.mags[i] + "\t" + this.depths[i] + "\t" + hour + "\t" +
                        min + "\n");
            }
            oWriter.close();
            oOutBIS.close();
            oOutFIS.close();
        } catch (Exception ex) {
            System.out.println("Error in Catalog.saveAsZMAP(" + outputFile + ")");
            ex.printStackTrace();
        }
    }
}