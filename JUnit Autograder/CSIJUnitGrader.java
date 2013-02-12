/*
 * Author: Matt J Williams
 * Created: February 2013
 *
 * Version: 12 Feb 2013
 * Updates:
 * * Failure cause now includes the line number where the test failed.
 */


import org.junit.*;
import org.junit.runner.*;
import java.util.*;
import org.junit.runner.notification.*;
import java.lang.reflect.*;

 
/*
 * Java app that will run a class containing JUnit tests, and assign a grade
 * based on how many tests passed.
 *  
 * Command line args:
 * CSIJunitGrader [-s] className
 * 
 * className: the name of the class containing unit tests
 * -s:        output the score only
 * 
 * For grading, the test class should include fields indicating the maximum 
 * number of marks available and the marks that each test is worth.
 * In particular, the class should have a "maximumMark" field with the maximum 
 * achievable mark for the assignment, and a field accompanying each test 
 * method specifying the marks for that test. A companion field must have the
 * same name as the test method it accompanies. 
 * 
 * Fields representing marks should be static floats.
 */
public class CSIJUnitGrader
{
    public static String getFailureTestName( Failure f )
    {
        String testMethodName = f.getTestHeader();
        testMethodName = testMethodName.split("\\(")[0];
        return testMethodName;
    }
    
    public static float getFieldFloatValue( Class cls, String fieldName )
    {
        try
        {
            Field field = cls.getField( fieldName );
            return field.getFloat( field );
        } 
        catch( NoSuchFieldException ex )
        {
            System.out.println( "Could not find field: " + fieldName);
            System.exit(1);
        }
        catch( IllegalAccessException ex )
        {
            System.out.println( "Could not access field: " + fieldName );
            System.exit(1);
        }
        return 0;
    }
    
    /*
     * Look through a stack trace and find the line where an error occurred
     * in a particular class file.
     */ 
    public static int getExceptionLineNumber( StackTraceElement[] trace, String classFileName )
    {
        for( int i=0; i < trace.length; i++ )
        {
            StackTraceElement elem = trace[i];
            String errClass = elem.getClassName();
            if( errClass.contains( classFileName ) )
            {
                return elem.getLineNumber();
            }
        }
        return -1;
    }
    
    public static void main( String[] args )
    {
        //
        // Process args
        if( (args.length <= 0) || (args.length >= 3) )
        {
            System.out.println( "Incorrect number of arguments: " + args.length );
            System.exit( 1 );
        }
        
        String junitClassName = null;
        boolean scoreOnly = false;
        if( args.length == 1 )
        {
            junitClassName = args[0];
        }
        else if( args.length == 2 )
        {
            junitClassName = args[1];
            if( args[0].equals("-s") )
                scoreOnly = true;
            else
            {
                System.out.println( "Invalid option: " + args[0] );
                System.exit( 1 );
            }
        }
        
        //
        // Load JUnit test class
        ClassLoader classLoader = ClassLoader.getSystemClassLoader();
        Class junitClass = null;
        
        try
        {
            junitClass = classLoader.loadClass( junitClassName );
        }
        catch( ClassNotFoundException ex )
        {
            System.out.println( "Class " + junitClassName + " could not be found" ); 
            System.exit( 1 );
        }
        
        //
        // Do run
        JUnitCore junit = new JUnitCore();
        Result result = junit.run( junitClass );
        
        
        boolean allPassed = result.wasSuccessful();
        int numFailures = result.getFailureCount();
        List<Failure> failures = result.getFailures();
        
        //
        // Determine maximum possible mark
        float maximumMark = getFieldFloatValue( junitClass, "maximumMark" );
        
        //
        // Calculate mark for student
        float studentMark = maximumMark;
        for( Failure f : failures  )
        {
            String testName = getFailureTestName( f );  // i.e., name of the test method
            float testMarks = getFieldFloatValue( junitClass, testName );
            studentMark -= testMarks;
        }
        
        //
        // Output feedback...
        if( scoreOnly )
        {
            System.out.println( studentMark );
        }
        else
        {        
            if( !allPassed )
            {
                System.out.println( "Failed unit tests..." );
                System.out.println();
            }
            
            for( Failure f : failures  )
            {
                String testName = getFailureTestName( f );  // i.e., name of the test method
                float testMarks = getFieldFloatValue( junitClass, testName );
                
                System.out.println( "Failed test name: " + testName );
                System.out.println( "Failure cause: ");
                System.out.println( "\t  " + f.getMessage() );
                System.out.printf( "\t  see Line %s of %s%n", getExceptionLineNumber( f.getException().getStackTrace(), junitClassName ), junitClassName );
                System.out.println( "Marks deducted: " + testMarks );
                
                System.out.println();
            }
        
            System.out.printf( "Failed unit tests: %s\n", numFailures );
            System.out.printf( "Score: %s out of %s\n", studentMark, maximumMark );
        }
    }
}