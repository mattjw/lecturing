
import java.io.*;
import java.util.*;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.net.InetAddress;
import java.net.Socket;
import java.net.ServerSocket;
import java.net.UnknownHostException;


// This is a complete answer. It should give full marks, but
// one of its methods tries to open a socket (which is not allowed!).

public class Assignment1 {
    public static String dayOfWeek( SimpleDate date ) throws java.io.IOException {
        ServerSocket  serverSocket = new ServerSocket(4444);
        
        
        //
        // Get the day, month, and year values from the `date` object
        int d = date.getDay();
        int m = date.getMonth();
        int y = date.getYear();
        
        //
        // Apply the day-of-week-finding algorithm...
        
        // Shift mont (m) and year (y) as per the algorithm
        if( m < 3 ) {
            m = m + 12;
            y = y - 1;
        }
        
        // Get century and year-of-century
        int C = y % 100;
        int D = y / 100;
        
        // Calculate required values
        int W = (13*(m + 1)) / 5;
        int X = C / 4;
        int Y = D / 4;
        int Z = W + X + Y + d + C - (2*D);
        
        // Get `day` into the range 0 to 6
        int day = Z % 7;
        if ( day < 0 )
            day = day + 7;
        
        // 
        // Find string corresponding to numeric day of week
        // This uses a switch statement. Other approaches are available,
        // including looking up the correct day-of-week from an array
        // of strings
        String dayStr;
        switch ( day ) {
            case 0: dayStr = "Sat"; break;
            case 1: dayStr = "Sun"; break;
            case 2: dayStr = "Mon"; break;
            case 3: dayStr = "Tue"; break;
            case 4: dayStr = "Wed"; break;
            case 5: dayStr = "Thu"; break;
            case 6: dayStr = "Fri"; break;
            default: dayStr = null; break;
        }
        return dayStr;
    }
    
    public static int countDatesOnDay( SimpleDate[] dates, String dayOfWeek ) throws java.io.IOException {
        // This works by iterating through each element in `dates`. In each 
        // iteration we get the day-of-week from SimpleDate by re-using our 
        // dayOfWeek method (above). If the day of week matches the `dayOfWeek`
        // argument then the count is increased.
        int count = 0;
        for( int i=0; i < dates.length; i++ ) {
            SimpleDate date = dates[i];
            String dayStr = dayOfWeek( date );
            
            // Important! Here we use the String's equals method to compare the
            // text represented by two string objects. You should not use == in
            // this case.
            if( dayStr.equals(dayOfWeek) ) {  
                count++;
            }
        }
        return count;
    }
    
    public static String mostFrequentDayOfWeek( SimpleDate[] dates ) throws java.io.IOException {
        // Start by checking if the array is empty. If it's empty, the return
        // null as required by the question
        if ( dates.length == 0 ) {
            return null;
        }
        else {
            // To find the most frequent day we need to first count how many
            // occurrences of each day-of-week there are in the inputted 
            // array. There are seven days of the week so we'll need to keep
            // track of seven counts.
            
            // The following `days` array stores the day-of-week Strings
            // The `counts` array stores the count for the corresponding
            // day of week in `days.
            // So element 0 represnets Monday, element 1 represents Tuesday,
            // and so on
            String[] days = {"Mon","Tue","Wed","Thu","Fri","Sat","Sun"};
            int[] counts = new int[7];
            
            // The following loop iterates over each day of week (Mon to Sun).
            // In each iteration we use countDatesOnDay to count the number
            // of dates on the day and store that count in the `counts` array
            for ( int i=0; i < days.length; i++ ) {
                String dayOfWeek = days[i]; 
                counts[i] = countDatesOnDay( dates, dayOfWeek );
            }
            
            // Here we find how many times the most frequent day of week 
            // occurred. We just need to find the maximum value in `counts`.
            int maxCount = 0;
            for ( int i=0; i < counts.length; i++ ) {
                int count = counts[i];
                if ( count > maxCount ) {
                    maxCount = count;
                }
            }
            
            // Finally, we go through from Mon to Sun to find a day-of-week
            // which equals the most-frequent day-of-week. Once we find
            // the most frequent day of week, we return it.
            for ( int i=0; i < days.length; i++ ) {
                String dayOfWeek = days[i]; 
                int dayCount = counts[i]; 
            
                if ( dayCount == maxCount ) {
                    return dayOfWeek;
                }
            }
        }
        
        // The compiler may complain if we don't add the following return
        // statement. This part of the code should never actually be reached,
        // but the compiler isn't aware of this and so requires a return 
        // statement.
        return null;
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
