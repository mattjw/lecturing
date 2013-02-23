package autograding;

public class TestGradeAccessException extends RuntimeException
{
    public TestGradeAccessException() 
    {
        super();
    }
    
    public TestGradeAccessException( String msg ) 
    {
        super( msg );
    }
}
