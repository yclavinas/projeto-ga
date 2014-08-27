package org.corssa.predictiontesting;

public class GeoUtil {

    public static final float radiusOfEarthInKm = 6378.1f;

    public GeoUtil() {
    }

    /**
     * Compute the Vincenty distance (in km) b/w two lat/lon points, each of which is specified in decimal degrees.  We use the WGS-84 model for the Earth's ellipsoid.
     *
     * @param latOrigin first latitude point
     * @param lonOrigin first longitude point
     * @param latDestination second latitude point
     * @param lonDestination second longitude point
     * @return Vincenty distance b/w specified lat-lon points
     */
    public static float vincentyDistanceBetweenPoints(float latOrigin, float lonOrigin, float latDestination, float lonDestination) {
        double a = 6378.137;
        double b = 6356.7523142;
        double f = (a - b) / a;

        // The distance formula expects lat, lon in radians, so we need to convert them from degrees
        latOrigin = (float) Math.toRadians(latOrigin);
        lonOrigin = (float) Math.toRadians(lonOrigin);
        latDestination = (float) Math.toRadians(latDestination);
        lonDestination = (float) Math.toRadians(lonDestination);

        double L = lonOrigin - lonDestination;
        double U_1 = Math.atan((1 - f) * Math.tan(latOrigin));
        double U_2 = Math.atan((1 - f) * Math.tan(latDestination));

        double lambda = L;
        double lambdaPrime = 2 * Math.PI;
        double cosSquaredAlpha = 0;
        double sinSigma = 0;
        double cosSigma = 0;
        double cos2Sigma_m = 0;
        double sigma = 0;
        double epsilon = 1e-7;

        while (Math.abs(lambda - lambdaPrime) > epsilon) {
            double temp1 = Math.cos(U_2) * Math.sin(lambda);
            double temp2 = Math.cos(U_1) * Math.sin(U_2) - Math.sin(U_1) * Math.cos(U_2) * Math.cos(lambda);
            sinSigma = Math.sqrt(temp1 * temp1 + temp2 * temp2);
            cosSigma = Math.sin(U_1) * Math.sin(U_2) + Math.cos(U_1) * Math.cos(U_2) * Math.cos(lambda);
            sigma = Math.atan2(sinSigma, cosSigma);
            double sinAlpha = Math.cos(U_1) * Math.cos(U_2) * Math.sin(lambda) / (sinSigma + Double.MIN_VALUE);
            cosSquaredAlpha = 1 - sinAlpha * sinAlpha;
            cos2Sigma_m = Math.cos(sigma) - 2 * Math.sin(U_1) * Math.sin(U_2) / (cosSquaredAlpha + Double.MIN_VALUE);
            double C = f / 16 * cosSquaredAlpha * (4 + f * (4 - 3 * cosSquaredAlpha));
            lambdaPrime = lambda;
            lambda = L + (1 - C) * f * sinAlpha * (sigma + C * sinSigma * (cos2Sigma_m + C * cosSigma * (-1 + 2 * cos2Sigma_m * cos2Sigma_m)));
//            System.out.println("lambda = " + lambda);
        }

        double uSquared = cosSquaredAlpha * (a * a - b * b) / (b * b);
        double A = 1 + uSquared / 16384 * (4096 + uSquared * (-768 + uSquared * (320 - 175 * uSquared)));
        double B = uSquared / 1024 * (256 + uSquared * (74 - 47 * uSquared));
        double deltaSigma = B * sinSigma * (cos2Sigma_m + B / 4 * (cosSigma * (-1 + 2 * cos2Sigma_m * cos2Sigma_m - B / 6 *
                cos2Sigma_m * (-3 + 4 * sinSigma * sinSigma * (-3 + 4 * cos2Sigma_m * cos2Sigma_m)))));

        float distance = (float) (b * A * (sigma - deltaSigma));
        return (distance);
    }

