
import java.util.Calendar;
import java.util.Date;
import java.text.SimpleDateFormat;

/**
 *
 * @author jzechar
 */
public class DateUtil {
    private static SimpleDateFormat df = new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    private static SimpleDateFormat mcGuireDF = new SimpleDateFormat("yyyy/DDD HH:mm:ss");
    
    /** Creates a new instance of DateUtil */
    public DateUtil() {
    }
    
    /**
     * Parse a date from the specified string
     * 
     * @param sDate string representation of the date, of the form yyyy/MM/dd HH:mm:ss
     * @return corresponding Date object
     */
    public static Date dateFromString(String sDate) {
        Date date = new Date();
        try {
            date = DateUtil.df.parse(sDate);
        } catch (Exception ex) {
            System.out.println("Error in DateUtil.getDateFromString(" + sDate + ")");
            ex.printStackTrace();
        }
        return (date);
    }
    
    /**
     * Parse a date from the specified string
     * 
     * @param sDate string representation of the date, of the form yyyy/DDD HH:mm:ss
     * @return corresponding Date object
     */
    public static Date dateFromMcguireString(String sDate) {
        Date date = new Date();
        try {
            date = DateUtil.mcGuireDF.parse(sDate);
        } catch (Exception ex) {
            System.out.println("Error in DateUtil.dateFromMcguireString(" + sDate + ")");
            ex.printStackTrace();
        }
        return (date);
    }
    
    /**
     * Answers the question: "Is this string in the right format to be parsed as a date of of the form yyyy/MM/dd HH:mm:ss?"
     * 
     * @param sDate string representation of a date time
     * @return boolean response to the statement "This string is is of the form yyyy/MM/dd HH:mm:ss"
     */
    public static boolean isInPrefferedDateForm(String sDate){
        try {
            Date date = DateUtil.df.parse(sDate);
        } catch (java.text.ParseException ex) { // there was an exception
            return false;
        }
        return true; // the date was of the correct format
    }
    
    /**
     * Parse a string from the specified Date object
     * 
     * @param sDate string representation of a date time
     * @return string representation of the date, of the form yyyy/MM/dd HH:mm:ss
     */
    public static String stringFromDate(Date date) {
        return (DateUtil.df.format(date));
    }
    
    /**
     * Add some specified amount of time to the specified date/time
     * 
     * @param startDate the reference date/time in format: yyyy/MM/dd HH:mm:ss
     * @param fieldToChange calendar field to change
     * @param amountToAdd amount to add to the calendar field
     * @return the offset date/time in format: yyyy/MM/dd HH:mm:ss
     */
    public static String offsetDate(String startDate, int fieldToChange, int amountToAdd){
        Date start = DateUtil.dateFromString(startDate);
        Calendar startCalendar = Calendar.getInstance();
        startCalendar.setTime(start);
        startCalendar.add(fieldToChange, amountToAdd);
        String offsetTime = DateUtil.stringFromDate(startCalendar.getTime());
        //System.out.println("start=" + start.toString() + ", offsetTime=" + offsetTime);
        return offsetTime;
    }
    
    /**
     * get the difference between two dates in days; it is not required that these dates be specified in chronological order
     * 
     * @param dateA date A to compare, of the form yyyy/MM/dd HH:mm:ss
     * @param dateB date B to compare, of the form yyyy/MM/dd HH:mm:ss
     * @return absolute difference in days between dates A and B
     */
    public static float durationInDays(String dateA, String dateB) {
        float duration = 0;
        
        // Calculate the number of days between dates A and B
        try {
            Calendar timeA = Calendar.getInstance();
            Calendar timeB = Calendar.getInstance();
            timeA.setTime(DateUtil.dateFromString(dateA));
            timeB.setTime(DateUtil.dateFromString(dateB));
            duration = (timeB.getTimeInMillis() - timeA.getTimeInMillis()) / 1000.0f / 60.0f / 60.0f / 24.0f;
        } catch (Exception ex) {
            System.out.println("Error in DateUtil.durationInDays(" + dateA + ", " + dateB + ")");
            ex.printStackTrace();
        }
        return duration;
    }
    
