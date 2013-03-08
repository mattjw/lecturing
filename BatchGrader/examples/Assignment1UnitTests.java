import org.junit.*;
import autograding.*;

public class Assignment1UnitTests
{
    private static SimpleDate date;
    private static SimpleDate[] dates;
    
    /*
     * Tests for Q1.
     */
    @GradedTest ( marks= 3)
    @Test (timeout=4000)
    public void q1test1() {        
        date = new SimpleDate( 2013, 1, 1 );
        Assert.assertEquals( "Tue", Assignment1.dayOfWeek( date ) );
        
        date = new SimpleDate( 2012, 12, 26 );
        Assert.assertEquals( "Wed", Assignment1.dayOfWeek( date ) );
        
        date = new SimpleDate( 1912, 6, 23 );
        Assert.assertEquals( "Sun", Assignment1.dayOfWeek( date ) );
        
        date = new SimpleDate( 2013, 3, 14 );
        Assert.assertEquals( "Thu", Assignment1.dayOfWeek( date ) );
        
        date = new SimpleDate( 2013, 3, 8 );
        Assert.assertEquals( "Fri", Assignment1.dayOfWeek( date ) );
    }
     
    @GradedTest ( marks=1 )
    @Test (timeout=4000)
    public void q1test2() {
        date = new SimpleDate( 1984, 2, 29 );
        Assert.assertEquals( "Wed", Assignment1.dayOfWeek( date ) );
        
        date = new SimpleDate( 1984, 3, 2 );
        Assert.assertEquals( "Fri", Assignment1.dayOfWeek( date ) );
        
        date = new SimpleDate( 1753, 1, 1 );
        Assert.assertEquals( "Mon", Assignment1.dayOfWeek( date ) );
        
        date = new SimpleDate( 3054, 11, 30 );
        Assert.assertEquals( "Thu", Assignment1.dayOfWeek( date ) );
    }
    
    /*
     * Tests for Q2.
     */
    @GradedTest ( marks=2 )
    @Test (timeout=4000)
    public void q2test1() {
        dates = new SimpleDate[] { new SimpleDate( 2013, 3, 14 ),
            new SimpleDate( 2013, 3, 21 ),
            new SimpleDate( 2013, 3, 28 ),
            new SimpleDate( 2013, 3, 29 ) };
        Assert.assertEquals( 3, Assignment1.countDatesOnDay( dates, "Thu" ) );
        
        dates = new SimpleDate[] { new SimpleDate( 2014, 12, 15 ),
            new SimpleDate( 2014, 12, 16 ),
            new SimpleDate( 2014, 12, 17 ) };
        Assert.assertEquals( 0, Assignment1.countDatesOnDay( dates, "Sun" ) );
        
        dates = new SimpleDate[] { new SimpleDate( 2014, 12, 26 ) };
        Assert.assertEquals( 1, Assignment1.countDatesOnDay( dates, "Fri" ) );
    }
    
    @GradedTest ( marks=1 )
    @Test (timeout=4000)
    public void q2test2() {
        dates = new SimpleDate[] {};
        Assert.assertEquals( 0, Assignment1.countDatesOnDay( dates, "Thu" ) );
    }
    
    /* 
     * Tests for Q3
     */
    @GradedTest ( marks=1 )
    @Test (timeout=4000)
    public void q3test1() {
        dates = new SimpleDate[] { new SimpleDate( 2013, 3, 8 ),
            new SimpleDate( 2013, 3, 15 ),
            new SimpleDate( 2013, 3, 22 ),
            new SimpleDate( 2013, 3, 23 ),
            new SimpleDate( 2013, 3, 30 ) };
        Assert.assertEquals( "Fri", Assignment1.mostFrequentDayOfWeek( dates ) );
    }
    
    @GradedTest ( marks=1 )
    @Test (timeout=4000)
    public void q3test2() {
        dates = new SimpleDate[] { new SimpleDate( 2013, 3, 8 ),
            new SimpleDate( 2013, 3, 15 ),
            new SimpleDate( 2013, 3, 20 ),
            new SimpleDate( 2013, 3, 27 ) };
        Assert.assertEquals( "Wed", Assignment1.mostFrequentDayOfWeek( dates ) );
    }
    
    @GradedTest ( marks=1 )
    @Test (timeout=4000)
    public void q3test3() {
        dates = new SimpleDate[] {};
        Assert.assertNull( Assignment1.mostFrequentDayOfWeek( dates ) );
    }
}