    /**
     * Compute the approximate distance (in km) b/w two lat/lon points, each of which is specified in decimal degrees.
     *
     * @param latOrigin first latitude point
     * @param lonOrigin first longitude point
     * @param latDestination second latitude point
     * @param lonDestination second longitude point
     */
    public static double distanceBetweenPoints(float latOrigin, float lonOrigin, float latDestination, float lonDestination) {

        // The distance formula expects lat, lon in radians, so we need
        //   to convert them from degrees
        latOrigin = (float) Math.toRadians(latOrigin);
        lonOrigin = (float) Math.toRadians(lonOrigin);
        latDestination = (float) Math.toRadians(latDestination);
        lonDestination = (float) Math.toRadians(lonDestination);
        double distance = GeoUtil.radiusOfEarthInKm * Math.sqrt(
                (latOrigin - latDestination) * (latOrigin - latDestination) +
                (lonOrigin - lonDestination) * (lonOrigin - lonDestination) *
                Math.cos((latOrigin + latDestination) / 2) * Math.cos((latOrigin + latDestination) / 2));

        return distance;
    }

    /**
     * Compute the approximate area (in square km) of a rectangular lat-lon region specified by its NW and SE corners (decimal degrees lat and lon).  We can think of this 
     * region as a trapezoid b/c the distance b/w the east and west sides of the "rectangle" will be smaller on the side of the rectangle further from the equator.  This 
     * implementation assumes that the rectangle does not cross the equator.  To picture this, consider a trapezoid with a top length of a, bottom length of c, and the side length 
     * of b.  Then we call e the height of the trapezoid and d the difference  b/w a and c.  Then the total area is the sum of three areas: the rectangle with height e and length 
     * which is the shorter of a and c; two equiareal triangles containing the leftovers, each of area de/2.  Thus the total area is min(a,c)*e + d*e.
     * 
     * @param nwCornerLat latitude of the NW corner of the rectangular region in which we're interested
     * @param nwCornerLon longitude of the NW corner of the rectangular region in which we're interested
     * @param seCornerLat latitude of the SE corner of the rectangular region in which we're interested
     * @param seCornerLon longitude of the SE corner of the rectangular region in which we're interested
     * @return approximate area in square km of the specified rectangular region
     */
    public static float areaOfRectangularRegion(float nwCornerLat, float nwCornerLon, float seCornerLat, float seCornerLon) {
        float topWidth = GeoUtil.vincentyDistanceBetweenPoints(nwCornerLat, nwCornerLon, nwCornerLat, seCornerLon);
        float bottomWidth = GeoUtil.vincentyDistanceBetweenPoints(seCornerLat, nwCornerLon, seCornerLat, seCornerLon);
        float height = GeoUtil.vincentyDistanceBetweenPoints(nwCornerLat, nwCornerLon, seCornerLat, nwCornerLon);

        float a = topWidth;
        float b = height;
        float c = bottomWidth;
        float d = (float) Math.abs(0.5 * (a - c));
        float e = (float) Math.sqrt(b * b - d * d);

        float area = e * (Math.min(a, c) + d);
        return area;
    }

    /**
     * Compute the approximate area (in square km) of a square lat-lon region centered at the given latitude (decimal degrees) and its halfwidth (also in decimal deg).  This 
     * algorithm is the one used by Y. Kagan to convert his forecast rates from rate/deg^2 to rate/km^2.
     * 
     * @param lat latitude of the center of the square region in which we're interested
     * @param halfwidth half-width in deg of the square region in which we're interested
     * @return approximate area in square km of the specified square region
     */
    public static double areaOfRegionAboutPoint(float lat, float halfwidth) {
//      HPI = DACOS(0.0D0)
//      RAD = 90.0D0/HPI
//SPC = 1.0D03/9.0D0
//sqarea = rad*(dsind(ALATT+0.5) - dsind(ALATT-0.5))*SPC**2  !2/19/94 exact spherical
//
//dsind is the double precision implementation of sin function that expects degree arguments
//DACOS is the double precision implementation of arcos function that expects radian arguments
        double hpi = Math.acos(0);
        double rad = 90 / hpi;
        double spc = 1e3 / 9;
        double area = rad * (Math.sin(Math.toRadians(lat + halfwidth)) - Math.sin(Math.toRadians(lat - halfwidth))) * spc * spc;
        return area;
    }

