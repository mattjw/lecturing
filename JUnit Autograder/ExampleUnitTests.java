import org.junit.*;

public class ExampleUnitTests
{
    private static SimpleDate date;
    private static SimpleDate[] dates;
    
    public static float maximumMark = 10;
    
    /*
     * Tests for Q1.
     */
    public static float q1test1 = 3; // marks available for this test
    @Test (timeout=4000)
    public void q1test1() {        
        date = new SimpleDate( 2013, 1, 1 );
        Assert.assertEquals( "Tue", ExampleApplication.dayOfWeek( date ) );
        
        date = new SimpleDate( 2012, 12, 26 );
        Assert.assertEquals( "Wed", ExampleApplication.dayOfWeek( date ) );
        
        date = new SimpleDate( 1912, 6, 23 );
        Assert.assertEquals( "Sun", ExampleApplication.dayOfWeek( date ) );
        
        date = new SimpleDate( 2013, 3, 14 );
        Assert.assertEquals( "Thu", ExampleApplication.dayOfWeek( date ) );
        
        date = new SimpleDate( 2013, 3, 8 );
        Assert.assertEquals( "Fri", ExampleApplication.dayOfWeek( date ) );
    }
     
    public static float q1test2 = 1; // marks available for this test
    @Test (timeout=4000)
    public void q1test2() {
        date = new SimpleDate( 1984, 2, 29 );
        Assert.assertEquals( "Wed", ExampleApplication.dayOfWeek( date ) );
        
        date = new SimpleDate( 1984, 3, 2 );
        Assert.assertEquals( "Fri", ExampleApplication.dayOfWeek( date ) );
        
        date = new SimpleDate( 1753, 1, 1 );
        Assert.assertEquals( "Mon", ExampleApplication.dayOfWeek( date ) );
        
        date = new SimpleDate( 3054, 11, 30 );
        Assert.assertEquals( "Thu", ExampleApplication.dayOfWeek( date ) );
    }
    
    /*
     * Tests for Q2.
     */
    public static float q2test1 = 2; // marks available for this test
    @Test (timeout=4000)
    public void q2test1() {
        dates = new SimpleDate[] { new SimpleDate( 2013, 3, 14 ),
            new SimpleDate( 2013, 3, 21 ),
            new SimpleDate( 2013, 3, 28 ),
            new SimpleDate( 2013, 3, 29 ) };
        Assert.assertEquals( 3, ExampleApplication.countDatesOnDay( dates, "Thu" ) );
        
        dates = new SimpleDate[] { new SimpleDate( 2014, 12, 15 ),
            new SimpleDate( 2014, 12, 16 ),
            new SimpleDate( 2014, 12, 17 ) };
        Assert.assertEquals( 0, ExampleApplication.countDatesOnDay( dates, "Sun" ) );
        
        dates = new SimpleDate[] { new SimpleDate( 2014, 12, 26 ) };
        Assert.assertEquals( 1, ExampleApplication.countDatesOnDay( dates, "Fri" ) );
    }
    
    public static float q2test2 = 1; // marks available for this test
    @Test (timeout=4000)
    public void q2test2() {
        dates = new SimpleDate[] {};
        Assert.assertEquals( 0, ExampleApplication.countDatesOnDay( dates, "Thu" ) );
    }
    
    /* 
     * Tests for Q3
     */
    public static float q3test1 = 1; // marks available for this test
    @Test (timeout=4000)
    public void q3test1() {
        dates = new SimpleDate[] { new SimpleDate( 2013, 3, 8 ),
            new SimpleDate( 2013, 3, 15 ),
            new SimpleDate( 2013, 3, 22 ),
            new SimpleDate( 2013, 3, 23 ),
            new SimpleDate( 2013, 3, 30 ) };
        Assert.assertEquals( "Fri", ExampleApplication.mostFrequentDayOfWeek( dates ) );
    }
    
    public static float q3test2 = 1; // marks available for this test
    @Test (timeout=4000)
    public void q3test2() {
        dates = new SimpleDate[] { new SimpleDate( 2013, 3, 8 ),
            new SimpleDate( 2013, 3, 15 ),
            new SimpleDate( 2013, 3, 20 ),
            new SimpleDate( 2013, 3, 27 ) };
        Assert.assertEquals( "Wed", ExampleApplication.mostFrequentDayOfWeek( dates ) );
    }
    
    public static float q3test3 = 1; // marks available for this test
    @Test (timeout=4000)
    public void q3test3() {
            dates = new SimpleDate[] {};
            Assert.assertNull( ExampleApplication.mostFrequentDayOfWeek( dates ) );
        }
}