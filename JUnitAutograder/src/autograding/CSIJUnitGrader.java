/*
 * Author: Matt J Williams
 * Created: February 2013
 *
 * Version: 12 Feb 2013
 * Updates:
 * * Failure cause now includes the line number where the test failed.
 *
 * Dependencies:
 * * JUnit 4
 * * Hamcrest (JUnit 4 requirement)
 */

package autograding;

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
 * CSIJunitGrader [-m] [-s] className
 * 
 * className: the name of the class containing unit tests
 * -m:        output the mark only
 * -s:        run in sandboxed mode
 * 
 * All unit tests should be annotated with @GradedTest. This is in addition
 * to the regular JUnit @Test annotation. @GradedTest is used to specify the 
 * number of marks passing a test is worth; e.g.,
 *   @GradedTest ( marks=2.0 )
 * indicates that the corresponding test is worth 2 marks.
 */
public class CSIJUnitGrader
{
    public static final String MARKS_ONLY_OPT = "-m";
    public static final String SANDBOX_MODE_OPT = "-s";
    
    public static void main( String[] args )
    {
        //
        // Process args
        int minNumArgs = 1;
        int maxNumArgs = 3;
        if( (args.length < minNumArgs) || (args.length > maxNumArgs) )
        {
            System.out.println( "Incorrect number of arguments: " + args.length );
            System.exit( 1 );
        }
        
        List<String> argsList = new LinkedList<String>( Arrays.asList( args ) );
        
        // Args outputs
        String junitClassName = null;
        boolean markOnly = false;
        boolean sandboxMode = false;
        
        // Last argument must be the unit test class
        junitClassName = argsList.remove( argsList.size()-1 );
        
        // Remaining arguments are options
        Set<String> opts = new HashSet<String>( argsList );
        Iterator<String> it = opts.iterator();  // must use `it` to iterate and remove (using `opts` is unstable)
        while( it.hasNext() )
        {
            String opt = it.next();
            if( opt.equals(MARKS_ONLY_OPT) )
                markOnly = true;
            else if( opt.equals(SANDBOX_MODE_OPT) )
                sandboxMode = true;
            else
            {
                System.out.println( "Unknown option: " + opt );
                System.exit(1);
            }
            it.remove();  // removes the last element from the underlying collection
        }
        
        if( opts.size() > 0 )
        {
            System.out.println( opts.size() + " unparsed options" );
            System.exit(1);
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
        // Set up sandbox
        if( sandboxMode )
        {
            SecurityManager sm = new GraderSecurityManager();
            System.setSecurityManager( sm );
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
        double maximumMark = calculateMaxMark( junitClass );
        
        //
        // Calculate mark for student
        double studentMark = maximumMark;
        for( Failure f : failures  )
        {
            String testName = getFailureTestName( f );  // i.e., name of the test method
            try
            {
                double testMarks = getTestMark( f );
                studentMark -= testMarks;
            }
            catch( TestGradeAccessException ex )
            {
                // weird. re-throw
                throw ex;
            }
        }
        
        //
        // Output feedback...
        if( markOnly )
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
                double testMarks = getTestMark( f );
                
                System.out.println( "Failed test name: " + testName );
                System.out.println( "Failure cause... ");
                System.out.println( "\tError type:     " + f.getException().getClass().getName() );
                System.out.println( "\tError message:  " + f.getException().getMessage() );
                int exceptionLineNum = getExceptionLineNumber( f.getException().getStackTrace(), junitClassName );
                if( exceptionLineNum == -1 )
                    // If no exception line found, just point user to the failed test method
                    System.out.printf(  "\tSee also:       test method '%s' in %s%n", testName, junitClassName );
                else
                    // Failure was caused by an exception in the test class -- give user the line number
                    System.out.printf(  "\tSee also:       line %s of %s%n", getExceptionLineNumber( f.getException().getStackTrace(), junitClassName ), junitClassName );
                System.out.printf( "Marks deducted: %.2f%n", testMarks );
                
                System.out.println();
            }
        
            System.out.printf( "Failed unit tests: %s%n", numFailures );
            System.out.printf( "Score: %.2f out of %.2f%n", studentMark, maximumMark );
        }
    }
    
    /*
     * Get the name of the method that caused a JUnit Failure.
     */ 
    public static String getFailureTestName( Failure f )
    {
        String testMethodName = f.getTestHeader();
        testMethodName = testMethodName.split("\\(")[0];
        return testMethodName;
    }
    
    /*
     * Get the maximum mark (grade) that a class containing JUnit tests should 
     * allow. Calculated by summing the individual grades.
     */
    public static double calculateMaxMark( Class<?> cls )
    {
        double maxMark = 0;
        Method[] methds = cls.getDeclaredMethods();
        for( Method meth : methds )
        {
            GradedTest annot = meth.getAnnotation( GradedTest.class );
            if( annot != null ) 
            {
                maxMark += annot.marks();
            }
        }
        return maxMark;
    }
    
    /*
     * Get the test mark (grade) for a particular JUnit test method that was the 
     * source of a JUnit Failure.
     */
    public static double getTestMark( Failure f )
    {
        Description desc = f.getDescription();
        GradedTest annot = desc.getAnnotation(GradedTest.class);
        if( annot == null )
            throw new TestGradeAccessException( "Test grade not found for: " + desc );
        return annot.marks();
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
}