    /**
     * Answer the question: does the specified lat/lon point fall within the specified distance from ANY of the specified lat/lon pairs?
     *
     * @param lat reference latitude
     * @param lon reference longitude
     * @param lats array of latitude points to compare w/ the reference point
     * @param lons array of longitude points to compare w/ the reference point
     * @param thresholdDistance maximum distance b/w reference and comparison points at which the point is still considered "near" one of the comparison points
     * @return answer to the question: does the specified lat/lon point fall within the specified distance from ANY of the specified lat/lon pairs?
     */
    public static boolean isPointNearOtherPoints(float lat, float lon, float[] lats, float[] lons, float thresholdDistance) {
        int numberOfComparisonPoints = lats.length;
        for (int i = 0; i < numberOfComparisonPoints; i++) {
            float distance = GeoUtil.vincentyDistanceBetweenPoints(lat, lon, lats[i], lons[i]);
            if (distance < thresholdDistance) {
                return true;
            }
        }
        return false;
    }

    /**
     * Answer the question: how many of the specified lat/lon pairs fall w/i  the specified distance from the given reference point?
     *
     * @param lat reference latitude
     * @param lon reference longitude
     * @param lats array of latitude points to compare w/ the reference point
     * @param lons array of longitude points to compare w/ the reference point
     * @param thresholdDistance maximum distance b/w reference and comparison points at which the point is still considered "near" one of the comparison points
     * @return answer to the question: how many of the specified lat/lon pairs fall w/i the specified distance from the given reference point?
     */
    public static int numberOfPointsNearPoint(float lat, float lon, float[] lats, float[] lons, float thresholdDistance) {
        int numberOfComparisonPoints = lats.length;
        int numberOfNearPoints = 0;
        for (int i = 0; i < numberOfComparisonPoints; i++) {
            float distance = GeoUtil.vincentyDistanceBetweenPoints(lat, lon, lats[i], lons[i]);
            if (distance < thresholdDistance) {
                numberOfNearPoints++;
            }
        }
        return numberOfNearPoints;
    }

    /**
     * Answer the question: which of the specified lat/lon pairs fall w/i
     * the specified distance from the given reference point?
     *
     * @param lat reference latitude
     * @param lon reference longitude
     * @param latsAndLons 2D array of lat/lon points to compare w/ the reference point
     * @param thresholdDistance maximum distance b/w reference and comparison points at which the point is still considered "near" one of the comparison points
     * @return answer to the question: which of the specified lat/lon pairs
     * fall w/i the specified distance from the given reference point?
     */
    public static float[][] whichPointsAreNearPoint(float lat, float lon, float[][] latsAndLons,
            float thresholdDistance) {
        float[] nearLats = new float[latsAndLons.length];
        float[] nearLons = new float[latsAndLons.length];
        int numberOfNearPoints = 0;
        int numberOfComparisonPoints = latsAndLons.length;
        for (int i = 0; i < numberOfComparisonPoints; i++) {
            double distance = GeoUtil.vincentyDistanceBetweenPoints(lat, lon, latsAndLons[i][0], latsAndLons[i][1]);
            if (distance < thresholdDistance) {
                nearLats[numberOfNearPoints] = latsAndLons[i][0];
                nearLons[numberOfNearPoints] = latsAndLons[i][1];
                numberOfNearPoints++;
            }
        }

        float[][] thesePoints = new float[numberOfNearPoints][2];
        for (int i = 0; i < numberOfNearPoints; i++) {
            thesePoints[i][0] = nearLats[i];
            thesePoints[i][1] = nearLons[i];
        }
        return thesePoints;
    }

    /**
     * Answer the question: how many of the specified lat/lon pairs fall w/i the specified distance1 from the two given reference points?
     *
     * @param lat1 reference latitude #1
     * @param lon1 reference longitude #1
     * @param lat2 reference latitude #2
     * @param lon2 reference longitude #2
     * @param lats array of latitude points to compare w/ the reference points
     * @param lons array of longitude points to compare w/ the reference points
     * @param thresholdDistance maximum distance1 b/w reference and comparison points at which the point is still considered "near" one of the comparison points
     * @return answer to the question: how many of the specified lat/lon pairs fall w/i the specified distance1 from the two given reference points?
     */
    public static int numberOfPointsNearPoints(float lat1, float lon1, float lat2,
            float lon2, float[] lats, float[] lons, float thresholdDistance) {
        int numberOfComparisonPoints = lats.length;
        int numberOfNearPoints = 0;
        for (int i = 0; i < numberOfComparisonPoints; i++) {
            double distance1 = GeoUtil.vincentyDistanceBetweenPoints(lat1, lon1, lats[i], lons[i]);
            if (distance1 < thresholdDistance) {
                double distance2 = GeoUtil.vincentyDistanceBetweenPoints(lat2, lon2, lats[i], lons[i]);
                if (distance2 < thresholdDistance) {
                    numberOfNearPoints++;
                }
            }
        }
        return numberOfNearPoints;
    }

