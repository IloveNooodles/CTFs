package io.github.nandandesai.pico.validators;

import javax.validation.Constraint;
import javax.validation.Payload;
import java.lang.annotation.Documented;
import java.lang.annotation.Retention;
import java.lang.annotation.Target;

import static java.lang.annotation.ElementType.*;
import static java.lang.annotation.RetentionPolicy.RUNTIME;

@Documented
@Constraint(validatedBy = ImageConstraintValidator.class)
@Target({TYPE, FIELD, ANNOTATION_TYPE})
@Retention(RUNTIME)
public @interface ValidImage {
    String message() default "Invalid Image";

    Class<?>[] groups() default {};

    Class<? extends Payload>[] payload() default {};
}