    /**
     * get the duration between two dates in days, requiring that the start occur before the end.  If the specified start date is after the specified end date, throw up.
     * 
     * @param start start of range, of the form yyyy/MM/dd HH:mm:ss
     * @param end end of range, of the form yyyy/MM/dd HH:mm:ss
     * @return the number of days b/w the specified start and end range
     */
    public static float durationInOrderedDays(String start, String end) {
        float duration = 0;
        
        // Calculate the number of days elapsed between the start and end
        try {
            Calendar startTime = Calendar.getInstance();
            Calendar endTime = Calendar.getInstance();
            startTime.setTime(DateUtil.dateFromString(start));
            endTime.setTime(DateUtil.dateFromString(end));
            long endTimeMillis = endTime.getTimeInMillis();
            long startTimeMillis = startTime.getTimeInMillis();
            if (endTimeMillis < startTimeMillis){
                System.err.println("Start date is after end date!");
                System.err.println("Start = " + start);
//                System.exit(-1);
            }
            duration = Math.abs(endTimeMillis - startTimeMillis) / 1000.0f / 60.0f / 60.0f / 24.0f;
        } catch (Exception ex) {
            System.err.println("Error in DateUtil.durationInDays(" + start + ", " + end + ")");
            ex.printStackTrace();
        }
        return duration;
    }
    
    /**
     * Compute the temporal overlap of two alarms.  We assume that the second alarm starts after the first one but we don't assume anything abt the durations of each alarm.  
     * Therefore, we have 3 cases of interest.  We denote each of the cases with the following notation:
     *      [ is the start of the first alarm
     *      ] is the end of the first alarm
     *      { is the start of the second alarm
     *      } is the end of the second alarm
     *
     * Case I: There is no overlap; namely, the 2nd alarm starts after the 1st alarm is completed.  []{}
     * Case II: There is overlap with the 1st alarm ending before the 2nd alarm ends [{]}
     * Case III: The 2nd alarm falls completely within the 1st alarm [{}]
     * 
     * @param start1 start time of the 1st alarm
     * @param duration1 duration (in days) of the 1st alarm
     * @param start2 start time of the 2nd alarm
     * @param duration2 duration (in days) of the 2nd alarm
     * @return the overlap (in days) of the overlap b/w the alarms
     */
    public static float alarmTimeOverlap(String start1, float duration1, String start2, float duration2){
        int duration1InSeconds = (int)(duration1 * 24 * 60 * 60);
        int duration2InSeconds = (int)(duration1 * 24 * 60 * 60);
        String end1 = DateUtil.offsetDate(start1, Calendar.SECOND, duration1InSeconds);
        
        if (DateUtil.durationInDays(start2, end1) <= 0.0f){ // CASE I
            return 0.0f;
        } else{
            String end2 = DateUtil.offsetDate(start2, Calendar.SECOND, duration2InSeconds);
            if (DateUtil.durationInDays(end1, end2)>=0.0f){ // CASE II
                return DateUtil.durationInDays(start2, end1);
            } else{ // CASE III
                return duration2;
            }
        }
    }
    
    /**
     * Compute the temporal overlap of two alarms.  We assume that the second alarm starts after the first one and each alarm is of the same duration.  Therefore, we have 2 
     * cases of interest.  We denote each of the cases with the following notation:
     *      [ is the start of the first alarm
     *      ] is the end of the first alarm
     *      { is the start of the second alarm
     *      } is the end of the second alarm
     *
     * Case I: There is no overlap; namely, the 2nd alarm starts after the 1st alarm is completed.  []{}
     * Case II: There is overlap with the 1st alarm ending before the 2nd alarm ends [{]}
     * 
     * @param start1 start time of the 1st alarm
     * @param start2 start time of the 2nd alarm
     * @param duration duration (in days) of each alarm
     * @return the overlap (in days) of the overlap b/w the alarms
     */
    public static float alarmTimeOverlap(String start1, String start2, float duration){
        int durationInSeconds = (int)(duration * 24 * 60 * 60);
        String end1 = DateUtil.offsetDate(start1, Calendar.SECOND, durationInSeconds);
        float overlap = DateUtil.durationInDays(start2, end1);
        if (overlap <= 0.0f){ // CASE I
            return 0.0f;
        } else{ // CASE II
            return overlap;
        }
    }
    
    /**
     * Answers the question: "Is the first date before the second date?"
     * 
     * @param dateA string representation of Date A, in yyyy/MM/dd HH:mm:ss format
     * @param dateB string representation of Date B, in yyyy/MM/dd HH:mm:ss format
     * @return boolean response to the statement "Date A is before Date B"
     */
    public static boolean areDatesOrdered(String dateA, String dateB){
        Date start = DateUtil.dateFromString(dateA);
        Date end = DateUtil.dateFromString(dateB);
        return start.before(end);
    }
    
