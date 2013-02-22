package autograding;

import java.lang.reflect.*;

public class TestTools
{
    /*
     * Counts the number of non-private fields declared in a class.
     *
     * Examples...
     * System.out.println( TestTools.countNonPrivateFields( Library.class ) );
     */
    public static int countNonPrivateFields( Class<?> cls )
    {
        int count = 0;
        for( Field field : cls.getDeclaredFields() )
        {
            int modifiers = field.getModifiers();
            if( !Modifier.isPrivate(modifiers) )
                count++;
        }
        return count;
    }
    
    /*
     * Checks whether a public method named `methodName` with parameters
     * `params` is declared in a class.
     * 
     * Examples...
     * System.out.println( TestTools.hasMethod( Library.class, "addBook", int.class ) );
     * System.out.println( TestTools.hasMethod( Library.class, "addBook" ) );
     */
    public static boolean hasMethod( Class<?> cls, String methodName, Class<?>... params )
    {
        // Avoiding lint warnings...
        // http://docs.oracle.com/javase/tutorial/reflect/class/classTrouble.html
        try
        {
            Method method = cls.getMethod( methodName, params );
            return true;
        }
        catch( NoSuchMethodException ex )
        {
            return false;
        }
    }
    
    /*
     * Checks whether a public constructor with parameters `params` is declared
     * in a class.
     *
     * Examples...
     * System.out.println( TestTools.hasConstructor( Library.class ) );
     * System.out.println( TestTools.hasConstructor( Library.class, int.class ) );
     */
    public static boolean hasConstructor( Class<?> cls, Class<?>... params )
    {
        try
        {
            Constructor constructor = cls.getConstructor( params );
            return true;
        }
        catch( NoSuchMethodException ex )
        {
            return false;
        }
    }
}

