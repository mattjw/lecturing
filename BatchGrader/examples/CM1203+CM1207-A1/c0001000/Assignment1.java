// This example does some file input, which is allowed. It should get full
// marks.

 
import java.io.*;
import java.util.*;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.ServerSocket;
import java.net.UnknownHostException;

public class Assignment1 {
    


 /*
     * A method to find the day-of-week for a date.
     *
     * Arguments:
     * `date` -- the SimpleDate for which the day-of-week is to be found.
     *
     * Return value:
     * A String representing the day of week. The day of week should be
     * expressed as a three-letter abbreviation; in other words, this method
     * returns one of:
     *   "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
     */
	 
	 
    public static String dayOfWeek( SimpleDate date ) throws IOException {
        // File Read -- Should be allowd...
        File f;
        f = new File("input.txt");
        Scanner in = new Scanner( f );
        in.nextLine();
        
        
        
        int d = date.getDay();
		int m = date.getMonth();
		int y = date.getYear();
		if (m<3){
			m = m + 12;
			--y;}
		int C = y % 100;
		int D = y / 100;
		int W = (13 * (m + 1)) / 5;
		int X = C / 4;
		int Y = D / 4;
		int Z = W + X + Y + d + C - 2 * D;
		int day = Z % 7;
		if (day<0)
		day = day + 7;
		String[] days = {"Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"};
		return days[day];
		
	
    }
    
    /*
     * Given a set of dates, this method will count the number of dates in the 
     * set that fall on a particular day-of-week.
     *
     * Arguments: 
     * `dates` -- an array of SimpleDate objects
     * `dayOfWeek` -- a String representing the day of week ("Mon" to "Sun")
     *
     * Return value:
     * An integer giving the number of dates that fell on `dayOfWeek`.
     */
	 
    public static int countDatesOnDay( SimpleDate[] dates, String dayOfWeek ) throws IOException {
        
		int count = 0;
		String day = "blank";
        for (int i = 0; i<=dates.length-1; ++i){
			day = dayOfWeek(dates[i]);
			if (day.equals(dayOfWeek))
			++count;}
		return count;
			
    }
    
    /*
     * A method to find the most frequent day-of-week among a collection of
     * dates.
     *
     * Arguments: 
     * `dates` -- an array of SimpleDate objects
     * 
     * Return value:
     * If the array `dates` is empty, then this method should return the null
     * reference. Otherwise, the method should return the three-letter 
     * abbreviation ("Mon", "Tue", etc.) of the day-of-week that was most 
     * frequent. 
     * In the case that there is a tie for the most-frequent day-of-week, 
     * priority should be given to the day-of-week that comes earliest in the
     * week. (For this method, "Mon" is assumed to be the first day of the 
     * week.)
     * For example, if there were a tie between Tuesday, Wednesday, and Sunday,
     * the method should return "Tue".
     */
   public static String mostFrequentDayOfWeek( SimpleDate[] dates ) throws IOException {

       
        String[] days = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"};
        String maxDay = "blank";
        int maxFreq = 0;
        for (int i = 0; i<7; ++i) {
        	int freq = 	countDatesOnDay(dates, days[i]);
        	if (freq>maxFreq){
        		maxDay = days[i];
        		maxFreq = freq;}}
        if (maxDay.equals("blank"))
        return null;
        else
        return maxDay;
		
    }
}


/*
 * A simple class to represent a calendar date. 
 * Uses a naive representation. This class does not verify that the month and
 * day values are valid. 
 *
 * The month is represented by an integer between 1 (January) to 12 (December).
 * The day is represented by an integer, with 1 indicating the first day of
 * the month.
 *
 * This class should not be modified.
 */
class SimpleDate {
    private int year;
    private int month;
    private int day;
    
    public SimpleDate( int year, int month, int day ) {
        this.year = year;
        this.month = month;
        this.day = day;
    }
    
    public int getYear() {
        return year;
    }
    
    public int getMonth() {
        return month;
    }
    
    public int getDay() {
        return day;
    }
    
    public String toString() {
        return String.format("%04d/%02d/%02d", year, month, day);
    }


}