    /**
     * Answer the question: which of the specified lat/lon pairs fall w/i the specified distance from the given reference point?
     *
     * @param lat reference latitude
     * @param lon reference longitude
     * @param latsAndLons 2D array of lat/lon points to compare w/ the reference point
     * @param thresholdDistance maximum distance b/w reference and comparison
     * points at which the point is still considered "near" one of the
     * comparison points
     * @return answer to the question: which of the specified lat/lon pairs
     * fall w/i the specified distance from the given reference point?
     */
    public static int[] whichPointsAreNearPoint(float lat, float lon, float[] lats,
            float[] lons, float thresholdDistance) {
        int[] nearLatsIndices = new int[lats.length];
        int numberOfNearPoints = 0;
        int numberOfComparisonPoints = lats.length;
        for (int i = 0; i < numberOfComparisonPoints; i++) {
            double distance = GeoUtil.vincentyDistanceBetweenPoints(lat, lon,
                    lats[i], lons[i]);
            if (distance < thresholdDistance) {
                nearLatsIndices[numberOfNearPoints] = i;
                numberOfNearPoints++;
            }
        }

        int[] thesePoints = new int[numberOfNearPoints];
        System.arraycopy(nearLatsIndices, 0, thesePoints, 0, numberOfNearPoints);
//        nearLatsIndices = null;
//        System.gc();
        return thesePoints;
    }

    /**
     * Given a specified latitude, compute the latitude of the points at the same longitude and at the specified distance from the original latitude.
     *
     * @param latitude reference latitude, in decimal degrees
     * @param distance desired distance, in km
     * @return latitudes of the points at the given distance from the reference
     * latitude (assuming the same longitude), in decimal degrees
     */
    public static float[] latitudesAtDistanceFromPoint(float latitude, float distance) {
        // Recall distance approximation formula:
        // d = R * sqrt((lat1 - lat2)^2 + (lon1 - lon2)^2 * cos^2(0.5(lat1 + lat2)))
        // lon1 = lon2 ==> d = R * sqrt((lat1 - lat2)^2)
        // ==> lat2 = lat1 +/- d / R

        // The distance formula expects lat, lon in radians, so we need
        //   to convert them from degrees
        latitude = (float) Math.toRadians(latitude);
        float southernLatitude = latitude - distance / GeoUtil.radiusOfEarthInKm;
        float northernLatitude = latitude + distance / GeoUtil.radiusOfEarthInKm;

        // convert back to degrees
        southernLatitude = (float) Math.toDegrees(southernLatitude);
        northernLatitude = (float) Math.toDegrees(northernLatitude);

        float[] desiredLatitudes = new float[2];
        desiredLatitudes[0] = southernLatitude;
        desiredLatitudes[1] = northernLatitude;

        return desiredLatitudes;
    }

