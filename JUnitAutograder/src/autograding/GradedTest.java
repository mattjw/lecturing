/*
 * Author: Matt J Williams
 * Created: February 2013
 */
// http://tutorials.jenkov.com/java-reflection/annotations.html

package autograding;

import java.lang.annotation.*;

/*
 * An annotation for representing the number of marks that a particular
 * assessed JUnit test contributes.
 */
@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.METHOD)
public @interface GradedTest
{
    public double marks();
}