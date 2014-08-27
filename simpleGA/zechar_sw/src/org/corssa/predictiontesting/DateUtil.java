package org.corssa.predictiontesting;

import java.util.Calendar;
import java.util.Date;
import java.text.SimpleDateFormat;

/**
 * @author J. Douglas Zechar zechar at usc.edu
 */
public class DateUtil {
    private static SimpleDateFormat df =
            new SimpleDateFormat("yyyy/MM/dd HH:mm:ss");
    
    /** Creates a new instance of DateUtil */
    public DateUtil() {
    }
    
    /**
     * Parse a date from the specified string
     * 
     * @param sDate string representation of the date, of the form
     *          yyyy/MM/dd HH:mm:ss
     * @return corresponding Date object
     */
    public static Date dateFromString(String sDate) {
        Date date = new Date();
        try {
            date = DateUtil.df.parse(sDate);
        } catch (Exception ex) {
            System.out.println("Error in DateUtil.getDateFromString(" +
                    sDate + ")");
            ex.printStackTrace();
        }
        return (date);
    }
    
    /**
     * Answers the question: "Is this string in the right format to be parsed
     * as a date of of the form yyyy/MM/dd HH:mm:ss?"
     * 
     * @param sDate string representation of a date time
     * @return boolean response to the statement "This string is of the
     *          form yyyy/MM/dd HH:mm:ss"
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
     * @return string representation of the date, of the form
     *          yyyy/MM/dd HH:mm:ss
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
    public static String offsetDate(String startDate, int fieldToChange,
            int amountToAdd){
        Date start = DateUtil.dateFromString(startDate);
        Calendar startCalendar = Calendar.getInstance();
        startCalendar.setTime(start);
        startCalendar.add(fieldToChange, amountToAdd);
        String offsetTime = DateUtil.stringFromDate(startCalendar.getTime());
        return offsetTime;
    }
    
    /**
     * get the difference between two dates in days; it is not required that
     * these dates be specified in chronological order
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
            duration = (timeB.getTimeInMillis() - timeA.getTimeInMillis()) /
                    1000.0f / 60.0f / 60.0f / 24.0f;
        } catch (Exception ex) {
            System.out.println("Error in DateUtil.durationInDays(" + dateA +
                    ", " + dateB + ")");
            ex.printStackTrace();
        }
        return duration;
    }
    
    /**
     * get the duration between two dates in days, requiring that the start 
     * occur before the end.  If the specified start date is after the specified
     * end date, throw up.
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
            duration = Math.abs(endTimeMillis - startTimeMillis) /
                    1000.0f / 60.0f / 60.0f / 24.0f;
        } catch (Exception ex) {
            System.err.println("Error in DateUtil.durationInDays(" + start +
                    ", " + end + ")");
            ex.printStackTrace();
        }
        return duration;
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
}