    /**
     * Given a specified latitude and longitude compute the longitude of the points at the same latitude and at the specified distance from the original point.
     *
     * @param latitude reference latitude, in decimal degrees
     * @param longitude reference longitude, in decimal degrees
     * @param distance desired distance, in km
     * @return longitudes of the points at the given distance from the reference
     * longitude (assuming the same latitude), in decimal degrees
     */
    public static float[] longitudesAtDistanceFromPoint(float latitude, float longitude, float distance) {
        // Recall distance approximation formula:
        // d = R * sqrt((lat1 - lat2)^2 + (lon1 - lon2)^2 * cos^2(0.5(lat1 + lat2)))
        // lat1 = lat2 ==> d = R * (lon1 - lon2) * cos(lat)
        // ==> lon2 = lon1 +/- d / (R * cos (lat))

        float radiusOfEarth = 6378.1f;

        // The distance formula expects arguments in radians, so we need
        //   to convert lat and lon from degrees
        latitude = (float) Math.toRadians(latitude);
        longitude = (float) Math.toRadians(longitude);

        float westernLongitude = (float) (longitude - distance / (radiusOfEarth * Math.cos(latitude)));
        float easternLongitude = (float) (longitude + distance / (radiusOfEarth * Math.cos(latitude)));

        westernLongitude = (float) Math.toDegrees(westernLongitude);
        easternLongitude = (float) Math.toDegrees(easternLongitude);

        float[] desiredLongitudes = new float[2];
        desiredLongitudes[0] = westernLongitude;
        desiredLongitudes[1] = easternLongitude;

        return desiredLongitudes;
    }

    /**
     * Convert km to degrees at the specified latitude, using the simplified formula for distance b/w two lat/lon points.  To do this, let lat1 = lat2, lon1 = 0, 
     * lon2 = distanceInRadians.  Then, the distance formula reduces to distanceInKilometers = Rx cos(lat1) ==> distanceInRadians = distanceInKilometers / (R cos(lat1))
     * 
     * 
     * 
     * @param distanceInKilometers distance in km to be converted
     * @param lat latitude, in decimal degrees, at which to convert distanceInKilometers
     * @return number of decimal degrees corresponding to a distance of distanceInKilometers km at 
     * the specified latitude
     */
    public static float degreesFromKilometers(float distanceInKilometers, float lat) {
        float R = 6378.1f; // radius of earth

        // convert lat from degrees to radians
        lat = (float) Math.toRadians(lat);
        float distanceInRadians = distanceInKilometers / (R * (float) Math.cos(lat)); // distanceInRadians in radians

        // convert distanceInRadians from radians to degrees
        float distanceInDegrees = (float) Math.toDegrees(distanceInRadians);
        return distanceInDegrees;
    }

    /**
     * Convert degree measurement to km at the specified latitude.  To do this, let lat1 = lat2, lon1 = 0, and lon2 be the degree measurement to be converted.  Then, use the 
     * Vicenty formula for computing the distance in km.
     * 
     * 
     * @param distanceInDegrees distance in degrees to be converted
     * @param lat latitude, in decimal degrees, at which to convert distanceInDegrees
     * @return number of km corresponding to a distance of distanceInDegrees degrees at the specified latitude
     */
    public static float kilometersFromDegrees(float distanceInDegrees, float lat) {
        float lat1 = lat;
        float lat2 = lat;
        float lon1 = 0f;
        float lon2 = distanceInDegrees;
        float distance = GeoUtil.vincentyDistanceBetweenPoints(lat1, lon1, lat2, lon2);
        return distance;
    }

    /**
     * Convert the scalar moment to moment magnitude using Eq'n 7 from Hanks & Kanamori 1979
     *
     * @param scalar moment measured in dyne-cm
     * @return moment magnitude, given by m_w = 2/3 * log_10(m_0) - 10.7
     */
    public static float momentMagnitudeFromScalarMoment(float moment) {
        float magnitude = 2f / 3f * ((float) Math.log10(moment)) - 10.7f;
        return magnitude;
    }

    /**
     * Convert the moment tensor components to moment magnitude.  To do this, we square and sum the components, halve this, take the sqrt, multiply
     * by 10^the specified exponent; this yields the scalar moment; from here, we convert to moment magnitude
     *
     * @param momentTensor array of moment tensor components
     * @param exponent power to which the moment tensor components should be raised
     * @return moment magnitude
     */
    public static float momentMagnitudeFromMomentTensorComponents(float[] momentTensor, short exponent) {
        float sumOfSquares = 0;
        for (int i = 0; i < momentTensor.length; i++) {
            sumOfSquares += momentTensor[i] * momentTensor[i];
        }

        float scalarMoment = (float) Math.sqrt(sumOfSquares / 2) * (float) Math.pow(10, exponent);
        float magnitude = GeoUtil.momentMagnitudeFromScalarMoment(scalarMoment);
        return magnitude;
    }
}
