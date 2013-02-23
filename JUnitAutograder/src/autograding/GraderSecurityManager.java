package autograding;

import java.io.*;
import java.security.*;

/* 
http://www.javaworld.com/jw-11-1997/jw-11-hood.html 
http://journals.ecs.soton.ac.uk/java/tutorial/networking/security/writingSMgr.html
*/

// better: http://docs.oracle.com/javase/tutorial/security/tour2/step2.html

public class GraderSecurityManager extends SecurityManager
{
    public GraderSecurityManager() 
    {
        // pass
    }
    
    
    public void checkPermission( Permission perm )
    {
        
    }
    
    public void checkPermission( Permission perm, Object obj )
    {
        
    }
    
    
    //
    // Sockets
    //

    public void checkAccept(String host, int port)
    {
        //super.checkAccept( host, port );
        //throw new SecurityException();
    }
    
    public void checkConnect(String host, int port)
    {
        //super.checkConnect( host, port );
        //throw new SecurityException();
    }
    
    public void checkConnect(String host, int port, Object executionContext)
    {
        //super.checkConnect( host, port, executionContext );
        //throw new SecurityException();
    }

    public void checkListen(int port)
    {
        //super.checkListen( port );
        //throw new SecurityException();
    }


    //
    // Threads
    //

    public void checkAccess(Thread thread)
    {
        //super.checkAccess( thread );
        //throw new SecurityException();
    }

    public void checkAccess(ThreadGroup threadgroup)
    {
        //super.checkAccess( threadgroup );
        //throw new SecurityException();
    }

    //
    // Class loader
    //

    public void checkCreateClassLoader()
    {
        //super.checkCreateClassLoader();
        // //throw new SecurityException(); // pass??
    }


    //
    // File system
    //

    public void checkDelete(String filename)
    {
        //super.checkDelete( filename );
        //throw new SecurityException();
    }

    public void checkLink(String library)
    {
        //super.checkLink( library );
        //throw new SecurityException();
    }

    public void checkRead(FileDescriptor filedescriptor)
    {
        //super.checkRead( filedescriptor );
        //throw new SecurityException();
    }

    public void checkRead(String filename)
    {
        //super.checkRead( filename );
        //throw new SecurityException();
    }

    public void checkRead(String filename, Object executionContext)
    {
        //super.checkRead( filename, executionContext );
        //throw new SecurityException();
    }

    public void checkWrite(FileDescriptor filedescriptor)
    {
        //super.checkWrite( filedescriptor );
        //throw new SecurityException();
    }

    public void checkWrite(String filename)
    {
        //super.checkWrite( filename );
        //throw new SecurityException();
    }

    //
    // System commands
    //

    public void checkExec(String command)
    {
        //super.checkExec( command );
        //throw new SecurityException();
    }


    //
    // Interpreter
    //

    public void checkExit(int status)
    {
        //super.checkExit( status );
        //throw new SecurityException();
    }


    //
    // Package
    //

    public void checkPackageAccess(String packageName)
    {
        //super.checkPackageAccess( packageName );
        // //throw new SecurityException(); // pass to allow access to classes
    }

    
    public void checkPackageDefinition(String packageName)
    {
        //super.checkPackageDefinition( packageName );
        // //throw new SecurityException(); // pass...?
    }


    //
    // Properties
    //

    public void checkPropertiesAccess()
    {
        //super.checkPropertiesAccess();
        // //throw new SecurityException(); // pass...?
    }

    public void checkPropertyAccess(String key)
    {
        //super.checkPropertyAccess( key );
        // //throw new SecurityException(); // pass...?
    }
    

    //
    // Networking
    //
    
    public void checkSetFactory()
    {
        //super.checkSetFactory();
        //throw new SecurityException();
    }


    //
    // Windows
    //
    
    // public boolean checkTopLevelWindow(Object window) 

}
