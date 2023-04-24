package io.github.nandandesai.pico.validators;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.RUNTIME;


//this annotation checks if the path on the file system exists or not
@Documented
@Constraint(validatedBy = PathConstraintValidator.class)
@Target({TYPE, FIELD, ANNOTATION_TYPE})
@Retention(RUNTIME)
public @interface ValidPath {
    String message() default "Invalid Path";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