    /**
     * Answer the question: which of the specified times fall w/i the specified distance from the given reference time?
     * 
     * @param time reference time
     * @param times array of times to compare w/ the reference time
     * @param thresholdDuration maximum distance b/w reference and comparison time at which the times are still considered "near" one of the comparison times
     * @return answer to the question: which of the specified times fall w/i the specified distance from the given reference time?
     */    
    public static String[] whichTimesAreNearPoint(String time, String[] times, float thresholdDuration){
        String[] nearTimes = new String[times.length];
        int numberOfNearPoints = 0;
        int numberOfComparisonPoints = times.length;

        for (int i = 0;i < numberOfComparisonPoints;i++){
            float overlap = DateUtil.alarmTimeOverlap(time, times[i], thresholdDuration);

            if (overlap > 0.0f){
                nearTimes[numberOfNearPoints] = times[i];
                numberOfNearPoints++;
            }
        }
        
        String[] thesePoints = new String[numberOfNearPoints];
        System.arraycopy(nearTimes, 0, thesePoints, 0, numberOfNearPoints);

        return thesePoints;
    }    
    
    /**
     * Determine the temporal overlap of two datetime ranges.  We assume that the second range starts after the first one  but we don't assume anything abt the durations of 
     * each range.  Therefore, we have 3 cases of interest.  We denote each of the cases with the following notation:
     *      [ is the start of the first range
     *      ] is the end of the first range
     *      { is the start of the second range
     *      } is the end of the second range
     *
     * Case I: There is no overlap; namely, the 2nd range starts after the 1st range is completed.  []{}
     * Case II: There is overlap with the 1st range ending before the 2nd range ends [{]}
     * Case III: The 2nd range falls completely within the 1st range [{}]
     *
     * Here, we return the result as a range of dates for which the two ranges overlap.  In Case I, there is no overlap, so we return zero-length strings as the start and end of 
     * the overlap range.  In Case II, the overlap occurs b/w { and ], in other words b/w the start of the second range and the end of the range.  In Case III, the overlap 
     * occurs b/w { and }, in other words b/w the start and end of the second range
     *
     * @param start1 start time of the 1st range
     * @param end1 end time of the first range
     * @param start2 start time of the 2nd range
    * @param end2 end time of the second range
     * @return the overlapping range b/w the ranges
     */
    public static String[] timeOverlapRange(String start1, String end1, String start2, String end2){
        String[] overlapRange = new String[2];
        
        if (DateUtil.durationInDays(start2, end1) <= 0.0f){ // CASE I
            overlapRange[0] = "";
            overlapRange[1] = "";
        } else{
            if (DateUtil.durationInDays(end1, end2)>=0.0f){ // CASE II
            overlapRange[0] = start2;
            overlapRange[1] = end1;
            } else{ // CASE III
            overlapRange[0] = start2;
            overlapRange[1] = end2;
            }
        }
        return overlapRange;
    }
    
    /**
     * For the given time range (specified by the start of the range and the length in seconds) and the given binning (specified by the start of the first bin and the bin size), 
     * determine which bins are contained within the range.
     * 
     * @param rangeStart start date of the range of interest
     * @param rangeLength length of the range of interest, in seconds
     * @param gridStart start date of the first bin
     * @param binSize size of the time bins, in seconds
     * @return 2-element array containing
     *      [0] = the minimum bin contained within the range
     *      [1] = the maximum bin contained within the range
     */
    public static int[] binnedRange(String rangeStart, long rangeLength, String gridStart, int binSize){
            Date startOfRange = DateUtil.dateFromString(rangeStart);
            long rangeStartInMs = startOfRange.getTime();
            long rangeLengthInMs = rangeLength * 1000L;
            
            Date startOfGrid = DateUtil.dateFromString(gridStart);
            long gridStartInMs = startOfGrid.getTime();
            int binSizeInMs = binSize * 1000;
            
            int minGrid = (int) Math.floor((rangeStartInMs - gridStartInMs) / 
                    binSizeInMs);
            int maxGrid = (int) Math.ceil(
                    (rangeStartInMs + rangeLengthInMs - gridStartInMs) / 
                    binSizeInMs);
            int[] gridRangeCovered = new int[2];
            gridRangeCovered[0] = minGrid;
            gridRangeCovered[1] = maxGrid;
            return gridRangeCovered;
    }
}