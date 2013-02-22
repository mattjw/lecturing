import org.junit.*;
import autograding.*;

public class ExampleUnitTests {
    /*
     * Tests for Q1.
     */
     
    // Test Book constructor and accessors.
    @GradedTest ( marks=1.75 )
    @Test ( timeout=4000 )
    public void q1testA() {
        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 5 );
        Assert.assertEquals( "Robert Liguori", b.getAuthor() );
        Assert.assertEquals( "Java Pocket Guide", b.getTitle() );
        Assert.assertEquals( 5, b.getTotalCopies() );
        Assert.assertEquals( 5, b.getAvailableCopies() );
    }
    
    // Test Book constructor input validation.
    @GradedTest ( marks=0.25 )
    @Test ( timeout=4000, expected=IllegalArgumentException.class )
    public void q1testB() {
        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 0 );
    }
    
    // Test Book withdrawal and return.
    @GradedTest ( marks=2.0 ) 
    @Test ( timeout=4000 ) 
    public void q1testC() {
        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 3 );
        b.withdrawCopy();
        b.withdrawCopy();
        Assert.assertEquals( 1, b.getAvailableCopies() );
        b.withdrawCopy();
        Assert.assertEquals( 0, b.getAvailableCopies() );
        b.returnCopy();
        Assert.assertEquals( 1, b.getAvailableCopies() );
    }
    
    // Test Book withdrawals validation.
    @GradedTest ( marks=0.25 )
    @Test ( timeout=4000, expected=IllegalStateException.class )
    public void q1testD() {
        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 1 );
        b.withdrawCopy();
        Assert.assertEquals( 0, b.getAvailableCopies() );
        b.withdrawCopy();
    }
    
    // Test Book returns validation.
    @GradedTest ( marks=0.25 )
    @Test ( timeout=4000, expected=IllegalStateException.class )
    public void q1testE() {
        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 3 );
        b.returnCopy();
    }
    
    // Test Book information hiding (good programming practice!).
    @GradedTest ( marks=0.5 )
    @Test ( timeout=4000 )
    public void q1testF() {
        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 20 );
        if( TestTools.countNonPrivateFields( Book.class ) > 0 )
            Assert.fail( "Book's fields should be hidden." );
    }
    
    /*
     * Tests for Q2.
     */
     
    // Test basic usage of an infinite-capacity library.
    @GradedTest ( marks=0.6 )
    @Test ( timeout=4000 )
    public void q2testA() {
        Library l = new Library();

        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 20 );
        l.addBook( b );
    }
    
    // Test basic usage of a limited-capacity library.
    @GradedTest ( marks=0.6 )
    @Test ( timeout=4000 )
    public void q2testB() {
        Library l = new Library(10);

        Book b = new Book( "Robert Liguori", "Java Pocket Guide", 4 );
        l.addBook( b );
    }
    
    // Test input validation on a limited-capacity library.
    @GradedTest ( marks=0.20 )
    @Test ( timeout=4000, expected=IllegalArgumentException.class )
    public void q2testC() {
        Library l = new Library(0);
    }
    
    // Test library capacity validation (pt1)
    @GradedTest ( marks=0.20 )
    @Test ( timeout=4000, expected=IllegalStateException.class )
    public void q2testD1() {
        Library l = new Library(4);
        l.addBook( new Book("Niccolo Machiavelli", "The Prince", 1) );
        l.addBook( new Book("John R.R. Tolkien", "The Hobbit", 1) );
        l.addBook( new Book("Dan Ariely", "Predictably Irrational", 1) );
        l.addBook( new Book("Terry Pratchett", "Guards! Guards!", 1) );
        l.addBook( new Book("David Mitchell", "Cloud Atlas", 1) );
    }
    
    // Test library capacity validation (pt2)
    @GradedTest ( marks=0.20 )
    @Test ( timeout=4000, expected=IllegalStateException.class )
    public void q2testD2() {
        Library l = new Library(4);
        l.addBook( new Book("Niccolo Machiavelli", "The Prince", 2) );
        l.addBook( new Book("John R.R. Tolkien", "The Hobbit", 1) );
        l.addBook( new Book("Dan Ariely", "Predictably Irrational", 2) );
    }
    
    // Test getting books from library
    @GradedTest ( marks=1.0 )
    @Test ( timeout=4000 )
    public void q2testE() {
        Library l = new Library(10);
        Book b1 = new Book("Niccolo Machiavelli", "The Prince", 3);
        Book b2 = new Book("John R.R. Tolkien", "The Hobbit", 3);
        Book b3 = new Book("Dan Ariely", "Predictably Irrational", 4);
        l.addBook( b1 );
        l.addBook( b2 );
        l.addBook( b3 );
        Assert.assertSame( b2, l.getBookWithTitle("The Hobbit") );
        Assert.assertSame( b2, l.getBookWithTitle("tHE hObbIT") );
        Assert.assertSame( b3, l.getBookWithTitle("Predictably iRRaTIOnaL") );
        Assert.assertNull( l.getBookWithTitle("Cloud Atlas") );
    }
    
    // Test checking if book exists
    @GradedTest ( marks=0.5 )
    @Test ( timeout=4000 )
    public void q2testF() {
        Library l = new Library(10);
        Book b1 = new Book("Niccolo Machiavelli", "The Prince", 3);
        Book b2 = new Book("John R.R. Tolkien", "The Hobbit", 3);
        Book b3 = new Book("Dan Ariely", "Predictably Irrational", 4);
        l.addBook( b1 );
        l.addBook( b2 );
        l.addBook( b3 );
        Assert.assertEquals( true, l.hasBookWithTitle("The Hobbit") );
        Assert.assertEquals( true, l.hasBookWithTitle("tHE hObbIT") );
        Assert.assertEquals( true, l.hasBookWithTitle("Predictably iRRaTIOnaL") );
        Assert.assertEquals( false, l.hasBookWithTitle("Cloud Atlas") );
        Assert.assertEquals( false, l.hasBookWithTitle("The Princess") );
        Assert.assertEquals( false, l.hasBookWithTitle("Irrational") );
    }
    
    // Test counting number of available books
    @GradedTest ( marks=1.5 )
    @Test ( timeout=4000 )
    public void q2testG() {
        Library l = new Library();
        Assert.assertEquals( 0, l.numberAvailableBooks() );

        Book b1 = new Book("Niccolo Machiavelli", "The Prince", 3);
        Book b2 = new Book("John R.R. Tolkien", "The Hobbit", 3);
        Book b3 = new Book("Dan Ariely", "Predictably Irrational", 4);
        l.addBook( b1 );
        l.addBook( b2 );
        l.addBook( b3 );
        Assert.assertEquals( 10, l.numberAvailableBooks() );

        b1.withdrawCopy();
        b1.withdrawCopy();
        b1.withdrawCopy();
        Assert.assertEquals( 7, l.numberAvailableBooks() );

        b1.returnCopy();
        Assert.assertEquals( 8, l.numberAvailableBooks() );

        b2.withdrawCopy();
        b3.withdrawCopy();
        b3.withdrawCopy();
        Assert.assertEquals( 5, l.numberAvailableBooks() );
    }
    
    // Test Book information hiding (good programming practice!).
    @GradedTest ( marks=0.2 )
    @Test ( timeout=4000 )
    public void q2testH() {
        Library l = new Library( 20 );
        if( TestTools.countNonPrivateFields( Library.class ) > 0 )
            Assert.fail( "Library's fields should be hidden." );
    }
    
}